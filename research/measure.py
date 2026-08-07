#!/usr/bin/env python3
"""Reproduce every measured number in skills/academic-de-llm/references/sources.md.

    python3 research/fetch.py     # downloads the corpora (PubMed + arXiv)
    python3 research/measure.py   # prints the tables

Two corpora, because neither one alone can measure everything:

  PubMed, Sensors (Basel)   vocabulary and structural tells, four time windows.
                            CANNOT measure dashes: PubMed normalises every dash
                            to an ASCII hyphen. The raw XML contains zero U+2014
                            in every window including pre-2022. An earlier
                            version of this skill reported that zero as a
                            finding. It was an artifact.

  arXiv cs.LG               dashes, via preserved LaTeX markup (--- and --).

No API keys needed. Both are public endpoints.
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('DELLM_DATA', os.path.join(HERE, 'data'))

DOC_SEP = '\n\n'

PUBMED_WINDOWS = [('ypre', '2019-21'), ('y2024', '2024'), ('y2025', '2025'), ('y2026', '2026')]

PATTERNS = [
    ("Kobak's ten markers", r'\b(across|additionally|comprehensive|crucial|enhancing|exhibited|insights|notably|particularly|within)\b'),
    ("  crucial",           r'\bcrucial\b'),
    ("  delve/showcase/underscore", r'\b(delv|showcas|underscor)\w+\b'),
    ("  pivotal",           r'\bpivotal\b'),
    ("  robust",            r'\brobust\w*\b'),
    ("Superficial -ing",    r', (highlighting|underscoring|emphasizing|ensuring|reflecting|contributing to|allowing|enabling)'),
    ("Copula avoidance",    r'\b(serves as|stands as|functions as|boasts|offers|maintains)\b'),
    ("Undue emphasis",      r'plays a (crucial|pivotal|vital) role|is a testament'),
    ("Negative parallelism", r'not just .{0,40} but|not only .{0,40} but'),
    ("Vendor paste artifacts", r'contentReference|oaicite|grok_card|ppl-ai-file-upload|【'),
]

DASHES = [("--- (LaTeX em dash)", r'---'),
          ("-- (LaTeX en/em)",    r'(?<!-)--(?!-)'),
          ('spaced " - "',        r' - '),
          ("U+2014 literal",      r'—')]


def load(name):
    p = os.path.join(DATA, name)
    if not os.path.exists(p):
        sys.exit(f"missing {p}\nrun: python3 research/fetch.py")
    return io.open(p, encoding='utf-8', errors='replace').read()


def rate(text, pat):
    """Mean of per-document rates, not a pooled total.

    Pooling (all matches / all words) lets one enormous document dominate. It
    reversed a published direction once: em dash in full papers looked like it
    was falling, 6.1 to 4.7 pooled, and rises 3.1 to 4.9 per document. Every
    figure published before 2026-08-06 used the pooled form.
    """
    docs = [d for d in text.split(DOC_SEP) if len(d.split()) >= 80] or [text]
    rates = [len(re.findall(pat, d, re.I)) / max(len(d.split()), 1) * 10000 for d in docs]
    return sum(rates) / len(rates)


def concentration(text, pat):
    """Share of all matches held by the single worst document. Above ~25% the
    pooled figure is being driven by outliers and should not be quoted."""
    docs = [d for d in text.split(DOC_SEP) if len(d.split()) >= 80] or [text]
    counts = [len(re.findall(pat, d, re.I)) for d in docs]
    return max(counts) / sum(counts) * 100 if sum(counts) else 0.0


def table(title, corpora, patterns, note=''):
    print(f"\n{title}")
    if note:
        print(note)
    labels = [l for _, l in corpora]
    print(f"\n{'':<30}" + ''.join(f'{l:>11}' for l in labels))
    print('-' * (30 + 11 * len(labels)))
    for name, pat in patterns:
        print(f"{name:<30}" + ''.join(f'{rate(t, pat):>11.1f}' for t, _ in corpora))
    print(f"{'words':<30}" + ''.join(f'{len(t.split()):>11,}' for t, _ in corpora))


def main():
    pm = [(load(f'pubmed/{f}.txt'), l) for f, l in PUBMED_WINDOWS]
    table("Sensors (Basel), PubMed. Tells per 10k words. Same journal throughout.",
          pm, PATTERNS,
          "Sources 3 and 5 in references/sources.md. Dashes are NOT measurable here.")

    pp = [(load('papers/ypre.txt'), 'pre'), (load('papers/y2026.txt'), '2026')]
    table("PMC open-access full texts. Tells per 10k words.", pp, PATTERNS,
          "Source 3b. Full papers, not abstracts. Heading markup is NOT preserved,\n"
          "so nothing here says whether a paper's headings are title case.")

    ax = [(load('arxiv/pre.txt'), '2020'), (load('arxiv/y2026.txt'), '2026')]
    table("arXiv cs.LG abstracts. Dash forms per 10k words.", ax, DASHES,
          "The em dash correction in source 3. arXiv preserves LaTeX dash markup.")

    print("\nEvery figure above is prevalence or before-and-after, never a")
    print("counterfactual projection. Only Kobak et al. do the projection.")


if __name__ == '__main__':
    main()
