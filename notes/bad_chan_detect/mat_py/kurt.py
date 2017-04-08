import numpy as np
from scipy.stats import kurtosis
from scipy.stats import skew
import scipy.io
import matplotlib.pyplot as plt
import os
import StringIO

from helper import *
#iplot([{"x": [1, 2, 3], "y": [3, 1, 6]}])
# Fix random seed
np.random.seed(123456789)


# kurt bad detec
def kurt_baddetec(inEEG, thresh):
    orig_dim = inEEG.ndim
    if inEEG.ndim == 2:
        inEEG = np.expand_dims(inEEG, axis=1)

    electrodes = inEEG.shape[0]
    trials = inEEG.shape[1]
    timepnts = inEEG.shape[2]
    print "Electrodes:", electrodes
    print "Trials:", trials
    print "Timepnts:", timepnts

    # eng = matlab.engine.start_matlab()
    # Then, initialize a probability vector of electrode length
    kurtvec = np.zeros((electrodes, trials))
    # iterate through electrodes and get kurtoses
    for i in range(electrodes):
        for j in range(trials):
            # add kurtosis to the vector
            kurtvec[i, j] = kurtosis(inEEG[i,j,:])
    # then figure out which electrodes are bad
    
    #print probvec
    if orig_dim == 3:
        ones = np.ones(kurtvec.shape)
        mean = np.mean(kurtvec, axis=1, keepdims=True)
        std = np.std(kurtvec, axis=1, keepdims=True)
        kurtvec = np.divide(kurtvec - mean * ones, std)
    else:
        kurtvec = np.divide(kurtvec - np.mean(kurtvec), np.std(kurtvec))
    
    # Reject bad elecs
    rej = []
    for i in thresh:
        rej.append(abs(kurtvec) > i)
    return kurtvec, np.asarray(rej)


