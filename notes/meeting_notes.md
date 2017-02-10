
## Data Setting
We take two subjects from the original data set. Each scan is partitioned into 10 equal length time segments. Each of these segments is a 'trial'.

We compute discriminibility with the subject id as the label, 20 trials, and various metrics. Rather than computing discriminibility once on all 20 trials, we will 'leave one out' and compute discriminibility all 20 subsets of 19 trials, do get a pseudo-distribution.

### Raw Data
[image](plots/raw.png)

### Raw Data with Nitin's detected bad electrodes masked (set to 0) for each trial
[image](plots/nitin_mask.png)

### Raw Data with 'True' bad electrodes masked (set to 0) for all trials
[image](plots/true_mask.png)

### Discriminibility change when Nitin's bad electrodes are masked, with respect to unmasked Raw Data
[image](plots/raw_vs_nitin.png)

### Discriminibility change when 'True' bad electrodes are masked, with respect to unmasked Raw Data
[image](plots/raw_vs_true.png)

### Discriminibility change when Nitin's bad electrodes are masked, with respect to 'True' masked data
[image](plots/nitin_minus_true.png)
