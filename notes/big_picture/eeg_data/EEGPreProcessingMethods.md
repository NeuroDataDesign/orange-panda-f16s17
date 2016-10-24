## Preprocessing Methods Used
### 1. PREP pipeline
- remove line-noise "without committing a filtering strategy"
- reference signal relative to an estimate of the "true" average reference
- interpolate bad channels
- reversible by leaving evidence

-No mention of PCA, ICA, dimesnion reduction methods in order to remove bad channels

### 2. Makoto's Preprocessing Pipeline
- downsampling data - maybe from 500 Hz to 250 Hz
- high pass filter
- import labeling of the channel and use a standardized system
- remove bad channels (Nitin)
- interpolate removed channels (Ryan)
- re-reference data to average - net charge should be 0 by charge conservation, therefore the average reference makes the scalp topography have zero potential
- epoch data -> reject epochs for cleaning
- ICA (Mike)
 