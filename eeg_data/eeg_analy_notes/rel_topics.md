## Currently relevant info from Mike's Notes
#### On 9/16/2016- Nitin

I'm only putting the names of the topics, because they're already in note form in Mike's notes, just need to know what to search and keep in mind while doing the frequency analyses for this week.

### [Mike's notes](http://upward-spiral-science.github.io/orange-panda/AnalyzingNeuralTimeSeriesData_Week02.pdf)


#### Time Domain:
- 2.3 Interpreting Voltage Values from the EEG Signal
    - Look for general patterns, not specific voltage

#### Frequency:
- Lose temporal precision in transformation to frequency domain
- Brain rhythms (frequency bands)
	- Delta (2-4Hz)
	- Theta (4-8Hz)
	- Alpha (8-12Hz)
	- Beta (15-30Hz)
	- Lower Gamma (30-80Hz)
	- Upper Gamma (80-150Hz)
	- Subdelta (<600Hz)
- Ways of viewing (search 3.2 Ways to View Time-Frequency Results)
- 3.5 Things to Be Suspicious of When Viewing Time-Frequency
Results

### Preprocessing:
- 7.3 Creating Epochs
- 7.5 Filtering
	- 50 Hz or 60 Hz: electrical line noise
	- High pass filters only apply on the whole dataset before making epochs so that smaller artifacts with delayed effects don't damage results

### Noise Artifacts
- 8.2 can use eyetracking events to filter data (remove saccades, blinks and all)
