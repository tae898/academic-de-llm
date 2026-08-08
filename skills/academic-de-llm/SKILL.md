---
name: academic-de-llm
version: 0.1.0
description: |
  Last-pass polish for academic writing: strip the surface markers that make a
  paper, abstract or academic blog post read as machine-generated, without
  flattening the prose or weakening a claim. Use when the user says "de-LLM",
  "de-slop", "remove the AI tells", "this reads like ChatGPT", or asks why a
  draft sounds generated. Covers LaTeX, Markdown and HTML. Scoped deliberately
  to scholarly prose, where the tells were measured.
license: MIT
metadata:
  sources: >
    Kobak et al., Science Advances 2025 (arXiv:2406.07016);
    Wikipedia:Signs of AI writing (community-maintained);
    own corpus measurements over 1.3M words of academic text, 2026-08
    (see references/sources.md)
  last_reviewed: 2026-08
  changelog: CHANGELOG.md
  review_process: research/REVIEW.md
---

# Academic de-LLM: Remove the Tells, Keep the Argument

Generated prose is rarely wrong. It is recognizable. This is the pass you run
last, after the argument is settled and before submission.

Scoped to academic writing on purpose. The measurements behind it come from
1.3M words of journal abstracts, open-access full texts and arXiv preprints.
Every claim here is measured or cited, and `references/sources.md` says which,
including what each source does **not** establish and which claims have no
source at all.

## What moves, and what does not

**One thing rises, and it is not a word list.** Sentences that grade the work
rather than report it. Three to eight times a pre-ChatGPT baseline in the same
journal, in abstracts and full papers alike, and still rising in 2026.

**Vocabulary rises too, and decays fastest.** `crucial` fell 84% and `delve` 89%
between 2024 and 2026 while `robust` rose 46%. A snapshot with an expiry date.

**Formatting is mostly the venue's.** Section headings sit flat across 2021 to
2026 in full texts, because "2. Materials and Methods" is what the form
requires. So that section is scoped by a question rather than a rate: **did you
choose this formatting?**

**Sentence rhythm did not move at all.** It is not a tell. It is the damage this
skill does, which is what the second directive bounds.

Figures in `references/sources.md`, which also says which claims have no
measurement behind them.

Related but separate, and by a different author: `SimpleEnglish` (ASD-STE100).
Use that when a reader might misread the text. Use this one when a reader might
think a machine wrote it. On a paper, run only this one, because STE bans the
modals that carry your certainty.

## Two directives, equally binding

**Delete the tell, keep the claim.** A rewrite that makes a sentence claim more than the evidence supports has broken the text to pass a style check. That is worse than the tell.

**Delete the tell, keep the rhythm.** This is the measured failure mode, not a
hypothetical, and it is why these rules override everything below.

On paper sections, a de-slop pass takes the standard deviation of sentence
length from 15.0 to 6.8 and the longest sentence from 69 words to 36. Comma
density halves. Every rewriter tested does this; following the guidance below
thoroughly makes it slightly worse.

**Keep the longest sentence long.** The single checkable version of this rule.
If the longest sentence in your output is roughly as long as the longest in the
input, you have not flattened the text, whatever else you did.

**Do not split a long sentence into three short ones just because the join was a participle.** Rewrite the participle in place, or make the clause subordinate. One long sentence among short ones is what a human paragraph looks like.

**Keep the connective tissue.** Phrases that signal what a sentence is doing, contrasting, conceding, moving on, are how a reader follows an argument. Several look like tells. Removing them scores well and reads worse.

**A pattern is not a verdict.** Frequency measures how often a construction
appears, not whether this instance earns its place for the reader. Only you can
answer the second question.

## Step zero: the skip pass

Do this before matching anything. These are never edited, and a pass that touches them does real damage:

Fenced code blocks and inline code spans. YAML, TOML, and JSON frontmatter or config. Markdown tables, including cells that use a dash as a "not applicable" placeholder. Task lists. Footnotes and citation blocks. Direct quotations from other people. Error messages and log lines. Identifiers, CLI flags, and file paths. En dashes inside numeric ranges such as `0.88–0.98`. Anything written before November 2022.

Say what you skipped when you report back ("skipped: 3 code blocks, 1 table, frontmatter"). It makes the pass auditable and it is the main defense against the false-positive rate documented below.

## Unearned evaluation

**Run this on every document. It is the skill.**

Four patterns were listed separately here until they were measured against each
other and turned out to be one move: adding an evaluation the evidence does not
carry. Not a claim about the subject, a claim about the work's value. That is
why the first directive keeps applying — the tell *is* a claim.

Together they rise **3 to 8 times** against a pre-ChatGPT baseline in the same
journal, in abstracts and full papers alike, and they held across 2024 to 2026
while the vocabulary below decayed.

One component has not peaked: the unmeasured quality claim runs 1.2, 7.0, 8.7,
**10.1** per 10k across 2019-21, 2024, 2025 and 2026.

**The test, which replaces four trigger lists.** For each candidate, ask:

> **What measurement supports this?** If the sentence rates the work and no
> number, comparison or result stands behind the rating, the rating is the tell.
> Cut the rating, keep the fact.

Four shapes it takes. Read them as descriptions, not as a match list.

**An evaluation hung off a fact**, usually as a participial clause. "…, which
enables robust detection", "…, highlighting the importance of careful tuning".
The fact is fine; the clause grades it. This is the largest single tell measured
in academic prose and it does not need a comma to be one.

> Before: Attention is computed over the full sequence, enabling long-range dependencies and improving downstream accuracy.
> After: Attention is computed over the full sequence. That is what lets the model use tokens 400 positions back.

**A quality claim with no number.** "provides an efficient and reliable
solution", "offers a cost-effective, robust, low-latency framework". The verb is
incidental — this was mis-specified as a verb list for months, which cost a
retracted finding. The praise adjective with nothing behind it is the tell.
Ask what was measured; if the answer is nothing, delete the adjective.

> Before: This work provides an efficient and reliable solution for real-time control.
> After: The controller runs in 4 ms on the target hardware.

**Generic importance where a fact belongs.** "plays a crucial role", "is
essential for", "is a testament to". Say what it does instead.

**Significance manufactured by contrast.** "Unlike prior work that optimises
accuracy in isolation, this study emphasises…". A position is attributed to
unnamed prior work so the next clause can improve on it.

> Before: Unlike prior work that optimises accuracy in isolation, this study emphasises the accuracy-latency tradeoff.
> After: Prior work optimises accuracy in isolation. This study measures accuracy against latency.

### What this is NOT

The failure mode here is over-firing, and every case below was flagged wrongly
by an earlier version of this file. Each names a real function that the flat
alternative loses.

| Looks like it | Actually | Why it stays |
|---|---|---|
| "X **remains** a challenge" | persistence | means *still open, despite prior work*. `is` is grammatically fine and drops the reason the paper exists |
| "descriptors **serve as** a correction signal" | functional role | names what a thing does. "are a correction signal" is worse English |
| "may **serve as** a biomarker" | hedged claim | the hedge is carrying real uncertainty |
| "can **not only** recognise terrain **but** also estimate slip" | conjunction | asserts two true things. Not a false contrast |
| "the three failure modes were A, B and C" | a real triad | three things that exist. Delete the third only if it measures nothing |

A judge panel called 21 instances of `remains a challenge` genuine tells,
unanimously, because it was handed a regex match and asked whether the match was
real. Unanimity of agreement is not accuracy. **Read the sentence, not the
match.**

Roughly half of what any pattern in `references/patterns.md` matches is not a
real instance. On one paper the em dash pattern returned 8 hits and 2 were worth
fixing; the rest were code comments, a table placeholder and numeric en dashes.
Step zero is what keeps that survivable.

### Also in this family, unmeasured

Own observation, no baseline, listed apart so it can be challenged.

**Vague attribution**: "Observers have cited", "Experts argue", "several
sources". Name who, or drop the claim. **The challenges formula**: "Despite its
X, it faces several challenges", then vague positivity. **False ranges**: "from
X to Y" where the two are not on a common scale. **Elegant variation**: rotating
synonyms to avoid repeating a word. In technical prose this is actively harmful,
because one thing should have one name.

## Vocabulary

**Run this on every document too, and trust it less.** It is the only section with a *published* measurement behind it and the only one measured to decay.

Kobak et al.'s ten strongest markers: `across`, `additionally`, `comprehensive`, `crucial`, `enhancing`, `exhibited`, `insights`, `notably`, `particularly`, `within`. The strongest single words were `delves`, `underscores` and `showcasing`.

The finding under it, which is what makes the list worth having: the excess is **stylistic, not topical**. Two thirds of it is verbs. A real subject-matter shift moves nouns instead, so a paragraph heavy in these is a paragraph where the *manner* changed, not the topic. Method and figures in `references/sources.md`.

Wikipedia's independently compiled list overlaps heavily, which is the useful part, two methods converging: `delve`, `underscore`, `showcase`, `crucial`, `pivotal`, `intricate`, `meticulous`, `robust`, `testament`, `tapestry`, `landscape`, `realm`, `align with`, `foster`, `garner`, `enhance`, `interplay`, `vibrant`, `enduring`, `commendable`.

Do not blanket-replace these. Every one is a legitimate English word, and a banned-word list is the failure mode of every other tool in this space. `Crucial` in a sentence that establishes why something is crucial is fine. The signal is density and co-occurrence: several of them in one paragraph, doing no work.

**This list decays, and the decay is measured.** In one journal `crucial` fell
from 6.0 per 10k in 2024 to 1.0 in 2026, back to its pre-ChatGPT level, and
`delve` effectively vanished. Both were the most publicised markers, and
publicity is what kills a word-level tell. `robust` went the other way and is
still climbing. Excess vocabulary shifts rather than disappearing, so a fixed
list ages badly in both directions.

Treat Kobak's method as the durable part and this list as a snapshot. Over the
same window the structural tells held. Figures in `references/sources.md`.

## Markup, if you chose it

**Skip this section for a paper.** In a journal template or a LaTeX class the headings, numbering and list style are the venue's, and changing them is not de-LLMing, it is breaking the submission. Full texts show heading style flat across 2021 to 2026 for exactly that reason.

Run it on an academic blog post, where you picked the formatting yourself. Nothing here has an academic baseline: an abstract has no markup and the full-text corpus does not preserve it, so this section rests on that argument rather than on a rate.

### Em dash

The exception. It occurs in prose without any markup at all, and it is the one item here with a measurement.

In arXiv preprints it roughly doubled between 2020 and 2026, 3.1 to 7.7 per 10k words. In full papers it is low either way and one document holds a third of the matches, so it is worth a glance in a blog post or an abstract and rarely repays one in a paper.

**Search for the dash the format actually uses.** A source file rarely contains U+2014. In the arXiv corpus the LaTeX `---` went from 0.00 to 2.71 per 10k while the literal `—` stayed at exactly 0.00 in both windows, so a search for the character finds nothing and reports a clean file. LaTeX writes `---` and `--`; HTML writes `&mdash;` and `&ndash;`; a word processor writes the character. Check all of them, and check `--` against numeric and page ranges before touching it.

Wikipedia lists "em dash overuse", not em dash use. Rewrite rather than substitute:

| Before | After |
|---|---|
| The model failed to converge — the learning rate was too high. | The model failed to converge. The learning rate was too high. |
| Error fell 3x — well outside run-to-run variance. | Error fell 3x, well outside run-to-run variance. |
| Two baselines — SARSA and Q-learning — gained nothing. | Neither SARSA nor Q-learning gained anything. |

Comma if the tail is a modifier, full stop if it is its own claim, parentheses if it is an aside. Never a semicolon.

### The rest

Title case headings, inline-header bold lists, emoji as decoration, boldface applied mid-paragraph as "key takeaways", thematic breaks, heading levels that skip, curly quotes, and Markdown leaking into a format that is not Markdown. Each with its pattern and its keep-or-convert rule in `references/patterns.md`. They are mechanical once you have decided this section applies at all.

One of them is a judgment call rather than a rule. Keep an inline-header bold list when the items are genuinely parallel and a reader will scan rather than read, such as a table of hyperparameters. Convert it when the "list" is three sentences wearing a costume.

## Paste artifacts

Strings a model emitted that no human would type. Near-conclusive when present, and trivial to match.

They measured zero across every corpus here, because they are web-interface citation renderings that only survive a copy-paste out of a chat window. That is the one thing a manuscript does and a file an agent wrote does not, so run it once on a draft even at a measured rate of zero. Do not lead with it.

One pass for `contentReference`, `oaicite`, `[cite: 1]`, `grok_card`, `attached_file`, lenticular brackets `【 】`, and `utm_source=` left in a cited URL. Full list per vendor in `references/patterns.md`.

Then the citation checks a regex cannot do: DOIs that resolve to unrelated papers, invalid ISBNs, and named references declared but never used.

## What is NOT evidence

Four things every other guide leads with, each measured here and found flat or
backwards. Looking for them wastes the pass and produces false accusations.

| Commonly claimed | Measured, same venue, pre-ChatGPT to 2026 |
|---|---|
| AI writes uniform, short sentences | sd of sentence length **8.6 → 8.0** in abstracts, **15.9 → 16.8** in papers. Flat |
| AI repeats sentence openers | **11.3% → 6.4%**. It went *down*; 2026 prose varies openings more than 2019 prose |
| Title case headings signal AI | flat across 2021 to 2026 in full papers. It is the venue's house style |
| Vendor paste artifacts are the strongest tell | **0.00 per 10k in every corpus measured.** Near-conclusive when present, and almost never present |

Uniform rhythm is what this skill *produces*, not what it should look for. See
the second directive.

And the older warnings, which still hold. Text that predates ChatGPT (November
2022) cannot be AI-generated, whatever it looks like. An author who can explain
their choices is an author. Irregular syntax is a human pattern, not a machine
one. None of these markers is proof: Kobak et al. estimate a population rate,
and population statistics do not classify individuals.

Do not use this checklist as evidence about who wrote something. Use it to edit.

## Self-check

1. Run the skip pass. Announce what you excluded.
2. Decide whether the markup section applies: did you choose this formatting, or did the venue?
3. For every candidate, ask what measurement supports the rating. If a number, comparison or result stands behind it, leave it.
4. Check the What-this-is-NOT table before cutting. `remains a challenge`, a functional `serve as`, a hedge, and a real triad all survive.
5. Count vocabulary markers per paragraph. One is nothing. Four doing no work is the signal.
6. For every hedge you removed, ask whether the sentence now claims more than the evidence supports. Put back any that does.
7. **Compare the longest sentence in your output with the longest in the input.** If it has dropped by much, you have flattened the text and must put a long sentence back. This is the measured failure mode and the one check that catches it.

## Limits

This removes markers of machine authorship. It does not make text true, well argued, or worth reading, and it cannot certify authorship in either direction.

It preserves voice deliberately. If the author writes long sentences by choice, the evaluation pass still applies, but do not sand their register into house style. The rhythm measurements say this is the likeliest way to get it wrong.

Voice fingerprinting, meaning a statistical profile built from the author's own corpus, is a deliberate non-goal. It requires stored state and a corpus, and "sounds like you" is not falsifiable the way the rest of this file tries to be.

## References

- `references/patterns.md` for every pattern in one file
- `references/sources.md` for what each source says, and what it does not
