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

## 0.2.0 (2026-08-08)

**The corpus went from one journal to seven publishers**, and that changed what
the skill can claim. `research/audit.py` is new: it tests every candidate tell
against ten corpora — *Sensors* abstracts and full texts, PLOS ONE, BMJ Open,
Nature Communications, and arXiv `cs.LG`, `cs.AI`, `cs.CL`, `econ.EM`,
`math.ST` — and keeps only what rises in a venue it was not tuned on.

Four of twenty-six candidates survive: copula avoidance, Kobak's ten as a set,
the superficial `-ing` clause, and dash-as-punctuation. Seven produce four
matches across sixty documents between them. Five moved the wrong way: `novel`
falls in 9 of 10 venues, glue-word openers in 9, `crucial` in 7.

**The em dash is the one with the cleanest evidence.** It rises in all five
arXiv categories, 2.0x to 3.5x, and sits at 1.1x to 1.6x in published journals.
Authors type it and copy editors take it out, which is why readers name it
first and why it looks flat in the published literature.

**A retraction.** "The skill relocates copula avoidance rather than removing
it" was published and withdrawn the same day. Most of what the judge panel
called copula avoidance was `X remains a challenge`, which means *still open
despite prior work* and is not a dressed-up copula. `SKILL.md` now says never
to edit it, and states the rule as `is` **without loss of meaning** rather than
`is` grammatically — a one-word bug that had stood for months.

**Rhythm moved from detection to guardrail.** Published academic prose did not
get flatter after ChatGPT: sentence-length variation is unchanged and repeated
openers went down. Flatness is what a de-slop pass *creates* — it halves the
standard deviation and the longest sentence. The directive now has a checkable
form: keep the longest sentence long.

**Six challengers were measured and rejected**, which is why `SKILL.md` is
nearly unchanged despite all of the above. A category collapse, a semantic
reframe, a 5KB condensation, a 19-line prompt, an edit-locality rule, and a
cut of the dead patterns all scored worse on the judged outcome. Two findings
came out of losing:

- **A list and a test do different jobs.** Deleting the participle list in
  favour of a description cost 67% of those removals down to 24%.
- **Hedging in an instruction is not free.** Demoting three patterns to "a
  question about your field" cost sixteen points of style score for three
  points of safety. In a document a caveat is accuracy; in an instruction it is
  permission not to act.

**Three harness bugs**, each of which would have inverted a published result:
`judge.py` keyed its resume on document index, so re-running an arm silently
reused the previous skill's verdicts; the rewriter labelled its input
`ABSTRACT:` and short prompts echoed it back, penalising brevity in the exact
comparison that was measuring brevity; and the papers corpus was half
tables-of-contents with its bodies duplicated 1.85x.

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

**Four structural patterns became one category.** Copula avoidance,
superficial `-ing`, undue emphasis and negative parallelism were listed and
measured separately for months. They are one move: adding an evaluation the
evidence does not carry. The section is now `Unearned evaluation`, defined by a
test — *what measurement supports this rating?* — rather than by four trigger
lists.

That is not only tidier, it measures better. Reframing the quality-claim regex
off the verb and onto the praise adjective took its excess from **2.7x to 8.1x**
against a pre-ChatGPT baseline, because the verb form was matching ordinary
academic prose: `X remains a challenge` and `Mw serves as the primary
conditioning variable` were roughly nine tenths of its pre-2022 count and are
not tells. Precision went 60.7% to 64.3%, and on the 18 labelled cases the new
form catches 8 of 8 real and fires on 0 of 10 false, against 4 of 8 for a
noun-anchored version. `copula avoidance` is renamed `unmeasured quality claim`
throughout, floors refrozen with the reason recorded in `floors.json`.

**Rhythm moved from the detection side to the guardrail**, because it was
measured and is not a tell. In published academic prose the standard deviation
of sentence length is flat across the ChatGPT boundary (8.6 → 8.0 in abstracts,
15.9 → 16.8 in papers) and consecutive same-openers went *down*, 11.3% to 6.4%.
In raw model output it collapses: a de-slop pass halves both the variance and
the longest sentence. So "uniform rhythm" is what this skill produces, not what
it should look for, and the directive now has a checkable form — **keep the
longest sentence long**.

**A `What is NOT evidence` table**, four claims every other guide leads with,
each measured flat or backwards here: uniform sentence length, repeated
openers, title case headings in a paper, and paste artifacts.

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
