# BCI Textbook notes
## Ryan Marren, Sept 11 2016

### Chapter 1 (Introduction)
* A primary application of BCIs is as sensory prosthetic devices to treat deafness, blindless, ect. In the data sharing paper, certain brain activity is typical of certain psychological disease (e.g. decreased surround supression performance in schizophrenic subjects). Perhaps a sensory prosthetic device can help this symptom and possibly improve subject quality of life?

* If we have access to the raw data, it may be beneficial to go through the signal processing portions of this textbook to see if we can better preprocess the data for our application.


### Chapter 2 (Basic Neuroscience)

####Basic neurons
* No information is conveyed in the shape of an action potential, all information is present in the firing rate. 

* The entire process of spike generation has information not relevant to our problem. We can think of neurons as threshold models, essentiallly a hybrid analog-digital computing device

####Neuroplasticity
* Via the ideas of LTP and LTD, we can probably assume that if two electrodes are highly correlated, that there is a high percentage of neurons from the two areas that are connected (directly or through interneurons)

* Could the ideas of Hebbian STDP be used to modify someone's neural circuitry (e.g., is some disorder causes two areas which should be firing together to fire at different times, perhaps this could be fixed by transmitting signals with the EEG rather than reading them?)
###Midbrain

*The tectum is composed of the inferior and superior colliculus and is involved in the control of eye movements and visual reflexes. Data from this region would probably be very interesting for many of the paradigms in our dataset, but this area is in the midbrain so it is likely not reachable by non-invasive EEG.

####Neocortex
* The neocortex contains about 30 billion neurons arranged in 6 layers. It would be interesting to know how far down into the neocortex our EEG method measures, and what percentage of the neocortex this corresponds to.

* Neocortex exhibits functional specialization (e.g. areas map to different cognitive functions). It would be interesting to take into account which function is realized in the area of each electrode.
  * Occipital areas near the back of the head specialize in basic visual processing
  * Pareital areas toward the top of the head specialize in spacial reasoning and motion processing.
  * Visual and auditory recognition occurs in the temporal areas
  * Frontal areas are involved in planning and higher cognitive functions.

###Chapter 3

####Invasive techniques
* Can directly measure action potentials of specific neurons.
* Non-invasive techniques (such as the ones used to obtain our dataset) indirectly measure these action potentials using indirect correlates in neural activity.
  * These are based on much coarser timescales and are not as accurate
* Multi-electrode arrays can be used to give spatial resolution and give the ability to record information such as signal position and velocity.
* Electrocorticography offers a compramise between invasive and non-invasive procedures.
  * Electrodes are surgically placed on the surface of the brain  * Can record coherent activity of large populations of neurons
  * Do not record spikes directly, but is more direct than EEG procedures
  * Are large in size, methods being created (microECoG) which should give finer resulotion

####Noninvasive Techniques
* EEG
  * Summnation of postsynaptic potentials from many thousands of neurons oriented radially to the scalp, tangential currents are not detected by EEG.
  * Deep brain currents are not detected bt EEG (voltage fields fall off with the square of distance to the source)
  * Predominantly captures activity in cerebral cortex
  * Spatial resolution is poor, but temporal resulution is good (this is because of layers of tissue between electrode and the measured activity, which act as volume conductors and low pass filters)
  * Artifacts caused by muscle activity and nearby electrical devices, filtered by algorithms

* EEG standardized positions
  * C = central
  * P = parietal
  * T = temporal
  * F = frontal
  * Fp = frontal polar
  * O = occipita
  * A = mastoids

* MEG magnetoencephalography
  * measures electrical fields produced by electrical activity in the brain
  * Only sensitive to currents originating tangentially to the scalp
  * Not distorted by intervening organic matter
  * Bulky and expensive, EEG better for large scale application

####Chapter 4 Signal processing

* Frequency Domain Analysis
  * Noninvasive approaches measure activity of several thousands of neurons, so only captures correated activities of large populations.
  * Often the recorded signal is oscillary activity

* Fourier analysis
  * We can decompose signals from EEG into a weighted sum of sine and cosine waves of different frequencies.
  * Allows us to perform filtering based on frequency

  * Has a computable inverse
  * Can be modified to work with a signal sampled at discrete time intervals
  * FFT is an optimization on of a DFT which takes TlogT time instead of T^2
  * wavelet transform gets the best tradeoff between temporal and frequency resolution using a short time forier transform
  * WT uses 'wavelets' as basis functions, which are derived from a mother wavelet
  * Fractal dimension is a measure of the self similarity of a wave, and can characterize the complexity of a time varying signal
  * Autoregressive models can use past measurements to predict the next measurement.
  * Particle filtering allows for estimation of posterior distribution, but does not assume linear and gaussian dynamics like a Kalman filter
  * Spatial filterng can reduce data dimentionality and enhance the local activity measured.

#####Artifact Reduction
* An attempt to reduce events outside of brain activity which influence the signal recieved by an EEG (e.g. rhythmic artifacts like respiration, heartbeat, power line noise, and event artifacts like muscle mocements, eye movements, ect.)
* Notch filtering can be sued to filter artifacts from certain frequency bands
* EOG measures eye movements and can be used to remove artifacts caused by the eyes.
