#!/usr/bin/env python3
"""Diff the current measurement against the last recorded baseline.

    python3 research/drift.py            # report drift
    python3 research/drift.py --write     # record current numbers as the baseline

The point is to make decay a command rather than a discovery. `crucial` fell 85%
between 2024 and 2026 and nobody noticed for two years, because there was
nothing to notice it with.
"""
import argparse, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('DELLM_DATA', os.path.join(HERE, 'data'))
BASELINE = os.path.join(HERE, 'baseline.json')

sys.path.insert(0, HERE)
from measure import PATTERNS, PUBMED_WINDOWS, DASHES, rate   # noqa: E402

THRESHOLD = 0.30      # report anything that moved more than this fraction


def rates():
    out = {}
    for tag, label in PUBMED_WINDOWS:
        p = os.path.join(DATA, f'pubmed/{tag}.txt')
        if not os.path.exists(p):
            sys.exit(f'missing {p}\nrun: make fetch')
        t = io.open(p, encoding='utf-8', errors='replace').read()
        out[label] = {n.strip(): round(rate(t, pat), 2) for n, pat in PATTERNS}
    for tag, label in (('ypre', 'papers-pre'), ('y2026', 'papers-2026')):
        p = os.path.join(DATA, f'papers/{tag}.txt')
        if not os.path.exists(p):
            continue
        t = io.open(p, encoding='utf-8', errors='replace').read()
        out[label] = {n.strip(): round(rate(t, pat), 2) for n, pat in PATTERNS}
    for tag, label in (('pre', 'arxiv-2020'), ('y2026', 'arxiv-2026')):
        p = os.path.join(DATA, f'arxiv/{tag}.txt')
        if not os.path.exists(p):
            continue
        t = io.open(p, encoding='utf-8', errors='replace').read()
        out[label] = {n: round(rate(t, pat), 2) for n, pat in DASHES}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--date', default=os.environ.get('DELLM_DATE', ''))
    a = ap.parse_args()
    cur = rates()

    if a.write or not os.path.exists(BASELINE):
        if not a.date:
            sys.exit('pass --date YYYY-MM so the baseline records when it was taken')
        json.dump({'recorded': a.date,
                   'corpus': 'PubMed Sensors (Basel); arXiv cs.LG. See research/README.md',
                   'rates': cur}, open(BASELINE, 'w'), indent=1, sort_keys=True)
        print(f'wrote {BASELINE} ({a.date})')
        return

    base = json.load(open(BASELINE))
    print(f"baseline recorded {base['recorded']}, comparing against current corpora\n")
    moved = 0
    for window, pats in cur.items():
        old = base['rates'].get(window)
        if not old:
            print(f'  {window}: NEW window, not in baseline')
            continue
        for name, now in pats.items():
            was = old.get(name)
            if was is None:
                print(f'  {window:<12} {name:<30} NEW pattern')
                moved += 1
                continue
            if was == 0 and now == 0:
                continue
            delta = (now - was) / was if was else float('inf')
            if abs(delta) >= THRESHOLD:
                arrow = 'up' if delta > 0 else 'down'
                pct = '  new' if was == 0 else f'{delta*100:+.0f}%'
                print(f'  {window:<12} {name:<30} {was:>7.2f} -> {now:>7.2f}  {pct:>7} {arrow}')
                moved += 1
    print()
    if moved:
        print(f'{moved} moved more than {THRESHOLD:.0%}. See research/REVIEW.md step 5.')
    else:
        print(f'nothing moved more than {THRESHOLD:.0%}.')


if __name__ == '__main__':
    main()
