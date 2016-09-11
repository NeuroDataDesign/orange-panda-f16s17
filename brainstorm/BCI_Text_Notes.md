# BCI Textbook notes (ch 1, 2)
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

####Midbrain

*The tectum is composed of the inferior and superior colliculus and is involved in the control of eye movements and visual reflexes. Data from this region would probably be very interesting for many of the paradigms in our dataset, but this area is in the midbrain so it is likely not reachable by non-invasive EEG.

####Neocortex
* The neocortex contains about 30 billion neurons arranged in 6 layers. It would be interesting to know how far down into the neocortex our EEG method measures, and what percentage of the neocortex this corresponds to.

* Neocortex exhibits functional specialization (e.g. areas map to different cognitive functions). It would be interesting to take into account which function is realized in the area of each electrode.
  * Occipital areas near the back of the head specialize in basic visual processing
  * Pareital areas toward the top of the head specialize in spacial reasoning and motion processing.
  * Visual and auditory recognition occurs in the temporal areas
  * Frontal areas are involved in planning and higher cognitive functions.


