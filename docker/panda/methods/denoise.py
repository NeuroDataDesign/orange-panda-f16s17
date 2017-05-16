from math import radians, cos, sin, asin, sqrt
import pywt
import numpy as np
import copy
from pcp import pcp as pcp
from signals import butter_bandstop_filter, butter_highpass_filter, butter_lowpass_filter

def eog_regress(D, p_local, p_global):
    p_local['eog_in'] = False
    Y, N = (D[p_global['eeg_chans'], :], D[p_global['eog_chans'], :])
    m_Y = np.mean(Y, axis = 1).reshape(-1, 1)
    Y = Y - m_Y
    m_N = np.mean(N, axis = 1).reshape(-1, 1)
    N = N - m_N
    return (Y - ((Y.dot(N.T)).dot(np.linalg.pinv(N.dot(N.T)))).dot(N), p_local)

def highpass(D, p_local, p_global):
    order = p_global['hpf']['order']
    Fs = p_global['hpf']['Fs']
    cutoff = p_global['hpf']['cutoff']
    one_chan = lambda i: butter_highpass_filter(D[i, :], cutoff, Fs, order)
    D = np.vstack(one_chan(i) for i in range(D.shape[0]))
    return (D, p_local)

def lowpass(D, p_local, p_global):
    order = p_global['lpf']['order']
    Fs = p_global['lpf']['Fs']
    cutoff = p_global['lpf']['cutoff']
    one_chan = lambda i: butter_lowpass_filter(D[i, :], cutoff, Fs, order)
    D = np.vstack(one_chan(i) for i in range(D.shape[0]))
    return (D, p_local)

def bandstop(D, p_local, p_global):
    order = p_global['bsf']['order']
    Fs = p_global['bsf']['Fs']
    for cutoff in p_global['bsf']['cutoffs']:
            one_chan = lambda i: butter_bandstop_filter(D[i, :],
							cutoff,
							Fs, order)
	    D = np.vstack(one_chan(i) for i in range(D.shape[0]))
    return (D, p_local)

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
    X_via = X[np.abs(X) <= g_thresh]
    X_sort = np.sort(X_via)
    csX = np.cumsum(X_sort)
    R = np.arange(X_via.shape[0])
    L = map(lambda t: n - 2 * t + csX[t] + (n - t) * X_sort[t]**2, R)
    if len(L) == 0:
        min_thresh = g_thresh
    else:
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
    return (d_den, p_local)

def visu_shrink(X):
    n = X.shape[0]
    g_thresh = np.sqrt(2 * np.log(n))
    min_thresh = g_thresh
    absX = np.abs(X)
    X[absX < min_thresh] = 0
    X[X > min_thresh] = X[X > min_thresh] - min_thresh
    X[X < -min_thresh] = X[X < -min_thresh] + min_thresh
    return (X, min_thresh)

def visu_shrink_denoise(f, wave, v):
    true_coefs = pywt.wavedec(f, wave, level=2)
    res = [visu_shrink(coef) for coef in true_coefs]
    den_coefs, thresholds = zip(*res)
    den_coefs = list(den_coefs)
    #den_coefs.insert(0, true_coefs[0])
    f_denoised = pywt.waverec(den_coefs, wave)
    return f_denoised

def wavelet_visushrink(d, p_local, p_global):
    C = d.shape[0]
    T = d.shape[1]
    wave = p_global['wave_visu']['wave']
    v = p_global['wave_visu']['verbose']
    # Make sure even length timesteps
    if T % 2 == 1:
        d = d[:, :-1]

    # Get original coeffs for plot
    if v:
        coefs = [pywt.wavedec(d[c, :], wave) for c in range(C)]

    # Denoise each channel
    d_den = np.vstack(map(lambda i: visu_shrink_denoise(d[i, :], wave, v),
                  range(d.shape[0])))

    # Get new coeffs for plot
    if v:
        den_coefs = [pywt.wavedec(d_den[c, :], wave) for c in range(C)]
        from viz import cross_compare
        for i in range(3):#range(len(coefs[0]))[1:]:
            cross_compare(coefs, den_coefs, i)
    return (d_den, p_local)

def pca_denoise(D, p_local, p_global):
    d, s_vals = D
    k = p_global['pca_den']['k']
    U_k = s_vals[:, :k]
    P_k = U_k.dot(U_k.T)
    return P_k.dot(d - np.mean(d, axis=1).reshape(-1, 1))

def rpca_denoise(D, p_local, p_global):
    M = p_global['rpca']['max_iter']
    v = p_global['rpca']['verbose']
    method = p_global['rpca']['pca_method']
    delta = p_global['rpca']['delta']
    mu = p_global['rpca']['mu']
    return (pcp(D, mu = mu, delta = delta, maxiter=M, verbose=v, svd_method=method)[0], p_local)

def wave_rejection(D, p_local, p_global):
    sigs = []
    wave = p_global['wave_rej']['wave']
    thresh = p_global['wave_rej']['thresh']
    all_coefs = [pywt.wavedec(D[i, :], wave, level = None) for i in range(D.shape[0])]
    for i, coefs in enumerate(all_coefs):
        for j , coef in enumerate(coefs[1:]):
            mu = np.mean(coef)
            std = np.std(coef)
            coef = np.array(coef)
            coef[np.abs(coef) > mu + thresh * std] = 0
            all_coefs[i][j + 1] = coef
    for coef in all_coefs:    
        sigs.append(pywt.waverec(coef, 'db2'))
    if p_global['wave_rej']['rec']:
        return (np.vstack(sigs), p_local)
    else:
        return (all_coefs, p_local)

def amp_shrinkage(D, p_local, p_global):
    thresh = p_global['amp_rej']['thresh']
    method = p_global['amp_rej']['method']
    D = np.copy(D)
    std = np.std(D)
    mu = np.mean(D)
    high = D > mu + thresh * std
    low = D < mu - thresh * std
    if method == 'zero':
        D[high] = 0
        D[low] = 0
    elif method == 'shrink':
        D[high] = mu + thresh * std
        D[low] = mu - thresh * std
    return (D, p_local)
