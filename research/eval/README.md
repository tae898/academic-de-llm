# Eval harness

Does the skill beat naively asking an LLM to de-slop? Without that comparison an
eval only shows that an LLM can edit, which was never in question.

```bash
make eval          # rewrite -> judge -> analyse
```

Costs OpenRouter credits and hits third-party APIs, so it never runs in CI.
Needs `OPENROUTER_API_KEY` or `~/.tokens/openrouter_token`.

| Stage | Does |
|---|---|
| `rewrite.py` | produces arm B (naive prompt) and arm C (same prompt plus `SKILL.md`) from one rewriter model, so the skill is the only variable |
| `judge.py` | blind pairwise style choice, plus fidelity with the substantive/evaluative split |
| `analyse.py` | the tables in `../EVAL.md` |

Output lands in `out/`, gitignored, each file carrying a `manifest` block with
model ids, date, corpus and seed.

## Two things here exist because of specific failures

**Incremental writes.** The first run held 240 results in memory and wrote once
at the end. It was killed at 40 and all of it was lost. Every stage now writes
atomically after each call.

**The fidelity split.** The first fidelity prompt asked judges to flag anything
"dropped, altered or WEAKENED". They flagged the removal of `crucial`,
`comprehensive` and `remarkable`, which is what the skill is *for*, and returned
22% faithful against the naive prompt's 71%. Separating substantive loss from
evaluative softening turned the same data into 91% against 94%. Do not merge
those buckets again.

## Sampling

Three eras, because era turned out to matter more than expected:

- **2026** the text the skill will actually meet
- **2024** old-era slop, whose profile is largely extinct (`crucial` and `delve`
  are back at pre-ChatGPT baselines), kept so the difference is visible
- **pre-2022** cannot be AI-generated, so it bounds what the style metric means

Abstracts are picked by tell density rather than at random, because random
sampling mostly selects text the skill correctly leaves alone.
