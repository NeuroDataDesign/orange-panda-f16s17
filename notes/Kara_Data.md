## Notes from Kara meeting 2/3/2017

### Experiment:
- 2 dots appeared on screen, drew imaginary line in head. New dot appeared, had to decide if the dot lay on line
- 2 dots appear on screen, must remember something about the dots (ie what color was higher on screen)
- Each trial approx 6 seconds
- Fixation target appeared in center of screen between trials approx. 1 second
- 512 trials per patient
- approx. 75-80 patients total
- 47 channels!

### Bad trials:
- High noise (muscle movement)
- Eye movement (trials removed rather than filtered, as indicates failure as they didn't follow instructions to keep eyes centered on screen)
- Failing task (ie getting question wrong)

### Preprocessing Pipeline (uses Fieldtrip, MATLAB Preprocessing Toolbox):
1. Read data -> ALL.mat
2. High- and Low-Pass Filter: .2 - 35 Hz
3. Look for bad electodes- Go through each trial **MANUALLY** to see consistent poor data across trials (ie ridiculous noise or really small data recognition amongst others. Looks different)
4. ICA for blinking artifact filtering -> companalysis.mat
	1. Plot the components
	2. Identify blinks and remove it (usually first component)
	3. Again **manual** decision making of component to remove
5. Visually inspect each trial for eye movement and gross muscle movement
	1. Eye electrodes only inspected
	2. Look for square waves for lateral eye movement or high freq. high amplitude spikes for muscle movement
	3. **Remove entire trial**
	4. **Manual inspection**
6. Look at all electrodes **manually** for random spikes indicating other movement (remove trials) -> data_clean.mat
7. Sort trials