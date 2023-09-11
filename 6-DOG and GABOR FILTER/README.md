# DOG and Gabor Filter

## Visual Cortex

The Project begins with an introduction to the visual cortex, the part of the brain responsible for processing visual information. It explains the primary visual cortex (V1) and its association with both the "What Pathway" and the "Where Pathway" in the brain.

## DoG Filter (Difference of Gaussian)

The DoG filter, simulating ganglion cells in the retina, is introduced as a means of detecting points in a background with different colors. It involves subtracting two smoothed versions of an image to preserve specific spatial frequencies, thereby removing high-frequency noise components.

The report then provides several examples of applying DoG filters to images, varying parameters such as kernel size, sigma values, and gamma to observe their effects on image processing. It demonstrates how DoG filters can enhance edges and remove noise.

The project also covers Time to First Spike (TTFS) encoding, showing how the spikes of neurons correspond to pixel values in convolved images. It discusses how different parameter settings affect the encoding results.

## Gabor Filter

Gabor filters, simulating V1 simple cells, are introduced to detect lines with specific orientations. These filters are described as sinusoidal signals modulated by a Gaussian wave. The parameters of Gabor filters, including wavelength (λ), orientation (θ), sigma (σ), and gamma (γ), are explained.

The project provides examples of applying Gabor filters to images and shows how they can detect features at different orientations. It explores the effects of changing lambda values on feature extraction and encoding.

## Interactive Filters

The code offers an interactive component that allows users to manipulate filter parameters and visualize the real-time effects on convolved images. This interactive feature facilitates a hands-on understanding of the filters' behavior.

For detailed code implementations and interactive exploration, refer to the accompanying Jupyter notebook.