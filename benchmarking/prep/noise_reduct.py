import numpy as np
import pywt
import numpy as np
from pcp import pcp
from pathos.multiprocessing import ProcessingPool as Pool

def pca(d):
    m = np.mean(d, axis=1).reshape(-1, 1)
    d_cent = d - m
    U, _, _ = np.linalg.svd(d_cent, full_matrices = False)
    print 'Finished a PCA.'
    return U
    
def pca_denoise(d, params):
    k = params['k'] # Number of singular vectors to take.
    d, U = d
    m = np.mean(d, axis=1).reshape(-1, 1)
    P_k = U[:, :k].dot(U[:, :k].T)
    return P_k.dot(d - m) + m

def rpca(d):
    return pca(pcp(d, maxiter=3, verbose=True, svd_method="randomized")[0])

def full_pca(d, k):
    m = np.mean(d, axis=1).reshape(-1, 1)
    U = pca(d)
    P_k = U[:, :k].dot(U[:, :k].T)
    return P_k.dot(d - m) + m

def full_rpca(d, k):
    m = np.mean(d, axis=1).reshape(-1, 1)
    U = rpca(d)
    P_k = U[:, :k].dot(U[:, :k].T)
    return P_k.dot(d - m) + m
    
def identity(d, theta):
    return d

def nan_to_num(d, theta):
    return np.nan_to_num(d)

def SURE(t, X):
    x_gt = np.abs(X) > t
    y = np.ones(X.shape) * t
    y[x_gt] = np.abs(X)[x_gt]
    S = np.sum(np.square(y))
    n = X.shape[0]
    card = np.sum(np.logical_not(x_gt))
    return n + S -2 * card

def SURE_SHRINK_FAST(X):
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
    return X

def SURE_SHRINK(X):
    bound =np.log(2* X.shape[0])
    X_small = X[X < bound]
    L = map(lambda x: SURE(x, X), X_small)
    min_thresh = X_small[np.argmin(L)]
    #min_thresh = bound
    absX = np.abs(X)
    X[absX < min_thresh] = 0 
    X[X > min_thresh] = X[X > min_thresh] - min_thresh
    X[X < -min_thresh] = X[X < -min_thresh] + min_thresh
    #for i in range(X.shape[0]):
    #    if np.abs(X[i]) <= min_thresh:
    #        X[i] = 0
    #    elif X[i] > min_thresh:
    #        X[i] = X[i] - min_thresh
    #    elif X[i] < -min_thresh:
    #        X[i] = X[i] + min_thresh
    return X

def SURE_SHRINK_DENOISE(f, wave):
    true_coefs = pywt.wavedec(f, wave, level=None)
    den_coefs = [SURE_SHRINK_FAST(coef) for coef in true_coefs[1:]]
    den_coefs.insert(0, true_coefs[0])
    f_denoised = pywt.waverec(den_coefs, wave)
    return f_denoised

def wavelet_sureshrink(d, wave):
    if d.shape[1] % 2 == 1:
        d = d[:, :-1]
    par = Pool(10)
    print '.'
    return np.vstack(par.map(lambda i: SURE_SHRINK_DENOISE(d[i, :], wave),
                  range(d.shape[0])))
