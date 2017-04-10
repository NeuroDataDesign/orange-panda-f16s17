import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from helper import *

# Write wrapper pop_jointprob
# inEEG = C x T x N, channels x trials x timepoints, numpy array
# elecrange = range of electrodes, list/numpy array
# locthresh = threshold for individual electrode inspection
# globthresh = threshold for entire dataset inspection
def pop_jointprob(inEEG, elecrange, locthresh, globthresh):
    # first, do localized individual electrode inspection
    jp, rej = jointprob(inEEG[elecrange,:,:], locthresh, 1)
    # now reshape data for global inspection
    globEEG = np.rollaxis(inEEG, 2)
    np.reshape(globEEG, (globEEG.shape[0], globEEG.shape[1] * globEEG.shape[2]))
    # run global inspection
    jpG, rejG = jointprob(globEEG[elecrange,:], globthresh, 1)
    return jp, rej, jpG, rejG

# Write next level wrapper, jointprob
# Joint prob can use different prob functions to get the distribution
# S = C x T x N, channels x trials x timepoints, numpy array
# OR
# S = C x (T x N), timepoints x (channels x trials), numpy array
# OR
# S = (N x C x T), straight vector of all timepoints, numpy array
# thresholds
# norm = choose normalization: 0 = none, 1 = normalize entropy, 2 = 20% trim
# thresh = threshold
def jointprob(S, thresh, oldjp, normalize, discret = 1000):
    # get num chans and trials and time
    channels = 0
    trials = 0
    timepts = 0
    if S.ndim == 1 or S.ndim == 2:
        channels = S.shape[0]
        trials = S.shape[1]
    elif S.ndim == 3:
        channels = S.shape[0]
        trials = S.shape[1]
        timepts = S.shape[2]
    else:
        print "Bad dimensions"
        return
    # Get Joint Probs
    jp = np.zeros((channels, trials))
    if oldjp.size:
        jp = oldjp
    else:
        jp = []
        if S.ndim == 3:
            for c in range(channels):
                tmp, dist = realproba(S[c,:,:], discret)
                jp.append(np.log(tmp))
            jp = np.asarray(jp)
            jp = -np.sum(jp, axis=2)    
        elif S.ndim == 2:
            print "Swag"
            jp, dist = realproba(S[:,:], discret)
            jp = -np.sum(np.log(jp), axis=1)
            print np.mean(jp), np.std(jp)
    # Normalize data
    if normalize:
        tmpjp = jp
        if normalize == 2:
            tmpjp = sort(jp);
            totrim = round(len(tmpjp) * 0.1)
            tmpjp = tmpjp[totrim : -totrim]
        if S.ndim == 2:
            jp = (jp - np.mean(tmpjp)) / np.std(tmpjp)
        elif S.ndim == 3:
            ones = np.ones(jp.shape)
            mean = np.mean(jp, axis=1, keepdims=True)
            std = np.std(jp, axis=1, keepdims=True)
            jp = np.divide(jp - mean * ones, std)
    # Reject bad elecs
    rej = []
    for i in thresh:
        rej.append(abs(jp) > i)
    return jp, np.asarray(rej)

# Histogram binning implementation
# D = T x N, D = data Trials, Number of timepts
# b = bins, default 1000
def realproba(D, b = 1000):
    SIZE = D.shape[0] * D.shape[1]
    P = np.zeros(b)
    P_dist = np.zeros(b)
    minimum = np.min(D)
    maximum = np.max(D)
    D = np.floor((D - minimum)/(maximum - minimum) * (b - 1)).astype(int)
    D_flat = np.ndarray.flatten(D)
    for i in range(SIZE):
        P_dist[D_flat[i]] = P_dist[D_flat[i]] + 1
    P = P_dist[D] / SIZE
    P_dist = P_dist / SIZE
    if P_dist.ndim < P.ndim:
        P_dist = np.expand_dims(P_dist, P.ndim - P_dist.ndim)
    return P, P_dist.T


