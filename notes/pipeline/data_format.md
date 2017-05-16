# Input Data Format
Data input into this pipeline should be in a [BIDS](http://bids.neuroimaging.io/)-like data format.
Specifically, the format should be as follows:

```
bids_raw/
├── chan_locs.pkl
├── participants.tsv
└── sub-0001
    ├── ses-01
    │   └── eeg
    │       └── sub-0001_ses-01.pkl
    ├── ses-02
    │   └── eeg
    │       └── sub-0001_ses-02.pkl
    └── ses-3
        └── eeg
            └── sub-0001_ses-3.pkl


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
