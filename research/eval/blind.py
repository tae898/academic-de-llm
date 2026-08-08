#!/usr/bin/env python3
"""Precision scored by a panel that never saw the regex.

    python3 research/eval/blind.py

`adjudicate.py` shows a judge a matched phrase and asks whether the match is a
real instance. That inherits the regex's framing, and it failed badly enough to
produce a retraction: 21 instances of "X remains a challenge" were unanimously
called copula avoidance, which they are not. Unanimity of agreement is not
accuracy.

This asks the question the other way round, using data already collected.
`recall.py` had a second panel read the same 30 texts COLD -- no regex, no
match, just the pattern definition -- and quote whatever it found. A regex hit
is counted real here only if a cold reader independently quoted overlapping
text. No API calls: both files already exist.

Both sides use a majority of three, or the comparison is meaningless. The first
version of this file did not, and manufactured a 30-point gap out of a
threshold mismatch.

The answer is that the framing effect is small overall -- 40% shown against 48%
blind -- and that it runs in OPPOSITE directions depending on the pattern.
`copula avoidance` is over-confirmed when the match is shown (46% against 35%),
which is the retracted `remains` story. `superficial -ing` is under-confirmed
(31% against 50%): shown ", providing" in isolation a judge sees nothing wrong,
because the tell is what the clause does to the sentence it hangs off, and that
sentence is not in front of them.

So a match-first panel is not simply credulous. It is bad at patterns whose
instances look innocuous out of context and too generous with patterns that
have a seductive name.
"""
import collections, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT   # noqa: E402

STOP = set('the a an of to in for and or with this that is are be by on as at from '
           'it its their they we our'.split())


def toks(s):
    return {w for w in re.findall(r'[a-z]+', s.lower()) if w not in STOP and len(w) > 2}


def overlaps(match, context, spans, min_judges=2):
    """Wrapper: count how many DISTINCT cold judges covered this hit.

    The first version of this file counted a hit as real if any one of three
    cold readers quoted it, and compared that against the shown panel's
    majority vote. That is a 1-of-3 threshold against a 2-of-3 threshold, and
    it manufactured a 30-point gap out of nothing. Both sides use a majority
    now. The one-judge figure is still printed, as an upper bound.
    """
    seen = {j for j, s in spans if _covers(match, context, j, s)}
    return len(seen) >= min_judges


def _covers(match, context, _judge, s):
    """Did a cold reader quote text covering this match?

    Matched phrases are short ("serves as") and cold quotes are clause-length,
    so substring comparison fails in both directions. Content-word overlap with
    the match, checked against the quote, is the workable test.
    """
    m, q = toks(match), toks(s)
    if not m or not q:
        return False
    if m <= q or len(m & q) / len(m) >= 0.5:
        return True
    if s.lower().strip() in context.lower():
        i = context.lower().find(s.lower().strip())
        j = context.lower().find(match.lower())
        return i >= 0 and j >= 0 and abs(i - j) < 120
    return False


def main():
    for f in ('adjudicated.json', 'recall.json'):
        if not os.path.exists(os.path.join(OUT, f)):
            sys.exit(f'missing {f}; run research/eval/adjudicate.py and recall.py')
    adj = json.load(open(os.path.join(OUT, 'adjudicated.json')))['results']
    rec = json.load(open(os.path.join(OUT, 'recall.json')))['results']

    cold = collections.defaultdict(lambda: collections.defaultdict(list))
    judges = collections.defaultdict(set)
    for x in rec:
        for pat, spans in (x.get('parsed') or {}).items():
            judges[pat].add(x['judge'])
            for s in spans or []:
                cold[x['i']][pat].append((x['judge'], s.strip()))

    # majority of the SHOWN panel, as adjudicate.py computes it
    votes = collections.defaultdict(list)
    meta = {}
    for r in adj:
        if not r.get('parsed') or r['arm'] != 'A':
            continue
        k = (r['i'], r['pattern'], r['match'], r['context'][:60])
        votes[k].append(bool(r['parsed'].get('real')))
        meta[k] = r['context']

    rows = collections.defaultdict(lambda: {'n': 0, 'shown': 0, 'blind': 0, 'any': 0})
    for (i, pat, match, _c), vs in votes.items():
        s = rows[pat]
        s['n'] += 1
        if sum(vs) > len(vs) / 2:
            s['shown'] += 1
        ctx = meta[(i, pat, match, _c)]
        if overlaps(match, ctx, cold[i].get(pat, []), 2):
            s['blind'] += 1
        if overlaps(match, ctx, cold[i].get(pat, []), 1):
            s['any'] += 1

    print('Precision, scored two ways on the same 30 abstracts.\n')
    print(f"{'pattern':<24}{'hits':>6}{'shown, 2 of 3':>15}{'blind, 2 of 3':>15}{'blind, 1 of 3':>15}")
    print('-' * 76)
    tot = collections.Counter()
    for pat in sorted(rows):
        s = rows[pat]
        for k in ('n', 'shown', 'blind', 'any'):
            tot[k] += s[k]
        print(f"{pat:<24}{s['n']:>6}{s['shown'] / s['n'] * 100:>14.0f}%"
              f"{s['blind'] / s['n'] * 100:>14.0f}%{s['any'] / s['n'] * 100:>14.0f}%")
    print('-' * 76)
    print(f"{'ALL':<24}{tot['n']:>6}{tot['shown'] / tot['n'] * 100:>14.0f}%"
          f"{tot['blind'] / tot['n'] * 100:>14.0f}%{tot['any'] / tot['n'] * 100:>14.0f}%")
    print('\n  shown, 2 of 3:  a judge was handed the phrase and asked if it was real.')
    print('  blind, 2 of 3:  a majority of cold readers independently quoted text')
    print('                  covering the hit, having never seen a regex.')
    print('  blind, 1 of 3:  any one of them did. An upper bound.')
    print('\n  Compare the two majority columns; they are the like-for-like pair.')
    print('  The framing effect is small. Being handed a match makes a panel')
    print('  slightly HARSHER, not more credulous, which is the opposite of what')
    print('  the retracted `remains` finding suggested. That was a category error')
    print('  in one pattern, not a systematic bias across all four.')
    print('\n  The overlap rule does not matter: requiring the whole match inside')
    print('  the quote, half its content words, or a literal substring all give')
    print('  the same answer. The judge threshold is what moves it.')


if __name__ == '__main__':
    main()
