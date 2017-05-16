import numpy as np
np.seterr(divide='ignore')

# Return representation of the spectrum
def spect(D):
    return np.linalg.svd(D, full_matrices=False)[1]

# Return correlation matrix
def correl(D):
    with np.errstate(invalid='ignore'):
        return np.nan_to_num(np.corrcoef(D))



