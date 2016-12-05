"""Contains basic signal processing utilities.

"""
from utils.fourier import butter_highpass_filter, butter_lowpass_filter, butter_bandstop_filter
from sklearn.decomposition import FastICA, PCA
import numpy as np
import pandas as pd
from utils.plots import plotly_hack, sparklines, correlation
import preprocessing.prep_plots as plt
import preprocessing.messages as messages

def reduce_noise(T, A):
  r"""Reduce noise of the EEG data.

  Reduces noise based on method in the arguments.
  
  Parameters
  ----------
  T : eeg_panda_format dictionary (https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/PANDA_data_format.md)
  A : global arguments set in config.txt

  Returns
  -------
  T : eeg_panda_format dictionary (https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/PANDA_data_format.md)
    Returns the same data with noise reduced.

  Notes
  -----
  methods available:
  .. 'placeholder' - general band pass and high pass filtering.
  .. 'RPCA' - noise reduction with Robust PCA

  """
  if A['red_noise']['method'] == 'placeholder': # for Minimum Viable Product
        for c in range(T['meta']['n_chans']):
          T['eeg'][:, c] = butter_highpass_filter(T['eeg'][:, c], 0.1, 500)
          for k in range(60, 299, 60):
            T['eeg'][:, c] = butter_bandstop_filter(T['eeg'][:, c], [k-5,k+5], 500)
  T['meta']['red_noise_method'] = A['red_noise']['method']
  T['report']['red_noise_message'] = messages.red_noise(T['meta'])
  return T

def eye_artifact(T, A):
  r"""Detect eye artifacts.

  Detect and remove artifacts from the EEG data..
  
  Parameters
  ----------
  T : eeg_panda_format dictionary (https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/PANDA_data_format.md)
  A : global arguments set in config.txt

  Returns
  -------
  T : eeg_panda_format dictionary (https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/PANDA_data_format.md)
    Returns the same data with eye artifacts removed. (Not yet, will be implemented soon.)

  Notes
  -----
  methods available:
  .. 'ICA' - detect eye artifacts with FastICA.
  

  """

  if A['eye_artifact']['method'] == 'ICA':
    ica = FastICA()
    ica.fit(T['eeg'][::A['eye_artifact']['ds']])
    ica_ind_component = ica.transform(T['eeg'])
    components = ica.components_
  T['meta']['eye_artifact_method'] = A['eye_artifact']['method']
  T['report']['eye_artifact_message'] = messages.eye_artifact(T['meta'])
  return T