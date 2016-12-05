# Description of the data format used by the EEG PANDA Pipeline.

Data input into and used within the EEG PANDA pipeline strictly follows the following format.

Suppose you conduct an experiment with P patients by running each patient p_i through t_i trials.
The data from the entire experiment will be held within one [pickled](https://docs.python.org/3/library/pickle.html) Python dictionary as follows:

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


If you have data in this format, the correct formatting token is `eeg_panda_token`.
If you have data in another format you can convert it using Python scripts or, [drop us an issue](https://github.com/NeuroDataDesign/orange-panda/issues) with a detailed description of the file or a link to an example and we can make a script and token pair for you.

Currently supported formatting tokens:
* `eeg_panda_format` - the standard pickled Python dictionary format detailed above.
* `fcp_indi_eeg` - an file from the 'fcp_indi' bucket. (TODO: what is the name of this data-set?)

An example of pickled files of this format can be found on our aws bucket. Bucket name is `neurodatadesign-test`.
The file name for data in the `eeg_panda_format` format is `eeg_data.pkl`.
The file name for data in the `fcp_indi_eeg` format is `test.mat`.

These values are defaulted in the current web service load-out.
