With the development of intelligent transportation systems, new methods emerge
to overcome the limitations of traditional fixed-timing traffic signal control.
Among these methods, intelligent signal timing control based on reinforcement
learning (RL) boasts promising prospects. Classic RL algorithms have flaws like
high estimation bias and lack of robustness, while the newer complex-structure
algorithms have issues with training time and unstable convergence speed. To
overcome these limitations, this paper develops a two-branch cooperative signal
control framework integrating Expected SARSA and SARSA(λ) for isolated
signalized intersections, constructing a traffic-adaptive Markov Decision
Process (MDP) dynamic decision model using real-time traffic flow data. Expected
SARSA reduces policy variance and Q-value overestimation by calculating expected
action values. SARSA(λ) adopts eligibility traces for multi-step temporal
difference error backpropagation to significantly boost sample utilization
efficiency and overall model robustness. Experiments cover algorithm comparison,
framework generality and hyperparameter robustness. Experimental results reveal
that under the framework proposed in this paper, the two improved algorithms
outperform the baseline algorithms in quantitative evaluations conducted from
three dimensions. Scenario and parameter tests validate its generality and
robustness. This work offers an efficient and reliable solution for real-time
adaptive signal control of isolated intersections.
