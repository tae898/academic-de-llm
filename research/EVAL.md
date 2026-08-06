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

## Style: which reads more machine-generated

Lower is better. Position randomised and corrected for.

| Corpus | skill vs naive | naive vs original |
|---|---|---|
| **2026** | **4.2%** vs 95.8% | 17.0% vs 83.0% |
| 2024 | 22.9% vs 77.1% | 12.5% vs 87.5% |
| pre-2022 control | 0.0% vs 100% | **68.8%** vs 31.2% |

On 2026 text the skill's rewrite was judged more human than the naive rewrite in
**96% of blind pairings**.

The control row is the most informative line in this document. On text that
genuinely predates ChatGPT, the naive rewrite was judged **more** machine-like
than the untouched original 68.8% of the time. Asked to de-slop prose that was
never slopped, the model added machine-like qualities. The skill-guided rewrite
did not.

That also repairs the metric. An earlier run showed rewrites beating pre-2022
originals 100% of the time, which suggested the judges were only detecting
"edited". With current judges the control lands near even on human text and
decisive on machine text, which is the behaviour a valid style metric should
show.

## Fidelity: is the substance preserved

Praise-word removal is not counted as loss. That distinction is the whole
measurement; see the limits section for what happened without it.

| Corpus | Arm | Substantively faithful | Major losses | Losses per judgement | Evaluative-only edits |
|---|---|---|---|---|---|
| 2026 | naive | 40/40 (100%) | 0 | 0.0 | 3.3 |
| 2026 | **skill** | **38/39 (97%)** | **0** | **0.0** | **4.3** |
| 2024 | naive | 40/40 (100%) | 0 | 0.0 | 4.0 |
| 2024 | skill | 36/39 (92%) | 0 | 0.2 | 4.9 |
| pre-2022 | naive | 14/14 (100%) | 0 | 0.0 | 2.1 |
| pre-2022 | skill | 13/13 (100%) | 0 | 0.0 | 3.0 |

Zero major losses anywhere. The skill costs about three points of substantive
fidelity on 2026 text while making roughly a third more evaluative edits, which
is the trade it is designed to make: strip praise language, keep the facts.

## Tell density: objective, no judge

Per 10k words, 2026 abstracts.

| Pattern | original | naive | skill |
|---|---|---|---|
| Superficial `-ing` | 24.4 | 8.5 | **4.6** |
| Copula avoidance | 20.3 | **4.2** | 13.7 |
| Kobak's ten markers | 134.1 | 93.3 | **82.2** |
| Undue emphasis | 8.1 | 4.2 | **0.0** |
| Negative parallelism | 4.1 | 0.0 | 0.0 |

Two warnings about this table, and the second one is the more important.

**It is partly circular for arm C.** A rewrite guided by pattern X will reduce
pattern X. Treat the style and fidelity judgements as the real evidence.

**It is raw regex counts, which this skill exists to warn against.** The copula
row appears to show the naive prompt beating the skill, 4.2 against 13.7.
Adjudicating all nine hits by hand says otherwise:

| Arm | Raw hits | Real copula avoidance | False positives |
|---|---|---|---|
| original | 5 | **3** | 2 |
| naive | 1 | **0** | 1 |
| skill | 3 | **0** | 3 |

The three real instances were `boasts promising prospects`, `offers an efficient
and reliable solution` and `serves as a proof of concept`. **Both arms removed
all three.** Every remaining hit is `maintains` used as an ordinary active verb,
as in "maintains a high execution speed of 35 FPS", which is not a dressed-up
copula at all.

So the skill is not worse on copula avoidance. The apparent gap is entirely the
finder misfiring, at n=5, which is noise even before adjudication.

This is the skill's own central claim turned on its own eval: patterns find
candidates, not violations, and someone has to read each hit. An automated
density table cannot do that, so read this table as a mechanism check and
nothing more.

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

| | Recall | Precision |
|---|---|---|
| Patterns as shipped in v3.1.0 | **8%** | 32% |
| After retiering on this data | **52%** | **42%** |

**Recall was the real problem, not precision.** The v3.1.0 finders caught about
one real instance in twelve. A 32% precision rate is defensible for a triage
filter whose hits an agent reads; a 8% recall rate is not defensible as
anything.

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

Negative parallelism has 75% recall and **0% precision**: the cold-reading panel
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

## Quality: is the edit any good?

Style asks whether text reads machine-written. Fidelity asks whether the facts
survived. Neither asks whether the result is worth reading, and a de-slopped
passage can pass both while being flat. Four judges, 560 judgements, rewriter
`gpt-5.6-sol-pro`, on 2026 abstracts:

| Arm | Better | Same | **Worse** | **Flatter** | Lost something |
|---|---|---|---|---|---|
| Naive prompt | 94% | 6% | **0%** | **5%** | 8% |
| **This skill** | 84% | 2% | **13%** | **20%** | 15% |

**The skill makes text flatter four times as often as a naive prompt**, and 13%
of its edits are judged worse where the naive prompt produces none.

Fidelity is untouched by this: 120/120 substantively faithful on the same texts,
better than the naive prompt's 119/120, with zero major losses. The problem is
not accuracy. It is prose.

The judges agree on the mechanism, unprompted:

> chops complex academic sentences into a series of short, repetitive structures
> that make the rhythm flat and monotonous

> uniformly flat We-led prose with no gain in rhythm, voice, or precision

> discards useful framing such as "remains", "This work presents",
> "Beyond implementation"

That is this file applied thoroughly. Tier 2 says to break participial clauses
into separate sentences; Tier 3 flags connective vocabulary. Do both across a
paragraph and you get short declaratives sharing a subject, every tell gone and
the cadence gone with them.

Worth noting that `remains` is a trigger added the same day at 87% precision.
It scores well as a tell and its removal was flagged as a loss of framing.
**Precision measures how reliably a pattern indicates machine authorship. It says
nothing about whether the phrase earns its place for the reader.**

`SKILL.md` now carries rhythm preservation as a directive equal to "keep the
claim", with three rules that override the tier guidance where they conflict.
`tests/rhythm.py` enforces it on the worked example, which was itself guilty:
before the check existed, `prose-after.md` had 3.4 sentence-length variance
against the original's 8.4.

**Not yet re-measured after that change.** The 20% figure describes the skill as
it was when the eval ran.

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
- **One genre, one journal, one publisher.** *Sensors* abstracts. Nothing here
  covers READMEs, commit messages, documentation or email, which is most of the
  skill's claimed range. This is the largest gap and the most valuable follow-up.
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
[`sources.md`](../skills/de-llm/references/sources.md) implies.
