# Convolution and Pooling Connections

## Convolution

The project highlights the significance of padding, which is used to extract features from image corners and maintain image size after convolution. Additionally, stride, which determines the step size of the kernel, is discussed as a means of down-sampling input data.

## Pooling

Pooling, a crucial step following convolution, focuses on feature extraction from convolution layer outputs. Max Pooling, a widely used technique, retains only the highest values in a pool, effectively capturing significant features. The report discusses local and global pooling, highlighting their roles in dimension reduction.

## Spiking Neural Network With Convolution and Pooling

The project provides insights into the integration of convolution and pooling into Spiking Neural Networks (SNNs). It outlines the transformation of the original image through convolution with a Difference of Gaussian (DoG) filter, encoding the result using Time to First Spike (TTFS) encoding. The impact of pooling connections is studied, with a focus on how pooling affects spike generation and feature extraction.

## Conclusion

This report provides a detailed exploration of convolution and pooling connections in the context of Computational Neuroscience. It showcases the significance of these techniques in feature extraction, dimension reduction, and spike generation within Spiking Neural Networks. The examples presented illustrate the importance of parameter selection for optimal results.