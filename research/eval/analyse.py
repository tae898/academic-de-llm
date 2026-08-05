#!/usr/bin/env python3
"""Stage 3: the tables in research/EVAL.md, computed from the JSON.

    python3 research/eval/analyse.py
"""
import collections, json, os, re, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load   # noqa: E402

ARM = {'A': 'original', 'B': 'naive', 'C': 'skill'}

DENSITY = [
    ('Superficial -ing', r', (highlighting|underscoring|emphasizing|ensuring|reflecting|contributing to|allowing|enabling|focusing on)'),
    ('Copula avoidance', r'\b(serves as|stands as|functions as|boasts|offers|maintains)\b'),
    ("Kobak's ten markers", r'\b(across|additionally|comprehensive|crucial|enhancing|exhibited|insights|notably|particularly|within)\b'),
    ('Undue emphasis', r'\bpivotal\b|is critical for|plays a (crucial|pivotal|vital) role|is a testament'),
    ('Negative parallelism', r'not just .{0,40} but|not only .{0,40} but'),
]


def show_manifest(d, label):
    m = d['manifest']
    print(f"{label}: {m['date']}  rewriter={m['rewriter']}  judges={', '.join(m['judges'])}")
    print(f"  corpus: {m['corpus']}\n")


def style(d):
    ok = [r for r in d['results'] if r.get('parsed')]
    print(f"=== STYLE: how often each arm is judged the MORE machine-like of a pair ===")
    print(f"    lower is better. position randomised and corrected for. {len(ok)} parsed\n")
    for era in ('2026', '2024', 'pre-2022'):
        rows = [r for r in ok if r['era'] == era]
        if not rows:
            continue
        print(f"  -- {era} --")
        for pair in ('C_vs_B', 'C_vs_A', 'B_vs_A'):
            sub = [r for r in rows if r['pair'] == pair]
            if not sub:
                continue
            first, second = pair.split('_vs_')
            cnt = collections.Counter()
            for r in sub:
                p = str(r['parsed'].get('more_machine_like', ''))
                if p not in ('1', '2'):
                    continue
                cnt[(second if p == '1' else first) if r['flip']
                    else (first if p == '1' else second)] += 1
            tot = sum(cnt.values())
            if tot:
                print(f"     {ARM[first]:>8} {cnt[first]/tot*100:>5.1f}%  vs  "
                      f"{ARM[second]:>8} {cnt[second]/tot*100:>5.1f}%   (n={tot})")
        print()
    print("  CAVEAT: the pre-2022 originals cannot be AI-generated, yet judges call them")
    print("  more machine-like than a rewrite. This metric partly measures 'edited'.")
    print("  skill-vs-naive survives that (both arms are edited). Do not quote vs-original.\n")


def fidelity(d):
    ok = [r for r in d['results'] if r.get('parsed')]
    print(f"=== FIDELITY: substantive only. praise-word removal is not a failure. {len(ok)} parsed ===\n")
    for era in ('2026', '2024', 'pre-2022'):
        for arm in ('B', 'C'):
            sub = [r for r in ok if r['arm'] == arm and r['era'] == era]
            if not sub:
                continue
            f = sum(1 for r in sub if r['parsed'].get('substantively_faithful') is True)
            sev = collections.Counter(r['parsed'].get('severity') for r in sub)
            loss = statistics.mean(len(r['parsed'].get('substantive_losses') or []) for r in sub)
            ev = statistics.mean(float(r['parsed'].get('evaluative_only_changes') or 0) for r in sub)
            print(f"  {era:<9} {ARM[arm]:<9} faithful {f:>2}/{len(sub)} ({f/len(sub)*100:>3.0f}%)  "
                  f"major={sev.get('major', 0)}  losses/judgement {loss:.1f}  eval-only {ev:.1f}")
        print()


def density(d):
    ok = [r for r in d['results']
          if not r['B'].startswith('__ERROR__') and not r['C'].startswith('__ERROR__')]
    for era in ('2026', '2024', 'pre-2022'):
        rows = [r for r in ok if r['era'] == era]
        if not rows:
            continue
        print(f"=== TELL DENSITY, per 10k words, {len(rows)} {era} abstracts ===")
        print("    objective, no judge involved. partly circular for arm C.\n")
        print(f"{'pattern':<24}{'original':>10}{'naive':>10}{'skill':>10}")
        print('-' * 54)
        for name, pat in DENSITY:
            vals = []
            for arm in ('A', 'B', 'C'):
                n = sum(len(re.findall(pat, r[arm], re.I)) for r in rows)
                w = sum(len(r[arm].split()) for r in rows)
                vals.append(n / max(w, 1) * 10000)
            print(f"{name:<24}" + ''.join(f'{v:>10.1f}' for v in vals))
        print()
    print("\n  RAW REGEX COUNTS. Patterns find candidates, not violations, and this")
    print("  table cannot read a hit in context. Adjudicating the 2026 copula row by")
    print("  hand turned 'naive beats skill' into 'both removed 3 of 3 real cases,")
    print("  the rest are `maintains` as an ordinary verb'. Check before quoting.")
    print("  Also partly circular for the skill arm.\n")


def adjudicated(d, rw):
    """Real-hit counts after a judge panel classifies each regex match."""
    import collections as _c
    votes = _c.defaultdict(list)
    for r in d['results']:
        if not r.get('parsed'):
            continue
        key = (r['i'], r['arm'], r['pattern'], r['match'], r['context'][:60])
        votes[key].append(bool(r['parsed'].get('real')))

    era_of = {x['i']: x['era'] for x in rw['results']}
    real = _c.Counter(); raw = _c.Counter(); unanimous = 0
    for (i, arm, pat, _m, _c2), vs in votes.items():
        era = era_of.get(i)
        raw[(era, pat, arm)] += 1
        if len(set(vs)) == 1:
            unanimous += 1
        if sum(vs) > len(vs) / 2:
            real[(era, pat, arm)] += 1

    print(f"=== ADJUDICATED HITS: panel majority of {len(next(iter(votes.values())))} judges "
          f"on {len(votes)} matches ===")
    print(f"    unanimous on {unanimous}/{len(votes)} ({unanimous/len(votes)*100:.0f}%)\n")
    pats = sorted({p for _e, p, _a in raw})
    for era in ('2026', '2024', 'pre-2022'):
        if not any(e == era for e, _p, _a in raw):
            continue
        n = sum(1 for x in rw['results'] if x['era'] == era)
        print(f"  -- {era}, {n} abstracts --")
        print(f"     {'pattern':<22}{'original':>18}{'naive':>16}{'skill':>16}")
        for pat in pats:
            cells = []
            for arm in ('A', 'B', 'C'):
                cells.append(f"{real[(era,pat,arm)]} real /{raw[(era,pat,arm)]:>3} raw")
            print(f"     {pat:<22}" + ''.join(f'{c:>18}' if i == 0 else f'{c:>16}'
                                              for i, c in enumerate(cells)))
        print()
    print("  'real' = majority of the panel called it a genuine instance, not a")
    print("  words-matched false positive. Raw counts are what an unadjudicated")
    print("  density table would have reported.\n")


def calibrate(d):
    """Does the panel agree with the hand labels made before it existed?"""
    import collections as _c
    hp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'handlabels.json')
    if not os.path.exists(hp):
        return
    hand = json.load(open(hp))['labels']
    votes = _c.defaultdict(list)
    for r in d['results']:
        if r.get('parsed'):
            votes[(r['pattern'], r['match'].lower(), r['context'])].append(bool(r['parsed'].get('real')))

    agree = dis = miss = 0
    print("=== CALIBRATION: panel vs the author's hand labels ===\n")
    for h in hand:
        found = [v for (p, m, ctx), v in votes.items()
                 if p == h['pattern'] and h['context_fragment'][:40].lower() in ctx.lower()]
        if not found:
            miss += 1
            continue
        vs = found[0]
        panel = sum(vs) > len(vs) / 2
        if panel == h['real']:
            agree += 1
        else:
            dis += 1
            print(f"  DISAGREE  {h['pattern']}: hand={h['real']} panel={panel}")
            print(f"            \"{h['context_fragment'][:70]}\"")
    tot = agree + dis
    if tot:
        print(f"\n  agreed on {agree}/{tot} ({agree/tot*100:.0f}%), {miss} hand labels not "
              f"matched in this run's hits")
    print("  The hand labels are one person, unblinded, with a stake in the result.")
    print("  Disagreement is not automatically the panel being wrong.\n")


def main():
    rw = load('rewrites.json')
    show_manifest(rw, 'rewrites')
    density(rw)
    try:
        adj = load('adjudicated.json')
        adjudicated(adj, rw)
        calibrate(adj)
    except SystemExit:
        print("  (adjudicated.json not found, run research/eval/adjudicate.py)\n")
    for name, fn in (('style.json', style), ('fidelity.json', fidelity)):
        try:
            fn(load(name))
        except SystemExit:
            print(f"  ({name} not found, run research/eval/judge.py)\n")


if __name__ == '__main__':
    main()
