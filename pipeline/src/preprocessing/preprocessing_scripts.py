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

def prep_data(file_path, token):
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

  f_name, ext = os.path.splitext(file_path)
  if token == "pickled_pandas":
    return '<h1> No preprocessing was done. </h1>'
  if token == "fcp_indi_eeg":
    return eeg_prep(f_name, ext)


def eeg_prep(f_name, ext):
  html = ''
  d = make_h5py_object(f_name + ext)
  html += "<h1> Preprocessing Report for " + os.path.basename(f_name) + "</h1>"
  # Wrap this patient's data.
  D = [d]
  # Clean the data
  clean_data, clean_report = clean(D)
  html += clean_report
  eeg_data, times, coords = clean_data
  # simulate a time / channes / trials / patients data frame
  eeg_data = eeg_data.reshape(eeg_data.shape[0], eeg_data.shape[1],
                              1, eeg_data.shape[2])
  eeg_data, bad_chans, bad_report = bad_chan_detect(eeg_data,
                                          "KDE",
                                          threshold=2,
                                          times = times,
                                          ds = 1000)
  html += bad_report
  pool = 10 # How many electrodes to interp against?
  eeg_data, int_report = interpolate(eeg_data,
                                    'Inv_GC',
                                    bad_chans,
                                    times=times,
                                    coords = coords,
                                    npts = pool)
  html += int_report
  eeg_data, red_report = reduce_noise(eeg_data, 'placeholder')
  html += red_report
  eeg_data, eye_report = eye_artifact(eeg_data,
                                      'ICA',
                                      times=times,
                                      ds=1000,
                                      n_rm = 5)
  html += eye_report
  d = eeg_data[:, :, -1]
  t = times[:, :, -1]
  cct = [pd.DataFrame(data=d[:, x]) for x in range(d.shape[1])]
  df = pd.concat(cct, axis=1)
  df.columns = [str(x) for x in range(d.shape[1])]
  df.index = map(lambda x: x[0]/1000.0, t)
  with open(f_name + '.pkl', 'wb') as f:
    pickle.dump(df, f)
  return html

def clean(D):
  print 'cleaning data'
  # Extract for each patient
  C = []
  for d in D:
      tmp = {}
      tmp["eeg"] = get_eeg_data(d)
      tmp["times"] = get_times(d)
      tmp["coords"] = get_electrode_coords(d, 'spherical')
      C.append(tmp)

  # Go from python base list to numpy ndarray
  eeg_data = np.dstack(subject["eeg"] for subject in C)
  times = np.dstack(subject["times"] for subject in C)
  electrodes = np.dstack(subject["coords"] for subject in C)

  # Make sure the dimensions make sense
  assert eeg_data.ndim == 3
  assert times.ndim == 3
  assert electrodes.ndim == 3

  # During first 5 seconds electrode is 'reving' up.
  eeg_data = eeg_data[2500:]
  times = times[2500:]

  # Create a report for the cleaning procedure
  out = ''
  out += "<h3>CLEANING DATA</h3>"
  out += "<ul>"
  out += "<li>Extracted EEG data with " + str(eeg_data.shape[1]) + \
          " channels and " + str(eeg_data.shape[0]) + \
          " observations.</li>"
  out += "<li>Extracted timing data with " + str(times.shape[0]) + \
          " timesteps.</li>"
  out += "<li>Extracted electrode coordinate data.</li>"
  out += "<li>Removed first 5 seconds of data.</li>"
  out += "</ul>"

  return (eeg_data, times, electrodes), out
