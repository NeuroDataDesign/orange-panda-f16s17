from math import radians, cos, sin, asin, sqrt
import pywt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import copy
from viz import cross_compare

def haversine(rad, lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    if r == 'degrees':
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    return c

def gc(coords, i, j, r):
    t = coords[i][0]
    t_ = coords[j][0]
    p = coords[i][1]
    p_ = coords[j][1]
    args = {'rad' : r, 'lon1' : t,
      'lat1' : p, 'lon2' : t_, 'lat2': p_}
    return haversine(**args)

def neighbors(chan, chan_locs, candidates, k, r):
    dist = np.array(map(lambda c: gc(chan_locs, chan, c, r), candidates))
    closest = candidates[np.argsort(dist)[:k]]
    dist = dist[np.argsort(dist)[:k]]
    tot = np.sum(dist)
    return dist, closest, tot

def wavelet_coefficient_interp(d, p_local, p_global):
    C = d.shape[0]
    T = d.shape[1]
    bad_chans = p_local['bad_chans']
    chan_locs = p_global['chan_locs']
    wave = p_global['wave']
    r = p_global['loc_unit']
    v = p_global['verbose']
    k = p_global['k']

    # Transform to wavelet coefficients
    coefs = [pywt.wavedec(d[c, :], wave) for c in range(C)]
    orig_coefs = copy.deepcopy(coefs)
    candidates = np.setdiff1d(range(C), bad_chans)
    for bc in bad_chans:
        dist, neigh, tot = neighbors(bc, chan_locs, candidates, k)
        num_levels = len(coefs[bc])
        if v:
            print 'bad chan =', bc, ',', 'closest =', neigh, ',',
            print 'distances =', dist, 'num levels =', num_levels
        for i in range(num_levels)[1:]:
            coefs[bc][i] = np.sum([coefs[n][i] * dist[p]/tot for p, n in enumerate(neigh)], axis=0)
    d_int = np.vstack([pywt.waverec(c, wave) for c in coefs])

    # Plotting
    if v:
        timesteps = np.arange(T)* 1./500
        for c in bad_chans:
            _, neigh, _ = neighbors(c, chan_locs, np.setdiff1d(np.arange(C), bad_chans), k)
            # Plot the original bad electrode
            plt.plot(timesteps, d[c, :], color='blue',
                     linewidth = 1, label = 'bad ' + str(c))

            # Plot electrodes we interpolate against
            for n in neigh:
                plt.plot(timesteps, d_int[n, :], color='red',
                         linewidth = 1, label = 'neigh ' + str(n))

            # Plot the interpolated electrode
            plt.plot(timesteps, d_int[c, :], color='green',
                     linewidth = 1, label = 'interp')
            plt.legend()
            plt.show()
    for i in range(5):#range(len(coefs[0]))[1:]:
        cross_compare([orig_coefs[c] for c in bad_chans],
                      [coefs[c] for c in bad_chans], i)
    return d_int