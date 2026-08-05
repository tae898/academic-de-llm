#!/usr/bin/env python3
"""Score the current regexes against the frozen labels. No API calls, no cost.

A regex change is a measurable change, not a matter of taste. This replays every
labelled hit through the current pattern and reports what happens to precision.

    python3 research/eval/regress.py           # score, exit 1 if a floor is broken
    python3 research/eval/regress.py --set-floors   # record current scores as the floors

Runs in `make test`, so it guards every commit.
"""
import argparse, collections, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adjudicate import PATTERNS   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LABELS = os.path.join(HERE, 'labels.json')
FLOORS = os.path.join(HERE, 'floors.json')


def score():
    """Replay each labelled context through the current regex.

    A label is (context, real). If the current regex still matches that context
    it is still surfaced, and its label tells us whether that was worth doing.
    """
    labels = json.load(open(LABELS))['labels']
    out = collections.defaultdict(lambda: {'kept_real': 0, 'kept_false': 0,
                                           'dropped_real': 0, 'dropped_false': 0})
    for l in labels:
        if l['arm'] != 'A':                 # unedited text is the use case
            continue
        spec = PATTERNS.get(l['pattern'])
        s = out[l['pattern']]
        still = bool(spec and re.search(spec['regex'], l['context'], re.I))
        if still:
            s['kept_real' if l['real'] else 'kept_false'] += 1
        else:
            s['dropped_real' if l['real'] else 'dropped_false'] += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--set-floors', action='store_true')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()

    if not os.path.exists(LABELS):
        print('no labels.json; run research/eval/score.py --freeze')
        return 0
    s = score()

    cur = {}
    for pat, v in s.items():
        surfaced = v['kept_real'] + v['kept_false']
        cur[pat] = dict(precision=round(v['kept_real'] / surfaced, 3) if surfaced else 0.0,
                        real_kept=v['kept_real'], surfaced=surfaced,
                        real_lost=v['dropped_real'])

    if a.set_floors:
        json.dump({'_note': 'Precision floors from the frozen labels. A regex edit that drops '
                            'below these, or that stops surfacing a real instance, fails '
                            'tests. Regenerate deliberately, never to make a red test green.',
                   'floors': cur}, open(FLOORS, 'w'), indent=1, sort_keys=True)
        print(f'wrote {FLOORS}')
        return 0

    if not os.path.exists(FLOORS):
        print('no floors.json; run research/eval/regress.py --set-floors')
        return 0
    floors = json.load(open(FLOORS))['floors']

    bad = 0
    if not a.quiet:
        print(f"{'pattern':<26}{'precision':>12}{'floor':>9}{'real kept':>12}{'real lost':>11}")
        print('-' * 70)
    for pat, c in sorted(cur.items()):
        f = floors.get(pat)
        flag = ''
        if f:
            if c['precision'] < f['precision'] - 0.001:
                flag = ' PRECISION DROPPED'; bad += 1
            elif c['real_kept'] < f['real_kept']:
                flag = ' STOPPED FINDING A REAL INSTANCE'; bad += 1
        if not a.quiet:
            print(f"{pat:<26}{c['precision']*100:>11.1f}%{(f['precision']*100 if f else 0):>8.1f}%"
                  f"{c['real_kept']:>12}{c['real_lost']:>11}{flag}")
    if bad:
        print(f"\n{bad} pattern(s) regressed against research/eval/floors.json")
        return 1
    if not a.quiet:
        print("\nno regressions")
    return 0


if __name__ == '__main__':
    sys.exit(main())
