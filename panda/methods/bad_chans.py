import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, kurtosis
import seaborn as sns
import sys
import traceback
import copy

def bad_detec(D, p_local, p_global):
    D = np.copy(D)
    zero_chans = []
    for c in range(D.shape[0]):
        if np.sum(D[c, :]) == 0:
	    zero_chans.append(c)
    zero_chans = np.array(zero_chans, dtype=np.uint8)
    print 'Channels which are zero', zero_chans
    all_bcs = [zero_chans]
    for meas in p_global['bad_detec']['measure']:
        chans = np.arange(D.shape[0])
        chans = np.setdiff1d(chans, p_global['eog_chans'])
        chans = np.setdiff1d(chans, zero_chans)
        statistics = get_statistic(
                           D,
                           meas,
                           p_global['bad_detec']['trim'],
                           p_global['bad_detec']['discret'],
                           p_global['bad_detec']['verbose'],
                           chans)
        thresh = p_global['bad_detec']['thresh']
        bad_chans = chans[np.logical_or(statistics < -thresh, statistics > thresh)]
        print 'Channels determined bad by', meas, ':', bad_chans
        all_bcs.append(bad_chans)
    if len(all_bcs) > 0:
        all_bcs = np.hstack(all_bcs)
        p_local.update({'bad_chans': all_bcs})
        D[all_bcs, :] = 0
    else:
        all_bcs = None
        p_local.update({'bad_chans': all_bcs})
    print 'All channels removed', all_bcs
    return (D, p_local)


def gaussian_normalize(samples):
    mu = np.mean(samples)
    var = np.var(samples)
    normalized = (samples - mu) / np.sqrt(var)
    return normalized

def gaussian_trim(samples, trim_factor):
    z_thresh = norm.ppf(trim_factor)
    samples = samples[samples > z_thresh]
    samples = samples[samples < -z_thresh]
    return samples
    
def qq_plot(normalized, title):
    M = np.max(normalized)
    m = np.min(normalized)
    width = M - m
    ticks = np.linspace(0, 1, normalized.shape[0])
    plt.plot(np.linspace(0, 1, normalized.shape[0]), np.sort(normalized))
    plt.plot(np.linspace(0, 1, normalized.shape[0]), ticks * width + m)
    plt.show()

def std_norm(x):
    return norm.ppf((1 / np.sqrt(2 * np.pi)) * np.exp(-(x)**2 / 2))

def get_cdf(array, ticks):
    return np.array(map(lambda t: np.mean(array < t), ticks))


def get_statistic(D, measure, trim, discret, verbose, chans):
    # get num chans and time
    channels = D.shape[0]
    timepts = D.shape[1]

    statistic = []

    for c in chans:
        ra = D[c, :]
        if measure == 'prob':
            ra = gaussian_normalize(ra)
            M = np.max(ra)
            m = np.min(ra)
            ticks = np.linspace(0, 1, discret) * (M - m) + m 
            true_cdf = np.array(map(lambda x: norm.cdf(x), ticks))
            sample_cdf = get_cdf(ra, ticks)
            statistic.append(np.max(true_cdf - sample_cdf))
        elif measure == 'kurtosis':
            statistic.append(kurtosis(ra))
        elif measure == 'std':
            statistic.append(np.std(ra))
        elif measure == 'spread':
            statistic.append(np.max(ra) - np.min(ra))
        elif measure == 'max':
            statistic.append(np.max(np.abs(ra)))
    muS = np.mean(statistic)
    sigS = np.sqrt(np.var(statistic))
    normalized_statistic = (statistic - muS) / sigS
    return normalized_statistic

