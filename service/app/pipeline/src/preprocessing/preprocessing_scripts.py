"""Contains basic signal processing utilities.

"""
import os
import pickle
from utils.clean_data import (get_eeg_data,
                              get_times,
                              get_electrode_coords)
from preprocessing.interp import interpolate
from preprocessing.baddetec import bad_chan_detect
from preprocessing.noise_reduct import reduce_noise, eye_artifact
from utils.get_data import make_h5py_object
import pandas as pd
import numpy as np
import preprocessing.messages as messages
from utils.misc import apply_over

def prep_data(prep_args_web, prep_args_loc):
  r"""Router for tokenized pre-processing scripts.

    Takes a preprocessing token and applies the correct script.

    Parameters
    ----------
    file_path : str
      A path to the file you are pre-processing.
    token : str
      Token for your corresponding pre-processing script.

    Returns
    -------
    html
      A report for what happened during preprocessing.

    Notes
    -----
    Supported tokens:

    fcp_indi_eeg - token for EEG data from the fcp.

    pickled_pandas - token for a pickled pandas object, no pre-processing is done, only analysis.

    """

  f_name, ext = os.path.splitext(prep_args_web['data_path'])
  if prep_args_web['token'] == "pickled_pandas":
    return '<h1> No preprocessing was done. </h1>'
  if prep_args_web['token'] == "fcp_indi_eeg":
    return eeg_prep(f_name, ext, prep_args_web, prep_args_loc)


def eeg_prep(f_name, ext, prep_args_web, prep_args_loc):
  A = prep_args_loc
  d = make_h5py_object(f_name + ext)
  # Wrap this patient (patient 0, trial 0).
  D = []
  P = []
  T1 = {'raw': d}
  P.append(T1)
  D.append(P)
  # Clean the data
  D = clean(D)
  D = apply_over(D, bad_chan_detect, A)
  D = apply_over(D, interpolate, A)
  D = apply_over(D, reduce_noise, A)
  D = apply_over(D, eye_artifact, A)
  D = apply_over(D, html_out, A)
  with open(f_name + '.pkl', 'wb') as f:
    pickle.dump(D, f)
  return D[0][0]['report']['full_report']

def clean(D):
  print 'cleaning data'
  # Extract for each patient
  for P in D:
    for T in P:
      T["eeg"] = get_eeg_data(T["raw"])
      T["times"] = get_times(T["raw"])
      T["coords"] = get_electrode_coords(T["raw"], 'spherical')
      T["meta"] = {
        'n_chans' : T["eeg"].shape[1],
        'n_obs' : T["times"].shape[0],
        'freq_times' : 500,
        'freq_unit' : 'second',
        'coord_unit' : 'spherical'
      }
      T["report"] = {}
      T["report"]["clean_message"] = messages.clean(T["meta"])
      T.pop("raw") 
  print D
  return D

def html_out(T, A):
  html = "<h1> Preprocessing Report </h1>"
  html += T['report']['clean_message']
  html += T['report']['bad_chans_message']
  html += T['report']['bad_chans_plot']
  html += T['report']['interp_message']
  html += T['report']['interp_plot']
  html += T['report']['red_noise_message']
  html += T['report']['eye_artifact_message']
  T['report']['full_report'] = html
  return T
