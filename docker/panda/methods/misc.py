import numpy as np

# Mean center and record max and min value in matrix (for plotting)
def setup(D, p_local, p_global):
    D = D - np.mean(D, axis = 1).reshape(-1, 1)
    zero_chans = []
    p_local['max'] = np.max(D)
    p_local['min'] = np.min(D)
    return (D, p_local)
