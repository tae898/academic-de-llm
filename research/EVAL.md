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

Two corpora, both *Sensors* (Basel), both chosen by tell density:

- **Abstracts**, 30 from 2026, in `research/eval/out/`. What the eval has
  always used.
- **Paper sections**, 24 from 2026 plus 6 from pre-2022 as a control, in
  `research/eval/out-papers/`. Top-level sections of PMC open-access full
  texts, 250 to 900 words, mean 534. This is the register the skill exists for
  and it had never been evaluated until 2026-08-08. A whole paper is the wrong
  unit: nobody polishes 8,000 words in one pass and a pairwise judge cannot
  read two of them carefully.

The pre-2022 control predates ChatGPT and cannot be machine-generated, so
whatever the judges say about it bounds what the style metric means.

Judges: three models from three labs, none from Anthropic (which authored the
skill) and none from OpenAI (which produced the rewrites). See
[`MODELS.md`](MODELS.md). Blind, position-randomised, never told a skill exists.

Reproduce with `make eval`; the sections run adds `--pool`, `--words` and
`DELLM_EVAL_OUT`. Raw output carries a manifest of model ids, date, corpus,
pool paths and seed.

**These two runs sample different documents from those the archived runs used.**
The earlier eval sampled through a `--pool` override at a file no script
produced and no document named, and the manifest recorded the same corpus
string either way. That is fixed, and the consequence is that today's numbers
are a fresh measurement rather than a paired before-and-after against the
archive.

## Results

All figures below come from one configuration: `gpt-5.6-luna` rewriting,
`grok-4.5` + `glm-5.2` + `deepseek-v4-flash` judging at `effort: low`, 30 2026
*Sensors* abstracts. `make eval` reproduces them. Where an earlier configuration
gave a different answer, both are shown, because the difference is one of the
more useful things this repo knows.

### Head to head

Two corpora now. Abstracts are what the eval has always used; **paper sections
are the register the skill exists for and had never been tested on.**

| Measure | Abstracts, naive | Abstracts, **skill** | Sections, naive | Sections, **skill** |
|---|---|---|---|---|
| Reads more machine-like of the pair | 77.8% | **22.2%** | 70.4% | **29.6%** |
| Substantively faithful | **99%** | 96% | **97%** | 92% |
| Major content losses | **0** | **0** | **0** | **0** |
| Edit judged better | **94%** | 91% | **100%** | **100%** |
| Edit judged worse | **0%** | 7% | **0%** | **0%** |
| Made prose flatter | **3%** | 16% | **0%** | 6% |
| Lost something worth keeping | **2%** | 16% | **0%** | 3% |

30 abstracts and 24 sections, all 2026. Bold is the better column of a pair.

**The skill wins on the thing it is for, on both registers.** It is somewhat
weaker on sections (29.6% against 22.2%), which is the expected direction: a
534-word section holds more legitimate prose to preserve than a 200-word
abstract.

**The quality cost is length-dependent, and that is new.** On abstracts the
skill is judged flatter 16% of the time against the naive prompt's 3%, and
discards something worth keeping 16% against 2%. On sections both collapse to
6% and 3%, with nothing judged worse at all. A 200-word abstract is already
compressed; removing tells from it leaves little room for varied rhythm. A
section has room. If you run this on one thing, run it on a section, not on an
abstract you have already cut to the bone.

The rhythm directive has moved the absolute number (it was ~20% before the
directive existed) but **not the ratio**: the skill still flattens roughly five
times as often as simply asking. It has not solved the problem it was written
for.

### The copula finding, and its retraction

**Published 2026-08-08 and retracted the same day.** It is kept here because the
mistake is more instructive than the claim was.

The claim was that the skill *relocates* copula avoidance rather than removing
it: adjudicated real instances fell only 17 to 14 (-18%) against -62% for every
other structural pattern, while `remains` rose 4 to 6 and `provides` 3 to 4 —
the two triggers `SKILL.md` hedges. The reading was that the rewriter drops
`serves as` and reaches for a verb the skill has told it is usually fine.

**Reading the instances kills it.** Of the 21 `remains` hits the panel called
real, nearly all are of one shape:

> Accurate distance measurement in outdoor environments **remains** a challenging problem
> Reliable quality control of AAV vectors **remains** a major bottleneck
> The relevant literature **remains** dispersed

That is not a dressed-up copula. `remains` means *continues to be, despite prior
work*, which is the standard opening move of an abstract and the thing that
justifies the paper existing. `is` is grammatically substitutable and drops the
meaning. `serves as` splits the same way: "descriptors **serve as** a correction
signal" and "alpha-band modulation may **serve as** a biomarker" name a
functional role, while "this review **serves as** a comprehensive guide" is the
tell.

Classified by what the construction does rather than which verb it uses:

| | original | naive | **skill** |
|---|---|---|---|
| **Praise-copula**, the real tell | 6 | 6 | **3** |
| Persistence, `remains a challenge` | 4 | 11 | 6 |
| Functional role, `serve as a signal` | 3 | 2 | 2 |
| Other | 4 | 0 | 3 |

**On the real tell the skill removes 50% and the naive prompt removes none.**
The naive prompt writes *more* `remains a challenge` (4 to 11), which is also
not a defect: it is reaching for standard academic phrasing.

Three things follow, and they matter more than the retracted number.

**The panel inherited the regex's framing.** It was asked whether each match was
a real instance of "copula avoidance", having been handed a match. Unanimity was
high (3/3 on most `remains` hits) and unanimity is not accuracy. A judge panel
shown a hit is answering a narrower question than a judge panel shown a text.

**The trigger list was the wrong abstraction.** Every genuine hit shares
something no verb list captures: an unmeasured quality claim. `provides an
efficient and reliable solution`, `offers a cost-effective, robust, low-latency
solution`, `serves as a comprehensive guide`. The verb is incidental; the
praise adjective with no number behind it is the tell.

**`remains` should come out of the trigger list**, and the section should ask a
question rather than match a verb: *does this sentence claim quality without a
measurement?* That keeps every real hit above and drops every false one.

### Rhythm: measured on both sides, and the folklore is half wrong

"AI writes uniform, short, choppy sentences" is the most repeated claim in this
space. `research/rhythm.py` tests it against the same venue before and after
ChatGPT, and then against raw model output. The two answers disagree.

**In published academic prose, rhythm barely moved.**

| | abstracts pre-2022 | abstracts 2026 | papers pre-2022 | papers 2026 |
|---|---|---|---|---|
| sd of sentence length | 8.6 | **8.0** | 15.9 | **16.8** |
| longest sentence | 40.5 | **39.6** | 110.7 | **118.4** |
| % sentences 15-30 words | 61.7 | 66.3 | 51.0 | 51.3 |
| commas per sentence | 1.3 | **1.6** | 1.5 | **2.0** |
| % consecutive same opener | 11.3 | **6.4** | 11.0 | **7.5** |

Burstiness is flat. The longest sentence is flat. Repeated openers went *down*,
so 2026 prose varies its sentence openings **more** than 2019 prose did. The one
metric that moved is clause density, up 23% in abstracts and 33% in papers,
which is the superficial `-ing` finding seen from another angle.

**So sentence rhythm is not a detection signal.** A section telling a reader to
look for uniform sentence length in a draft would be encoding folklore this
corpus refutes.

**In raw model output, rhythm collapses.**

| | original | naive | **skill** |
|---|---|---|---|
| sd of sentence length | 15.0 | 7.6 | **6.8 (-54%)** |
| longest sentence | 69.4 | 39.8 | **35.7 (-49%)** |
| mean sentence length | 33.3 | 21.8 | **19.7 (-41%)** |
| commas per sentence | 2.2 | 1.4 | **1.1 (-50%)** |
| % sentences 15-30 words | 50.0 | 69.4 | **68.8 (+38%)** |

Paper sections, n=24. Asking any model to de-slop halves the variance and halves
the longest sentence; the skill goes slightly further than the naive prompt on
every row. On abstracts the same effect is smaller (sd -22%) because an abstract
starts closer to uniform.

**This is the second directive's evidence, and it is much harder than the judge
opinion that used to stand in for it.** "Made prose flatter 16% of the time" is
a panel's impression. "The longest sentence fell 49% and comma density halved"
is the mechanism, and it gives the directive something checkable: **keep the
longest sentence long.** A pass that leaves the longest sentence near its
original length has not flattened the text, whatever else it did.

### Five prompt lengths on one corpus: shorter measured worse, every time

30 *Sensors* 2026 abstracts, same rewriter, same judges, same arm B throughout.
Only the instruction file changed.

| instruction | size | reads machine-like | faithful | judged worse | lost something |
|---|---|---|---|---|---|
| naive one-liner | 1 line | 78% | **99%** | **0%** | **2%** |
| **shipped skill** | **19KB** | **22.2%** | **96%** | **7%** | **16%** |
| condensed | 5KB | **13.3%** | 77% | 28% | 38% |
| minimal | 19 lines | 30.7% | 84% | 41% | 54% |
| minimal + edit locality | 19 lines | 53.9% | 71% | **71%** | **80%** |

**The long file wins on balance and three attempts to shorten it all lost.**
The condensed version buys nine points of style for twenty-two points of
fidelity and twenty-two of loss. The two minimal versions are worse on every
axis at once.

**Edit locality is actively harmful**, which was not the prediction. The
instruction was "do not rewrite a sentence that contains nothing to fix; change
the fewest words that remove it". It produced the best figures this repo can
compute without a judge — 79% of the largest tell removed, 53% of sentences
untouched, sentence-length variation within 4% of the original — and the worst
figures with one. The samples show why:

> "boasts promising prospects" became "has prospects"
> "enables online damping adjustment, improving dynamic adaptability" became
> "enables online damping adjustment and dynamic adaptability"

Told to change as few words as possible, the model **excises instead of
rewriting**. The trigger word leaves and a damaged sentence stays. A regex sees
a clean document; a reader sees broken English. It is the sharpest example this
repo has of why the density table is not evidence.

**What the long file appears to buy is worked examples.** Every short version
kept the descriptions and dropped the before-and-after pairs, and the failure
mode of the shortest is precisely not knowing what a good edit looks like. That
is the next thing to test, and it is cheap: the same 19 lines plus three worked
pairs.

**A harness bug found on the way, and worth recording.** The rewriter labelled
its input `ABSTRACT:` and asked for no preamble. Under a long instruction the
model ignored the label; under a short one it echoed it into the output — 0 of
30 for the 19KB file, 10 of 30 at 19 lines, 15 of 30 at 19 lines plus locality.
The harness was penalising prompts in proportion to their brevity, in the exact
comparison it existed to make. Input is fenced now. Re-running with it fixed
moved the numbers by a few points and changed no conclusion, so the effect was
real and not the explanation.

### Calibration language suppresses action

Seven patterns in `SKILL.md` were measured across ten corpora and found to
produce **four matches in sixty documents** between them. Three more turned out
to be field habits rather than general tells: `robust` rises 3.5x in biomedical
abstracts and falls in every arXiv category. The obvious edit was to cut the
seven and demote the three to a section headed *field-varying, check before you
cut*.

The prediction was no change, since a pattern that never fires cannot be
removed. The result:

| | 19KB | after the edit |
|---|---|---|
| reads machine-like | **22.2%** | **38.2%** |
| substantively faithful | 96% | **97%** |
| judged worse | **7%** | 9% |
| flatter | 16% | **12%** |
| lost something worth keeping | 16% | **13%** |

**Sixteen points of the primary outcome, for three points of safety.**

Length does not explain it: the 5KB condensation scored the *best* style number
of any version tested (13.3%). What the edit added was permission. Telling the
model that three patterns are "a question about your field rather than a
finding" moved them from *remove this* to *consider whether this applies*, and
removals fell accordingly.

The general form, which is uncomfortable for a repository built on
qualification: **hedging in an instruction is not free.** In a document a
caveat costs the reader nothing and buys accuracy. In an instruction it is a
licence not to act, and the model takes it. Every version tested today with
more hedging removed fewer tells.

That does not make the measurement wrong. Those seven patterns genuinely do not
occur and `references/sources.md` says so at length. It means the finding
belongs in the evidence file rather than in the instruction, and that trimming
an instruction on the strength of a corpus measurement needs its own A/B before
shipping.

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
