import numpy as np
import pandas as pd

def naive_D_partial(eeg_data, subjects, subject, trial1, trial2, dist):
    t1 = eeg_data[subjects == subject][trial1]
    t2 = eeg_data[subjects == subject][trial2]
    d_t1_t2 = dist(t1, t2)
    d_ra = [dist(t1, x) for x in eeg_data[subjects != subject]]
    return np.mean(d_t1_t2 < d_ra)

def naive_D(eeg_data, subjects, dist):
    sra = []
    tra = []
    ttra = []
    mra = []
    partials = []
    for s in np.unique(subjects):
        num = len(eeg_data[subjects == s])
        for t in np.arange(num):
            for tt in np.setdiff1d(np.arange(num), [t]):
                p = naive_D_partial(eeg_data,
                              subjects,
                              s,
                              t,
                              tt,
                              dist)
                partials.append(p)
                sra.append(s)
                tra.append(t)
                ttra.append(tt)
                mra.append(p)
    info = pd.DataFrame(data = np.array([sra, tra, ttra, mra]).T,
                        columns=['Subject',
                                 'Trial',
                                 'Trial_Prime',
                                 'Partial Discriminibility'])         
    return np.mean(partials), info

def D_partial(D, subjects, subject, trial1, trial2, dist):
    enum = np.arange(D.shape[0])
    t1 = enum[subjects == subject][trial1]
    t2 = enum[subjects == subject][trial2]
    d_t1_t2 = D[t1][t2]
    d_ra = [D[t1][x] for x in enum[subjects != subject]]
    return np.mean(d_t1_t2 < d_ra)

def distance_matrix(eeg_data, dist):
    n = len(eeg_data)
    D = np.zeros([n, n])
    for i in range(n):
        for j in range(i):
            D[i][j] = dist(eeg_data[i], eeg_data[j])
            D[j][i] = dist(eeg_data[i], eeg_data[j])
    return D

def D(eeg_data, subjects, dist):
    sra = []
    tra = []
    ttra = []
    mra = []
    partials = []
    D = distance_matrix(eeg_data, dist)
    for s in np.unique(subjects):
        num = len(eeg_data[subjects == s])
        for t in np.arange(num):
            for tt in np.setdiff1d(np.arange(num), [t]):
                p = D_partial(D,
                              subjects,
                              s,
                              t,
                              tt,
                              dist)
                partials.append(p)
                sra.append(s)
                tra.append(t)
                ttra.append(tt)
                mra.append(p)
    info = pd.DataFrame(data = np.array([sra, tra, ttra, mra]).T,
                        columns=['Subject',
                                 'Trial',
                                 'Trial_Prime',
                                 'Partial Discriminibility'])         
    return np.mean(partials), info
