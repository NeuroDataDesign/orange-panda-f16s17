from math import radians, cos, sin, asin, sqrt
import pywt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import copy
from viz import cross_compare

def sure(t, X):
    x_gt = np.abs(X) > t
    y = np.ones(X.shape) * t
    y[x_gt] = np.abs(X)[x_gt]
    S = np.sum(np.square(y))
    n = X.shape[0]
    card = np.sum(np.logical_not(x_gt))
    return n + S -2 * card

def sure_shrink_fast(X):
    n = X.shape[0]
    X_sort = np.sort(X)
    csX = np.cumsum(X_sort)
    R = np.arange(n)
    L = map(lambda t: n - 2 * t + csX[t] + (n - t) * X_sort[t]**2, R)
    min_thresh = X_sort[np.argmin(L)]
    absX = np.abs(X)
    X[absX < min_thresh] = 0
    X[X > min_thresh] = X[X > min_thresh] - min_thresh
    X[X < -min_thresh] = X[X < -min_thresh] + min_thresh
    return (X, min_thresh)

def sure_shrink_denoise(f, wave, v):
    true_coefs = pywt.wavedec(f, wave, level=None)
    res = [sure_shrink_fast(coef) for coef in true_coefs[1:]]
    den_coefs, thresholds = zip(*res)
    den_coefs = list(den_coefs)
    den_coefs.insert(0, true_coefs[0])
    f_denoised = pywt.waverec(den_coefs, wave)
    #if v:
    #    for tup in zip(range(len(thresholds)), thresholds):
    #        print 'Scale:', tup[0], ',', 'Threshold:', tup[1]
    return f_denoised

def wavelet_sureshrink(d, p_local, p_global):
    C = d.shape[0]
    T = d.shape[1]
    wave = p_global['wave']
    v = p_global['verbose']
    # Make sure even length timesteps
    if T % 2 == 1:
        d = d[:, :-1]

    # Get original coeffs for plot
    if v:
        coefs = [pywt.wavedec(d[c, :], wave) for c in range(C)]

    # Denoise each channel
    d_den = np.vstack(map(lambda i: sure_shrink_denoise(d[i, :], wave, v),
                  range(d.shape[0])))

    # Get new coeffs for plot
    if v:
        den_coefs = [pywt.wavedec(d_den[c, :], wave) for c in range(C)]

        for i in range(10):#range(len(coefs[0]))[1:]:
            cross_compare(coefs, den_coefs, i)
    return d_den