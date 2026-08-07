# Does this beat just asking an LLM to de-slop?

That is the only question worth asking about a skill like this. A model told
"make this sound less AI-generated" already does something useful, so an eval
that only compares against the untouched original measures nothing.

**Read the limits section.** It is not boilerplate; two of the findings below
reversed once the models and the corpus were made current.

## Design

| Arm | What |
|---|---|
| A | the original abstract, untouched |
| B | **naive**: one prompt, "rewrite so it does not read as AI-generated" |
| C | **skill**: the same prompt with the full `SKILL.md` prepended |

One rewriter model produces both B and C, so the skill is the only variable.

Corpus: 28 *Sensors* (Basel) abstracts from PubMed, chosen by tell density.
Twelve from **2026** (the text the skill actually meets), twelve from **2024**
(whose slop profile is largely extinct), four from **pre-2022** as a control.
The control predates ChatGPT and cannot be machine-generated, so whatever the
judges say about it bounds what the style metric means.

Judges: four models from four labs, none from Anthropic (which authored the
skill) and none from OpenAI (which produced the rewrites). See
[`MODELS.md`](MODELS.md). Blind, position-randomised, never told a skill exists.
560 calls, 520 parsed.

Reproduce with `make eval`. Raw output in `research/eval/out/`, each file
carrying a manifest of model ids, date, corpus and seed.

## Results

All figures below come from one configuration: `gpt-5.6-luna` rewriting,
`grok-4.5` + `glm-5.2` + `deepseek-v4-flash` judging at `effort: low`, 30 2026
*Sensors* abstracts. `make eval` reproduces them. Where an earlier configuration
gave a different answer, both are shown, because the difference is one of the
more useful things this repo knows.

### Head to head

| | Naive prompt | de-llm |
|---|---|---|
| Reads machine-generated | 72% | **28%** |
| Tells remaining per 10k words | 58.6 | **27.5** |
| Substantively faithful | **100%** | 99% |
| Major content losses | **0** | **0** |
| Edit judged better | **92%** | 90% |
| Edit judged worse | **4%** | 7% |
| Made prose flatter | **9%** | 13% |

Original text: 70.1 tells per 10k words. The skill removes 61% of them, the
naive prompt 16%.

The quality columns run consistently a few points against the skill across every
run today. At n=30 each is close to noise, but the direction does not vary, so
treat it as a real and small cost rather than as measurement error.

### The skill's advantage is conditional on the model

Measured on `gpt-5.6-sol-pro`, a stronger and 50x more expensive rewriter, the
same skill and the same texts gave:

| | luna | sol-pro |
|---|---|---|
| Style advantage over naive | 72 / 28 | **85 / 15** |
| Quality: better | 91% (naive 92%) | **97%** (naive 94%) |
| Quality: worse | 6% (naive 4%) | **1%** (naive 0%) |
| Quality: flatter | 12% (naive 9%) | **6%** (naive 5%) |

Both arms use the same rewriter in each column, so this is not a handicap. A
weaker model applies the skill less faithfully, and it applies the rhythm
directive less faithfully too, so it gets less de-slopping and less protection
against flattening at the same time.

**The honest claim, then:** on a capable model the skill clearly beats asking for
a de-slop in one line. On a mid-tier model it removes more tells at a small cost
in naturalness, roughly a wash. It is not a free win, and how much it is worth
depends on what is executing it.

That also means the cheap panel is right for regression testing and wrong for
headline claims. Use `DELLM_REWRITER=openai/gpt-5.6-sol-pro make eval` for
anything published.

## Pattern quality: precision and recall per finder

The eval above asks whether the skill's guidance helps a model. This asks
whether the finders themselves work, which turns out to be a different and
harsher question.

Method: 60 abstracts. One judge panel labels every regex hit real or a
words-matched false positive (2,103 calls, 701 labels). A second panel reads the
same texts **cold**, never shown a regex, and lists what it finds; an instance
counts when two of three judges quote the same span. Precision is the first
number, recall the second. `make eval` reproduces it; `research/eval/tune.py`
re-scores a candidate pattern against the collected data for free.

| Pattern | Precision | Recall |
|---|---|---|
| Undue emphasis | 8/10 (80%) | 15/18 (83%) |
| Copula avoidance | 17/37 (46%) | 20/25 (80%) |
| Superficial `-ing` | 16/52 (31%) | 34/50 (68%) |
| Negative parallelism | 0/3 (0%) | 1/2 (50%) |
| **Overall** | **51%** | **74%** |

Against the finders as they shipped in v0.3.1: **8% recall at 32% precision**.
Recall roughly quadrupled.

Overall precision counts only labels the current patterns still match. Across
every label ever collected, including hits from triggers since removed, it is
40% — that figure describes the history, not the current behaviour.

### What was actually wrong

Three specific defects, none of them conceptual:

**A comma.** `, enabling` required one. "sensor signals enabling precise and
robust detection" has none, and that single character cost most of the recall on
the highest-volume pattern.

**Missing inflections.** `serves as` was listed and `serve as` was not, so
"is intended to serve as a reproducible reference" was invisible.

**The wrong form entirely.** Negative parallelism searched for `not just X but`.
Across 60 abstracts that matched 14 times and not one was real. Every genuine
instance used `unlike traditional studies that optimise accuracy, this work...`.

### Trigger strength, measured

Precision varies more **within** a pattern than between patterns, which is why
the skill now publishes per-trigger strength instead of a flat list:

| Trigger | Real / matched | |
|---|---|---|
| `is crucial` | 13/14 | 93% |
| `is essential` | 8/9 | 89% |
| `remains` | 13/15 | 87% |
| `serves as` / `serve as` / `serving as` | 11/11 | 100% |
| `thereby <verb>ing` | 6/8 | 75% |
| `enhancing` | 18/29 | 62% |
| `providing` | 8/23 | 35% |
| `enabling` | 5/36 | 14% |
| `offer` | 0/7 | 0% |
| `maintains` | 0/11 | 0% |

**Third person singular is the tell; the base form is an ordinary verb.**
`remains` 87% against `remain` 25%, `provides` 36% against `provide` 11%,
`offers` 35% against `offer` 0%. "The framework provides X" dresses up "is".
"We provide X" does not. That distinction is not in either published source.

### What was tried and rejected

Dropping every weak trigger raised precision to 40% and dropped recall to 46%.
Rejected: on a finder whose hits an agent reads, a false positive costs a glance
and a miss costs the fix. Recall is the metric that matters and the tradeoff
runs the wrong way. Kept in `research/eval/tune.py` so it is not retried.

### Still unresolved

Negative parallelism has 50% recall and **0% precision**: the cold-reading panel
finds instances, and the adjudicating panel then calls every matched hit false.
Two panels, same definition, opposite verdicts. Until that is understood the
pattern should be read as a hint, not a finding.

## Two findings that reversed

Recorded because they are the reason the limits section exists.

**"The naive prompt backfires" is dead.** With `openai/gpt-5` on 2024 abstracts,
the naive prompt made superficial `-ing` 31% worse and copula avoidance 160%
worse. It was a good story: the model fixes vocabulary it has heard about and
walks into structural patterns it has no name for. With `openai/gpt-5.6-terra`
on 2026 abstracts it cuts both. The model learned to de-slop on its own.

Worth noting that the old figure was measured the same unadjudicated way as the
copula row above, so "160% worse" was probably part artifact too. It was never
checked by hand, because it flattered the skill. Findings that agree with you
get less scrutiny, which is the argument for fixing the method rather than the
number.

**The first fidelity number was meaningless.** Asking judges to flag anything
"dropped, altered or WEAKENED" returned 22% faithful for the skill against 71%
for naive, which looked disqualifying. The judges were flagging the removal of
`crucial`, `comprehensive` and `remarkable`, which is precisely the job.
Separating substantive loss from evaluative softening turned the same data into
91% against 94%. The confound hit the skill hardest because the skill removes
more praise words.

## How much of this is about the judges?

Every number here was re-measured after the model panel changed on 2026-08-06,
and the answers moved. Same corpus, same skill, same prompts:

| | sol-pro rewriter, 4 judges | luna rewriter, 3 judges |
|---|---|---|
| Skill vs naive on style | 15.1% / 84.9% | **28.1% / 71.9%** |
| Copula avoidance precision | 37% | **43%** |
| Superficial `-ing` precision | 38% | **27%** |
| Undue emphasis precision | 81% | **89%** |

The direction of every finding survived. The magnitudes did not.

Two causes, and they are different:

**The rewriter.** Both arms use the same model, so a weaker rewriter does not
handicap the skill directly. What it does is apply the skill less faithfully,
which moves arm C toward arm B and narrows the gap. The skill's benefit scales
with how well the model follows a 14KB instruction file. That is worth knowing
before quoting any single figure as the skill's effect size.

**The judges.** `deepseek-v4-flash` is more conservative than the `qwen3.8-max`
it replaced, so fewer matched hits get labelled real. Precision moved in both
directions by up to 11 points depending on the pattern, which is the range within
which no precision figure here should be treated as precise.

**Treat every number in this file as configuration-dependent.** The manifest in
each output file under `research/eval/out/` names the models that produced it.
A finding that only holds on one panel is a finding about the panel.

## Limits

- **Small.** 28 abstracts, four judges. Differences of a few percentage points
  are noise.
- **Abstracts only, one journal, one publisher.** *Sensors* abstracts, ~200
  words each. The skill's main target is a full paper, and nothing here has been
  run on one: a paper has sections, citations, equations and a related-work
  register that an abstract does not. The PMC full-text corpus is already
  fetched by `research/fetch.py` and unused by the eval. This is the largest
  gap and the most valuable follow-up.
- **One rewriter.** The two reversals above both came from changing the model.
  Assume every number here is specific to `gpt-5.6-terra`.
- **The density table is partly circular** for the skill arm.
- **Nothing here tests detection.** The eval measures whether text reads as
  machine-generated to other models, not whether it was. The skill disclaims
  detection explicitly and so does this document.
- **Author's own eval of the author's own artefact.** The judge panel excludes
  the authoring family, which is a mitigation, not a solution.

## Verdict

On current text with a current model, the skill beats a naive prompt on the
judged outcome by a wide margin (96% of pairings on 2026 text), at a cost of
about three points of substantive fidelity with zero major losses.

Its clearest advantage is the one that was not expected: on prose that did not
need de-slopping, the naive prompt made things worse and the skill did not. The
machinery for knowing what to leave alone turns out to matter more than the
pattern lists, which is also what the decay measurement in
[`sources.md`](../skills/academic-de-llm/references/sources.md) implies.
