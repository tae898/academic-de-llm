#!/usr/bin/env python3
"""Stage 5: what do the finders MISS?

`adjudicate.py` answers "of what the regex caught, how much was real" — that is
precision. On its own it is half a claim: a pattern that matched nothing would
score 100%.

Here judges read whole texts cold, never seeing a regex, and list every instance
they find. Anything they find that the regex does not match is a miss.

An instance counts only if at least two of three judges independently quote the
same span. One judge listing something is as likely to be a hallucinated
instance as a real miss, and there is no human step anywhere in this pipeline to
catch that.

    python3 research/eval/recall.py [--era 2026] [--n 60]
"""
import argparse, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import JUDGES, Incremental, call, load, manifest   # noqa: E402
from adjudicate import PATTERNS                                # noqa: E402

PROMPT = """Read the scientific abstract below and find every instance of the writing patterns listed.

{patterns}

Quote each instance EXACTLY as it appears, copying the words verbatim from the abstract.
Include enough words to locate it, roughly five to fifteen.
If a pattern does not occur, give an empty list. Do not invent instances.

ABSTRACT:
{text}

Strict JSON only, no other output:
{{{schema}}}"""


def build_prompt(text):
    blocks, schema = [], []
    for i, (name, spec) in enumerate(PATTERNS.items(), 1):
        blocks.append(f"{i}. {name.upper()}\n   IS: {spec['definition']}\n   IS NOT: {spec['not_a_hit']}")
        schema.append(f'"{name}": ["exact quote", ...]')
    return PROMPT.format(patterns='\n\n'.join(blocks), text=text, schema=', '.join(schema))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--era', default='2026')
    ap.add_argument('--n', type=int, default=60)
    a = ap.parse_args()

    rw = load('rewrites.json')
    rows = [r for r in rw['results'] if r['era'] == a.era][:a.n]
    jobs = [dict(i=r['i'], era=r['era'], judge=j, text=r['A'], prompt=build_prompt(r['A']))
            for r in rows for j in JUDGES[:3]]

    op = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'recall.json')
    done = set()
    prev = []
    if os.path.exists(op):
        allprev = json.load(open(op))['results']
        prev = [r for r in allprev if r.get('parsed')]      # failures get retried
        done = {(r['i'], r['judge']) for r in prev}
        if len(allprev) - len(prev):
            print(f'  retrying {len(allprev)-len(prev)} failed calls', flush=True)
    jobs = [j for j in jobs if (j['i'], j['judge']) not in done]
    print(f'{len(jobs)} calls remaining ({len(done)} done), {len(rows)} abstracts x 3 judges',
          flush=True)
    if not jobs:
        print('nothing to do'); return

    out = Incremental('recall.json', manifest(rw['manifest']['corpus'], stage='recall',
                                              era=a.era, abstracts=len(rows)))
    for r in prev:
        out.data['results'].append(r)
    out.flush()

    def work(job):
        raw = call(job['judge'], job.pop('prompt'), max_tokens=8000, timeout=600)
        m = re.search(r'\{.*\}', raw, re.S)
        try:
            job['parsed'] = json.loads(m.group(0)) if m else None
        except Exception:                                    # noqa: BLE001
            job['parsed'] = None
        if not job['parsed']:
            job['raw'] = raw[:200]
        job.pop('text', None)
        return job

    with ThreadPoolExecutor(max_workers=4) as ex:
        for n, r in enumerate(ex.map(work, jobs), 1):
            out.append(r)
            if n % 25 == 0:
                print(f'  {n}/{len(jobs)}', flush=True)
    print(f'wrote {out.path}\nnext: python3 research/eval/score.py')


if __name__ == '__main__':
    main()
