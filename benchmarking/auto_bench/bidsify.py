import numpy as np
import os
import cPickle as pkl
import glob
import sys
import csv

def fast_csv_load(f_path):
    with open(f_path,'r') as dest_f:
        data_iter = csv.reader(dest_f, 
                               delimiter = ',', 
                               quotechar = '"')
        data = [data for data in data_iter]
    data_array = np.asarray(data, dtype = np.float32)  
    return data_array

def make_file_structure(set_name, num_subjects):
    subj_names = []
    os.makedirs(set_name)
    for i in range(1, num_subjects + 1):
        subj_name = 'sub-%04d' % (i)
        os.makedirs(set_name + '/' + subj_name)    
        os.makedirs(set_name + '/' + subj_name + '/eeg/')
        subj_names.append(subj_name)
    return subj_names

def raw_paths(path):
    subjs = glob.glob(path + '/*')
    file_paths = []
    for sub in subjs:
        all_paths = glob.glob(sub + '/EEG/raw/csv_format/*')
        filtered_paths = filter(lambda x: '_events' not in x, all_paths)
        file_paths.append(filtered_paths)
    return file_paths 

def preprocessed_paths(path):
    subjs = glob.glob(path + '/*')
    file_paths = []
    for sub in subjs:
        all_paths = glob.glob(sub + '/EEG/preprocessed/csv_format/*')
        filt = lambda x: '_interpolated' not in x and '_events' not in x
        filtered_paths = filter(filt, all_paths)
        file_paths.append(filtered_paths)
    return file_paths 

def move(paths, path2):
    for sub_number, subject in enumerate(paths, start=1):
        sub_id = 'sub-%04d' % sub_number
        bids_base = '%s/%s' % (path2, sub_id)
        for trial_number, path in enumerate(subject, start=1):
            d = fast_csv_load(path)
            print 'Converting file at', path

            fmt = (bids_base, 'eeg', sub_id, trial_number) 
            f_path = '%s/%s/%s_trial-%02d.pkl' % fmt
            print 'Saving converted at', f_path
            with open(f_path, 'wb') as f:
                pkl.dump(d, f, protocol = pkl.HIGHEST_PROTOCOL)

def participants(path, heads, rows):
    with open(path + '/participants.tsv', 'w') as f:
        f.write('\t'.join(heads) + '\n')
        for row in rows:
            f.write('\t'.join(row) + '\n')

def fake_data_set(set_name):
    subj_names = []
    os.makedirs(set_name)
    for i in range(1, 4 + 1):
        subj_name = 'sub-%04d' % (i)
        os.makedirs(set_name + '/' + subj_name)    
        os.makedirs(set_name + '/' + subj_name + '/eeg/')
        for i in range(1, 3 + 1):
            trial = os.path.join(set_name,
                                 subj_name,
                                 'eeg',
                                 subj_name + '_trial-%02d.pkl' % (i))
            ra = np.random.normal(0, 1, (10, 1000))
            pkl.dump(ra, open(trial, 'wb'), pkl.HIGHEST_PROTOCOL)
        subj_names.append(subj_name)
    return subj_names

if __name__ == '__main__':
    _, command, frm, to = sys.argv
    paths = None
    if command == 'fake':
        subjects = fake_data_set('fake_data')
        num_trials = map(str, [3, 3, 3, 3])
        participants('fake_data', ['participant_id', 'num_trials'],
                     zip(subjects, num_trials))
    elif command == 'bids_raw':
        paths = raw_paths(frm)
    elif command == 'bids_interpolated':
        paths = preprocessed_paths(frm)
    if paths is None:
        print 'Did not work, bad command'
        sys.exit(0)
    num_subjects = len(paths)
    num_trials = [str(len(x)) for x in paths]
    subjects = make_file_structure(to, num_subjects)
    move(paths, to)
    participants(to, ['participant_id', 'num_trials'],
                 zip(subjects, num_trials))
