# Changelog

Versions below 1.0.0 mean the patterns, their ordering and the file layout can
still change without notice. The version number is the *released* version: commits
between releases do not touch it.

## A note on the numbering

Development ran through 2.x and 3.x before this repository existed and before
anything was released. Those numbers implied a stability that was never earned:
v3.1.0 shipped with pattern finders that caught **8% of real instances**, which
was only discovered afterwards by measuring.

Reset to **0.1.0** on 2026-08-07 for the first release, with no tags or installs
to break. Everything below happened before that release and is recorded because
the corrections are the useful part.

## 0.1.0 (2026-08-07) — first release

Scope narrowed to **academic writing**: papers, abstracts and academic blog
posts, in LaTeX, Markdown and HTML. The earlier version also claimed software
documentation, commit messages, PR descriptions and email, a range the
evaluation never tested.

Renamed from `de-llm` to `academic-de-llm` to match.

**Tiers replaced by named sections, ordered for academic prose.** Tier numbers
encoded a priority that the narrowed scope inverted: Tier 1 was labelled
"highest yield" and skipped on two of three document types, and every number
supporting it came from a corpus that is no longer in scope. The numbering had
already drifted once, leaving a review note in `sources.md` that named the wrong
tiers. Sections are now **structure**, **vocabulary**, **markup if you chose
it**, **paste artifacts**, in that order, so file order matches what to do
first. The markup section is scoped by a question rather than a rate: did you
choose this formatting, or did the venue?

**Out-of-scope corpora and their derived numbers deleted**, not just unreferenced
— the collection script, the prevalence section in `sources.md`, and every
percentage in `SKILL.md` that came from them. What survives is the conclusion
they supported, which the academic corpora support independently: heading style
in full texts is flat across 2021 to 2026, so a paper's formatting is the
venue's.

**Fixtures rebuilt per register.** A LaTeX paper pair and an academic blog pair
replace the software-documentation ones. The LaTeX pair is new coverage: the
skill has claimed LaTeX since it was written and had no worked example, and it
is the fixture that asserts `\section{Related Work}` and a `---` em dash must
*survive* a pass. 81 assertions, up from 54.

**Case sensitivity documented.** The eval scores structure and vocabulary
case-insensitively and `patterns.md` never said so. Matching them
case-sensitively silently drops every sentence-initial hit, including
`Unlike prior work, this study...`, which is the most common form of negative
parallelism.

**Both regex sets are now measured.** `measure.py` had carried the narrow
pre-0.4.0 patterns while `patterns.md` shipped the retiered ones, so the corpus
tables tracked patterns the skill no longer used. Rather than pick one, it now
reports a **probe** (tight definition, low baseline, interpretable ratio) and
the **shipped** regex imported from `research/eval/adjudicate.py`, and
`baseline.json` tracks both. They answer different questions: 8.9x is how much
the tell rose, 3.7x is what a real pass will find.

That immediately surfaced a finding the probe had hidden. **Copula avoidance is
the only tell measured here that has not peaked** — under the shipped regex it
rises in every window, 10.2 to 27.3 per 10k, with 2026 the highest. The probe
showed it peaking in 2025 and falling back, because the triggers carrying the
growth (`remains`, `presents a`, the copular `provides a`) were added in 0.4.0
and are absent from it.

**The papers corpus is measured at last.** `fetch.py` downloads 539k words of
PMC full text, `sources.md` published figures from it, and no committed script
read it, so that column was not reproducible.

**`make eval` was broken.** `research/eval/rewrite.py` still read
`skills/de-llm/SKILL.md` and would have raised `FileNotFoundError` on the first
stage of every run since the rename.

Everything below is pre-release development history.

## Pre-release: 0.4.0 (2026-08-06)

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
