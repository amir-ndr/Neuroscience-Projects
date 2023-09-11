# FlatSTDP and FlatRSTDP Learning Report

## Introduction

This report delves into the world of neural learning, specifically focusing on two learning rules: FlatSTDP and FlatRSTDP. The project explores these learning mechanisms by implementing a model comprising two layers of Leaky Integrate-and-Fire (LIF) neurons. The first layer receives input in the form of spike trains, while the second layer consists of two neurons aiming to learn specific patterns. These layers are fully connected, and the patterns to be learned are generated from Poisson distributions.

Throughout this project, we inject inputs into the first layer and employ FlatSTDP and FlatRSTDP learning rules to train the neurons in the second layer. The report analyzes the evolution of synaptic weights during the training process and investigates the effects of parameter variations.

## Results

In this project, a two-layer LIF model with ten neurons in the first layer and two neurons in the second layer is utilized. Two different patterns are generated using Poisson distributions and injected into the first layer. The second layer is trained using the FlatSTDP and FlatRSTDP learning rules. Parameters such as `A+`, `A-`, `cte-pre`, and `cte-post` are tuned to control synaptic changes.

The results show that the neurons in the second layer learn patterns as the synaptic weights change during the training process. Raster plots and weight change visualizations are presented to illustrate the learning progress.

Additionally, the report introduces Reward-modulated Spike-Timing-Dependent Plasticity (RSTDP), which incorporates dopamine as a modulator to selectively train neurons. The results show that this method can be used to guide specific neurons to learn particular patterns based on rewards and punishments.

Explore the detailed findings and visualizations in the report to gain a deeper understanding of these neural learning mechanisms and their applications.