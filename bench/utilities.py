import sys
import csv
import numpy as np
import cPickle as pkl
import os
import traceback
from glob import glob as glob
import dataset_creation as dc
from pathos.multiprocessing import ProcessingPool as Pool

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
        par = Pool(8)
        def f(x):
            try:
                return function(x, params['p_local'], params['p_global'])
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
	        print "*** print_tb:"
	        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
	        print "*** print_exception:"
	        traceback.print_exception(exc_type, exc_value, exc_traceback,
				      limit=2, file=sys.stdout)
	        print "*** print_exc:"
	        traceback.print_exc()
        for item in par.imap(f, factory()):
            yield item
    return nested_generator

def tgf(factory1, factory2):
    def tup_generator():
        for item in ((a, b) for (a, b) in zip(factory1(), factory2())):
            yield item
    return tup_generator

def ngff(init, functions, params):
    nfg = init
    for function in functions:
        nfg = ngf(nfg, function, params)
    return nfg

def apply_all(D, functs, map_method):
    res = []
    for funct in functs[::-1]:
        res.append(map(funct, map_method(lambda d: d, D)))
    return res
