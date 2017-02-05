"""Contains basic signal processing utilities.

"""
from utils.fourier import butter_highpass_filter, butter_lowpass_filter, butter_bandstop_filter
from sklearn.decomposition import FastICA, PCA
import numpy as np
import pandas as pd
from utils.plots import plotly_hack, sparklines, correlation
import preprocessing.prep_plots as plt
import preprocessing.messages as messages
import statsmodels
from statsmodels import robust
from sklearn.covariance import EmpiricalCovariance, MinCovDet

## Definition of a Gaussian
def gaussian(x, mu, sig):
  return 1./(math.sqrt(2.*math.pi)*sig)*np.exp(-np.power((x - mu)/sig, 2.)/2)

## Removing Outliers Using the Median Absolute Deviation 
def remove_outliers(data):
  filtered = []
  m = 3
  u = np.median(data)
  s = robust.mad(data, c = 1, axis = 0 )
  #print ("The Median of the Data and the Median Absolute Deviant, Respectively")
  #print u
  #print s
  #print "\n"
  for e in range(data.shape[0]):
    if u-3*s < data[e] < u+3*s:
      filtered.append(data[e])
    else:
      filtered.append(np.nan)
  return filtered

## Returning a 2-D Array given a 4-D Array
def dimension_reduction(eegdata, c, d):
  temp = eegdata[:,:,c,d]
  return temp

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
  if A['red_noise']['method'] == 'rpca':
    T = rpca(T, A)    
  T['meta']['red_noise_method'] = A['red_noise']['method']
  T['report']['red_noise_message'] = messages.red_noise(T['meta'])
  return T

def rpca(T, A):
  new_data = []
  eeg_data = T['eeg'][::A['red_noise']['ds']]
  for c in range(T['meta']['n_chans']):
    if new_data == []:
      temp = remove_outliers(eeg_data[:, c])
      new_data = temp
    else:
      temp = remove_outliers(eeg_data[:, c])
      new_data = np.vstack((new_data, temp))
  maskedarr = np.ma.array(new_data, mask=np.isnan(new_data))
  cov_mat = np.ma.cov(maskedarr,rowvar=False,allow_masked=True)

  eig_val_cov, eig_vec_cov = np.linalg.eig(cov_mat)
  for i in range(len(eig_val_cov)):
    eigvec_cov = eig_vec_cov[:,i].reshape(1, eeg_data.shape[1]).T
  eig_pairs = [(np.abs(eig_val_cov[i]), eig_vec_cov[:,i]) for i in range(len(eig_val_cov))]
  eig_pairs.sort(key=lambda x: x[0], reverse=True)

  array = []
  for x in range(T['n_obs']):
    array.append(eig_pairs[x][0])
  array2 = [x * 1000 for x in array] 

  p1 = len(array2)
  totalSum = [0]*(p1-1)

  for q in range(1,p1):
    FirstArray, SecondArray = np.split(array2, [q,])
    mu1 = np.mean(FirstArray)
    mu2 = np.mean(SecondArray)
    s1 = np.var(FirstArray)
    s2 = np.var(SecondArray)
    if q-1 == 0:
      s1 = 0
    totalvariance = (((q-1)*(s1*s1)) + ((p1-q-1)*(s2*s2))) / (p1-2)
    Sum1 = 0
    Sum2 = 0
    for i in range(len(FirstArray)):
      x = FirstArray[i]
      x1 = np.log10(gaussian(x, mu1, totalvariance))
      Sum1 += x1
    for j in range(len(SecondArray)):
      y = SecondArray[j]
      y1 = np.log10(gaussian(y, mu2, totalvariance))
      Sum2 += y1
    totalSum[q-1] = Sum1 + Sum2
  dimension = np.argmax(totalSum) + 1
  matrix_w = eig_pairs[0][1].reshape(eeg_data.shape[1],1)
  for x in range(0, dimension-1):
    matrix_w = np.hstack((matrix_w, eig_pairs[x][1].reshape(eeg_data.shape[1], 1)))
  T['eeg'] = matrix_w.T.dot(T['eeg'])
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