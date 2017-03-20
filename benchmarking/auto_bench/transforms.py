import numpy as np
np.seterr(divide='ignore')

# Return representation of the spectrum
def spect(D):
    return np.linalg.svd(D, full_matrices=False)[1]

# Return identity
def identity(D):
    return D

# Return correlation matrix
def correl(D):
    with np.errstate(invalid='ignore'):
        return np.nan_to_num(np.corrcoef(D))

# Return spectrum of the correlation matrix
def correl_spec(D):
    with np.errstate(invalid='ignore'):
        return np.linalg.svd(np.nan_to_num(np.corrcoef(D)), full_matrices=False)[1]

# Return thresholded correlation matrix
def thresh_correl(D, k):
    with np.errstate(invalid='ignore'):
        return np.nan_to_num(np.corrcoef(D)) > k - np.eye(D.shape[0])

def tc_make(k):
    def tc(D):
        return thresh_correl(D, k)
    return tc
