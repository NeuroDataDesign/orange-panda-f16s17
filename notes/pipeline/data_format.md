# Input Data Format
Data input into this pipeline should be in a [BIDS](http://bids.neuroimaging.io/)-like data format.
Specifically, the format should be as follows:

```
.
├── chan_locs.pkl
├── participants.tsv
├── sub-0001
│   └── eeg
│       ├── sub-0001_trial-01.pkl
│       ├── sub-0001_trial-02.pkl
│       └── sub-0001_trial-03.pkl
├── sub-0002
│   └── eeg
│       ├── sub-0002_trial-01.pkl
│       ├── sub-0002_trial-02.pkl
│       └── sub-0002_trial-03.pkl
└── sub-0003
    └── eeg
        ├── sub-0003_trial-01.pkl
        ├── sub-0003_trial-02.pkl
        └── sub-0003_trial-03.pkl


```

Each `sub-000X_trial-XX.pkl` should be a [pickled](https://docs.python.org/2/library/pickle.html) `C x T ndarray` where `C`
is the number of channels in the data while `T` is the number of observations (timesteps) in the data.

The `chan_locs.pkl` file should be a `C x 3 ndarray` of the cartesian coordinates of electrode positions.
Column 1 is the `X` coordinate, column 2 is the `Y` coordinate, and column 3 is the `Z` coordinate.
Row `i` corresponds to the position of electrode `i`.

Finally, `participants.tsv` should be a tab separated value file with two columns: the subject IDs and the number of trials for each. Explicitly, you should follow this example:
```
participant_id	num_trials
sub-0001	3
sub-0002	3
sub-0003	3
```
