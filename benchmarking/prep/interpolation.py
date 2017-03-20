import numpy as np
from scipy.interpolate import SmoothSphereBivariateSpline

def gen_noise(data, params):
    n = params['n_to_corrupt']
    sigma = params['sigma']
    mu = params['mu']
    rand_idx = np.random.choice(data.shape[0], n, replace=False)
    noise = np.random.normal(mu, sigma, n * data.shape[1])
    noise = noise.reshape(n, data.shape[1])
    return (noise, rand_idx)

def corrupt_and_interpolate(d, params):
    d, e = d
    noise, bad_chans = e
    d_corrupted = d.copy()
    d_corrupted[bad_chans] = d_corrupted[bad_chans] + noise
    params.update({'bad_idx': bad_chans})
    return ssi_wrapper(d_corrupted, params)

def corrupt_no_interpolate(d, params):
    d, e = d
    noise, bad_chans = e
    d_corrupted = d.copy()
    d_corrupted[bad_chans] = d_corrupted[bad_chans] + noise
    return d_corrupted

def ssi_wrapper(D, params):
    coords = params['coords']
    rm_idx = params['bad_idx']
    s_val = params['s']
    return intp(D, coords, rm_idx, s = s_val) 

def intp(D, coords, rm_idx, s=1000):
    old = D[rm_idx, :]
    samp_idx = np.setdiff1d(np.arange(D.shape[0]), rm_idx)
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
    try:
        F = SmoothSphereBivariateSpline(P[:, 0], P[:, 1],
                                    E, s=s)
    except:
        F = None
    return F    

