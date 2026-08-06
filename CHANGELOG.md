# Changelog

Versions below 1.0.0 mean the patterns, tier ordering and file layout can still
change without notice. They have changed materially twice in the last day, both
times because a measurement contradicted the previous version. 1.0.0 is for when
a review cycle passes without a finding that forces a rewrite.

## A note on the numbering

Early development used 2.x and 3.x before this repository existed and before
anything was released. Those numbers implied a stability that was never earned:
v3.1.0 shipped with pattern finders that caught **8% of real instances**, which
was only discovered afterwards by measuring.

Renumbered to 0.x on 2026-08-06, with no releases or installs to break. The
mapping:

| Old | New | What it was |
|---|---|---|
| 2.0.0 | pre-release | private skill, never published |
| 3.0.0 | 0.3.0 | tier ordering inverted to formatting-first |
| 3.1.0 | 0.3.1 | register branch, decay data, Kobak figures corrected |
| — | **0.4.0** | finders retiered on measured precision and recall |

## 0.4.0 (2026-08-06)

**Finders retiered on measurement rather than judgement.** Recall went from 8%
to **74%**; precision from 32% to **51%**. Method: one judge panel labels every
regex hit real or a words-matched false positive, a second panel reads the same
texts cold and lists what it finds. Every figure in this release was re-measured
on a single model configuration after the panel changed; see `research/EVAL.md`
for how much moved.

Three defects, none conceptual:

- `, enabling` required a comma. "sensor signals enabling precise detection"
  has none. One character cost most of the recall on the highest-volume pattern.
- `serves as` was listed, `serve as` was not.
- Negative parallelism searched `not just X but`, matched 14 times across 60
  abstracts and was never once real. Every genuine instance used
  `unlike traditional studies that..., this work...`.

**A third register: academic papers.** 538k words of open-access full text show
title case headings flat across 2021 to 2026 (10.9 to 11.7 per 10k) and em
dashes *falling* (6.1 to 4.7). Both are journal house style. `SKILL.md` now says
to skip Tier 1 on a paper even though it has headings, because flagging
"2. Materials and Methods" is the fastest way to waste a pass.

**Per-trigger strength published.** Precision varies more inside a pattern than
between patterns: `serves as` 9/9, `is crucial` 13/14, `enabling` 5/36,
`maintains` 0/11. An agent reading a hit can now tell a certainty from a coin
flip.

**New finding, in neither published source:** third person singular is the tell
and the base form is an ordinary verb. `remains` 87% against `remain` 25%,
`provides` 36% against `provide` 11%, `offers` 35% against `offer` 0%.

Also: a quality judge that asks whether an edit is any *good*, not merely
faithful and unmachine-like; a regression fixture so a regex change is scored
against 701 labels with no API calls; and a rewriter upgraded to the strongest
available model, because a skill that only helps a weak model is not worth
shipping.

## 0.3.1 (2026-08-05)

Register branch: formatting dominates Markdown, structure dominates prose.
Vocabulary decay measured 2024 to 2026 (`crucial` down 85%, `delve` effectively
gone, structural tells holding).

Corrected every figure from Kobak et al., which had been carried from arXiv v1
for two years and was wrong in ten of eleven claims. Retracted an em-dash
finding built on a PubMed encoding artifact. Corrected a pattern attributed to
Wikipedia that is not on that page.

## 0.3.0 (2026-08-05)

Tier ordering inverted after measuring 35 agent-written READMEs: formatting
tells beat vocabulary tells by ten to fifty times, and per-vendor paste
artifacts fire zero times in agent-written text.

Fixed four pattern bugs that had shipped broken. They passed locally only
because the author's shell aliased `grep` to `ugrep`.
