Fixed-timing traffic signal control has known limits, and reinforcement learning
(RL) is one route past them. Classic RL algorithms carry high estimation bias and
are not robust, while newer complex-structure algorithms train slowly and
converge unevenly.

This paper develops a two-branch cooperative signal control framework for
isolated signalized intersections that combines Expected SARSA and SARSA(λ),
building a traffic-adaptive Markov Decision Process (MDP) decision model from
real-time traffic flow data. Expected SARSA reduces policy variance and Q-value
overestimation by calculating expected action values. SARSA(λ) uses eligibility
traces for multi-step temporal difference error backpropagation, which improves
sample utilization efficiency and model robustness.

Experiments cover algorithm comparison, framework generality, and hyperparameter
robustness. Across the three quantitative evaluation dimensions both improved
algorithms outperform the baselines, and scenario and parameter tests support the
framework's generality and robustness.
