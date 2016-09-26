# Notes on Filtering

## 1. Gaussian Filtering - [Reference](https://www.cs.auckland.ac.nz/courses/compsci373s1c/PatricesLectures/Gaussian%20Filtering_1up.pdf)

### Function
-used to blur images and remove noise and detail.
-a function to relate the standard deviation of the distribution and filter out the things that are "too far away"
-the distribution is assumed to have a mean of 0.
-this works for a bell shaped Gaussian distribution.

### Standard Deviation
-remember one standard deviation is 68%
-we design Gaussian kernel of fixed length.
-normally we limit the kernel size to contain values within 3 standard deviation from the mean.

### Facts
-non-uniform low pass filter.
-kernel coefficients diminish with increasing distance from the kernel's center
-Central pixels have a higher weighting
-Larger values of stdev produce a wider peak (greater blurring)
-Kernel size must increase with increasing stdev to maintain Gaussian
-Gaussian kernel coefficient depends on stdev
-At edge: coefficients lim -> 0
-Kernel rotationally symmetric
-Gaussian kernel is separable!
-MIGHT NOT preserve image brightness

## 2. Finite Impulse Response (FIR) filters
-non-recursive digital filters (no feedback)
-ideal filter approximation
-filter order increases -> increases the complexity and the amount needed for processing input samples of a signal being filtered
-only use when linear phase characteristic is necessary (when phase response is a function of frequency)
-FIR is very high order, so only use when you NEED to
-but the variables are guaranteed to be stable

-Window Method - the most commonly used method

### List of Filters
-Low Pass Filters - frequency cutoffs
-High Pass Filters
-Band Pass Filters
-Band Stop Filters

-Z transform - converts discrete time doamin signal into a complex frequency-domain representation.

### Ideal Filter Approximation
-compute ideal filter samples
-ideal filter frequency sampling must be performed in a finite number of points
-error is less as the filter order increases
-ideal filter frequency response can be computed via inverse Fourier transform

### Window Functions

#### How
1. Defining filter specifications - filter order, sampling frequency, passband cut-off frequency
2. Specifying a window function according the specs - check the different shapes
3. Computing the filter order given specs - a total number of filter coefficients compared to order
4. Computing the window function coefficients
5. Computing the ideal filter coefficients according to the filter order - equations are given
6. Computing FIR filter coefficients according to the obtained window function and the ideal filter coefficients
7. If the resulting filter has too wide/ too narrow transition region, it is necessary to change the filter order by increases or decreasing it according to needs. Then repeat 4,5,6

Last but not least, note that the final objective is to find the desireed normal frequency, transition width, and stopband attenuation.

-will include some algorithms in another .md file.

### Window Method
A window is a finite array consisting of coefficients selected to satisfy some certain requirements.
These coefficients can be denoted by w[n]
It is necessary for us to specify 
1. a window to be used
2. a filter order according to the required specifications (selectivity and stopband attenuation)

Each function is a "compromise" because
-the higher the selectivity, the narrower the transition region
-the higher suppression of undesirable spectrum, the higher the stopband attenuation

Note: Stopband attenuation is just the point to pass vs stop the signal

Some useful links:

[Different algorithms for different shape of windows](http://learn.mikroe.com/ebooks/digitalfilterdesign/chapter/window-functions/)

[Examples](http://learn.mikroe.com/ebooks/digitalfilterdesign/chapter/examples/)

3. Infinite Impulse Response (IIR) filters
-most efficient in digital signal processing (DSP)
-for any non-linear phase characteristic signal
-"biquad" of filters.
-potential instabilitiy due to the feedback aspect
-difficult control and can have limit cycles

### Design
-most commonly used via the reference analog prototype filter
-again best for all standard types of filters.
-need to determine:
1. a type of reference analog prototype filter
2. scaling of frequency range to turn analog prototype filter into an analog filter
3. convert from analog to digital filter
	-most common is bilinear transformation method

-stable IIR filters will have all poles inside the unit circle

Butterworth filter!!
-frequency response is a monotonious descending function
-maximally flat magnitude filters at frequency of omega = 0
-it is necessary to know filter order beforehand

Chebyshev Analog filter
-least oscillation in frequency response in the entire passband
-equal ripple in the passband and the stopband frequency response is a monotoniously descending fucntion.