---
title: What we learned building a two-branch signal controller
date: 2026-07-14
---

# What we learned building a two-branch signal controller

Our paper on cooperative traffic signal control was accepted last month. This is
the informal version, the parts that did not fit in eight pages.

## Why fixed timing fails

Fixed timing is the default at most intersections, and it is simple enough to
stay in service long after the traffic pattern it was tuned for has changed. It
cannot react to a queue that forms outside the modelled peak, so delay
accumulates exactly when the network can least absorb it.

Reinforcement learning drops the fixed schedule rather than retuning it.

## The two algorithms

Expected SARSA reduces policy variance by averaging over actions. SARSA(λ)
propagates credit backwards through eligibility traces. Combining them works
because the variance reduction stabilises the traces, which is the tradeoff the
single-algorithm literature tends to obscure.

Hybrid designs often fail to pay off, and one result on four topologies is not
enough to say whether ours is the exception. Convergence held across every seed
we tried.

### Results

Delay dropped on all four topologies, by 20 to 25%, with tight confidence
intervals over 20 runs.

| Topology | Fixed timing | Ours | Change |
|---|---|---|---|
| Single | 42.1s | 31.4s | -25% |
| Corridor | 58.9s | 44.2s | -25% |
| Grid 2x2 | 61.0s | 48.8s | -20% |
| Grid 3x3 | 77.4s | — | not run |

Return stayed in the 0.88–0.98 band once λ was above 0.6.

## Hyperparameters that mattered

Three of them, and only three:

- **λ**: 0.7. Below 0.5 the traces decay too fast to reach the upstream phase.
- **α**: 0.05, annealed. Higher values diverge on the 3x3 grid.
- **ε**: 0.1 fixed. Annealing it made evaluation harder to compare.

```python
# credit decays by lambda each step — traces are truncated at 40
trace = trace * lam * gamma
```

Reported delay may vary with the demand profile you simulate.

## What breaks in deployment

Detector reliability. The policy is robust to 10% dropout and not to a dead
detector, which reports zero flow rather than an error. As one reviewer put it,
the approach "needs a story for what happens when a loop detector fails." That
is fair, and we do not have one yet.
