import csv
import numpy as np
import cPickle as pkl
import os
from glob import glob as glob

INFO_FMT = '%14s %14s %10s'
DATE_STRING = '%02d d, %02d h, %02d m, %02d s'

def participant_info(dataset):
    f_name = '%s/%s' % (dataset, 'participants.tsv')
    participants = []
    with open(f_name, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter = '\t')
        next(tsvin, None)
        for row in tsvin:
            participants.append(row)
    return participants 

def apply_all(D, functs, map_method):
    res = []
    for funct in functs[::-1]:
        res.append(map_method(funct, D))
    return res


def data_generator_factory(dataset):
    subjects, trials = zip(*participant_info(dataset))
    trials = map(int, trials)
    subjects = np.array(subjects)
    zips = zip(subjects, trials)
    zips = [[x[0]] * x[1] for x in zips]
    labels = [item for sublist in zips for item in sublist]
    print labels
    def data_gen():
        c = -1
        for i, subject in enumerate(subjects):
            for trial in range(1, trials[i] + 1):
                trial = '%s_trial-%02d' % (subject, int(trial))
                pkl_path = '%s/%s/eeg/%s.pkl' % (dataset, subject, trial)
                with open(pkl_path, 'rb') as f:
                    yield pkl.load(f)
    def factory():
        return data_gen()
    return factory, labels

def print_info(dataset):
    f_name = '%s/%s' % (dataset, 'participants.tsv')
    with open(f_name, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter = '\t')
        for row in tsvin:
            print '\t'.join(row)

def dict_index(dictionary, tuple):
    values = {}
    for key, number in zip(dictionary.keys(), tuple):
        values.update({key: dictionary[key][number]})
    return values

def iterdim(a, axis=0) :
    a = np.asarray(a);
    leading_indices = (slice(None),)*axis
    for i in xrange(a.shape[axis]) :
        yield a[leading_indices+(i,)]

def get_param_dims(param_map):
    param_dims = map(lambda x: len(x), param_map.values())
    return param_dims
    

def time_str(unix_time):
    seconds = np.floor(unix_time / 1)
    minutes = np.floor(seconds / 60)
    seconds -= 60 * minutes
    hours = np.floor(minutes / 60)
    minutes -= 60 * hours
    days = np.floor(hours / 24)
    hours -= 24 * days
    return DATE_STRING % (days, hours, minutes, seconds)

def nested_generator_factory(factory, function, params):
    def nested_generator():
        for item in factory():
            yield function(item, params)
    return nested_generator

def nested_generator_factory_factory(init, functions, params):
    nfg = init
    for function in functions:
        nfg = nested_generator_factory(nfg, function, params)
    return nfg
