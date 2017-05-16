import numpy as np

def frob(x, y):
    return np.linalg.norm(x-y)

# Diff Num 3 Cycles
def diff_num_3cycle(x, y):
    return np.abs(np.sum(x) - np.sum(y))

# Diff Num 4 Cycles
def diff_num_4cycle(x, y):
    def c4(A):
        return np.trace(np.linalg.matrix_power(A, 4)) + \
               np.trace(np.linalg.matrix_power(A, 2)) - \
               np.sum(np.sum(A, 0)**2)
    return np.abs(c4(x) - c4(y))

def diff_trace(x, y):
    return np.abs(np.trace(x) - np.trace(y))
