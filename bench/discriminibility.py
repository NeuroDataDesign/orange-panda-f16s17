import numpy as np
from utilities import apply_all
import numpy as np
from pathos.multiprocessing import ProcessingPool as Pool

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

def disc_all(factory, labels, transforms, metrics, names):
    discs = []
    D = factory()
    D = [d for d in D]
    par = Pool(8) 
    derivitives = apply_all(D, transforms, par.imap)
    for i in range(len(derivitives)):
        print names[i]
        disc = discriminibility(
                    derivitives[i],
                    labels,
                    metrics[i]
                )
        discs.append(disc)
        print disc
    return discs

def disc_plot(discs, disc_names, exp_names):
    import seaborn as sns
    import matplotlib.pyplot as plt
    discs = np.vstack(discs).T
    for disc_method in range(discs.shape[1]):
        plt.plot(discs[:, disc_method], '*', label = disc_names[disc_method])
    plt.xticks(range(len(exp_names)), exp_names)
    plt.legend()
    plt.tight_layout()
    return plt.gcf()
