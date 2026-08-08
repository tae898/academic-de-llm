# Sources

What each source actually establishes, and what it does not. Read this before citing anything in `SKILL.md` to someone else.

Every measured number below is reproducible: `python3 research/fetch.py && python3 research/measure.py`. See `research/README.md`.

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

## 3. Own before-and-after measurement, journal abstracts (2026-08)

Not published, not peer-reviewed, and reported here so it can be checked. It has a baseline, and it is the only figure in this skill that separates "common" from "more common than it should be" outside Kobak's own work.

**Method.** All abstracts from *Sensors* (Basel, MDPI) indexed in PubMed, split into a pre-ChatGPT window and a post window, same journal and same genre on both sides:

- 298 abstracts from 2019 to 2021, 61,166 words.
- 293 abstracts from 2024, 57,220 words.

*Sensors* was chosen because Kobak measures it at Δ = 0.25, among the highest of any journal, so the effect should be visible in a small sample. Patterns were counted per 10k words in each window.

**Result**

| Pattern | pre-2022 | 2024 | ratio |
|---|---|---|---|
| Superficial `-ing` clause | 1.03 | 9.19 | **8.9x** |
| `insights` | 0.85 | 3.40 | 4.0x |
| `crucial` | 1.56 | 6.04 | 3.9x |
| Kobak's ten markers, combined | 15.46 | 50.87 | **3.3x** |
| Undue emphasis | 0.36 | 0.97 | 2.7x |
| Copula avoidance | 1.73 | 4.14 | 2.4x |
| Negative parallelism | 0.61 | 1.11 | 1.8x |
| `delve` / `showcase` / `underscore` | 0.00 | 2.04 | absent, then present |
| Em dash | 0.0 | 0.0 | no change |
| Paste artifacts | 0.0 | 0.0 | no change |

**What it establishes**

- **Kobak's vocabulary finding replicates on a sample they did not use.** Their ten markers rose 3.3x in a journal they measured independently.
- **Structural patterns show excess too, and the largest one is structural.** The superficial `-ing` clause rose 8.9x by 2024, higher than any vocabulary marker here (it has since fallen to 6.4x baseline, see source 5). Kobak measured only vocabulary; Wikipedia lists structural patterns with no numbers at all. As far as this file's authors know, that 8.9x is the first excess figure published for a structural tell.
- **Markup-specific formatting cannot be measured here and is not claimed.** Inline-header lists and title case headings require markup, so their absence from abstracts is definitional rather than a finding.

**Correction, 2026-08-05.** An earlier version of this section reported em dash at 0.0 per 10k in abstracts in both windows and concluded that formatting tells track markup rather than machine authorship. **That was a data artifact and the conclusion was wrong.** PubMed normalises every dash to an ASCII hyphen: the raw XML contains zero U+2014 and zero U+2013 characters in all four windows, including pre-2022. Em dash is simply not measurable in that corpus.

Measured instead on arXiv `cs.LG` abstracts, which preserve LaTeX dash markup, 299 abstracts from 2020 (52k words) against 300 from 2026 (59k words):

| Form | 2020 | 2026 |
|---|---|---|
| `---` (LaTeX em dash) | 0.00 | 2.71 |
| `--` | 3.14 | 7.73 |
| spaced ` - ` | 1.40 | 3.37 |

Em dash use roughly doubled in academic prose, and the 2026 instances are the parenthetical clause-separator pattern ("five influential benchmarks -- MMLU, ARC, ... -- revealing"). It is a real tell in prose, not only in Markdown. Two of the raw hits were a numeric range (`folds-1--5`) and a compound surname (`Kullback--Leibler`), at the false-positive rate this skill documents elsewhere.

**Two regex sets, on purpose (resolved 2026-08-08).** The figures above use a
**probe**: a tight definition of each tell, chosen so the pre-ChatGPT baseline is
low and the ratio is interpretable. `patterns.md` ships wider regexes tuned for
recall on an editing task, and those also match ordinary academic prose, which
raises the baseline and shrinks the ratio. Neither number is wrong and they
answer different questions, so `measure.py` now reports both and `baseline.json`
tracks both.

| Pattern | probe | shipped in `patterns.md` |
|---|---|---|
| Superficial `-ing` | 1.03 → 9.19, **8.9x** | 7.10 → 26.36, **3.7x** |
| Unmeasured quality claim | 1.73 → 4.14, 2.4x | **1.2 → 10.1, 8.1x** |
| Undue emphasis | 0.36 → 0.97, 2.7x | 3.97 → 9.67, 2.4x |
| Negative parallelism | 0.61 → 1.11, 1.8x | 1.19 → 1.82, 1.5x |

**Quote the probe for excess and the shipped set for what a pass will find.**
The probe answers "did this tell rise after ChatGPT"; the shipped regex answers
"how much will fire when I run this on a draft". A reader who takes 8.9x as a
hit rate will be surprised by the volume, and a reader who takes 3.7x as the
effect size will understate it.

**The shipped set also found something the probe hides**, and reframing it on
2026-08-08 sharpened the finding rather than removing it. The probe shows the
copula proxy peaking in 2025 and falling back (1.7, 4.1, 6.8, 4.5). The shipped
regex, once it stopped matching on the verb and started matching on the
unmeasured quality claim, runs **1.2, 7.0, 8.7, 10.1** — an 8.1x rise that has
not peaked, and the only tell measured here still climbing in 2026.

The verb-list version of the same regex read 10.2, 17.2, 25.8, 27.3, a 2.7x
rise. Both describe a real increase, but the higher baseline was ordinary
academic prose: `X remains a challenge` and `Mw serves as the primary
conditioning variable` are not tells and were roughly nine tenths of the
pre-ChatGPT count.

**What it does NOT establish**

- **One journal, one field, one publisher.** *Sensors* was picked because the effect is large there. It is not representative of publishing.
- **It is a raw before-and-after, not a counterfactual.** Kobak projects an expected 2024 frequency from 2021 to 2022 and measures the gap. This compares two observed windows, so it cannot separate LLM effects from five years of drift in the journal's topics, authorship, or editorial standards.
- **Small.** 118k words against Kobak's 15.1 million.
- Nothing about any individual abstract, for the same reason as everything else here.

---

## 3b. Abstracts against full texts (2026-08-06)

The figures behind the document branch in `SKILL.md`, as the mean of
per-document rates per 10k words. Arrows are pre-ChatGPT to now, in the same
venue. Abstracts are PubMed *Sensors*; papers are PMC open-access full texts.

**Corrected 2026-08-08.** Every figure in this table was wrong, twice over, and
both faults were in the collection code rather than the analysis:

- Half the "documents" were tables of contents. The corpus on disk predated the
  fix for the fabricated title-case rate, and still carried a synthesised
  heading block per paper. Weighted equally with 8,000-word bodies in a
  per-document mean, they held every rate down by 64 to 73%.
- The bodies were duplicated 1.85x. `art.iter('sec')` yields parent and child
  `<sec>` elements while `itertext()` on a parent already contains its
  children, so nested sections were counted twice. That biased the corpus
  toward deeply subdivided Methods and away from the flat Introduction and
  Discussion, which is where these tells concentrate.

Re-fetched with `<body>` taken once and whitespace collapsed, so one paper is
one document: 40 papers pre-2022 (227k words) and 39 from 2026 (269k).

| Tell | Abstracts | Full papers |
|---|---|---|
| Excess vocabulary (Kobak's ten) | 15.5 → **50.9** | 12.0 → **39.0** |
| Superficial `-ing`, probe | 1.0 → **9.2** | 1.0 → **5.7** |
| Superficial `-ing`, shipped | 7.1 → **26.4** | 4.4 → **16.3** |
| Copula avoidance, probe | 1.7 → **4.1** | 1.2 → **3.9** |
| Unmeasured quality claim, shipped | 1.2 → **10.1** | 0.5 → **2.2** |
| Undue emphasis, shipped | 4.0 → 9.7 | 0.7 → 1.3 |
| Negative parallelism, shipped | 1.2 → 1.8 | 1.4 → 1.3 |
| Em dash | not measurable | 3.1 → 4.9 |
| Title case headings | n/a | not measurable |

Two things this decides:

- **Structure and vocabulary rise in both**, three to four times, and by the
  same ordering. Nothing about the document type changes which of them to
  trust. Full papers run at roughly two thirds the rate of abstracts across
  every pattern, which is what you would expect: an abstract is the most
  compressed and most rewritten part of a paper.
- **Em dash barely moves in papers**, 3.1 to 4.9, on a base so small that one
  document holds a third of the matches. It is not a usable signal in a paper.
  The arXiv figures in source 3 are the ones to quote for prose.

`not measurable` means the corpus cannot carry the measurement, not that the
rate is zero. PubMed normalises every dash to an ASCII hyphen; the paper corpus
does not preserve heading markup, so nothing here says whether a paper's
headings are title case. That gap is why the markup pass is scoped by who chose
the formatting rather than by a measured rate.

---

## 3c. Seven venues, and what survives them (2026-08-08)

Sources 3 and 3b rest on **one journal**. *Sensors* abstracts and *Sensors*
full texts are the same publication sampled twice, so a claim that "rose in two
of three corpora" could be true of one venue and one field. That was the
weakest thing in this file and it is now fixed.

Ten corpora, seven publishers, four of them outside engineering: *Sensors*
abstracts and full texts, **PLOS ONE**, **BMJ Open**, **Nature
Communications**, and arXiv **cs.LG**, **cs.AI**, **cs.CL**, **econ.EM**,
**math.ST**. Same before-and-after design, same per-document rates.
Reproduce with `python3 research/audit.py`.

**Four patterns survive.**

| Pattern | venues | range |
|---|---|---|
| Copula avoidance | **9 of 10** | 1.2x - 3.5x |
| Kobak's ten, as a set | **9 of 10** | 1.3x - 3.4x |
| Superficial `-ing` | **8 of 10** | 1.3x - 3.7x |
| Dash as punctuation | **7 of 9 measurable** | 1.1x - 3.5x |

**Three that the narrow audit called confirmed are field habits.** `robust`
rises 3.5x in sensors and biomedical abstracts and falls below its pre-ChatGPT
rate in every arXiv category, because in machine learning it is a technical
term. `paradigm|landscape|realm` is 5.2x in full papers and 0.2x in PLOS ONE.
`undue emphasis` is 2.2x in BMJ Open and 0.7x in cs.LG.

This is the same failure that produced the retracted copula finding earlier the
same day: performance on the corpus a pattern was built from, mistaken for a
general result. Two venues cannot show it. Seven can.

**The dash result changed most.** It rises in **all five arXiv categories**,
2.0x to 3.5x, and sits at 1.1x to 1.6x in published journals. Authors type it
and copy editors take it out, so it is a genuine tell in a draft and nearly
invisible in the literature. That is why readers name the em dash first while
it measures flat in published corpora.

**The falsifications strengthened.** `novel` falls in 9 of 10 venues,
glue-word openers in 9 of 10, `crucial` in 7, `state-of-the-art` in 6. Seven
further patterns produce four matches across sixty documents between them and
were cut from `SKILL.md`: vague attribution, the challenges formula, false
ranges, negative parallelism, stacked hedges, `pave the way`, `pivotal`.

---

## 4. Method correction: pooled rates overstate (2026-08-06)

Every figure in source 3 and the first version of source 5 was a **pooled**
rate: all matches divided by all words. That lets one enormous document
dominate. In one corpus two link-list documents held 97% of all em dash matches
and only 19 of 120 documents contained any at all; the pooled rate was 39.7 per
10k and the median document was zero.

All rates are now the **mean of per-document rates**, and `research/measure.py`
also reports what share of matches the single worst document holds. Above
roughly 25%, a figure is being driven by outliers and should not be quoted.

What survived the recomputation and what did not:

- **The abstract corpus barely moves.** Documents there are all about 200
  words, so the two agree closely: Kobak's ten markers give 15.69 pooled against
  15.46 per document. The largest gap is the superficial `-ing` clause at 8.74
  against 9.19, about 5%. Every ratio in sources 3 and 5 survives the switch,
  and the 2024-to-2026 decay percentages move by at most 7 points.
- **One claim reversed.** Em dash in full papers was reported as falling, 6.1 to
  4.7 pooled. Per document it rises, 3.1 to 4.9. Both are small and heavily
  concentrated, so the honest statement is that em dash is not a usable signal
  in papers rather than that it moves in either direction.
- **One figure was fabricated by the collection code.** Papers appeared to show
  title case headings at 444 per 10k. `fetch.py` had been prepending `## ` to
  every `<title>` element when assembling the text, manufacturing the headings
  it then counted. Removed.

---

## 5. Own decay measurement, 2024 to 2026 (2026-08)

The skill has always claimed word-level tells decay faster than structural ones. This tests it.

**Method.** The same *Sensors* (Basel) PubMed corpus as source 3, extended to four windows: 2019-2021 (61k words), 2024 (57k), 2025 (64k), 2026 (69k, partial year through August). Same journal throughout, so genre and venue are held constant.

**Result**, tells per 10k words:

| Tell | 2019-21 | 2024 | 2025 | 2026 | 2024 to 2026 |
|---|---|---|---|---|---|
| `delve` / `showcase` / `underscore` | 0.00 | 2.04 | 1.34 | 0.23 | **-89%** |
| `crucial` | 1.56 | 6.04 | 4.12 | 0.96 | **-84%** |
| Undue emphasis | 0.36 | 0.97 | 0.32 | 0.33 | -66% |
| `pivotal` | 0.34 | 1.11 | 1.45 | 0.47 | -57% |
| Negative parallelism | 0.61 | 1.11 | 0.73 | 0.69 | -38% |
| Superficial `-ing` | 1.03 | 9.19 | 12.15 | 6.64 | -28% |
| Kobak's ten, combined | 15.46 | 50.87 | 50.80 | 39.41 | -23% |
| Copula avoidance | 1.73 | 4.14 | 6.84 | 4.53 | **+9%** |
| `robust` | 4.17 | 9.88 | 17.30 | 14.39 | **+46%** |

The same four structural tells under the regexes `patterns.md` actually ships:

| Tell (shipped regex) | 2019-21 | 2024 | 2025 | 2026 | peak |
|---|---|---|---|---|---|
| Unmeasured quality claim | 1.20 | 7.03 | 8.72 | **10.14** | **2026** |
| Superficial `-ing` | 7.10 | 26.36 | 27.52 | 22.90 | 2025 |
| Undue emphasis | 3.97 | 9.67 | 7.80 | 5.40 | 2024 |
| Negative parallelism | 1.19 | 1.82 | 0.73 | 1.31 | 2024 |

**What it establishes**

- **The famous words died.** `crucial` is back to its pre-ChatGPT level. `delve` is effectively gone. Both were the most publicized markers, and Kobak's own paper is part of why. Publicity appears to kill a word-level tell, whether by training or by authors editing it out.
- **The structural tells did not.** Superficial `-ing` is still 6.4x its pre-ChatGPT baseline in 2026 after peaking in 2025. **The unmeasured quality claim is the only tell measured here that has not peaked**: it rises in every window, 1.2 to 10.1 per 10k, and 2026 is the highest. It is invisible to the probe, which matches on the verb and so counts `X remains a challenge` in the pre-ChatGPT baseline. Unearned evaluation is the durable section, which is why `SKILL.md` puts it first and tells you to run it on everything.
- **Excess vocabulary shifts rather than vanishing.** `robust` is 3.5x baseline and up 46% since 2024. A fixed word list ages badly in both directions, not just downward.

**What it does NOT establish**

- **Cause.** MDPI introduced AI screening over this period. "Models changed their output" and "editors filtered it out" are indistinguishable in this data, and both would produce the same curve.
- 2026 is a partial year, through August.
- One journal, as with source 3. *Sensors* is a high-Δ venue and may respond to screening pressure faster than a typical one.
- Nothing about text outside peer review. An unedited 2026 chat transcript may still be full of `crucial`.

**Consequence for anyone using this skill:** re-run this measurement before trusting the vocabulary list. The method survives; the list is a snapshot. Structure is what to lean on.

Both sets are in the tables above. The vocabulary rows need only one, because
those regexes are identical in the probe and the shipped set.

---

## 6. Consulted and not used

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
- **The whole markup section, as a rate.** Sources 3 and 3b establish that structure and vocabulary rise in academic prose. Neither can measure headings or bold lists: an abstract has no markup and the full-text corpus does not preserve it. The section is kept for academic blog posts on the argument that the author chose that formatting, which is a reason rather than a measurement.
- **The inline-header bold list as a rewrite target.** Wikipedia lists the pattern; the rule for when to keep it (genuinely parallel, meant to be scanned) is mine.
- **False ranges.** Taken from the `humanizer` skill, which is Wikipedia-based, so it was assumed to be Wikipedia's. It is not: checked against the page on 2026-08-05 and no such section exists. Kept because the pattern is real, listed here because the attribution was wrong.

## Deliberate non-goals

**Voice fingerprinting.** Two competing skills (`humanizer`, `humanize-kit`) build a statistical profile from the author's own corpus and rewrite toward it. It is the most interesting idea in this space and it is excluded on purpose: it requires stored state and a corpus, it breaks the zero-dependency portability, and "sounds like you" cannot be falsified the way the rest of this file tries to be.

**Banned-word lists.** The dominant approach elsewhere (`anti-ai-writing` bans roughly 56 words outright). Rejected because every word on every list here is legitimate English, and Kobak's own finding is about frequency ratios, not about words being forbidden. Density and co-occurrence are the signal.

---

## Review schedule

Vocabulary decays fastest and is the section to re-check every cycle; source 5 measures how fast. Structure held across the same window. Paste artifacts have been stable across several model generations.

Last reviewed: **2026-08**.
