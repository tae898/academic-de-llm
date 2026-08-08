---
name: academic-de-llm
version: 0.2.0
description: |
  Last-pass polish for academic writing: strip the surface markers that make a
  paper, abstract or academic blog post read as machine-generated, without
  flattening the prose or weakening a claim. Use when the user says "de-LLM",
  "de-slop", "remove the AI tells", "this reads like ChatGPT", or asks why a
  draft sounds generated. Covers LaTeX, Markdown and HTML.
license: MIT
metadata:
  sources: >
    Kobak et al., Science Advances 2025 (arXiv:2406.07016);
    Wikipedia:Signs of AI writing; own measurement over 1.3M words of
    academic text in three fields, 2026-08 (see references/sources.md)
  last_reviewed: 2026-08
  changelog: CHANGELOG.md
  review_process: research/REVIEW.md
---

# Academic de-LLM

Do one more editing pass so the text reads less machine-generated. Preserve
every factual claim exactly.

## The four things worth looking for

Everything else people list was tested against pre-ChatGPT and post-ChatGPT
corpora in three fields and dropped: twelve candidates either never occur in
academic prose or became *less* common after 2022. `research/audit.py` is the
filter. Ratios below are the rise against the same venue before ChatGPT.

**1. A clause that grades a fact instead of adding one.** *"…, highlighting the
importance of careful tuning"*, *"sensor signals enabling robust detection"*.
The fact is fine; the clause rates it. No comma needed. Rose **3.2x / 3.7x /
2.6x** — the most consistent tell measured, in every field.

**2. An evaluative word with no number behind it.** *"provides an efficient and
reliable solution"* means *"is good"*. *"significantly improves"* with no figure
means *"improves"*. Ask what was measured; if nothing was, cut the rating and
keep the fact. Rose **2.7x / 3.5x / 2.1x**.

**3. Density of the excess vocabulary**, not any single word: `across`,
`additionally`, `comprehensive`, `crucial`, `enhancing`, `exhibited`,
`insights`, `notably`, `particularly`, `within`, plus `paradigm`, `landscape`,
`realm`. One is nothing. Four in a paragraph doing no work is the signal. The
*set* rose **2.5x / 3.2x / 2.6x** while `crucial` and `novel` individually fell
below their pre-2022 rates — so count the set, never ban a word.

**4. Em dashes used for emphasis** — but only in a draft. They rose 3.0x in
preprints and are flat in published papers, because journals normalise dashes to
house style. In LaTeX look for `---` and `--`; in HTML `&mdash;`. Searching for
the literal `—` in a `.tex` file finds nothing and reports a false clean.

## Remove about two thirds. Not all of it.

Human academics wrote all four of these before ChatGPT existed, at roughly a
third of today's rate. A pass that drives one to zero has gone *past* the human
baseline: it removes the author, not the model. Measured, this is the way this
pass fails — judges said an earlier version lost something worth keeping 42% of
the time, and it had cut one pattern to a third of what real 2019 papers used.

Two thirds is the number because the *rate* differs wildly between fields and
the *multiplier* does not. Pre-ChatGPT `leverage` runs 0.7 per 10k in biomedical
abstracts and 4.4 in machine learning, but both rose by about the same factor.

## Never change

Code and inline code, tables, quotations, citations and reference lists, YAML
frontmatter, error messages, identifiers and file paths, en dashes in numeric
ranges like `0.88–0.98`, headings and numbering in a journal template or LaTeX
class, and anything written before November 2022.

**"X remains a challenge" is not a tell.** It means *still open despite prior
work*, which is the sentence that justifies the paper. `is` replaces it
grammatically and drops the meaning. A judge panel called 21 of these genuine
tells because it was shown a regex match instead of a sentence.

Say what you skipped when you report back.

## Keep the longest sentence long

Splitting long sentences at every participle is how this pass goes wrong.
Measured: a de-slop pass takes the standard deviation of sentence length from
15.0 to 6.8 and the longest sentence from 69 words to 36. Compare your longest
sentence with the original's; if it dropped by much, put a long one back.

Published academic prose did **not** get flatter after ChatGPT — sentence-length
variation is unchanged and repeated openers went *down*. Uniform rhythm is
something this pass creates, not something to look for.

## What this is not

It is not a detector. Population statistics do not classify individuals, text
written before November 2022 cannot be AI-generated whatever it looks like, and
an author who can explain their choices is an author. Use it to edit, never as
evidence about who wrote something.

It does not make text true, well argued, or worth reading.

## References

- `references/patterns.md` — the regexes, and their false-positive rates
- `references/sources.md` — what each source establishes and what it does not
- `research/audit.py` — re-run before trusting the four above; the list ages
