# Eval harness

Does the skill beat naively asking an LLM to de-slop? Without that comparison an
eval only shows that an LLM can edit, which was never in question.

```bash
make eval          # rewrite -> judge -> analyse
```

Costs OpenRouter credits and hits third-party APIs, so it never runs in CI.
Needs `OPENROUTER_API_KEY` or `~/.tokens/openrouter_token`.

| Stage | Does | Costs credits |
|---|---|---|
| `rewrite.py` | produces arm B (naive prompt) and arm C (same prompt plus `SKILL.md`) from one rewriter model, so the skill is the only variable | yes |
| `judge.py` | blind pairwise style choice, plus fidelity with the substantive/evaluative split | yes |
| `adjudicate.py` | a panel labels every regex hit real or a words-matched false positive | yes |
| `recall.py` | judges read the same texts cold, never shown a regex, and list what they find | yes |
| `analyse.py` | the tables in `../EVAL.md` | no |
| `score.py` | precision and recall per trigger word; `--freeze` writes `labels.json` | no |
| `tune.py` | scores a candidate regex against data already collected | **no** |
| `regress.py` | replays the frozen labels through the current regex; runs in `make test` | **no** |
| `cheap_panel.py` | checks whether a cheaper model agrees with the frontier panel | yes, barely |

## Iterate for free

`tune.py` and `regress.py` read `labels.json` and `recall.json` and make no API
calls at all. Tuning a pattern is the thing you do most often, and it costs
nothing. Only a change of corpus or of models needs the paid stages, which is
why `REVIEW.md` schedules those quarterly rather than per-edit.

What the paid stages actually cost, measured rather than guessed: an
adjudication call is $0.0007 to $0.0028 depending on the judge. A recall call is
about $0.0155, because the prompt carries a whole abstract and reasoning models
spend heavily on it. A rewrite in arm C is about $0.03, because the entire
`SKILL.md` goes into every prompt. **Prompt size drives the bill, not call
count**: adjudication is the highest-volume stage and among the cheapest.

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
