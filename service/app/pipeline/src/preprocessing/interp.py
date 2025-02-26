"""Contains methods to interpolate voltages of electrode channels.

"""
import numpy as np
from math import radians, cos, sin, asin, sqrt
import pandas as pd
from utils.plots import plotly_hack, sparklines
import preprocessing.prep_plots as plt
import preprocessing.messages as messages


def interpolate(T, A):
  r"""Interpolate bad electrodes based on spectral analysis

  Will interpolate channels listed in T['meta']['bad_chans']
  
  Parameters
  ----------
  T : eeg_panda_format dictionary (https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/PANDA_data_format.md)
  A : global arguments set in config.txt

  Returns
  -------
  T : eeg_panda_format dictionary (https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/PANDA_data_format.md)
    Returns data with metadata added and bad channels interpolated.

  See Also
  --------
  fit_sphere, haversine, gc_invdist_interp

  Notes
  -----
  methods available:
  .. 'Inv_GC' inverse distance weighting based on great circle distance.

  """
  if A['interp']['method'] == 'Inv_GC':
    r = fit_sphere(T['coords'][:, 2])
    T['meta']['interp_npts'] = A['interp']['npts']
    eeg_data_interped, close = gc_invdist_interp(
                                T['eeg'],
                                T['meta']['bad_chans'],
                                T['coords'],
                                r,
                                A['interp']['npts'])
    T['eeg'] = eeg_data_interped
    T['meta']['interp_close'] = close
    T['report']['interp_plot'] = plt.interp_electrodes(T)
  T['meta']['interp_method'] = A['interp']['method']
  T['report']['interp_message'] = messages.interp(T["meta"])
  T['report']['interp_plot'] = plt.interp_electrodes(T)
  return T

def fit_sphere(r_values):
  r"""Find the radius of a sphere that best fits a set of 3-d points, given their distance from the origin.

  Parameters
  ----------
  r_values : float
      distance from each point to the origin (radius).

  Returns
  -------
  rad : float
      the best radius

  See Also
  --------
  gc : uses the haversine formula

  Notes
  -----
  Fit is based on minimizing `r` for the sum of the square distances from each point to a sphere of radius `r`.

  """
  H = np.linspace(0, 1000, 10000)
  def E(h):
    return np.sum(np.square(np.subtract(r_values, h)))
  Es = map(E, H)
  return H[np.argmin(Es)]


def haversine(rad, lon1, lat1, lon2, lat2):
  r"""Calculate the great circle distance between two points on a sphere of given radius.

  Parameters
  ----------
  rad : float
    the radius of the sphere

  lon1 : float
    the longitude of the first point

  lat1 : float
    the latitude of the first point

  lon2 : float
    the longitude of the second point

  lat2 : float
    the latitude of the second point

  Returns
  -------
  dist : float
    the great circle distance between :math:`p_1` and :math:`p_2`

  See Also
  --------
  gc : uses the haversine formula

  Notes
  -----
  :math:`\operatorname{hav}\left(\frac{d}{r}\right) = \operatorname{hav}(\varphi_2 - \varphi_1) + \cos(\varphi_1) \cos(\varphi_2)\operatorname{hav}(\lambda_2-\lambda_1)`

  * :math:`\varphi_i` is the latitude of point `i`.
  * :math:`\lambda_i` is the longitude of point `i`.
  * :math:`r` is the radius of a sphere

  And even use a greek symbol like :math:`omega` inline.

  References
  ----------

  [1] https://en.wikipedia.org/wiki/Haversine_formula

  """
  # convert decimal degrees to radians 
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

  # haversine formula 
  dlon = lon2 - lon1 
  dlat = lat2 - lat1 
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a)) 
  return c * rad

def gc(coords, i, j, r):
  r"""Given a list of coordinates on a sphere, return the great circle distance between any two of them..


  Parameters
  ----------
  coords : ``ndarray``
      a `(N, 3)` ``ndarray`` with `N` coordinates (3 values per coordinate for :math:`\varphi, \lambda, r`).

  i : int
      index of the first used coordinate from the `coords` list

  j : int
      index of the second used coordinate from the `coords` list

  r : float
      the radius of the sphere we are finding the great circle distance of.


  Returns
  -------
  dist : float
      the great circle distance between :math:`p_1` and :math:`p_2`

  See Also
  --------
  haversine : how the distance is calculated

  Notes
  -----
  :math:`\operatorname{hav}\left(\frac{d}{r}\right) = \operatorname{hav}(\varphi_2 - \varphi_1) + \cos(\varphi_1) \cos(\varphi_2)\operatorname{hav}(\lambda_2-\lambda_1)`

  * :math:`\varphi_i` is the latitude of point `i`.
  * :math:`\lambda_i` is the longitude of point `i`.
  * :math:`r` is the radius of a sphere

  """
  t = coords[i][0]
  t_ = coords[j][0]
  p = coords[i][1]
  p_ = coords[j][1]
  args = {'rad' : r, 'lon1' : t,
    'lat1' : p, 'lon2' : t_, 'lat2': p_}
  return haversine(**args)


def gc_invdist_interp(data, bad_electrodes, coords, r, numpts = 5):
  #all_indicies = np.array(range(coords.shape[0]))
  #bad_indicies = np.array(bad_electrodes)
  #indicies = np.setdiff1d(all_indicies, bad_indicies)
  #coords = coords[indicies]
  closest = []
  for ind in bad_electrodes:
    gcord = coords[ind]
    t, p, _ = gcord
    ds = np.zeros([coords.shape[0]])
    for c in range(coords.shape[0]):
      if c in bad_electrodes:
        ds[c] = float('Inf')
      else:
        ds[c] = haversine(r, t, coords[c][0],
                    p, coords[c][1])
    inds = np.argsort(ds)[1: numpts + 1]
    w = 1 / ds[inds]
    weighted = np.multiply(data[:, inds], w)
    predicted = np.sum(weighted, axis = 1) / sum(w)
    data[:, ind] = predicted
    closest.append(inds)
  return data, closest

