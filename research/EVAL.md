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

Mixed, and one row goes the wrong way: on copula avoidance the **naive prompt
beats the skill**, 4.2 against 13.7.

This measurement is partly circular for arm C, since a rewrite guided by pattern
X will reduce pattern X. Treat the style and fidelity judgements as the real
evidence and this table as a mechanism check.

## Two findings that reversed

Recorded because they are the reason the limits section exists.

**"The naive prompt backfires" is dead.** With `openai/gpt-5` on 2024 abstracts,
the naive prompt made superficial `-ing` 31% worse and copula avoidance 160%
worse. It was a good story: the model fixes vocabulary it has heard about and
walks into structural patterns it has no name for. With `openai/gpt-5.6-terra`
on 2026 abstracts it cuts both, and beats the skill on one. The model learned to
de-slop on its own. Any claim of this shape needs re-testing every time the
rewriter changes.

**The first fidelity number was meaningless.** Asking judges to flag anything
"dropped, altered or WEAKENED" returned 22% faithful for the skill against 71%
for naive, which looked disqualifying. The judges were flagging the removal of
`crucial`, `comprehensive` and `remarkable`, which is precisely the job.
Separating substantive loss from evaluative softening turned the same data into
91% against 94%. The confound hit the skill hardest because the skill removes
more praise words.

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
