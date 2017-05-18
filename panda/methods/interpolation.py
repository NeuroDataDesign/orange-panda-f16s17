from math import radians, cos, sin, asin, sqrt
import pywt
import numpy as np
import copy
from scipy.interpolate import SmoothSphereBivariateSpline

import math as m

def cart2sph(x,y,z):
    XsqPlusYsq = x**2 + y**2
    r = m.sqrt(XsqPlusYsq + z**2)               # r
    elev = m.atan2(z,m.sqrt(XsqPlusYsq)) + np.pi / 2     # theta
    az = m.atan2(y,x) + np.pi                           # phi
    return elev, az, r

def haversine(rad, lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    if rad == 'degrees':
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    return c

def gc(coords, i, j, r):
    t, p, r = cart2sph(coords[i][0], coords[i][1], coords[i][2])
    t_, p_, r_ = cart2sph(coords[j][0], coords[j][1], coords[j][2])
    args = {'rad' : r, 'lon1' : t,
      'lat1' : p, 'lon2' : t_, 'lat2': p_}
    return haversine(**args)

def neighbors(chan, chan_locs, candidates, k, r):
    dist = np.array(map(lambda c: gc(chan_locs, chan, c, r), candidates))
    closest = candidates[np.argsort(dist)[:k]]
    dist = dist[np.argsort(dist)[:k]]
    tot = np.sum(dist)
    return dist, closest, tot

def wave_interp(D, p_local, p_global):
    bad_chans = p_local['bad_chans']
    eog_chans = p_global['eog_chans']
    if bad_chans.size == 0:
        return (D, p_local)
    C = D.shape[0]
    T = D.shape[1]
    chan_locs = p_global['inter']['chan_locs']
    wave = p_global['inter']['wave']
    r = p_global['inter']['loc_unit']
    v = p_global['inter']['verbose']
    k = p_global['inter']['k']

    # Transform to wavelet coefficients
    coefs = [pywt.wavedec(D[c, :], wave) for c in range(C)]
    candidates = np.setdiff1d(range(C), bad_chans)
    candidates = np.setdiff1d(range(C), eog_chans)
    for bc in bad_chans:
        dist, neigh, tot = neighbors(bc, chan_locs, candidates, k, r)
        num_levels = len(coefs[bc])
        if v:
            print 'bad chan =', bc, ',', 'closest =', neigh, ',',
            print 'distances =', dist, 'num levels =', num_levels
        for i in range(num_levels):
            coefs[bc][i] = np.sum([coefs[n][i] * dist[p]/tot for p, n in enumerate(neigh)], axis=0)
    D_int = np.vstack([pywt.waverec(c, wave) for c in coefs])
    return (D_int, p_local)

def ssinterp(D, p_local, p_global):
    bad_chans = p_local['bad_chans']
    if bad_chans.size == 0:
        return (D, p_local)
    coords = p_global['inter']['chan_locs']
    coords = map(lambda x: cart2sph(*x), zip(coords[:, 0], coords[:, 1], coords[:, 2]))
    coords = np.vstack(coords)
    s_val = p_global['inter']['s']
    D = intp(D, coords, bad_chans, p_global['eog_chans'],  s = s_val)
    return (D, p_local) 

def intp(D, coords, rm_idx, eog_chans, s=1000):
    old = D[rm_idx, :]
    samp_idx = np.setdiff1d(np.arange(D.shape[0]), rm_idx)
    samp_idx = np.setdiff1d(samp_idx, eog_chans)
    sample = D[samp_idx]
    F = []
    for i in range(sample.shape[1]):
        F_i = ssi(sample[:, i],
                  coords[samp_idx],
                  s = s)
        F.append(F_i)
    pred = []
    for idx in rm_idx:
        itp = []
        for i, f in enumerate(F):
            if f is None:
                itp.append(D[idx, i])
            else:
                itp.append(f(coords[idx, 0],
                          coords[idx, 1])[0][0])
        pred.append(np.array(itp))
    D[rm_idx] = np.array(pred)
    return D


def ssi(E, P, s):
    F = None
    try:
        F = SmoothSphereBivariateSpline(P[:, 0], P[:, 1],
	                    		E, s=s)
    except:
        F = None
    return F    


