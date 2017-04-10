import sys
import csv
import numpy as np
import cPickle as pkl
import os
import traceback
from glob import glob as glob
import dataset_creation as dc
from pathos.multiprocessing import ProcessingPool as Pool
import matplotlib.pyplot as plt

def load_data(pkl_path):
    with open(pkl_path, 'rb') as f:
        return pkl.load(f)

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
            try:
                sub_path = 'figs/' + subject 
                os.makedirs(sub_path)
            except:
                print 'Already exists figure folder for ', subject
            for trial in range(1, trials[i] + 1):
                trial = '%s_trial-%02d' % (subject, int(trial))
                fig_path = 'figs/' + subject + '/' + trial + '/'
                try:
                    os.makedirs(fig_path)
                except:
                    print 'Already exists figure folder for ', trial
                print 'OPENING FILE', trial
                pkl_path = '%s/%s/eeg/%s.pkl' % (dataset, subject, trial)
                p_local = {
                    'fig_path': fig_path,
                    'step': 0,
                    'function_name': 'Raw'
                }
                yield (load_data(pkl_path), p_local)

    def factory():
        return data_gen()
    return factory, labels

def f(x, function, params):
    print x
    x0 = x[0]()
    try:
        x[1]['step'] = x[1]['step'] + 1
        print x[1]
        return function(x0, x[1], params['p_global'])
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

def ngf(factory, function, params):
    def nested_generator():
        for item in factory():
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

def capstone(D, p_local, p_global):
    def f():
        return D
    return (f, p_local)

def apply_all(D, functs, map_method):
    res = []
    for funct in functs[::-1]:
        res.append(map(funct, map_method(lambda d: d, D)))
    return res
