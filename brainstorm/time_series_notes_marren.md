## Main points of Mike's notes, for my future reference

### Fourier Analysis
* FT is the transformation of a continuous time signal to the sum of weighted cosine and sine functions at various frequencies.
  * This useful as it can give us information about the activity of the signal at different fundamental frequencies
  * DFT is a version of FT which works on a signal sampled at discrete times.
    * The normal algorithm runs in the square of the signal length
    * FFT is a version which runs in TlogT of the signal length, which a huge improvement.
  * FFT has a well defined inverse, the IFFT
  * Use FFT shift to avoid the mirrored power spectrum issue
  
### Wavelet Transforms
* Wavelet transforms are often better than fourier transforms, they get the best tradeoff between temporal and frequency resolution

### Filtering
* High-pass filter means all wave components above a certain frequency are allowed through the filter, and everything under is attenuated.
* Low pass filters are the opposite of high-pass filters.
* Notch (band) filters filter everything outside of a certain frequency range (e.g. 10 to 30 Hz)
