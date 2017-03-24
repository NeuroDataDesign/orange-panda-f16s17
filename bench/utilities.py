import csv
import numpy as np
import cPickle as pkl
import os
from glob import glob as glob
import dataset_creation as dc

def data_generator_factory(dataset):
    subjects, trials = zip(*dc.participant_info(dataset))
    trials = map(int, trials)
    subjects = np.array(subjects)
    zips = zip(subjects, trials)
    zips = [[x[0]] * x[1] for x in zips]
    labels = [item for sublist in zips for item in sublist]
    def data_gen():
        c = -1
        for i, subject in enumerate(subjects):
            for trial in range(1, trials[i] + 1):
                trial = '%s_trial-%02d' % (subject, int(trial))
                print 'OPENING FILE', trial
                pkl_path = '%s/%s/eeg/%s.pkl' % (dataset, subject, trial)
                with open(pkl_path, 'rb') as f:
                    yield pkl.load(f)
    def factory():
        return data_gen()
    return factory, labels

def ngf(factory, function, params):
    def nested_generator():
        for item in factory():
            yield function(item, params['p_local'], params['p_global'])
    return nested_generator

def ngff(init, functions, params):
    nfg = init
    for function in functions:
        nfg = ngf(nfg, function, params)
    return nfg

def apply_all(D, functs, map_method):
    res = []
    for funct in functs[::-1]:
        res.append(map_method(funct, D))
    return res
