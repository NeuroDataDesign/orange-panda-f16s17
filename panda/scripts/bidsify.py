import numpy as np
import os
import cPickle as pkl
import glob
import sys
import csv

def make_file_structure(set_name, num_subjects):
    subj_names = []
    try:
        os.makedirs(set_name)
    except:
        print 'Directory already exists! You should probably delete it.'
    for i in range(1, num_subjects + 1):
        subj_name = 'sub-%04d' % (i)
        os.makedirs(set_name + '/' + subj_name)    
        subj_names.append(subj_name)
    return subj_names

def participants(path, heads, rows):
    with open(path + '/participants.tsv', 'w') as f:
        f.write('\t'.join(heads) + '\n')
        for row in rows:
            f.write('\t'.join(row) + '\n')

def fake_dataset(set_name, t, s):
    subj_names = []
    make_file_structure(set_name, s)
    for i in range(1, s + 1):
        subj_name = 'sub-%04d' % (i)
        for j in range(1, t + 1):
            trial = os.path.join(set_name,
                                 subj_name,
                                 'eeg',
                                 subj_name + '_trial-%02d.pkl' % (j))
            ra = np.random.normal(0, 1, (128, 20000))
            ra2 = np.sin(2 * np.pi * np.linspace(0, 10, 20000) * np.random.random() * 4)
            ra = ra + ra2
            pkl.dump(ra, open(trial, 'wb'), pkl.HIGHEST_PROTOCOL)
        subj_names.append(subj_name)
    num_trials = map(str, [t] * s)
    participants(set_name, ['participant_id', 'num_trials'],
                     zip(subj_names, num_trials))

def derivative_set(dataset, derivitives, name):
    info = participant_info(dataset)
    num_subjects = len(info)
    set_name = dataset + '_' + name
    make_file_structure(set_name, num_subjects)
    i = 0
    for sub in range(num_subjects):
        subj_name = info[sub][0]
        num_trials = int(info[sub][1])
        for t in range(1, num_trials + 1):
            trial = os.path.join(set_name,
                                 subj_name,
                                 'eeg',
                                 subj_name + '_trial-%02d.pkl' % (t))
            pkl.dump(derivitives[i], open(trial, 'wb'),
                     pkl.HIGHEST_PROTOCOL)
            i = i + 1
    participants(set_name, ['participant_id', 'num_trials'], info)

def participant_info(dataset, pprint = False):
    f_name = '%s/%s' % (dataset, 'participants.tsv')
    participants = []
    with open(f_name, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter = '\t')
        next(tsvin, None)
        for row in tsvin:
            participants.append(row)
    return participants

def print_participant_info(dataset):
    f_name = '%s/%s' % (dataset, 'participants.tsv')
    with open(f_name, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter = '\t')
        for row in tsvin:
            print '\t'.join(row)