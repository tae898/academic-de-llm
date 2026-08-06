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

## Rule 6: price the panel on the invoice, not on one measured call

Added after a 24-hour bill came to $61.98 against an estimate of about $10. The
estimate came from timing a single call and multiplying. Reasoning token counts
vary by an order of magnitude between calls, so that method cannot work.

What the invoice showed, and none of it was visible from a sample of one:

- **Reasoning is 94% of all completion tokens.** 6.4M of 6.9M. It bills at output
  rates, which is why judge choice dominates everything else.
- **`qwen3.8-max` was 36% of the bill**, $22.38, at 1,626 reasoning tokens per
  call. A single measured call had shown 141.
- **Prompt caching only discounts input**, so it caps out around a fifth of the
  bill. It is not the lever it looks like. grok cached 1,611 of 1,640 calls and
  still cost $10.23.
- **The rewriter is priced by prompt size.** `SKILL.md` is ~13,300 tokens and
  rides in every arm-C call, so input price is what matters, not output.

Download the CSV from the OpenRouter dashboard and read it before assuming a
panel is affordable.

## Current panel (2026-08-06)

| Role | Model | Lab | $/call |
|---|---|---|---|
| Rewriter, arms B and C | `openai/gpt-5.6-luna` | OpenAI | 0.0016 |
| Judge | `x-ai/grok-4.5` | xAI | 0.0062 |
| Judge | `z-ai/glm-5.2` | Zhipu | 0.0016 |
| Judge | `deepseek/deepseek-v4-flash-0731` | DeepSeek | 0.0001 |

A 30-abstract cycle costs about **$1.50**, against $9.73 on the panel this
replaced. Override with `DELLM_REWRITER` and `DELLM_JUDGES` (comma-separated).

`deepseek-v4-flash` is conservative alone: tested against the frontier panel it
agreed 82% of the time and under-called real instances. Majority voting against
two stronger judges absorbs that. It would not be safe as a sole judge.

Before switching the rewriter, luna, `meituan/longcat-2.0` and
`openai/gpt-5.6-terra` were run on the same abstract with the full skill. All
three stripped the same tells, produced comparable length, and landed within 0.2
of each other on sentence-length variance. For a headline number worth
publishing, confirm on the top tier:

```bash
DELLM_REWRITER=openai/gpt-5.6-sol-pro make eval
```

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
