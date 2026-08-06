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
#
# Cost here is dominated by PROMPT tokens, not output: SKILL.md is roughly 13,300
# tokens and rides in every arm-C call. sol-pro bills input at $5/M, so it cost
# $0.0814 a call and was the largest single line on the 24-hour invoice, $20.57
# for 219 calls. luna bills input at $0.10/M: $0.0016 a call, 50x less.
#
# Checked before switching, on the same abstract: luna, longcat-2.0 and terra all
# stripped the same tells (-ing 4 -> 0), produced comparable length, and landed
# within 0.2 of each other on sentence-length variance. Following a 14KB
# instruction file is not what separates these tiers.
#
# This gets re-run every review cycle, so it has to be cheap. For a headline
# number worth publishing, confirm on the top tier:
#     DELLM_REWRITER=openai/gpt-5.6-sol-pro make eval
REWRITER = os.environ.get('DELLM_REWRITER', 'openai/gpt-5.6-luna')

# Judges must exclude the family that authored the skill (Anthropic) and the lab
# that produced the rewrites (OpenAI). Four labs, four countries of origin, so a
# shared house style cannot carry the result. See research/MODELS.md.
# Panel rebuilt 2026-08-06 on the actual bill rather than an estimate.
# A 24-hour invoice showed qwen3.8-max at $22.38 of $61.98, 36% of everything,
# because it spends 1,626 reasoning tokens per call and its prompts share no
# long prefix, so only 21 of 2,025 calls hit the cache. Dropped.
#
#   per adjudication call, measured:
#     qwen3.8-max     $0.0111      grok-4.5     $0.0062
#     gemini-3.6-flash $0.0080     glm-5.2      $0.0016
#     deepseek-v4-flash $0.0001
#
# Three labs, all models shipped within six weeks. deepseek-v4-flash is
# conservative on its own (it agreed with the frontier panel 82% and under-called
# real instances), which majority voting against two stronger judges absorbs.
JUDGES = os.environ.get('DELLM_JUDGES', ','.join([
    'x-ai/grok-4.5',                     # xAI       $0.0062
    'z-ai/glm-5.2',                      # Zhipu     $0.0016
    'deepseek/deepseek-v4-flash-0731',   # DeepSeek  $0.0001
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


def call(model, prompt, max_tokens=4000, retries=3, timeout=180):
    """One completion, with the reasoning-starvation failure handled explicitly.

    A reasoning model spends tokens thinking before it writes anything, and that
    thinking is charged against max_tokens. Starve it and the response comes back
    with finish_reason "length" and an EMPTY content field, which reads exactly
    like a refusal or a network failure. Observed: qwen3.8-max spending 4,876
    reasoning tokens before emitting 405 characters.

    You cannot switch this off. Verified against the API: `reasoning:
    {"exclude": true}` still consumed the full budget and returned nothing, and
    `effort: "low"` did the same. Those flags change what you are shown, not
    what is spent. The only fix is room, so starvation doubles the budget and
    retries rather than counting as an error.
    """
    budget = max_tokens
    for i in range(retries):
        try:
            body = json.dumps({'model': model,
                               'messages': [{'role': 'user', 'content': prompt}],
                               'max_tokens': budget}).encode()
            req = urllib.request.Request(URL, data=body, headers={
                'Authorization': f'Bearer {key()}', 'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.load(r)
            ch = d['choices'][0]
            content = (ch.get('message', {}) or {}).get('content')
            if content and content.strip():
                return content.strip()
            if ch.get('finish_reason') == 'length':
                spent = (d.get('usage', {}).get('completion_tokens_details', {})
                         or {}).get('reasoning_tokens')
                # Size the next attempt from what it actually spent rather than
                # blindly doubling: starting well below the requirement, doubling
                # runs out of retries before it ever reaches a workable budget.
                budget = max(budget * 2, (spent or budget) * 2 + 2000)
                if i == retries - 1:
                    return (f'__ERROR__ output starved by reasoning: spent {spent} reasoning '
                            f'tokens with no content, gave up below {budget}')
                continue                      # not transient, do not sleep
        except Exception as e:                # noqa: BLE001
            if i == retries - 1:
                return f'__ERROR__ {e}'
        time.sleep(3 * (i + 1))
    return '__ERROR__ empty response after retries'


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
