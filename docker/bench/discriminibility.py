import numpy as np
from utilities import apply_all
from copy import deepcopy
import networkx as nx

def loadGraphs(filenames, verb=False):
    """
    Given a list of files, returns a dictionary of graphs

    Required parameters:
        filenames:
            - List of filenames for graphs
    Optional parameters:
        verb:
            - Toggles verbose output statements
    """
    #  Initializes empty dictionary
    gstruct = OrderedDict()
    for idx, files in enumerate(filenames):
        if verb:
            print "Loading: " + files
        #  Adds graphs to dictionary with key being filename
        fname = os.path.basename(files)
        gstruct[fname] = nx.read_gpickle(files)
    return gstruct

def constructGraphDict(names, fs, verb=False):
    """
    Given a set of files and a directory to put things, loads graphs.

    Required parameters:
        names:
            - List of names of the datasets
        fs:
            - Dictionary of lists of files in each dataset
    Optional parameters:
        verb:
            - Toggles verbose output statements
    """
    #  Loads graphs into memory for all datasets
    graphs = OrderedDict()
    for idx, name in enumerate(names):
        if verb:
            print "Loading Dataset: " + name
        # The key for the dictionary of graphs is the dataset name
        graphs[name] = loadGraphs(fs[name], verb=verb)
    return graphs

def rdf(dist, ids):
    N = dist.shape[0]
    assert(N == len(ids))
    uniqids = list(set(ids))
    countvec = [ids.count(uniqid) for uniqid in uniqids]
    scans = np.max(countvec)
#     rdf = np.empty((N*(scans-1)))
    rdf = []

    for i in np.arange(0, N):
        ind = [idx for idx, x in enumerate(ids) if x == ids[i]]
        for j in ind:
            if i != j:
                di = deepcopy(dist[i,:])
                di[ind] = np.inf
                d = dist[i,j]
                diff = di[np.where(~np.isinf(di))]
#                 import pdb; pdb.set_trace()
                rdf += [1.0 - ((np.sum(diff < d) + 0.5*np.sum(diff == d)) / (1.0*(N-len(ind))))]
    return rdf

def partial_disc(D, labels, subject, trial1, trial2):
    enum = np.arange(D.shape[0])
    idx1 = [i for i, x in enumerate(labels) if x == subject]
    t1 = enum[idx1][trial1]
    t2 = enum[idx1][trial2]
    d_t1_t2 = D[t1][t2]
    
    idx2 = [i for i, x in enumerate(labels) if x != subject]
    d_ra = [D[t1][x] for x in enum[idx2]]
    
    return np.mean(d_t1_t2 < d_ra)

def distance_matrix(data, metric, symmetric = True):
    n = data.shape[2]
    dist_matrix = np.zeros((n, n))
    if symmetric:
        for i in range(n):
            for j in range(i):
                tmp = metric(data[:,:,i], data[:,:,j])
                dist_matrix[i][j] = tmp
                dist_matrix[j][i] = tmp
    else:
        for i in range(n):
            for j in range(n):
                dist_matrix[i][j] = metric(data[i], data[j])
    return dist_matrix

def discriminibility(data, labels, metric):
    dist_matrix = distance_matrix(data, metric)
    partials = []
    for s in list(set(labels)):
        num = ids.count(s)
        for t in range(num):
            for tt in range(num):
                if tt != t:
                    p = partial_disc(dist_matrix, labels, s, t, tt)
                    partials.append(p)
    return dist_matrix, np.mean(partials)

def disc_all(D, labels, transforms, metrics, names):
    discs = []
    derivitives = apply_all(D, transforms, map)
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
    discs = np.vstack(discs)
    print discs
    for disc_method in range(discs.shape[1]):
        plt.plot(discs[:, disc_method], '*', label = disc_names[disc_method])
    plt.xticks(range(len(exp_names)), exp_names)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.06),
          ncol=4, fancybox=True, shadow=True)
    plt.tight_layout()
    ax = plt.gca()
    ax.margins(0.05)
    return plt.gcf()

def intra_inter(dist, labels):
    within = []
    outside = []
    for i, label1 in enumerate(labels):
        for j, label2 in enumerate(labels):
            if label1 == label2:
                if i != j:
                    within.append(dist[i, j])
            else:
                outside.append(dist[i, j])
    return within, outside

