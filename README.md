# Static vs Actuated Traffic Signal Control

## Overview
This project compares **static** and **actuated** traffic signal control strategies at a single intersection using the **SUMO** (Simulation of Urban MObility) traffic simulation tool.  

The goal is to evaluate which type of signal control performs better by analyzing **vehicle** and **pedestrian time losses** under different traffic conditions.

## Methodology
- Simulated the intersection with both **static** and **actuated** signal programs.
- Generated traffic using stochastic (Poisson) demand.
- Collected key performance metrics:
  - Vehicle time loss
  - Pedestrian time loss
- Performed multiple simulation runs to compute **mean values** and **confidence intervals**.

## Results
The simulation outputs provide:
- Histograms of time loss for vehicles and pedestrians.
- Mean values and 95% confidence intervals for each control type.
- Comparative analysis to determine which signal control type is more efficient (Actuated Control performs slightly better than Static Control for both vehicles and pedestrians).

![Histogram of time loss](https://github.com/nikolabarac/static-vs-actuated-traffic-signal-control/blob/master/results.png)

