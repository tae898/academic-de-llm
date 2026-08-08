---
title: What we learned building a two-branch signal controller
date: 2026-07-14
---

# What We Learned Building A Two-Branch Signal Controller 🚦

Our paper on cooperative traffic signal control was accepted last month, and
this post is the informal version — the parts that did not fit in eight pages.

## Why Fixed Timing Fails

Fixed-timing control serves as the default at most intersections, and it boasts
a simplicity that keeps it in service long after the traffic pattern it was
tuned for has changed. It offers no way to react to a queue that forms outside
the modelled peak, ensuring that delay accumulates exactly when the network can
least absorb it.

Reinforcement learning is not just a way to retune those timings, but a way to
drop the fixed schedule entirely.

***

## The Comprehensive Picture

We combined two algorithms, highlighting a tradeoff that the single-algorithm
literature tends to obscure:

- **Expected SARSA**: Reduces policy variance by averaging over actions.
- **SARSA(λ)**: Propagates credit backwards through eligibility traces.
- **Together**: The variance reduction stabilises the traces.

Experts argue that hybrid designs rarely pay off, and our result may potentially
be an exception rather than a rule. Notably, the comprehensive sweep exhibited
robust convergence across every seed we tried, highlighting the importance of
the variance term. Getting the variance term right is crucial.

#### Results

Delay dropped significantly on all four topologies, and the confidence intervals
over 20 runs were tight. These findings offer insights into where the gain
actually comes from.

| Topology | Fixed timing | Ours | Change |
|---|---|---|---|
| Single | 42.1s | 31.4s | -25% |
| Corridor | 58.9s | 44.2s | -25% |
| Grid 2x2 | 61.0s | 48.8s | -20% |
| Grid 3x3 | 77.4s | — | not run |

Return stayed in the 0.88–0.98 band once λ was above 0.6.

## Hyperparameters That Mattered

Three of them, and only three:

- **λ**: 0.7. Below 0.5 the traces decay too fast to reach the upstream phase.
- **α**: 0.05, annealed. Higher values diverge on the 3x3 grid.
- **ε**: 0.1 fixed. Annealing it made evaluation harder to compare.

```python
# credit decays by lambda each step — traces are truncated at 40
trace = trace * lam * gamma
```

Reported delay may vary with the demand profile you simulate. Detector
placement remains an open question, and our controller offers a robust and
flexible solution for the topologies we tested.

## Limitations And Future Work

Despite its comprehensive coverage of the four topologies, the method faces
several challenges around detector reliability, which we are actively working to
address in follow-up work. As one reviewer put it, the approach “needs a story
for what happens when a loop detector fails.”

That is fair. :contentReference[oaicite:3]{index=3}
