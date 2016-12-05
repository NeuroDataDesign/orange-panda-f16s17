"""Contains basic signal processing utilities.

"""
import numpy as np
import pandas as pd
from scipy.stats import kurtosis
from sklearn.neighbors.kde import KernelDensity
from sklearn.grid_search import GridSearchCV
import preprocessing.prep_plots as plt
import preprocessing.messages as messages

def bad_chan_detect(T, A):
  r"""Takes the data and applies the proper bad channel detection method.

  Wrapper for bad channel detection methods, so there is one unified way to call them all.

  Parameters
  ----------
  eeg_data : ndarray
    (n,c,t,p) dimensional array, n = number of timesteps, c = number of channels
    t = number of trials, p = number of patients.
  method : string
    string corresponding to which bad channel detection method to be used.
    Available methods are in the 'notes' section of this docstring.
  times : ndarray
    A (n x 1) array of the time values of each index of `eeg_data`. For
    example, `[.002, .004, ...]` for eeg data sampled at 500Hz.
  coords : ndarray
    (c, 3, p) array of the coordinates of the c electrodes. Measured spherical
    coordinates rather than cartesian. (:math:`theta`, :math:`rho`, r) rather than
    (x,y,z).
  rm_zero : boolean
    True if identically zero (zero on every timestep) electrodes should be
    removed before bad electrode detection functions are run.
  **kwargs : dictionary
    Additional arguments specific to the bad electrode detection method used.

  Returns
  -------
  eeg_data : ndarray
    The eeg_data variable that was input with some changes.
    This can differ, for example, if you chose to remove the zeroed out electrodes.
  bad_chan_list : list of list of lists
    Top level list is per patient, 2nd level list is per trial, and 3rd
    level list contains bad electrodes.
    For example, bad_chan_list[3][4] contains the bad electrodes for
    patient 4 on trial 5. (0-indexed arrays).
  coords : ndarray
    The coordinate array which was input, minus any bad channels which were
    detected and removed.
  out : string
    HTML string detailing a report of the bad channel detection process.

  See Also
  --------
  prob_baddetec, kurt_baddetec, spec_baddetec

  Notes
  -----
  methods available:
  .. 'prob' for probability denity based on KDE
  .. 'kurt' for kurtosis based
  .. 'pow' for power spectrum based

  """
  if A['bad_detec']['rm_zero']:
    T['meta']['rm_zero'] = True
    T = detect_zeroed_chans(T)
    ind = np.setdiff1d(np.arange(T['meta']['n_chans']), T['meta']['zeroed_chans'])
    T['eeg'] = T['eeg'][:, ind] 
    T['coords'] = T['coords'][ind, :]
    T['meta']['n_chans'] = T['meta']['n_chans'] - T['meta']['n_zeroed_chans']
    T['report']['zeroed_message'] = messages.zeroed_electrodes(T["meta"])
    T['report']['zeroed_plot'] = plt.zeroed(T)
  if A['bad_detec']['method'] == 'prob':
    T['meta']['bad_chans'] = prob_baddetec(T['eeg'][::A['bad_detec']['ds']],
                                  A['bad_detec']['threshold_1'], kdewrap)
  elif A['bad_detec']['method'] == 'kurt':
    T['meta']['bad_chans'] = kurt_baddetec(T['eeg'][::A['bad_detec']['ds']],
                                  A['bad_detec']['threshold_1'])
  elif method == 'pow':
    T['meta']['bad_chans'] = spec_baddetec(T['eeg'][::A['bad_detec']['ds']],
                                  A['bad_detec']['threshold_1'],
                                  A['bad_detec']['threshold_2'])
  T['meta']['rm_zero'] = A['bad_detec']['rm_zero']
  T['meta']['bad_detec_method'] = A['bad_detec']['method']
  T['meta']['n_bad_chans'] = len(T['meta']['bad_chans'])
  T['report']['bad_chans_message'] = messages.bad_detec(T["meta"])
  T['report']['bad_chans_plot'] = plt.bad_electrodes(T)
  return T



def reshape(inEEG):
  r"""Reshape the data from the inputted format (timesteps, num channels, num patients) to (time, channels).

  Parameters
  ----------
  inEEG : array_like (3d or 2d)
    Paradigm data characterized by: (timesteps, num channels, num patients). If data previously transformed into (time, channels), also accept and don't alter.

  Returns
  -------
  inEEG: array_like(2d)
    (time, channels)

  Raises
  ------
  DimensionException
    Input is not 2d or 3d, not interpretable

  Examples
  --------
  These are written in doctest format, and should illustrate how to
  use the function.

  First with a 2D array input (preformatted)
  >>> success1 = np.column_stack([sin] * 50)
  >>> print success1.shape
  (1000L, 50L)
  >>> reshaped = reshape(success1).shape
  >>> print reshaped.shape
  (1000L, 50L)
  
  Now with 3D input (2 patients)
  >>> dummy = np.dstack([success1] * 2)
  >>> print dummy.shape
  (1000L, 50L, 2L)
  >>> reshaped = reshape(dummy).shape
  >>> print reshaped.shape
  (2000L, 50L)

  """
  if len(inEEG.shape) == 3:
    electrodes = inEEG.shape[1]
    times = inEEG.shape[0]
    trials = inEEG.shape[2]
    return np.reshape(inEEG, (inEEG.shape[0] * inEEG.shape[2], inEEG.shape[1]))
  elif len(inEEG.shape) != 1 and len(inEEG.shape) != 2:
    # fail case
    print "fail"
  else:
    return inEEG


def kdewrap(indata, kernel):
  r"""A wrapper for the KDE implementation from the scikit-learn package.

  Kernel density estimates are a method of estimating the distribution of a dataset non-parametrically.
  Basically, without any outside parameters bounding the data, we generate a distribution representing the data from a base kernel function.
  For each point, the base kernel function is generated, and the kernel is altered based on the distance between each individual point and every other point.
  Combining these kernels creates a fairly accurate density function of the data.

  Parameters
  ----------
  indata : list (data points per timestep)
    For a given electrode, a list of all the values for each timestamp
  kernel : string
    'gaussian', 'tophat', 'epanechnikov', 'exponential', 'linear', 'cosine' Choose which base kernel function to use.

  Returns
  -------
  kde.score_samples(indata[:, np.newaxis]): arraylike (timesteps, 1)
    Return an array of the densities for each electrode value and where it lies in the kernel function

  Notes
  -----
  For notes and refernces go to: https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/bad_chan_detect/baddetec/kernel-probability-density.pdf

  Examples
  --------
  These are written in doctest format, and should illustrate how to
  use the function.

  >>> inEEG = [0.2, 0.5, 3.6, 2.2, ...]
  >>> probdist = kdewrap(inEEG, 'gaussian')
  probdist = [...]

  """
  grid = GridSearchCV(KernelDensity(),
          {'bandwidth': np.linspace(0.1, 1.0, 30)},
          cv=2) # 20-fold cross-validation
  grid.fit(indata[:, None])
  kde = KernelDensity(kernel=kernel, bandwidth=grid.best_params_["bandwidth"]).fit(indata[:, np.newaxis])
  return kde.score_samples(indata[:, np.newaxis])

def prob_baddetec(inEEG, threshold, probfunc):
  r"""Detect bad electrodes based on probability

  Based on whether the joint probability of an electrode's time values (decided by a probability function passed in
  via the parameters) is too different from the other electrodes.

  Parameters
  ----------
  inEEG : numpy array (timesteps, channels, patients)
    For a given electrode, a list of all the values for each timestamp
  threshold : integer
    The number of standard deviations away from the mean joint probability counts an electrode's probability can be
    for it to count as a bad electrode
  probfunc : function. In this case takes in data and kernel as arguments
    function to make probability distribution

  Returns
  -------
  inEEG : original data
    Return original data because isn't changed
  o : string
    output string for basic comprehension of output
  badelec: list
    List of bad electrodes from list

  Notes
  -----
  Pseudocode located at: https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/bad_chan_detect/baddetec/bad-electrode-detection.pdf

  """
  electrodes = inEEG.shape[1]
  
  # Start by reshaping data (if necessary)
  inEEG = reshape(inEEG)
  
  # Then, initialize a probability vector of electrode length
  probvec = np.zeros(electrodes)
  
  # iterate through electrodes and get joint probs
  for i in range(0, electrodes):
    # get prob distribution
    probdist = probfunc(inEEG[:, i], 'gaussian')
    # using probdist find joint prob
    probvec[i] = np.sum(probdist) 
  
  # normalize probvec
  # first calc mean
  avg = np.mean(probvec)
  # then st, d dev
  stddev = np.std(probvec)
  # then figure out which electrodes are bad
  badelec = []
  #print probvec
  for i in range(0, len(probvec)):
    #print i, avg, stddev, (avg - probvec[i]) / stddev
    if np.abs((avg - probvec[i]) / stddev) >= threshold:
      badelec.append(i)
      
  return badelec

def kurt_baddetec(inEEG, threshold):
  r"""Detect bad electrodes based on kurtosis

  Based on the kurtosis of EEG voltage over time, find channels which have produced large outliers.

  Parameters
  ----------
  inEEG : numpy array (timesteps, channels, patients)
    For a given electrode, a list of all the values for each timestamp
  threshold : integer
    The number of standard deviations away from the mean joint probability counts an electrode's probability can be
    for it to count as a bad electrode

  Returns
  -------
  inEEG : original data
    Return original data because isn't changed
  o : string
    output string for basic comprehension of output
  badelec: list
    List of bad electrodes from list

  Notes
  -----
  Pseudocode located at: https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/bad_chan_detect/baddetec/bad-electrode-detection.pdf

  """
  electrodes = inEEG.shape[1]
  
  # Start by reshaping data (if necessary)
  inEEG = reshape(inEEG)
  
  # Then, initialize a probability vector of electrode length
  kurtvec = np.zeros(electrodes)
  
  # iterate through electrodes and get kurtoses
  for i in range(0, electrodes):
    # add kurtosis to the vector
    kurtvec[i] = kurtosis(inEEG[:, i])        
  
  # normalize kurtvec
  # first calc mean
  avg = np.mean(kurtvec)
  # then std dev
  stddev = np.std(kurtvec)
  # then figure out which electrodes are bad
  badelec = []
  #print probvec
  for i in range(0, len(kurtvec)):
    #print i, avg, stddev, (avg - kurtvec[i]) / stddev
    if np.abs((avg - kurtvec[i]) / stddev) >= threshold:
      badelec.append(i)
      
  return badelec

def spec_baddetec(inEEG, posthresh, negthresh):
  r"""Detect bad electrodes based on spectral analysis

  Based on the frequency spectrums 

  Parameters
  ----------
  inEEG : numpy array (timesteps, channels, patients)
    For a given electrode, a list of all the values for each timestamp
  posthresh : integer
    The amount above the mean average power spectrum an electrode's frequency can go
  negthresh : integer
    The amount below the mean average power spectrum an electrode's frequency can go

  Returns
  -------
  inEEG : original data
    Return original data because isn't changed
  o : string
    output string for basic comprehension of output
  badelec: list
    List of bad electrodes from list

  Notes
  -----
  Pseudocode located at: https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/bad_chan_detect/baddetec/bad-electrode-detection.pdf

  """
  electrodes = inEEG.shape[1]
  
  # Start by reshaping data (if necessary)
  inEEG = reshape(inEEG)
  
  # initialize badelec as an empty array
  badelec = []
  
  # iterate through electrodes and get spectral densities
  for i in range(0, electrodes):
    # get frequency spectrum for electrode
    sp = np.fft.fft(inEEG[:, i]).real
    sp = sp - np.mean(sp)
    for power in sp:
      if power > posthresh or power < negthresh:
        badelec.append(i)
        break
    
  return badelec

def good_elec(inEEG, badelec):
  r"""Detect bad electrodes based on probability

  Based on whether the joint probability of an electrode's time values (decided by a probability function passed in
  via the parameters) is too different from the other electrodes.

  Parameters
  ----------
  inEEG : numpy array (timesteps, channels, patients)
    For a given electrode, a list of all the values for each timestamp
  badelec : list
    List of all bad electrode indices in inEEG

  Returns
  -------
  newEEG: array (timesteps, good channels, patients)
    delete all bad electrode columns for the EEG data

  """
  return np.delete(inEEG, badelec, 1)

def detect_zeroed_chans(T):
  out = ''
  T['meta']['zeroed_chans'] = []
  for i in range(T['meta']['n_chans']):
    if sum(T['eeg'][:, i]**2) == 0:
      T['meta']['zeroed_chans'].append(i)
  T['meta']['n_zeroed_chans'] = len(T['meta']['zeroed_chans'])
  return T
