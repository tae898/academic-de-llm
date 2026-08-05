#!/usr/bin/env python3
"""Stage 6: score every finder on precision AND recall, per trigger word.

Precision alone is half a claim, and this is where the two halves meet.

    python3 research/eval/score.py            # scorecard
    python3 research/eval/score.py --freeze    # write labels.json, the regression fixture
"""
import argparse, collections, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load   # noqa: E402
from adjudicate import PATTERNS   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LABELS = os.path.join(HERE, 'labels.json')


def majority(votes):
    return sum(votes) > len(votes) / 2


def precision_labels():
    """Every adjudicated hit, collapsed to one label per match by panel majority."""
    d = load('adjudicated.json')
    votes = collections.defaultdict(list)
    keep = {}
    for r in d['results']:
        if not r.get('parsed'):
            continue
        k = (r['i'], r['arm'], r['pattern'], r['match'], r['context'][:60])
        votes[k].append(bool(r['parsed'].get('real')))
        keep[k] = r
    out = []
    for k, vs in votes.items():
        r = keep[k]
        out.append(dict(i=r['i'], era=r['era'], arm=r['arm'], pattern=r['pattern'],
                        match=r['match'], context=r['context'],
                        real=majority(vs), votes=vs, unanimous=len(set(vs)) == 1))
    return out, d['manifest']


def norm(s):
    return re.sub(r'\W+', ' ', (s or '').lower()).strip()


def recall_stats():
    """Instances at least two of three judges quoted independently, and whether
    the regex would have caught them."""
    try:
        d = load('recall.json')
    except SystemExit:
        return None
    rw = {r['i']: r['A'] for r in load('rewrites.json')['results']}
    found = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in d['results']:
        if not r.get('parsed'):
            continue
        for pat, quotes in (r['parsed'] or {}).items():
            if pat not in PATTERNS or not isinstance(quotes, list):
                continue
            for q in quotes:
                if isinstance(q, str) and len(q.split()) >= 3:
                    found[(r['i'], pat)][norm(q)].append(r['judge'])

    stats = collections.defaultdict(lambda: {'confirmed': 0, 'caught': 0, 'missed': []})
    for (i, pat), quotes in found.items():
        text = rw.get(i, '')
        for q, judges in quotes.items():
            # fuzzy-merge near-duplicate quotes from different judges
            allj = set(judges)
            for q2, j2 in quotes.items():
                if q2 != q and (q in q2 or q2 in q):
                    allj |= set(j2)
            if len(allj) < 2:
                continue                       # one judge only: not confirmed
            s = stats[pat]
            s['confirmed'] += 1
            # did the regex match anywhere inside the quoted span?
            span = next((text[max(0, m.start()-10):m.end()+10]
                         for m in re.finditer(re.escape(q[:40]), norm(text))), '')
            hit = bool(re.search(PATTERNS[pat]['regex'], q, re.I)) or \
                  bool(re.search(PATTERNS[pat]['regex'], span, re.I))
            if hit:
                s['caught'] += 1
            else:
                s['missed'].append(q[:70])
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--freeze', action='store_true')
    a = ap.parse_args()

    labels, man = precision_labels()
    if a.freeze:
        json.dump({'_note': 'Frozen adjudication labels. Regression fixture: a regex change '
                            'is scored against these rather than argued about. Panel majority '
                            'of 3 judges, no human in the loop.',
                   'manifest': man, 'labels': labels},
                  open(LABELS, 'w'), indent=1)
        print(f'wrote {LABELS} ({len(labels)} labels)')
        return

    print(f"corpus: {man['corpus']}\njudges: {', '.join(man['judges'])}\n")

    tok = collections.defaultdict(lambda: [0, 0])
    pat_p = collections.defaultdict(lambda: [0, 0])
    for l in labels:
        if l['arm'] != 'A':
            continue                            # unedited text is the use case
        tok[(l['pattern'], l['match'].lower())][1] += 1
        pat_p[l['pattern']][1] += 1
        if l['real']:
            tok[(l['pattern'], l['match'].lower())][0] += 1
            pat_p[l['pattern']][0] += 1

    rec = recall_stats()
    print(f"{'pattern / trigger':<40}{'precision':>18}{'recall':>16}")
    print('-' * 76)
    for pat in PATTERNS:
        pr, pa = pat_p[pat]
        rline = ''
        if rec and pat in rec:
            c, cf = rec[pat]['caught'], rec[pat]['confirmed']
            rline = f"{c}/{cf} {c/cf*100:>3.0f}%" if cf else 'no instances'
        print(f"{pat:<40}{f'{pr}/{pa}':>10}{(pr/pa*100 if pa else 0):>7.0f}%{rline:>16}")
        rows = sorted(((m, r, t) for (p, m), (r, t) in tok.items() if p == pat and t >= 2),
                      key=lambda x: (-x[1] / x[2], -x[2]))
        for m, r, t in rows:
            verdict = 'strong' if r / t >= 0.7 else ('weak' if r / t >= 0.2 else 'DROP')
            print(f"    {m[:34]:<36}{f'{r}/{t}':>10}{r/t*100:>7.0f}%{verdict:>16}")
        if rec and pat in rec and rec[pat]['missed']:
            for q in rec[pat]['missed'][:3]:
                print(f"    MISSED: {q}")
        print()
    if not rec:
        print("  (recall.json not found, run research/eval/recall.py)")


if __name__ == '__main__':
    main()
