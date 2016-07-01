## [Paper 3: Brain-Computer Interface With Single Channel EEG](https://people.ece.cornell.edu/land/courses/ece4760/FinalProjects/s2012/cwm55/cwm55_mj294/#)
### Publishing Date: 2012
#### Member: Michael Natenzon
 
### Summary:
This article discusses all of the specifications (technical, hardware, signal processing) related to
building a single channel EEG to play pong using an AVR microcontroller, and record EEG data during sleep.
They found that they could not use the P300 response to determine the color a user thought of from a list of
randomly flashed colors. However, they were able to prove that they could play a game of pong using alpha rhythm
modulation (concentrationg and relating) and mu suppression (visualizing motor movement). They also 
struggled with noise from 60Hz power-lines and galvanic voltages caused by insufficient electrode contact
with the skin.

An interesting point made in this article is regarding neurofeedback. 
If the user sees or hears the power of their alpha waves, and is able to manipulate their intensities, 
than they can learn to control their focus and BCI with greater discipline and precision.

### Scope of BCI:
The intensities of alpha and mu waves can be manipulated by the user through training. While this is not ideal for
out of the box applications, it offers a reliable means of controlling some aspects of BCI. By specifically
modulating either of these waves to a specific level, a user can for example open a predefined shortcut
to any function or application. This article also touches on the shortcomings of the P300 response, however, 
it does not disprove the feasability of using the P300 response as a means of identifying 
features/gameplay/content transitions that are unexpected to the user. The significance of noise is discussed in
the paper, however, no perfect methods were devised to completely eliminate all noise. This is a serious problem
to consider when designing programs for EEG headsets.
