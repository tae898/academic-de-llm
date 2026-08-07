---
name: trap
---

# Notes on the evaluation protocol

Legitimate academic prose. Several patterns fire on this file. The correct
output is **no changes at all**.

## Training BERT With PyTorch

Looks like title case, but the pattern does not fire here: `[A-Z][a-z]+` cannot
match `BERT`, and the word before `With` ends in a capital, so the run breaks.
That is an accident of the regex, not a guard against proper nouns. The next
heading proves it.

## Monte Carlo Tree Search

Fires the title-case pattern. It is a method name that is capitalised by
convention, and the heading is already correct. Reject it.

## Sample size

Seed count is one of the few choices here that is genuinely crucial: too few and
the variance between runs swamps the effect, too many and the compute budget
goes to error bars instead of ablations. That is one vocabulary marker, in a sentence that says why
it matters. Density is the signal, and one is not density.

The three failure modes we saw were reward hacking, trace truncation, and
premature annealing. Three real things, so deleting the third loses information.

### Notation

- **λ**: eligibility trace decay, swept over {0.5, 0.7, 0.9}
- **α**: learning rate, annealed from 0.05
- **ε**: exploration rate, held fixed at 0.1

An inline-header bold list, and the pattern cannot tell it apart from a hollow
one. It is a notation table: genuinely parallel, meant to be scanned rather than
read. Keep it.

## Measurements

Normalised return held at 0.88–0.98 of the ceiling across seeds. That is an en
dash in a numeric range, not an em dash.

| Topology | Delay | Notes |
|---|---|---|
| Corridor | 44.2s | — |
| Grid 2x2 | 48.8s | warm start |

## Implementation

```python
# strip the prefix — the parser needs the bare identifier
run_id = line.split("—")[0]
```

Pass `--seed` explicitly. Checkpoints are written to `~/runs/`.

Error: `simulation reset by peer — retrying`

## Prior art

Quoting a 2019 design note, which predates ChatGPT by three years and therefore
cannot be machine-generated whatever it looks like:

> Careful reward shaping stands as a crucial component of any robust control
> pipeline, serving as the bridge between the designer's intent and the agent's
> incentives, and underscoring the importance of early ablation.
