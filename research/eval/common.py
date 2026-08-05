"""Shared plumbing for the eval harness.

Two properties here exist because their absence cost us real work:

INCREMENTAL WRITES  the first run of this eval held 240 results in memory and
                    wrote once at the end. The process was killed at 40 and all
                    of it was lost. Everything now writes after every call.

MANIFEST            nothing in the first run recorded which models produced it.
                    Every output file now carries model ids, date and corpus, so
                    a later run can tell model drift from noise.
"""
import json, os, sys, time, urllib.request

URL = 'https://openrouter.ai/api/v1/chat/completions'

# The rewriter produces both rewrite arms, so the skill is the only variable.
REWRITER = os.environ.get('DELLM_REWRITER', 'openai/gpt-5.6-terra')

# Judges must exclude the family that authored the skill (Anthropic) and the lab
# that produced the rewrites (OpenAI). Four labs, four countries of origin, so a
# shared house style cannot carry the result. See research/MODELS.md.
JUDGES = os.environ.get('DELLM_JUDGES', ','.join([
    'qwen/qwen3.8-max',        # Alibaba
    'z-ai/glm-5.2',            # Zhipu
    'x-ai/grok-4.5',           # xAI
    'google/gemini-3.6-flash',  # Google
])).split(',')

SEED = 20260805
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('DELLM_EVAL_OUT', os.path.join(HERE, 'out'))


def key():
    k = os.environ.get('OPENROUTER_API_KEY')
    if k:
        return k.strip()
    path = os.path.expanduser('~/.tokens/openrouter_token')
    if os.path.exists(path):
        return open(path).read().strip()
    sys.exit('need OPENROUTER_API_KEY or ~/.tokens/openrouter_token')


def call(model, prompt, max_tokens=4000, retries=3):
    body = json.dumps({'model': model,
                       'messages': [{'role': 'user', 'content': prompt}],
                       'max_tokens': max_tokens}).encode()
    for i in range(retries):
        try:
            req = urllib.request.Request(URL, data=body, headers={
                'Authorization': f'Bearer {key()}', 'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=180) as r:
                c = json.load(r)['choices'][0]['message'].get('content')
            if c and c.strip():
                return c.strip()
        except Exception as e:                       # noqa: BLE001
            if i == retries - 1:
                return f'__ERROR__ {e}'
        time.sleep(3 * (i + 1))
    return '__ERROR__ empty response'


def manifest(corpus, **extra):
    """Provenance block. Date is passed in, never generated, so a rerun of the
    same data reproduces byte-identically."""
    m = {'date': os.environ.get('DELLM_DATE', time.strftime('%Y-%m-%d')),
         'rewriter': REWRITER, 'judges': JUDGES, 'corpus': corpus, 'seed': SEED}
    m.update(extra)
    return m


class Incremental:
    """Writes after every append. A kill costs one call, not the batch."""

    def __init__(self, name, manifest_block):
        os.makedirs(OUT, exist_ok=True)
        self.path = os.path.join(OUT, name)
        self.data = {'manifest': manifest_block, 'results': []}
        self.flush()

    def append(self, item):
        self.data['results'].append(item)
        self.flush()

    def flush(self):
        tmp = self.path + '.tmp'
        with open(tmp, 'w') as f:
            json.dump(self.data, f, indent=1)
        os.replace(tmp, self.path)          # atomic, so a kill never truncates


def load(name):
    p = os.path.join(OUT, name)
    if not os.path.exists(p):
        sys.exit(f'missing {p}\nrun the earlier stage first (see research/eval/README.md)')
    return json.load(open(p))
