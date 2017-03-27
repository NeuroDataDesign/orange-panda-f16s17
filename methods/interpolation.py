from math import radians, cos, sin, asin, sqrt
import pywt
import numpy as np
import copy

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
    d, bad_chans = d
    bad_chans = np.array(bad_chans, dtype=np.uint8).flatten()
    if bad_chans.size == 0:
        return d
    print bad_chans.shape
    C = d.shape[0]
    T = d.shape[1]
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
        dist, neigh, tot = neighbors(bc, chan_locs, candidates, k, r)
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
	    for i in range(5):#range(len(coefs[0]))[1:]
		from bench.viz import cross_compare
		cross_compare([orig_coefs[c] for c in bad_chans],
			      [coefs[c] for c in bad_chans], i)
    return d_int

def ssi_wrapper(D, p_local, p_global):
    coords = p_global['chan_locs']
    bad_chans = p_global['bad_chans']
    s_val = p_global['s']
    return intp(D, coords, bad_chans, s = s_val) 

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


