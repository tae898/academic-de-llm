---
name: de-llm
version: 3.0.0
description: |
  Strip the surface markers that make text read as machine-generated, without
  flattening its meaning. Use when the user says "de-LLM", "de-slop", "remove
  the AI tells", "make this sound human", "this reads like ChatGPT", "sounds
  like an LLM wrote it", or asks why a draft feels generated. Works on any
  register: READMEs, documentation, LaTeX and academic papers, commit messages,
  PR descriptions, issue comments, emails. Ordered by measured frequency in
  agent-written text, so the highest-yield fixes come first.
license: MIT
metadata:
  sources: >
    Kobak et al., Science Advances 2025 (arXiv:2406.07016);
    Wikipedia:Signs of AI writing (community-maintained);
    own corpus measurement, 2026-08 (see references/sources.md)
  last_reviewed: 2026-08
---

# De-LLM: Remove the Tells, Keep the Meaning

Generated prose is rarely wrong. It is recognizable. This skill removes what makes it recognizable.

Everything here comes from a published source, a community screening guide, or a measurement recorded in `references/sources.md`. Where a claim is unsourced, it says so.

| Source | What it is | What it gives |
|---|---|---|
| Kobak et al. 2025, *Science Advances*, "Delving into LLM-assisted writing in biomedical publications through excess vocabulary" ([arXiv:2406.07016](https://arxiv.org/abs/2406.07016), [data](https://github.com/berenslab/llm-excess-vocab)) | 14.2M PubMed abstracts, 2010 to 2024. Measures 2024 word frequencies against a counterfactual projected from 2021 to 2022, so "excess" is a measured quantity. | The vocabulary list, with frequency ratios |
| [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) | Maintained by editors who screen AI text at volume across millions of articles | The structural and formatting patterns, and the paste-era artifacts |
| Own measurement, 2026-08 | 35 agent-era plugin READMEs (51k words) and 2,298 plugin descriptions (116k words). No baseline, so it measures prevalence, not excess. | The ordering of this file |

## Why this file is ordered the way it is

Both published sources predate widely used coding agents. Kobak measured 2024 biomedical abstracts. Wikipedia screens encyclopedia edits, where most AI text arrives pasted out of a chat window. Neither measured what an agent writes directly into a file.

Measured on 35 agent-written READMEs:

| Tell | Files affected | Per 10k words |
|---|---|---|
| Em dash | 91% | 122.4 |
| Inline-header bold list | 49% | 46.4 |
| Title case headings | 83% | 22.3 |
| Copula avoidance | 34% | 3.1 |
| Excess vocabulary | 26% | 2.4 |
| Curly quotes | 0% | 0.0 |
| Vendor paste artifacts | 0% | 0.0 |

Formatting dominates by a factor of ten to fifty. So formatting comes first here, and the paste-era artifacts that older guides lead with come last.

Related but separate, and by a different author: `SimpleEnglish` (ASD-STE100). Use that when a reader might misread the text. Use this one when a reader might think a machine wrote it. On technical docs, run both. On a paper, run only this one, because STE bans the modals that carry your certainty.

## The Prime Directive

Delete the tell, keep the claim. A rewrite that makes a sentence claim more than the evidence supports has broken the text to pass a style check. That is worse than the tell.

## Step zero: the skip pass

Do this before matching anything. These are never edited, and a pass that touches them does real damage:

Fenced code blocks and inline code spans. YAML, TOML, and JSON frontmatter or config. Markdown tables, including cells that use a dash as a "not applicable" placeholder. Task lists. Footnotes and citation blocks. Direct quotations from other people. Error messages and log lines. Identifiers, CLI flags, and file paths. En dashes inside numeric ranges such as `0.88–0.98`. Anything written before November 2022.

Say what you skipped when you report back ("skipped: 3 code blocks, 1 table, frontmatter"). It makes the pass auditable and it is the main defense against the false-positive rate documented below.

## Tier 1: Formatting

Highest yield in agent-written text, and the tier older guides bury.

### Em dash

91% of files, 122 per 10k words, the single strongest signal.

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

Model-level generation habits rather than interface artifacts, so they survive across vendors and model generations. Wikipedia's categories, with its terminology.

### Copula avoidance

34% of files, the strongest structural tell measured. A plain `is` or `are` dressed up as `serves as`, `stands as`, `functions as`, `boasts`, `features`, `maintains`, `offers`.

### Superficial analysis via -ing

A participial clause that attaches vague interpretation to a fact: `highlighting`, `underscoring`, `emphasizing`, `ensuring`, `reflecting`, `contributing to`.

> Before: The cache is checked first, reducing round trips and improving latency.
> After: The cache is checked first. That removes one round trip.

### Negative parallelism

Three variants: `not just X, but Y`, `not X, but Y`, `X rather than Y`.

> Before: This is not about speed. It is about correctness.
> After: The change corrects the result. It does not make it faster.

### Rule of three

Triplet adjectives or phrases. Not every triad is a tell; three real things are three real things. The test is whether deleting the third loses information.

### Undue emphasis on significance

`stands as`, `is a testament to`, `plays a crucial role`, `reflects broader`, `left an indelible mark`. Generic importance replacing a specific fact.

### Vague attribution

`Observers have cited`, `Experts argue`, `Industry reports suggest`, `several sources`. Name who, or drop the claim.

### False ranges

`from X to Y` where X and Y are not on a common scale. "from the birth of stars to the enigmatic dance of dark matter" is a shape, not a range.

### The challenges formula

"Despite its X, it faces several challenges", followed by vague positivity.

### Elegant variation

Rotating synonyms to avoid repeating a word, an artifact of repetition penalties. In technical text this is actively harmful: one thing, one name.

## Tier 3: Excess vocabulary

26% of files, 2.4 per 10k words. Lower frequency than formatting, but the only tier with a published measurement behind it.

Kobak et al. found 2024's excess vocabulary is overwhelmingly stylistic, not topical: of 280 excess style words, 66% were verbs and 18% adjectives. That is the opposite of a real event like Covid, whose excess words were content nouns.

Highest frequency ratios (r = 2024 frequency ÷ counterfactual): `delves` 25.2, `showcasing` 9.2, `underscores` 9.1. Highest absolute gaps: `potential` 0.041, `findings` 0.027, `crucial` 0.026.

The authors' ten strongest combined markers: `across`, `additionally`, `comprehensive`, `crucial`, `enhancing`, `exhibited`, `insights`, `notably`, `particularly`, `within`.

Wikipedia's independently compiled list overlaps heavily, which is the useful part, two methods converging: `delve`, `underscore`, `showcase`, `crucial`, `pivotal`, `intricate`, `meticulous`, `robust`, `testament`, `tapestry`, `landscape`, `realm`, `align with`, `foster`, `garner`, `enhance`, `interplay`, `vibrant`, `enduring`, `commendable`.

Do not blanket-replace these. Every one is a legitimate English word, and a banned-word list is the failure mode of every other tool in this space. `Crucial` in a sentence that establishes why something is crucial is fine. The signal is density and co-occurrence: several of them in one paragraph, doing no work.

Word-level tells also decay fastest. Each model generation drops the previous one's giveaways, and `delve` became famous enough to get trained out. Treat Kobak's method as the durable part and the specific list as perishable.

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
8. If a fix flattened the rhythm, vary sentence length or restore one specific detail. Do not restore the tell.

## Limits

This removes markers of machine authorship. It does not make text true, well argued, or worth reading, and it cannot certify authorship in either direction.

It preserves voice deliberately. If the author writes long sentences by choice, the structural tiers still apply, but do not sand their register into house style.

Voice fingerprinting, meaning a statistical profile built from the author's own corpus, is a deliberate non-goal. It requires stored state and a corpus, and "sounds like you" is not falsifiable the way the rest of this file tries to be.

## References

- `references/patterns.md` for every pattern in one file
- `references/sources.md` for what each source says, and what it does not
