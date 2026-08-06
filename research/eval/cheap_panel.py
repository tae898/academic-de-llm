#!/usr/bin/env python3
"""Can a cheap panel replace the expensive one?

The frontier panel costs about $7.40 per 1000 adjudication calls, most of it
reasoning tokens billed at output rates. Flash-tier models are roughly 40x
cheaper. Whether that is a saving or a corruption is an empirical question, and
`labels.json` is the answer key: 193 hits already labelled by the frontier panel.

Replays those hits through candidate cheap models and reports agreement. A model
that matches the expensive panel closely can do the bulk work; disagreements can
be escalated.

    python3 research/eval/cheap_panel.py [--n 60]
"""
import argparse, collections, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import call   # noqa: E402
from adjudicate import PATTERNS, PROMPT   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

CANDIDATES = [
    'qwen/qwen3.7-flash',
    'deepseek/deepseek-v4-flash-0731',
    'tencent/hy3',
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=60, help='labels to replay per model')
    a = ap.parse_args()

    labels = json.load(open(os.path.join(HERE, 'labels.json')))['labels']
    # Balance the sample: agreement on an all-false set is easy and meaningless.
    real = [l for l in labels if l['real']][:a.n // 2]
    fake = [l for l in labels if not l['real']][:a.n // 2]
    sample = real + fake
    print(f'{len(sample)} labels ({len(real)} real, {len(fake)} false) x {len(CANDIDATES)} models\n',
          flush=True)

    jobs = [(m, l) for m in CANDIDATES for l in sample]

    def work(job):
        m, l = job
        spec = PATTERNS[l['pattern']]
        p = PROMPT.format(name=l['pattern'], match=l['match'], context=l['context'],
                          definition=spec['definition'], not_a_hit=spec['not_a_hit'])
        raw = call(m, p, max_tokens=2000)
        mm = re.search(r'\{.*\}', raw, re.S)
        try:
            got = bool(json.loads(mm.group(0)).get('real')) if mm else None
        except Exception:                                   # noqa: BLE001
            got = None
        return m, l, got

    res = collections.defaultdict(lambda: {'agree': 0, 'dis': 0, 'fail': 0,
                                           'false_neg': 0, 'false_pos': 0})
    with ThreadPoolExecutor(max_workers=8) as ex:
        for m, l, got in ex.map(work, jobs):
            r = res[m]
            if got is None:
                r['fail'] += 1
            elif got == l['real']:
                r['agree'] += 1
            else:
                r['dis'] += 1
                # missing a real instance is the costly error, not flagging a false one
                r['false_neg' if l['real'] else 'false_pos'] += 1

    print(f"{'model':<34}{'agreement':>12}{'missed real':>14}{'over-flagged':>14}{'failed':>9}")
    print('-' * 84)
    for m in CANDIDATES:
        r = res[m]
        tot = r['agree'] + r['dis']
        pct = r['agree'] / tot * 100 if tot else 0
        print(f"{m:<34}{pct:>11.0f}%{r['false_neg']:>14}{r['false_pos']:>14}{r['fail']:>9}")
    print("\n  Agreement is against the frontier panel, which is not ground truth")
    print("  either. It agreed with the author's hand labels only 70% of the time.")


if __name__ == '__main__':
    main()
