#!/usr/bin/env python3
"""Stage 4: decide which regex hits are real.

A density table built from raw regex counts is not evidence, and this repo says
so repeatedly. It said so while shipping one anyway: the 2026 copula row showed
"naive beats skill" until all nine hits were read by hand, at which point both
arms had removed 3 of 3 real instances and every remaining hit was `maintains`
used as an ordinary verb.

Hand-adjudication does not scale past a handful, and a single hand-labeller is
exactly the thing that should not be trusted unchecked. So each hit goes to a
panel, majority vote decides, and the panel is calibrated against the hand
labels in `handlabels.json` before its verdicts are used for anything.

    python3 research/eval/adjudicate.py
    python3 research/eval/adjudicate.py --calibrate   # agreement vs hand labels only
"""
import argparse, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import JUDGES, Incremental, call, load, manifest   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# Definitions are Wikipedia's, restated so a judge with no context can apply
# them. Each carries the false positive that actually occurred in practice.
PATTERNS = {
    'copula avoidance': dict(
        # `provides?` bare was 1/6 and mostly noise ("the tool provides X" is a
        # real verb). Narrowed to the copular form it keeps the one real instance
        # it was there for, "GeoSeqNet provides an effective and reliable
        # solution", and drops the five false positives: 43% -> 58% precision
        # with no recall lost.
        regex=r'\b(serves? as|serving as|stands? as|functions? as|boasts?|offers?|'
              r'remains?|positions? \w+ as|presents? a|'
              r'provides? an? [\w\s]{0,24}?(solution|approach|framework|means|basis))\b',
        definition="A plain `is` or `are` dressed up in a fancier verb. "
                   "'This model serves as a proof of concept' means 'is a proof of concept'.",
        not_a_hit="The verb is doing real work and cannot be replaced by 'is'. "
                  "'maintains a high execution speed of 35 FPS' describes sustained behaviour "
                  "over time, not identity. 'offers three modes' means it provides them."),
    'superficial -ing': dict(
        regex=r'[, ](highlighting|underscoring|emphasizing|ensuring|reflecting|'
              r'contributing to|providing|enhancing|allowing|helping|supporting|'
              r'maintaining|thereby \w+ing)\b',
        definition="A participial clause after a comma that attaches vague interpretation "
                   "to the fact before it, adding no information. "
                   "'The cache is checked first, improving performance.'",
        not_a_hit="The clause states a specific factual consequence rather than vague praise. "
                  "'..., enabling real-time synchronisation between the virtual and physical cell' "
                  "names a concrete capability. Also not a hit if the -ing word is a noun."),
    'undue emphasis': dict(
        # `pivotal` alone scores only 40% precision, and dropping it lifted the
        # pattern to 90%. It also lost two real instances ("are pivotal to
        # classification performance"). For a finder whose hits an agent reads
        # anyway, a miss costs more than a false positive, so it stays.
        regex=r'\b(pivotal|invaluable)\b|\bis (crucial|essential|vital|critical)\b|'
              r'plays a (crucial|pivotal|vital) role|is a testament|'
              r'significant potential|highlighting the importance',
        definition="Generic assertion of importance standing in for a specific fact. "
                   "'X plays a vital role in Y' tells the reader nothing about X.",
        not_a_hit="The importance claim is immediately substantiated, or the word is used "
                  "in a precise technical sense."),
    'negative parallelism': dict(
        regex=r'not just .{0,60} but|not only .{0,60} but|'
              r'unlike .{0,80}?\b(this work|this study|we|our)\b',
        definition="A false contrast erected so the next clause can knock it down, where the "
                   "first half was never in question.",
        not_a_hit="It corrects a real prior claim, or both halves carry distinct information "
                  "the reader needs."),
}

# Structured for prompt caching: the invariant block comes first and everything
# that varies per hit comes last. On the 24-hour bill, grok cached 1,611 of 1,640
# calls while qwen cached 21 of 2,025, because a short or variable prefix never
# reaches the provider's minimum cacheable length. Do not move the context up.
PREAMBLE = """You are checking whether text fragments are real instances of writing patterns.

A search matched some words. Your job is to say whether the match is a genuine
instance of the pattern, or whether the words merely coincided.

The patterns and their definitions:

{catalogue}

Judge only the single fragment given below, against the single pattern named.
Answer with strict JSON and nothing else: {{"real": true or false, "why": "one short sentence"}}
"""

CATALOGUE = '\n\n'.join(
    f"{n.upper()}\n  IS: {v['definition']}\n  IS NOT: {v['not_a_hit']}"
    for n, v in PATTERNS.items())

PROMPT = PREAMBLE + """
---
PATTERN TO JUDGE: {name}
MATCHED PHRASE: "{match}"
CONTEXT: ...{context}...
"""


def hits(text, regex):
    for m in re.finditer(regex, text, re.I):
        s, e = max(0, m.start() - 130), min(len(text), m.end() + 130)
        yield m.group(0), text[s:e].replace('\n', ' ')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--calibrate', action='store_true')
    a = ap.parse_args()

    rw = load('rewrites.json')
    jobs = []
    for r in rw['results']:
        if r['B'].startswith('__ERROR__') or r['C'].startswith('__ERROR__'):
            continue
        for arm in ('A', 'B', 'C'):
            for name, spec in PATTERNS.items():
                for match, ctx in hits(r[arm], spec['regex']):
                    for j in JUDGES[:3]:            # 3 is enough for a majority
                        jobs.append(dict(i=r['i'], era=r['era'], arm=arm, pattern=name,
                                         match=match, context=ctx, judge=j,
                                         prompt=PROMPT.format(catalogue=CATALOGUE, name=name,
                                                              match=match, context=ctx)))
    # Resume: a killed run costs nothing but the calls already made.
    done = set()
    prev = []
    op = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'adjudicated.json')
    if os.path.exists(op):
        allprev = json.load(open(op))['results']
        # Only SUCCESSFUL calls count as done. Keying on job identity alone makes
        # a transient failure permanent: an exhausted account or a rate limit
        # would be skipped forever on every subsequent run.
        prev = [r for r in allprev if r.get('parsed')]
        dropped = len(allprev) - len(prev)
        if dropped:
            print(f'  retrying {dropped} calls that failed in a previous run', flush=True)
        done = {(r['i'], r['arm'], r['pattern'], r['match'], r['context'][:60], r['judge'])
                for r in prev}
    jobs = [j for j in jobs
            if (j['i'], j['arm'], j['pattern'], j['match'], j['context'][:60], j['judge']) not in done]
    print(f'{len(jobs)} adjudication calls remaining ({len(done)} already done)', flush=True)
    if not jobs:
        print('nothing to do'); return

    out = Incremental('adjudicated.json', manifest(rw['manifest']['corpus'], stage='adjudicate'))
    for r in prev:
        out.data['results'].append(r)
    out.flush()

    def work(job):
        raw = call(job['judge'], job.pop('prompt'), max_tokens=6000, timeout=300)
        m = re.search(r'\{.*\}', raw, re.S)
        try:
            job['parsed'] = json.loads(m.group(0)) if m else None
        except Exception:                            # noqa: BLE001
            job['parsed'] = None
        if not job['parsed']:
            job['raw'] = raw[:200]                   # so a failure is diagnosable
        return job

    # as_completed, not map: map yields in submission order, so one slow judge
    # blocks every finished result behind it. That makes the incremental write
    # non-incremental and looks like a stall.
    with ThreadPoolExecutor(max_workers=24) as ex:
        futs = [ex.submit(work, j) for j in jobs]
        for n, f in enumerate(as_completed(futs), 1):
            out.append(f.result())
            if n % 100 == 0:
                print(f'  {n}/{len(jobs)}', flush=True)
    print(f'wrote {out.path}\nnext: python3 research/eval/analyse.py --adjudicated')


if __name__ == '__main__':
    main()
