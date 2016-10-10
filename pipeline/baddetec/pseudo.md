### Inputs:
- inEEG: input dataset (electrodes x time x trial)

### Outputs:
- badelec- indices of rejected electrodes

#### 3 Algorithms:

##### Joint Probability:

1. **reshape:**
	- *Input:* inEEG
	- *Output:* reshapedEEG
	- *Description:* convert EEG data from (channel x time x trial) to (channel x (time, trial))
2. **LOOP:**
	- loop iterating through channels, getting prob distribution and joint probs
	1. **Prob Distribution:**
		- *Input:* reshapedEEG
		- *Output:* probability distribution of data
		- *Description:* based on available data, calculate a probability distribution to represent the prob. of electrode vals occcurring
	2. **Joint Distribution:**
		- *Input:* probability distribution
		- *Output:* joint prob. of channel
		- *Description:* using given prob. distribution, find a joint probability. This will need a defined joint prob. algorithm that is interchangeable
	3. **Concatenate:**
		- *Input:* joint prob. of channel
		- *Output:* make one array of joint probs
		- *Description:* pretty self explanatory
3. **Normal Distribution:**
	- *Input:* joint prob. of channel
	- *Output:* normal distribution of joint probs
	- *Description:* get a normal dist of joint probs so that we can find outlier
4. **Threshold:**
	- *Input:* normal distribution of joint probs
	- *Output:* bad electrode array
	- *Description:* From the given normal distribution, use thresholds to get the bad electrode indices and **return them**