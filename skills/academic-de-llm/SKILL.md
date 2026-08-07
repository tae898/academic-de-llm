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

**Structure and vocabulary rise everywhere.** Two to four times against a
pre-ChatGPT baseline, in abstracts and in full texts alike. Those two sections
are the skill; run them on everything.

**Formatting is mostly the venue's, not yours.** In full texts, section headings
sit flat across 2021 to 2026, because "2. Materials and Methods" is what the
form requires. So the markup section is scoped by a question rather than a rate:
**did you choose this formatting?** In a journal template or a LaTeX class, no,
and you should skip it. In a blog post you wrote in Markdown, yes, and the em
dashes and bold lists are yours to answer for.

Figures and corpora behind this are in `references/sources.md`, which also says
plainly that no academic corpus here can measure markup at all.

Related but separate, and by a different author: `SimpleEnglish` (ASD-STE100).
Use that when a reader might misread the text. Use this one when a reader might
think a machine wrote it. On a paper, run only this one, because STE bans the
modals that carry your certainty.

## Two directives, equally binding

**Delete the tell, keep the claim.** A rewrite that makes a sentence claim more than the evidence supports has broken the text to pass a style check. That is worse than the tell.

**Delete the tell, keep the rhythm.** Applied thoroughly, the sections below produce short declaratives sharing a subject: every tell gone and the cadence gone with them. That is measured, not hypothetical, which is why these four rules override everything below wherever they conflict with it.

**Do not split a long sentence into three short ones just because the join was a participle.** Rewrite the participle in place, or make the clause subordinate. One long sentence among short ones is what a human paragraph looks like.

**Do not start consecutive sentences with the same subject.** If a fix produces "We do X. We do Y. We do Z", the fix is worse than what it replaced, whatever the pattern count says.

**Keep the connective tissue.** Phrases that signal what a sentence is doing, contrasting, conceding, moving on, are how a reader follows an argument. Several sit on trigger lists. Removing them scores well and reads worse.

**A high-scoring trigger is not automatically worth removing.** Precision measures how reliably a pattern indicates machine authorship. It says nothing about whether the phrase earns its place for the reader. Only you can answer the second question.

After any pass, read the result aloud. If every sentence is the same length, put one back.

## Step zero: the skip pass

Do this before matching anything. These are never edited, and a pass that touches them does real damage:

Fenced code blocks and inline code spans. YAML, TOML, and JSON frontmatter or config. Markdown tables, including cells that use a dash as a "not applicable" placeholder. Task lists. Footnotes and citation blocks. Direct quotations from other people. Error messages and log lines. Identifiers, CLI flags, and file paths. En dashes inside numeric ranges such as `0.88–0.98`. Anything written before November 2022.

Say what you skipped when you report back ("skipped: 3 code blocks, 1 table, frontmatter"). It makes the pass auditable and it is the main defense against the false-positive rate documented below.

## Structure

**Run this on every document.** It is the only section with a measured baseline behind it, it rises 2-4x against pre-ChatGPT academic text in both abstracts and full papers, and it held across 2024 to 2026 while the vocabulary below decayed. If you only have attention for one section, this is it.

Model-level generation habits rather than interface artifacts, so they survive across vendors and model generations. Wikipedia's categories and terminology, except false ranges, which is noted below.

### Copula avoidance

2.4x excess in journal abstracts after ChatGPT, and **the one tell here that has not peaked**: on the regex below it rises in every window through 2026, while every other pattern fell back from its 2024 or 2025 high. A plain `is` or `are` dressed up as `serves as`, `serve as`, `stands as`, `functions as`, `boasts`, `offers`, `remains`, `positions X as`, `presents a`, and `provides a ... solution`.

`serves as` is a real instance every time it appears. Bare `provides` was only 1 in 6, because "the tool provides X" is an ordinary verb, so it is narrowed to the copular form: "provides an effective solution" means "is an effective solution". `maintains` was never real across 11 matches. Read the verb: if `is` cannot replace it, leave it.

### Superficial analysis via -ing

**The strongest tell of any kind in academic prose.** Against a pre-ChatGPT baseline of 1.0 per 10k in one journal it hit 9.2 in 2024, peaked at 12.2 in 2025, and sits at 6.6 in 2026. Full texts show the same shape. Still 6.4x baseline after two years, while the vocabulary markers decayed.

A participial clause that attaches vague interpretation to a fact: `highlighting`, `underscoring`, `emphasizing`, `ensuring`, `reflecting`, `contributing to`, `providing`, `enhancing`, `allowing`, `helping`, `supporting`, `maintaining`, `thereby ...ing`.

**It does not need a comma.** "sensor signals enabling precise and robust detection" is the same pattern without punctuation, and looking only after commas missed most of them. `enabling` was dropped entirely: it matched 16 times and not one was a real instance, while accounting for a third of everything this pattern found.

> Before: Attention is computed over the full sequence, enabling long-range dependencies and improving downstream accuracy.
> After: Attention is computed over the full sequence. That is what lets the model use tokens 400 positions back.

### Negative parallelism

Four variants: `not just X, but Y`, `not X, but Y`, `X rather than Y`, and `unlike X, this work Y`.

The last one is the one that actually occurs. Searching only for the `not just` forms found 14 matches across 60 abstracts and not one was real, while every genuine instance took the `unlike traditional studies that optimise accuracy, this work emphasises...` shape.

> Before: Unlike prior work that optimises accuracy in isolation, this study emphasises the accuracy-latency tradeoff.
> After: Prior work optimises accuracy in isolation. This study measures accuracy against latency.

### Rule of three

Triplet adjectives or phrases. Not every triad is a tell; three real things are three real things. The test is whether deleting the third loses information.

### Undue emphasis on significance

`pivotal`, `is crucial`, `is essential`, `is vital`, `plays a crucial role`, `is a testament to`, `significant potential`, `highlighting the importance of`. Generic importance replacing a specific fact.

The most reliable of the structural patterns: about 3 matches in 4 are real. Bare `pivotal` is weaker at 2 in 5, and is kept anyway because it catches "are pivotal to classification performance", and on a finder whose hits get read a miss costs more than a false positive.

### Vague attribution

`Observers have cited`, `Experts argue`, `Industry reports suggest`, `several sources`. Name who, or drop the claim.

### False ranges

`from X to Y` where X and Y are not on a common scale. "from the birth of stars to the enigmatic dance of dark matter" is a shape, not a range.

Unsourced. Not on the Wikipedia page, unlike the rest of this section. See `references/sources.md`.

### The challenges formula

"Despite its X, it faces several challenges", followed by vague positivity.

### Elegant variation

Rotating synonyms to avoid repeating a word, an artifact of repetition penalties. In technical text this is actively harmful: one thing, one name.

## Vocabulary

**Run this on every document too, and trust it less.** It is the only section with a *published* measurement behind it and the only one measured to decay.

Kobak et al. found 2024's excess vocabulary is overwhelmingly stylistic, not topical: of 379 excess style words, 66% were verbs and 14% adjectives. That is the opposite of a real event like Covid, whose excess words were content nouns (79.2% of content words were nouns).

Highest frequency ratios (r = 2024 frequency ÷ counterfactual): `delves` 28.0, `underscores` 13.8, `showcasing` 10.7. Highest absolute gaps: `potential` 0.052, `findings` 0.041, `crucial` 0.037.

The authors' ten strongest combined markers: `across`, `additionally`, `comprehensive`, `crucial`, `enhancing`, `exhibited`, `insights`, `notably`, `particularly`, `within`.

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

## Patterns find candidates, not violations

Every pattern here is a finder. Read each hit.

Measured on one real paper: the em-dash pattern returned 8 hits, of which 2 were prose worth fixing. The rest were three code comments, a table placeholder, and two numeric en dashes. A pass that changed all 8 would have corrupted a table and three code samples.

Measured across 30 abstracts with a judge panel labelling every hit: of everything the finders match, **about half is a real instance**. The other half is a word that happened to coincide.

The skip pass in step zero is what keeps this rate survivable.

## What is NOT evidence

Wikipedia is explicit about this, and it matters more than the markers.

Text that predates ChatGPT (November 2022) cannot be AI-generated, whatever it looks like. An author who can explain their choices coherently is an author. Irregular syntax is a human pattern, not a machine one. None of these markers is proof: Kobak et al. estimate a population rate, and population statistics do not classify individuals.

Do not use this checklist as evidence about who wrote something. Use it to edit.

## Self-check

1. Run the skip pass. Announce what you excluded.
2. Decide whether the markup section applies: did you choose this formatting, or did the venue?
3. Read every hit from `references/patterns.md`. Fix only real ones. Structure first.
4. Count vocabulary markers per paragraph. One is nothing. Four doing no work is the signal.
5. Read your three-item lists. Delete a third item that measures nothing.
6. For every hedge you removed, ask whether the sentence now claims more than the evidence supports. Put back any that does.
7. Read the first sentence of each section. If it announces the section instead of stating a fact, rewrite it.
8. Read the result aloud. If sentences are uniformly short, or several start with the same subject, the pass has flattened the text and must be partly undone. See the second directive: this is the skill's own measured failure mode, not a hypothetical.

## Limits

This removes markers of machine authorship. It does not make text true, well argued, or worth reading, and it cannot certify authorship in either direction.

It preserves voice deliberately. If the author writes long sentences by choice, the structural pass still applies, but do not sand their register into house style.

Voice fingerprinting, meaning a statistical profile built from the author's own corpus, is a deliberate non-goal. It requires stored state and a corpus, and "sounds like you" is not falsifiable the way the rest of this file tries to be.

## References

- `references/patterns.md` for every pattern in one file
- `references/sources.md` for what each source says, and what it does not
