#!/usr/bin/env python3
"""Test every claimed AI tell against the corpora, and keep only what survives.

    python3 research/audit.py            # the table
    python3 research/audit.py --targets  # pre-AI rates, for SKILL.md

The skill used to ship whatever Wikipedia and the popular round-ups listed.
Several of those patterns occur ZERO times in academic prose, and two of them
went DOWN after ChatGPT, meaning the skill was telling authors to remove things
that had become less common. This is the filter that should have existed first.

A candidate earns a place by rising against a pre-ChatGPT baseline in the same
venue, in at least two of three corpora, at a rate high enough to matter. One
of the three is a different field entirely, so a pattern tuned on biomedical
abstracts cannot pass on its home turf alone.

Nothing here needs an API key. Run it before believing any claim about what AI
writing looks like, including the claims in this repository.
"""
import argparse, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('DELLM_DATA', os.path.join(HERE, 'data'))
sys.path.insert(0, HERE)
from measure import rate   # noqa: E402  (mean of per-document rates)

CORPORA = [
    ('Sensors abs', 'pubmed/ypre.txt', 'pubmed/y2026.txt'),
    ('PMC papers', 'papers/ypre.txt', 'papers/y2026.txt'),
    ('arXiv cs.LG', 'arxiv/pre.txt', 'arxiv/y2026.txt'),
]

# W = Wikipedia:Signs of AI writing.  K = Kobak et al. 2025.  O = own observation.
CANDIDATES = [
    # --- structure ---
    ('superficial -ing', 'W', r'[, ](highlighting|underscoring|emphasizing|ensuring|reflecting|'
                              r'contributing to|providing|enhancing|allowing|helping|supporting|'
                              r'maintaining|thereby \w+ing)\b'),
    ('copula avoidance', 'W', r'\b(serves? as|serving as|stands? as|functions? as|boasts?|offers?|'
                              r'remains?|positions? \w+ as|presents? a|'
                              r'provides? an? [\w\s]{0,24}?(solution|approach|framework|means|basis))\b'),
    ('undue emphasis', 'W', r'\b(pivotal|invaluable)\b|\bis (crucial|essential|vital|critical)\b|'
                            r'plays a (crucial|pivotal|vital) role|is a testament|'
                            r'significant potential|highlighting the importance'),
    ('negative parallelism', 'W', r'not just .{0,60} but|unlike .{0,80}?\b(this|our|we)\b'),
    ('vague attribution', 'W', r'Observers have|Experts (argue|say)|Industry reports|'
                               r'several sources|it is widely'),
    ('challenges formula', 'W', r'[Dd]espite .{0,80}?(faces|challenges)'),
    ('false ranges', 'O', r'from .{0,40} to .{0,40}, from'),
    ('bookends', 'O', r'(?:^|(?<=[.!?] ))(In summary|In conclusion|Ultimately|Overall)\b'),
    ('glue-word openers', 'O', r'(?:^|(?<=[.!?] ))(Moreover|Furthermore|Additionally|Consequently)\b'),
    ('stacked hedges', 'O', r'may potentially|can sometimes|might possibly|could potentially|'
                            r'generally tends'),
    ('self-referential frame', 'O', r'\bthis (paper|work|study) (presents|proposes|introduces|develops)\b'),
    ('intensifier, no number', 'O', r'\b(significantly|dramatically|substantially|considerably|markedly)\b'),
    ('pave the way', 'W', r'pave[sd]? the way|opens? (up )?new (avenues|possibilities)'),
    # --- vocabulary ---
    ("Kobak's ten", 'K', r'\b(across|additionally|comprehensive|crucial|enhancing|exhibited|'
                         r'insights|notably|particularly|within)\b'),
    ('delve/showcase/underscore', 'K', r'\b(delv|showcas|underscor)\w+\b'),
    ('crucial', 'K', r'\bcrucial\b'),
    ('robust', 'K', r'\brobust\w*\b'),
    ('leverage', 'O', r'\bleverag\w+\b'),
    ('comprehensive', 'K', r'\bcomprehensive\w*\b'),
    ('novel', 'O', r'\bnovel\b'),
    ('state-of-the-art', 'O', r'state[- ]of[- ]the[- ]art'),
    ('promising', 'O', r'\bpromising\b'),
    ('paradigm/landscape/realm', 'W', r'\b(paradigm|landscape|realm|tapestry)\b'),
    ('holistic/seamless/intricate', 'W', r'\b(holistic|seamless|meticulous|intricate)\b'),
    ('pivotal', 'K', r'\bpivotal\b'),
    ('to the best of our knowledge', 'O', r'to the best of (our|the authors)'),
]

MIN_RATE = 0.5      # per 10k in the post window; below this the pattern cannot matter
RISE = 1.5          # ratio that counts as a rise
NEEDED = 2          # corpora that must agree


def load(rel):
    p = os.path.join(DATA, rel)
    if not os.path.exists(p):
        sys.exit(f'missing {p}\nrun: python3 research/fetch.py')
    return io.open(p, encoding='utf-8', errors='replace').read()


def measure():
    texts = [(n, load(a), load(b)) for n, a, b in CORPORA]
    out = []
    for name, src, rx in CANDIDATES:
        cells = []
        for _, a, b in texts:
            x, y = rate(a, rx), rate(b, rx)
            cells.append((x, y, (y / x) if x > 0.02 else (float('inf') if y > MIN_RATE else 0.0)))
        rises = sum(1 for x, y, r in cells if r >= RISE and y >= MIN_RATE)
        dead = all(y < MIN_RATE for _, y, _ in cells)
        falls = sum(1 for x, y, r in cells if r < 1.0 and x >= MIN_RATE)
        if dead:
            v = 'DEAD, never occurs'
        elif rises >= NEEDED:
            v = f'CONFIRMED ({rises}/3)'
        elif falls >= NEEDED:
            v = f'FELL, not a tell ({falls}/3 down)'
        else:
            v = 'venue-limited'
        out.append((name, src, cells, v, rises))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--targets', action='store_true',
                    help='print the pre-AI rate of each confirmed pattern')
    a = ap.parse_args()
    rows = measure()

    if a.targets:
        print('Pre-ChatGPT rates per 10k words. These are the TARGET, not zero:\n')
        print(f"{'pattern':<28}" + ''.join(f'{n:>14}' for n, _, _ in CORPORA))
        for name, _s, cells, v, _r in rows:
            if v.startswith('CONFIRMED'):
                print(f'{name:<28}' + ''.join(f'{x:>14.1f}' for x, _y, _r in cells))
        print('\nHuman academic prose used all of these. A pass that drives one to')
        print('zero has gone past the baseline and is removing the author, not the model.')
        return

    print(f"{'candidate':<28}{'src':>4}" + ''.join(f'{n:>18}' for n, _, _ in CORPORA) + '   verdict')
    print('-' * (32 + 18 * len(CORPORA) + 24))
    for name, src, cells, v, rises in sorted(rows, key=lambda r: -r[4]):
        s = ''.join(f'{x:>7.1f}->{y:<5.1f}' + (f'{r:>4.1f}x' if r not in (0.0, float("inf")) else '    -')
                    for x, y, r in cells)
        print(f'{name:<28}{src:>4}{s}   {v}')
    print(f"\n  CONFIRMED = rises {RISE}x in >={NEEDED} of 3 corpora at >={MIN_RATE} per 10k.")
    print('  arXiv cs.LG is a different field and was never tuned on, but note that')
    print('  2020 ML preprints already ran high on `leverage`, `novel` and')
    print('  `state-of-the-art`, so a flat result there is weak evidence either way.')
    print('  src: W=Wikipedia, K=Kobak et al., O=own observation.')


if __name__ == '__main__':
    main()
