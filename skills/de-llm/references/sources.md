# Sources

What each source actually establishes, and what it does not. Read this before citing anything in `SKILL.md` to someone else.

---

## 1. Kobak, González-Márquez, Horvát & Lause (2025)

**"Delving into LLM-assisted writing in biomedical publications through excess vocabulary"**
*Science Advances* 11(27), July 2025. [doi:10.1126/sciadv.adt3813](https://doi.org/10.1126/sciadv.adt3813). Preprint: [arXiv:2406.07016](https://arxiv.org/abs/2406.07016). Data and code: [berenslab/llm-excess-vocab](https://github.com/berenslab/llm-excess-vocab).

**Every number below is from arXiv v5 (3 July 2025), which matches the published version.** Earlier drafts of this file carried v1 figures from June 2024, when the corpus stopped mid-2024. All of them were wrong. If you are re-checking, check against v5 or the *Science Advances* paper, not v1.

**Method.** 15.1 million English-language PubMed abstracts from 2010 onwards, cleaned. For each word, project a counterfactual 2024 frequency by linear extrapolation from 2021 and 2022, then measure both the gap δ = p − q and the ratio r = p/q against the observation. 2023 is deliberately excluded from the baseline because it could already be LLM-affected. The design is borrowed from excess-mortality analysis, so "excess" is a measured quantity against a baseline rather than a judgement about style.

**What it establishes**

- 2024's excess vocabulary is **stylistic, not topical**: of 379 excess style words in 2024, **66% verbs, 14% adjectives**. Content words were 79.2% nouns, and Covid-era excess words were almost entirely content words. That inversion is the fingerprint.
- Frequency ratios: `delves` r=28.0, `underscores` r=13.8, `showcasing` r=10.7.
- Absolute gaps in common words: `potential` δ=0.052, `findings` δ=0.041, `crucial` δ=0.037. A single marker word puts a floor under the estimate: δ=0.052 for `potential` alone implies at least 5.2% of 2024 abstracts went through an LLM.
- Ten strongest combined markers, the "common set" chosen to maximize Δ: across, additionally, comprehensive, crucial, enhancing, exhibited, insights, notably, particularly, within.
- Lower-bound prevalence: **at least 13.5% of 2024 abstracts**, from Δ = (Δ_common + Δ_rare)/2 = (0.134 + 0.136)/2 = 0.135. The rare set is 291 words, the common set is the 10 above, and the two sets do not overlap, so each is an independent estimate.
- Excess word count rose from 190 in 2021 to 454 in 2024 counting inflections, or 343 unique lemmas.
- Sub-population spread, as frequency gap Δ: computational fields and bioinformatics ≈0.20; China, South Korea and Taiwan ≈0.20; UK and Australia ≈0.05; MDPI 0.21, Frontiers 0.20; *Sensors* 0.25, *Cureus* 0.20; Nature family 0.10, *Science* and *Cell* 0.07. Intersections go higher: South Korean papers in *Sensors* 0.34, computation papers from China 0.41. The paper's own summary is that the bound ranges "from below 5% to over 40%".

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

## 3. Own prevalence measurement, agent-written READMEs (2026-08)

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

**The obvious next step**, not done: apply Kobak's counterfactual method to a timestamped GitHub corpus, projecting 2026 README and commit-message word frequencies from a 2019 to 2021 baseline. That would turn prevalence into measured excess for the README register too.

---

## 4. Own before-and-after measurement, journal abstracts (2026-08)

The measurement above has no baseline. This one does, and it is the only figure in this skill that separates "common" from "more common than it should be" outside Kobak's own work.

**Method.** All abstracts from *Sensors* (Basel, MDPI) indexed in PubMed, split into a pre-ChatGPT window and a post window, same journal and same genre on both sides:

- 298 abstracts from 2019 to 2021, 61,166 words.
- 293 abstracts from 2024, 57,220 words.

*Sensors* was chosen because Kobak measures it at Δ = 0.25, among the highest of any journal, so the effect should be visible in a small sample. Patterns were counted per 10k words in each window.

**Result**

| Pattern | pre-2022 | 2024 | ratio |
|---|---|---|---|
| Superficial `-ing` clause | 1.0 | 8.7 | **8.9x** |
| `crucial` | 1.5 | 5.9 | 4.0x |
| Kobak's ten markers, combined | 15.7 | 50.0 | **3.2x** |
| `insights` | 1.0 | 3.3 | 3.4x |
| Undue emphasis | 0.3 | 0.9 | 2.7x |
| Copula avoidance | 1.6 | 4.2 | 2.6x |
| Negative parallelism | 0.5 | 1.2 | 2.5x |
| `delve` / `showcase` / `underscore` | 0.0 | 1.9 | absent, then present |
| Em dash | 0.0 | 0.0 | no change |
| Paste artifacts | 0.0 | 0.0 | no change |

**What it establishes**

- **Kobak's vocabulary finding replicates on a sample they did not use.** Their ten markers rose 3.2x in a journal they measured independently.
- **Structural patterns show excess too, and the largest one is structural.** The superficial `-ing` clause rose 8.9x, higher than any vocabulary marker here. Kobak measured only vocabulary; Wikipedia lists structural patterns with no numbers at all. As far as this file's authors know, that 8.9x is the first excess figure published for a structural tell.
- **Formatting tells are a property of markup, not of machine authorship.** Em dashes, inline-header lists and title case headings are flat at zero in abstracts across both windows, while running at 122, 46 and 59 per 10k in agent-written READMEs. This is why `SKILL.md` now branches on register instead of giving one global ordering.

**What it does NOT establish**

- **One journal, one field, one publisher.** *Sensors* was picked because the effect is large there. It is not representative of publishing.
- **It is a raw before-and-after, not a counterfactual.** Kobak projects an expected 2024 frequency from 2021 to 2022 and measures the gap. This compares two observed windows, so it cannot separate LLM effects from five years of drift in the journal's topics, authorship, or editorial standards.
- **Small.** 118k words against Kobak's 15.1 million.
- Nothing about any individual abstract, for the same reason as everything else here.

---

## 5. Consulted and not used

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
- **False ranges.** Taken from the `humanizer` skill, which is Wikipedia-based, so it was assumed to be Wikipedia's. It is not: checked against the page on 2026-08-05 and no such section exists. Kept because the pattern is real, listed here because the attribution was wrong.

## Deliberate non-goals

**Voice fingerprinting.** Two competing skills (`humanizer`, `humanize-kit`) build a statistical profile from the author's own corpus and rewrite toward it. It is the most interesting idea in this space and it is excluded on purpose: it requires stored state and a corpus, it breaks the zero-dependency portability, and "sounds like you" cannot be falsified the way the rest of this file tries to be.

**Banned-word lists.** The dominant approach elsewhere (`anti-ai-writing` bans roughly 56 words outright). Rejected because every word on every list here is legitimate English, and Kobak's own finding is about frequency ratios, not about words being forbidden. Density and co-occurrence are the signal.

---

## Review schedule

Tier 1 artifacts and Tier 2 vocabulary decay fastest; re-check them against current sources roughly twice a year. Tiers 3 and 4 have been stable across several model generations.

Last reviewed: **2026-08**.
