from math import radians, cos, sin, asin, sqrt
import pywt
import numpy as np
import copy

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
    g_thresh = np.sqrt(2 * np.log(n))
    X_via = X[np.abs(X) < g_thresh]
    X_sort = np.sort(X_via)
    csX = np.cumsum(X_sort)
    R = np.arange(X_via.shape[0])
    L = map(lambda t: n - 2 * t + csX[t] + (n - t) * X_sort[t]**2, R)
    if len(L) == 0:
        min_thresh = g_thresh
    else:
        min_thresh = X_sort[np.argmin(L)]
        min_thresh = min(min_thresh, g_thresh)
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
    return f_denoised

def wavelet_sureshrink(d, p_local, p_global):
    C = d.shape[0]
    T = d.shape[1]
    wave = p_global['wave_sure']['wave']
    v = p_global['wave_sure']['verbose']
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
        from viz import cross_compare
        for i in range(3):#range(len(coefs[0]))[1:]:
            cross_compare(coefs, den_coefs, i)
    return d_den

def pca_singvals(d):
    m = np.mean(d, axis = 1).reshape(-1, 1)
    d_cent = d - m
    U, _, _ = np.linalg.svd(d_cent, full_matrices = False)
    return U
