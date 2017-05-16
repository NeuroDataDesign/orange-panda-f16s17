import numpy as np
import os
import StringIO
from joint_prob import *
from helper import *
import matlab.engine

currwd = os.getcwd()
os.chdir("/home/nitin/hopkins/neurodata/orange-panda/notes/bad_chan_detect")

eng = matlab.engine.start_matlab()

# List all patient names
patient_names = [
    "gp_A00051826001"
]

incorrect_patients = []
incorrect_elec_patients = []

# function [EEG, locthresh, globTmp, globthresh, nrej, com] = pop_jointprob( EEG, icacomp, elecrange, ...
#                        		locthresh, globthresh, superpose, reject, vistype, topcommand,plotflag);

for name in patient_names:
    out = StringIO.StringIO()
    outfile = open("/home/nitin/hopkins/neurodata/nicolas/analysis/" + name + ".txt", "w")
    
    py_jp = []
    py_rej = []
    mat_jp = []
    mat_rej = []
    
    # get patient data
    patient, time, zero = list(get_patient(name + ".mat")[i] for i in [0, 1, 4])
    # get rid of 0 electrodes
    test_dat = patient[:, list(set(range(111)) - set(zero))]
    # reshape data with trials
    num_trials = 4
    test_dat = trials(test_dat, num_trials)

    load_dat = np.load("/home/nitin/hopkins/neurodata/nicolas/numpy/" + name + ".npz")

    test_glob_dat = np.reshape(test_dat, (test_dat.shape[0], test_dat.shape[1] * test_dat.shape[2]))
    out = StringIO.StringIO()
    mat_jp_mat, mat_glob_jp, mat_glob_rej = eng.jointprob(to_matlab_comp(test_glob_dat, eng), 3, [], 1, 1000.0, nargout=2, stdout=out)
    print out.getvalue()
    print "MATLAB Global Done"
    np.savez("/home/nitin/hopkins/neurodata/nicolas/numpy/test.npz", mat_jp_mat=mat_jp_mat, mat_glob_jp=mat_glob_jp, mat_glob_rej=mat_glob_rej)
#   mat_glob_jp = np.asarray(mat_glob_jp)
#   mat_glob_rej = np.asarray(mat_glob_rej)
#   py_glob_jp, py_glob_rej = jointprob(test_glob_dat, [3], np.asarray([]), 1, 1000)
    print name, "Done!"
