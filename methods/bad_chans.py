import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, kurtosis
import seaborn as sns
from viz import bad_chan_plot



def bad_detec(D, p_local, p_global):
    all_bcs = []
    for meas in p_global['bad_detec']['measure']:
        statistics = get_statistic(
                           D,
                           meas,
                           p_global['bad_detec']['trim'],
                           p_global['bad_detec']['discret'],
                           p_global['bad_detec']['verbose'])
        thresh = p_global['bad_detec']['thresh']
        chans = np.arange(D.shape[0])
        bad_chans = chans[np.logical_or(statistics < -thresh, statistics > thresh)]
        bad_chan_plot(statistics, p_local, meas)
        all_bcs.append(bad_chans)
    all_bcs = np.hstack(all_bcs)
    p_local.update({'bad_chans': all_bcs})
    D[p_local['bad_chans'], :] = 0
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


def get_statistic(D, measure, trim, discret, verbose):
    # get num chans and time
    channels = D.shape[0]
    timepts = D.shape[1]

    statistic = []

    for c in range(channels):
        ra = D[c, :]
        if measure == 'prob':
            ra = gaussian_normalize(ra)
            if trim is not None:
                #qq_plot(ra, title = 'qq-plot before gaussian trim')
                ra = gaussian_trim(ra, .1)
                ra = gaussian_normalize(ra)
                #qq_plot(ra, title = 'qq-plot after gaussian trim')
            M = np.max(ra)
            m = np.min(ra)
            ticks = np.linspace(0, 1, discret) * (M - m) + m 
            true_cdf = np.array(map(lambda x: norm.cdf(x), ticks))
            sample_cdf = get_cdf(ra, ticks)
            #plt.plot(ticks, true_cdf, 'r.', label='true')
            #plt.plot(ticks, sample_cdf, 'b.', label='sample')
            #plt.legend()
            #plt.title('Sample CDF compared to normal')
            #plt.show()
            statistic.append(np.max(true_cdf - sample_cdf))
        elif measure == 'kurtosis':
            statistic.append(kurtosis(ra))
    muS = np.mean(statistic)
    sigS = np.sqrt(np.var(statistic))
    normalized_statistic = (statistic - muS) / sigS
    return normalized_statistic

