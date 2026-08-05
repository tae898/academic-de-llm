#!/usr/bin/env python3
"""Stage 3: the tables in research/EVAL.md, computed from the JSON.

    python3 research/eval/analyse.py
"""
import collections, os, re, statistics, sys

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
    print("\n  The naive arm getting WORSE is the non-circular part: it was not")
    print("  optimising for these patterns either way.\n")


def main():
    rw = load('rewrites.json')
    show_manifest(rw, 'rewrites')
    density(rw)
    for name, fn in (('style.json', style), ('fidelity.json', fidelity)):
        try:
            fn(load(name))
        except SystemExit:
            print(f"  ({name} not found, run research/eval/judge.py)\n")


if __name__ == '__main__':
    main()
