---
name: de-llm
version: 0.4.0
description: |
  Strip the surface markers that make text read as machine-generated, without
  flattening its meaning. Use when the user says "de-LLM", "de-slop", "remove
  the AI tells", "make this sound human", "this reads like ChatGPT", "sounds
  like an LLM wrote it", or asks why a draft feels generated. Works on any
  register: READMEs, documentation, LaTeX and academic papers, commit messages,
  PR descriptions, issue comments, emails. Branches on register, because the
  tells differ: formatting dominates documents with markup, structure dominates
  plain prose.
license: MIT
metadata:
  sources: >
    Kobak et al., Science Advances 2025 (arXiv:2406.07016);
    Wikipedia:Signs of AI writing (community-maintained);
    own corpus measurements, 2026-08 (see references/sources.md)
  last_reviewed: 2026-08
  changelog: CHANGELOG.md
  review_process: research/REVIEW.md
---

# De-LLM: Remove the Tells, Keep the Meaning

Generated prose is rarely wrong. It is recognizable. This skill removes what makes it recognizable.

Every claim here is measured or cited, and `references/sources.md` says which,
including what each source does **not** establish and which claims have no source
at all.

## Read the register first, then pick a tier

The tells are not universal, and running the wrong tier first wastes the pass.

**Structure and vocabulary rise in every register with a baseline**, two to four
times. Tier 2 and Tier 3 are the ones to trust everywhere.

**Formatting is register-specific and usually is not a tell.** Decide by how the
document was written, not by whether it contains markup:

| Document | Start at | Because |
|---|---|---|
| Written end to end by an agent | **Tier 1** | em dashes and bold lists run about ten times a maintained repository |
| A README a human maintains | **Tier 2** | em dashes have *fallen* since 2022 and title case is flat; both are house style. Check the inline-header bold list first, the one formatting tell that rose |
| An academic paper | **Tier 2** | section headings are journal template, not authorship. "2. Materials and Methods" is what the form requires |
| Plain prose: abstracts, email, commit bodies | **Tier 2** | only the em dash carries over from Tier 1. The rest needs markup to exist |

Figures, corpora and the before-and-after comparisons behind this table are in
`references/sources.md`.

Related but separate, and by a different author: `SimpleEnglish` (ASD-STE100). Use that when a reader might misread the text. Use this one when a reader might think a machine wrote it. On technical docs, run both. On a paper, run only this one, because STE bans the modals that carry your certainty.

## Two directives, equally binding

**Delete the tell, keep the claim.** A rewrite that makes a sentence claim more than the evidence supports has broken the text to pass a style check. That is worse than the tell.

**Delete the tell, keep the rhythm.** Applied thoroughly, the tiers below produce short declaratives sharing a subject: every tell gone and the cadence gone with them. That is measured, not hypothetical, which is why these four rules override the tier guidance wherever they conflict with it.

**Do not split a long sentence into three short ones just because the join was a participle.** Rewrite the participle in place, or make the clause subordinate. One long sentence among short ones is what a human paragraph looks like.

**Do not start consecutive sentences with the same subject.** If a fix produces "We do X. We do Y. We do Z", the fix is worse than what it replaced, whatever the pattern count says.

**Keep the connective tissue.** Phrases that signal what a sentence is doing, contrasting, conceding, moving on, are how a reader follows an argument. Several sit on trigger lists. Removing them scores well and reads worse.

**A high-scoring trigger is not automatically worth removing.** Precision measures how reliably a pattern indicates machine authorship. It says nothing about whether the phrase earns its place for the reader. Only you can answer the second question.

After any pass, read the result aloud. If every sentence is the same length, put one back.

## Step zero: the skip pass

Do this before matching anything. These are never edited, and a pass that touches them does real damage:

Fenced code blocks and inline code spans. YAML, TOML, and JSON frontmatter or config. Markdown tables, including cells that use a dash as a "not applicable" placeholder. Task lists. Footnotes and citation blocks. Direct quotations from other people. Error messages and log lines. Identifiers, CLI flags, and file paths. En dashes inside numeric ranges such as `0.88–0.98`. Anything written before November 2022.

Say what you skipped when you report back ("skipped: 3 code blocks, 1 table, frontmatter"). It makes the pass auditable and it is the main defense against the false-positive rate documented below.

## Tier 1: Formatting

Highest yield **in documents with markup**, and the tier older guides bury.

On plain prose only the em dash below applies. Everything else in this tier needs markup to exist, so it cannot occur.

### Em dash

The strongest signal in documents with markup: 91% of READMEs, 122 per 10k words. It is also the one Tier 1 pattern that occurs in plain prose, where it roughly doubled in arXiv abstracts between 2020 and 2026 (3.7 to 7.8 per 10k).

Wikipedia lists "em dash overuse", not em dash use. Rewrite rather than substitute:

| Before | After |
|---|---|
| The build failed — the cache was stale. | The build failed. The cache was stale. |
| Latency rose 3x — well outside run-to-run spread. | Latency rose 3x, well outside run-to-run spread. |
| Two engines — Chroma and Qdrant — gained nothing. | Neither Chroma nor Qdrant gained anything. |

Comma if the tail is a modifier, full stop if it is its own claim, parentheses if it is an aside. Never a semicolon.

### Inline-header bold lists

49% of files, 46 per 10k words. The shape is `- **Term**: explanation`, repeated down a list where prose belongs.

> Before:
> - **Fast**: Runs in under a second.
> - **Portable**: No dependencies.
>
> After: It runs in under a second and has no dependencies.

Keep the list when the items are genuinely parallel and a reader will scan rather than read, such as a flag reference. Convert it when the "list" is three sentences wearing a costume.

### Title case headings

83% of files, 22 per 10k words. `## Getting Started With The Config` becomes `## Getting started with the config`. Sentence case throughout, except for proper nouns.

### Lower-frequency formatting

Excessive boldface, especially bolding terms mid-paragraph as "key takeaways". Emoji as bullets, separators, or heading decoration (11% of files). Heading levels that skip, H2 straight to H4. Thematic breaks before headings. Markdown leaking into a format that is not Markdown. Curly quotes where straight ones belong, which measured 0% here but still appears in text pasted from word processors.

## Tier 2: Structure

Model-level generation habits rather than interface artifacts, so they survive across vendors and model generations. Wikipedia's categories and terminology, except false ranges, which is noted below.

### Copula avoidance

34% of READMEs, and 2.6x excess in journal abstracts after ChatGPT. A plain `is` or `are` dressed up as `serves as`, `serve as`, `stands as`, `functions as`, `boasts`, `offers`, `remains`, `positions X as`, `presents a`, and `provides a ... solution`.

`serves as` is a real instance every time it appears. Bare `provides` was only 1 in 6, because "the tool provides X" is an ordinary verb, so it is narrowed to the copular form: "provides an effective solution" means "is an effective solution". `maintains` was never real across 11 matches. Read the verb: if `is` cannot replace it, leave it.

### Superficial analysis via -ing

**The strongest tell of any kind in plain prose, and it does not occur in READMEs at all.** Against a pre-ChatGPT baseline of 1.0 per 10k in one journal it hit 8.7 in 2024, peaked at 12.2 in 2025, and sits at 6.9 in 2026. Still nearly 7x baseline after two years, while the vocabulary markers decayed.

A participial clause that attaches vague interpretation to a fact: `highlighting`, `underscoring`, `emphasizing`, `ensuring`, `reflecting`, `contributing to`, `providing`, `enhancing`, `allowing`, `helping`, `supporting`, `maintaining`, `thereby ...ing`.

**It does not need a comma.** "sensor signals enabling precise and robust detection" is the same pattern without punctuation, and looking only after commas missed most of them. `enabling` was dropped entirely: it matched 16 times and not one was a real instance, while accounting for a third of everything this pattern found.

> Before: The cache is checked first, reducing round trips and improving latency.
> After: The cache is checked first. That removes one round trip.

### Negative parallelism

Four variants: `not just X, but Y`, `not X, but Y`, `X rather than Y`, and `unlike X, this work Y`.

The last one is the one that actually occurs. Searching only for the `not just` forms found 14 matches across 60 abstracts and not one was real, while every genuine instance took the `unlike traditional studies that optimise accuracy, this work emphasises...` shape.

> Before: This is not about speed. It is about correctness.
> After: The change corrects the result. It does not make it faster.

### Rule of three

Triplet adjectives or phrases. Not every triad is a tell; three real things are three real things. The test is whether deleting the third loses information.

### Undue emphasis on significance

`pivotal`, `is crucial`, `is essential`, `is vital`, `plays a crucial role`, `is a testament to`, `significant potential`, `highlighting the importance of`. Generic importance replacing a specific fact.

The most reliable of the structural patterns: about 3 matches in 4 are real. Bare `pivotal` is weaker at 2 in 5, and is kept anyway because it catches "are pivotal to classification performance", and on a finder whose hits get read a miss costs more than a false positive.

### Vague attribution

`Observers have cited`, `Experts argue`, `Industry reports suggest`, `several sources`. Name who, or drop the claim.

### False ranges

`from X to Y` where X and Y are not on a common scale. "from the birth of stars to the enigmatic dance of dark matter" is a shape, not a range.

Unsourced. Not on the Wikipedia page, unlike the rest of this tier. See `references/sources.md`.

### The challenges formula

"Despite its X, it faces several challenges", followed by vague positivity.

### Elegant variation

Rotating synonyms to avoid repeating a word, an artifact of repetition penalties. In technical text this is actively harmful: one thing, one name.

## Tier 3: Excess vocabulary

26% of files, 2.4 per 10k words. Lower frequency than formatting, but the only tier with a published measurement behind it.

Kobak et al. found 2024's excess vocabulary is overwhelmingly stylistic, not topical: of 379 excess style words, 66% were verbs and 14% adjectives. That is the opposite of a real event like Covid, whose excess words were content nouns (79.2% of content words were nouns).

Highest frequency ratios (r = 2024 frequency ÷ counterfactual): `delves` 28.0, `underscores` 13.8, `showcasing` 10.7. Highest absolute gaps: `potential` 0.052, `findings` 0.041, `crucial` 0.037.

The authors' ten strongest combined markers: `across`, `additionally`, `comprehensive`, `crucial`, `enhancing`, `exhibited`, `insights`, `notably`, `particularly`, `within`.

Wikipedia's independently compiled list overlaps heavily, which is the useful part, two methods converging: `delve`, `underscore`, `showcase`, `crucial`, `pivotal`, `intricate`, `meticulous`, `robust`, `testament`, `tapestry`, `landscape`, `realm`, `align with`, `foster`, `garner`, `enhance`, `interplay`, `vibrant`, `enduring`, `commendable`.

Do not blanket-replace these. Every one is a legitimate English word, and a banned-word list is the failure mode of every other tool in this space. `Crucial` in a sentence that establishes why something is crucial is fine. The signal is density and co-occurrence: several of them in one paragraph, doing no work.

**This list decays, and the decay is measured.** In one journal `crucial` fell
from 5.9 per 10k in 2024 to 0.9 in 2026, back to its pre-ChatGPT level, and
`delve` effectively vanished. Both were the most publicised markers, and
publicity is what kills a word-level tell. `robust` went the other way and is
still climbing. Excess vocabulary shifts rather than disappearing, so a fixed
list ages badly in both directions.

Treat Kobak's method as the durable part and this list as a snapshot. Over the
same window the structural tells in Tier 2 held. **If you only have attention for
one tier on prose, use Tier 2.** Figures in `references/sources.md`.

## Tier 4: Paste-era artifacts

Strings a model emitted that no human would type. Near-conclusive when present, and trivial to match.

They measured 0% across both corpora here, because they are web-interface citation renderings. They only appear when someone pastes out of a chat window, which agent-written text never does. Keep the check, since it costs one pass, but do not lead with it.

| Model | Artifact strings |
|---|---|
| ChatGPT | `contentReference`, `oaicite`, `turn0search0` |
| Gemini | `[cite: 1]`, `[span_1](start_span)` |
| Grok | `grok_card`, `grok_render_citation_card_json` |
| DeepSeek | lenticular brackets `【 】`, stray dagger `†` |
| Perplexity | `attached_file`, `ppl-ai-file-upload` |

Also check `utm_source=` left in cited URLs, DOIs that resolve to unrelated papers, invalid ISBNs, and named references declared but never used.

## Patterns find candidates, not violations

Every pattern here is a finder. Read each hit.

Measured on one real paper: the em-dash pattern returned 8 hits, of which 2 were prose worth fixing. The rest were three code comments, a table placeholder, and two numeric en dashes. A pass that changed all 8 would have corrupted a table and three code samples.

A second measurement, on this skill's own research: a keyword search for writing-related plugins across 278 marketplace entries returned 48 hits and 0 real ones. `docs` matched documentation tools, `write` matched "write optimized SQL", `style` matched UI themes.

The skip pass in step zero is what keeps this rate survivable.

## What is NOT evidence

Wikipedia is explicit about this, and it matters more than the markers.

Text that predates ChatGPT (November 2022) cannot be AI-generated, whatever it looks like. An author who can explain their choices coherently is an author. Irregular syntax is a human pattern, not a machine one. None of these markers is proof: Kobak et al. estimate a population rate, and population statistics do not classify individuals.

Do not use this checklist as evidence about who wrote something. Use it to edit.

## Self-check

1. Run the skip pass. Announce what you excluded.
2. Fix formatting first. It is where the volume is.
3. Read every hit from `references/patterns.md`. Fix only real ones.
4. Count Tier 3 words per paragraph. One is nothing. Four doing no work is the signal.
5. Read your three-item lists. Delete a third item that measures nothing.
6. For every hedge you removed, ask whether the sentence now claims more than the evidence supports. Put back any that does.
7. Read the first sentence of each section. If it announces the section instead of stating a fact, rewrite it.
8. Read the result aloud. If sentences are uniformly short, or several start with the same subject, the pass has flattened the text and must be partly undone. See the second directive: this is the skill's own measured failure mode, not a hypothetical.

## Limits

This removes markers of machine authorship. It does not make text true, well argued, or worth reading, and it cannot certify authorship in either direction.

It preserves voice deliberately. If the author writes long sentences by choice, the structural tiers still apply, but do not sand their register into house style.

Voice fingerprinting, meaning a statistical profile built from the author's own corpus, is a deliberate non-goal. It requires stored state and a corpus, and "sounds like you" is not falsifiable the way the rest of this file tries to be.

## References

- `references/patterns.md` for every pattern in one file
- `references/sources.md` for what each source says, and what it does not
