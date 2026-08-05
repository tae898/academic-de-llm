# Models

Which models produced which result, and the rules for picking them.

Every eval output in `research/eval/out/` carries a `manifest` block with the
model ids, date, corpus and seed. Nothing in this repo reports a model-derived
number without one.

## Selection rules

**1. No judge from the family that wrote the skill.**
Claude authored this skill. No Claude model judges it. Self-evaluation is the
default failure mode of an artefact like this and it is not worth arguing about
after the fact.

**2. No judge from the lab that produced the rewrites.**
The rewriter is OpenAI, so no OpenAI model judges. A model asked to score text
its own family generated has an interest in the answer.

**3. Judges from distinct labs.**
Four labs across two countries of origin, so a shared house style cannot carry
the result. If all judges agreed because they were trained on similar data, the
finding would be about the judges rather than the text.

**4. Current models only, checked by date.**
Sort OpenRouter's `/models` by `created` and read the top of the list. Do not
keyword-search for names you already know, which is how the first panel ended up
a year stale (see below).

**5. The rewriter is one model across both rewrite arms.**
Arms B and C differ only by whether `SKILL.md` is in the prompt. Two different
rewriters would confound the thing being measured.

## Current panel (2026-08)

| Role | Model | Lab |
|---|---|---|
| Rewriter, arms B and C | `openai/gpt-5.6-terra` | OpenAI |
| Judge | `qwen/qwen3.8-max` | Alibaba |
| Judge | `z-ai/glm-5.2` | Zhipu |
| Judge | `x-ai/grok-4.5` | xAI |
| Judge | `google/gemini-3.6-flash` | Google |

Override with `DELLM_REWRITER` and `DELLM_JUDGES` (comma-separated).

## Superseded panel (2026-08-05, archived)

| Role | Model | Why it was wrong |
|---|---|---|
| Rewriter | `openai/gpt-5` | superseded by the 5.6 family in July 2026 |
| Judge | `google/gemini-2.5-pro` | roughly a year old, Gemini was on 3.6 |
| Judge | `x-ai/grok-4.5` | current, kept |
| Judge | `deepseek/deepseek-r1` | DeepSeek was on v4 |

Results in `research/eval/out/archive-2026-08-05-gpt5/`.

**How this happened, because it will happen again.** The panel was assembled by
searching OpenRouter for model names already known to the author, which returns
whatever is still listed rather than what is current. Sorting 338 models by
creation date takes one command and shows that the field had moved: Qwen 3.8,
DeepSeek V4, GLM 5.2, Kimi K3, Gemini 3.6, the GPT-5.6 family and Grok 4.5 were
all released in the four months before the run.

Two of three judges were a generation behind. The archived results are kept
rather than deleted, because comparing them against the current panel is the
only direct evidence about whether a finding survives a model generation, which
is the question this whole repo exists to keep asking.

## What is not claimed

These models were chosen for currency and lab diversity, not because they are
good at judging prose. Nothing here validates them as evaluators. If a future
run disagrees with an earlier one, the model panel is a candidate explanation
before the text is.
