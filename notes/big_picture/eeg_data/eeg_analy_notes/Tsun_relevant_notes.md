## Some Highlights on Mike's Notes

### 2. Advantages and Limitations of Time- and Time-Frequency-Domain Analysis

#### 2.3 Interpreting Voltage Values from the EEG Signal
-Check if we need explanation or variation on EEG recording

#### 2.4 and 2.5
-Explains Event-Related Potential (ERPs)

#### 2.6 and 2.7
-Time-Frequency-Based Approaches

### 3. More Time Frequency

#### 3.2 Viewing Time-Frequency Results
-Gives a list of possible plots

#### 3.4 How to view and interpret time-frequency results
-Gives things that we can use to analyze our plots

### 7. PREPROCESSING

#### 7.2 Balance between Signal and Noise
-How much noise can we remove while keeping the signal?

#### 7.3 Creating Epochs
-How to cut our data?

#### 7.5-7.7 - Filtering, Trial Rejection, Spatial Flitering

#### 7.9 Interpolating Bad Electrodes

### 11 Discrete Time Fourier Transform

-EEG Data can be thought of as the sum of a bunch of waves- and using that assumption, Fourier transform can compute the dot product between the signals and sine waves of different frequencies (kernels)
-Have different properties

#### 11.3 The Discrete Time Fourier Transform
-Gives equation

-Note that a bunch of other stuff is also explained. We understand that FFT is better than regular Fourier Transform because it's about 1000x faster. We also learned that we have to use fftshift on our data because of Hermitian symmetry.