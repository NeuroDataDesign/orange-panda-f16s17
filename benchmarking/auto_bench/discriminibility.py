import numpy as np

def partial_disc(D, labels, subject, trial1, trial2):
    enum = np.arange(D.shape[0])
    t1 = enum[labels == subject][trial1]
    t2 = enum[labels == subject][trial2]
    d_t1_t2 = D[t1][t2]
    d_ra = [D[t1][x] for x in enum[labels != subject]]
    return np.mean(d_t1_t2 < d_ra)

def distance_matrix(data, metric, symmetric = True):
    n = len(data)
    dist_matrix = np.zeros([n, n])
    if symmetric:
        for i in range(n):
            for j in range(i):
                dist_matrix[i][j] = metric(data[i], data[j])
                dist_matrix[j][i] = dist_matrix[i][j]
    else:
        for i in range(n):
            for j in range(n):
                dist_matrix[i][j] = metric(data[i], data[j])
    return dist_matrix

def discriminibility(data, labels, metric):
    dist_matrix = distance_matrix(data, metric)
    labels = np.array(labels)
    partials = []
    for s in np.unique(labels):
        num = np.sum(labels == s)
        for t in range(num):
            for tt in range(num):
                if tt != t:
                    p = partial_disc(dist_matrix,
                        labels, s, t, tt)
                    partials.append(p)
    return np.mean(partials)
