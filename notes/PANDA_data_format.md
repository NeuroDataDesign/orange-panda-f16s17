# Description of the data format used by the EEG PANDA Pipeline.

Data input into and used within the EEG PANDA pipeline strictly follows the following format.

Suppose you conduct an experiment with P patients by running each patient p_i through t_i trials.
The data from the entire experiment will be held within one Python dictionary as follows:

```
E = {
  ...
  p_i = {
    ...
    t_i = {
      'eeg' = a (n, c) ndarray of the eeg voltage values.
      'times' = a (n, 1) ndarray of the observation timesteps.
      'coords' = a (c, 3) ndarray of the electrode positions in space (in spherical coordinates).
      'meta' = {
        ...
        various metadata to be set within the pipeline, or included for experimenter use
        ...
      }
      'report' = {
        ...
        various reports about pipeline results to be generated within the pipeline
        ...
      }
      }
    ...
  }
  ...
}
```
where:
* n = the number of observations (e.g. 1 sample per second over a minute, n would be 60).
* c = the number of channels.
