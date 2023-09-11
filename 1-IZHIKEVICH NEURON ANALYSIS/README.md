# Izhikevich Neuron Analysis

The Izhikevich neuron model is a powerful computational model in computational neuroscience that reproduces spiking and bursting behavior seen in cortical neurons. It combines the biological plausibility of Hodgkin and Huxley neurons with the computational efficiency of integrate-and-fire neurons. Key points about this model:

- It efficiently replicates the spiking and bursting of cortical neurons and allows simulating thousands of them on a regular computer.

- Unlike Hodgkin and Huxley's neurons, which are highly accurate but computationally expensive, or integrate-and-fire neurons, which are computationally effective but too simple, the Izhikevich neuron model strikes a balance, making it the most efficient and powerful model in computational neuroscience.

The model can be represented through a system of differential equations:

1. dv/dt = 0.04v^2 + 5v + 140 - u + I
2. du/dt = a(bv - u)

There's also a resetting mechanism: If v > 30 mV, then [v = c and u = u + d].

**Parameters in the equations:**

- v: Membrane potential of the neuron
- u: Membrane recovery variable, affecting ionic currents
- I: Input current
- a: Time scale of the recovery variable u
- b: Sensitivity of u to subthreshold fluctuations in v
- c: After-spike reset value of v
- d: After-spike reset value of membrane recovery variable

Different combinations of these parameters yield various neuron behaviors. Here are some notable neuron types:

1. **Regular Spiking (RS) Neurons:**
   - Parameters: a = 0.02, b = 0.2, c = -65, d = 8
   - Exhibit spike frequency adaptation, firing a few times in short periods.

2. **Intrinsically Bursting (IB) Neurons:**
   - Parameters: a = 0.02, b = 0.2, c = -55, d = 4
   - Initially burst but transition to normal spiking behavior over time.

3. **Chattering (CH) Neurons:**
   - Parameters: a = 0.02, b = 0.2, c = -50, d = 2
   - Fire closely spaced bursts with high-frequency spikes.

4. **Fast Spiking (FS) Neurons:**
   - Parameters: a = 0.1, b = 0.2, c = -65, d = 8
   - Fire spikes at high frequencies with no adaptation.

5. **Low-Threshold Spiking (LTS) Neurons:**
   - Parameters: a = 0.02, b = 0.25, c = -65, d = 8
   - Spike at low thresholds, with increasing intervals over time.

6. **Resonator (RZ) Neurons:**
   - Parameters: a = 0.1, b = 0.26, c = -65, d = 8
   - Exhibit sustained subthreshold oscillations and spike when input current is briefly increased.

7. **Saddle-Node Bifurcation (b < a) Neurons:**
   - Parameters: a = 0.1, b = 0.05, c = -65, d = 8
   - Demonstrates a saddle-node bifurcation, showing a balance in spike intervals.

## Interactive Izhikevich Model

An interactive Izhikevich model has been implemented, allowing users to explore the behavior of different neuron types. It supports two modes: step-input and noisy-input current. Users can adjust parameters and observe changes in the membrane potential.

You can see this part by running `interactive_Izhikevich_model.py`

For detailed diagrams and simulations, refer to the full report and code.