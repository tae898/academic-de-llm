# Sources

What each source actually establishes, and what it does not. Read this before citing anything in `SKILL.md` to someone else.

---

## 1. Kobak, Gonzalez-Marquez, Horvát et al. (2025)

**"Delving into LLM-assisted writing in biomedical publications through excess vocabulary"**
*Science Advances*. Preprint: [arXiv:2406.07016](https://arxiv.org/abs/2406.07016). Data and code: [berenslab/llm-excess-vocab](https://github.com/berenslab/llm-excess-vocab).

**Method.** 14.2 million PubMed abstracts, 2010–2024. For each word, project a counterfactual 2024 frequency from 2021–22 data, then measure the gap between projection and observation. The design is borrowed from excess-mortality analysis, so "excess" is a measured quantity against a baseline rather than a judgement about style.

**What it establishes**

- 2024's excess vocabulary is **stylistic, not topical**: of 280 excess style words, **66% verbs, 18% adjectives**. Covid-era excess words were content nouns. That inversion is the fingerprint.
- Frequency ratios: `delves` r=25.2, `showcasing` r=9.2, `underscores` r=9.1.
- Absolute gaps in common words: `potential` δ=0.041, `findings` δ=0.027, `crucial` δ=0.026.
- Ten strongest combined markers: across, additionally, comprehensive, crucial, enhancing, exhibited, insights, notably, particularly, within.
- Lower-bound prevalence: **≥10% of 2024 abstracts** in the arXiv version (Δ_rare=0.103, independently confirmed at Δ_common=0.098). The published *Science Advances* version reports a higher figure. Cite the published number if precision matters.
- Sub-population spread: computational fields ~20%, MDPI/Frontiers ~17%, China/South Korea/Taiwan >15%, Nature/Science/Cell ~6%.

**What it does NOT establish**

- Nothing about any individual paper. It is a population estimate with an explicit lower bound.
- Nothing outside biomedical abstracts. The genre is narrow and the register is formulaic even without LLMs.
- Nothing about sentence structure. It is a vocabulary study.
- Nothing durable about the specific words. A word that becomes a known tell gets trained out.

---

## 2. Wikipedia:Signs of AI writing

[en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) — community-maintained.

**What it is.** A working screening guide by editors who review suspected AI text at volume across millions of articles. Not peer-reviewed. Its authority is accumulated practice and adversarial pressure, and it updates as models change.

**What it gives that Kobak does not**

- **Per-vendor leftover artifacts** (`contentReference`, `oaicite`, `[cite: 1]`, `grok_card`, `ppl-ai-file-upload`). Objective and near-conclusive. Nothing else on either list comes close to this reliability.
- **Structural patterns**: negative parallelism, rule of three, superficial `-ing` analysis, undue emphasis on significance, copula avoidance, vague attribution, the challenges formula, elegant variation.
- **Formatting patterns**: title case headings, excessive boldface, inline-header lists, em dash overuse, emoji as bullets, curly quotes, heading level skipping, thematic breaks.
- **Citation pathologies**: broken links, invalid DOIs and ISBNs, DOIs pointing at unrelated papers, `utm_source=` left in URLs, unused named references.
- **An explicit "not evidence" section**, which is the most valuable part.

**What it does NOT give**

- Frequencies, effect sizes, or base rates. Every claim is qualitative.
- Any correction for the fact that human writing also contains all of these.
- Generalization beyond encyclopedic prose. Its formatting rules are partly Wikipedia house style.

---

## 3. Own corpus measurement (2026-08)

Not published, not peer-reviewed, and reported here so it can be checked.

**Method.** Two corpora of 2026 developer prose, both largely AI-assisted:

- 35 README files from Claude Code community-marketplace plugin repositories, 51,055 words.
- 2,298 plugin descriptions from the same marketplace, 115,993 words.

Each pattern from `SKILL.md` was matched against both and reported as files affected and occurrences per 10k words.

**Result, on the README corpus**

| Tell | Files | Per 10k words |
|---|---|---|
| Em dash | 91% | 122.4 |
| Title case headings | 83% | 22.3 |
| Inline-header bold list | 49% | 46.4 |
| Copula avoidance | 34% | 3.1 |
| Excess vocabulary | 26% | 2.4 |
| Emoji | 11% | 2.7 |
| Curly quotes | 0% | 0.0 |
| Vendor paste artifacts | 0% | 0.0 |

**What it establishes**

- Formatting tells dominate agent-written developer prose by a factor of ten to fifty over vocabulary tells.
- Vendor paste artifacts fire zero times across 167k words of it. They are web-interface citation renderings and cannot appear in text an agent writes directly to a file.
- This is the basis for the tier ordering in `SKILL.md`, which inverts the order both published sources imply.

**What it does NOT establish**

- **There is no baseline.** This measures prevalence, not excess. Kobak's counterfactual design is what separates "common" from "more common than it should be", and none of that is done here. A 91% em dash rate is not evidence of machine authorship, only of frequency.
- Structural patterns are undercounted. The description corpus averages ~50 words per item, too short for negative parallelism or the challenges formula to appear, so their near-zero rates there are partly an artifact of document length.
- The em dash count does not exclude code blocks or tables. The paper measurement in `patterns.md` suggests roughly a quarter of raw hits are real prose, which would put the true rate near 30 per 10k. Still the largest by a wide margin.
- One genre, one month, one language.

**The obvious next step**, not done: apply Kobak's counterfactual method to a timestamped GitHub corpus, projecting 2026 README and commit-message word frequencies from a 2019 to 2021 baseline. That would turn prevalence into measured excess for a register nobody has studied.

---

## 4. Consulted and not used

**"Explaining Generalization of AI-Generated Text Detectors Through Linguistic Analysis"** (arXiv:2601.07974). Fetched 2026-08. Discusses clause types, participles, coordination, lexical diversity and punctuation, and reports that some markers generalize across models while others are domain-sensitive. **No usable numbers were extracted**, so nothing in `SKILL.md` cites it. Worth a proper read if this skill is revised.

**Popular "signs of AI writing" round-ups** (Forbes and similar, republished every few months). Useful as a leading indicator of which words are currently burned, useless as evidence. Their own framing concedes the list changes constantly. Not cited.

---

## What is unsourced in SKILL.md

Stated plainly so it can be challenged:

- **Stacked hedges** ("may potentially", "can sometimes") as a tell. Own observation. Not in any source.
- **Bookends and false directness** ("In summary", "Here's the part most people miss"). Wikipedia covers adjacent ground under promotional language and collaborative tone, but not this exact pattern.
- **Glue words opening consecutive sentences.** Kobak has `additionally` in the top ten as a *word*; the consecutive-sentence claim is mine.
- **The measured-vs-inferred hedging rule.** From the academic-writing hedging literature, not from any source above.
- **The 8-hits-2-real em dash figure.** One paper, one measurement, no generality claimed.
- **The tier ordering.** From source 3 above, which has no baseline. The ordering claim is "this fires more often", not "this is stronger evidence of machine authorship". Those are different claims and only the first is supported.
- **The inline-header bold list as a rewrite target.** Wikipedia lists the pattern; the rule for when to keep it (genuinely parallel, meant to be scanned) is mine.

## Deliberate non-goals

**Voice fingerprinting.** Two competing skills (`humanizer`, `humanize-kit`) build a statistical profile from the author's own corpus and rewrite toward it. It is the most interesting idea in this space and it is excluded on purpose: it requires stored state and a corpus, it breaks the zero-dependency portability, and "sounds like you" cannot be falsified the way the rest of this file tries to be.

**Banned-word lists.** The dominant approach elsewhere (`anti-ai-writing` bans roughly 56 words outright). Rejected because every word on every list here is legitimate English, and Kobak's own finding is about frequency ratios, not about words being forbidden. Density and co-occurrence are the signal.

---

## Review schedule

Tier 1 artifacts and Tier 2 vocabulary decay fastest; re-check them against current sources roughly twice a year. Tiers 3 and 4 have been stable across several model generations.

Last reviewed: **2026-08**.
