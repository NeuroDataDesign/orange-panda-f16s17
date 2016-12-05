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
    prep_args_web : dict
      A dictionary of arguments from user input into the 'get data' form on
      the webservice. This will include a token, a file name, a file path, and a
      s3 bucket name.

    prep_args_loc : dict
      A dictionary of arguments to the pipeline preprocessing. These are the
      hard-coded options of the pipeline which we have determined to produce the 
      best results.

    Returns
    -------
    html
      A HTML report for what happened during preprocessing.

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
    d = make_h5py_object(f_name + ext)
    # Wrap this patient (patient 0, trial 0).
    D = []
    P = []
    T1 = {'raw': d}
    P.append(T1)
    D.append(P)
    D = apply_over(D, clean, prep_args_loc)
    D = eeg_prep(D, prep_args_loc)
    with open(f_name + '.pkl', 'wb') as f:
      pickle.dump(D, f)
    return D[0][0]['report']['full_report']
  if prep_args_web['token'] == "eeg_panda_format":
    D = pickle.load(open(f_name + ext))
    D = apply_over(D, set_meta, prep_args_loc)
    D = eeg_prep(D, prep_args_loc)
    with open(f_name + '.pkl', 'wb') as f:
      pickle.dump(D, f)
    return D[0][0]['report']['full_report']

def eeg_prep(D, A):
  D = apply_over(D, bad_chan_detect, A)
  D = apply_over(D, interpolate, A)
  D = apply_over(D, reduce_noise, A)
  D = apply_over(D, eye_artifact, A)
  D = apply_over(D, html_out, A)
  return D

def clean(T, A):
  r"""Cleans data examples from the Nicolas' data set.

  This is for demo purposes only, when we have more example
  formats this will be abstracted to a tokenized function.

  Parameters
  ----------
  D : dictionary of the PANDA data format.
    A dictionary conforming to the PANDA data format.

  prep_args_loc : dict
    A dictionary of arguments to the pipeline preprocessing. These are the
    hard-coded options of the pipeline which we have determined to produce the 
    best results.

  Returns
  -------
  html
    A HTML report for what happened during preprocessing.

  Notes
  -----
  Supported tokens:

  fcp_indi_eeg - token for EEG data from the fcp.

  pickled_pandas - token for a pickled pandas object, no pre-processing is done, only analysis.

  """
  # Extract for each patient
  T["eeg"] = get_eeg_data(T["raw"])
  T["times"] = get_times(T["raw"])
  T["coords"] = get_electrode_coords(T["raw"], 'spherical')
  T = set_meta(T, A)
  T.pop("raw") 
  return T

def set_meta(T, A):
  T["meta"] = {
    'n_chans' : T["eeg"].shape[1],
    'n_obs' : T["times"].shape[0],
    'freq_times' : 500,
    'freq_unit' : 'second',
    'coord_unit' : 'spherical'
  }
  T["report"] = {}
  T["report"]["clean_message"] = messages.clean(T["meta"])
  return T

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
