import numpy as np
import os
import StringIO
from kurt import *
from helper import *
import matlab.engine

currwd = os.getcwd()
os.chdir("/home/nitin/hopkins/neurodata/orange-panda/notes/bad_chan_detect")

eng = matlab.engine.start_matlab()


# List all patient names
patient_names = [
#   "gp_A00051826001",
#   "bip_A00053375001",
#   "gip_A00051955001",
#   "gip_A00053440001",
#   "gip_A00054417001",
#   "bip_A00054215001",
#   "gip_A00054207001",
    "gp_A00054039001"
]

incorrect_patients = []
incorrect_elec_patients = []

for name in patient_names:
    out = StringIO.StringIO()
    outfile = open("/home/nitin/hopkins/neurodata/nicolas/analysis/" + name + "_kurt.txt", "w")
    
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

    load_dat = np.load("/home/nitin/hopkins/neurodata/nicolas/numpy/" + name + "_kurt.npz")
    test_glob_dat = np.reshape(test_dat, (test_dat.shape[0], test_dat.shape[1] * test_dat.shape[2]))
    out = StringIO.StringIO()
    mat_glob_kurt, mat_glob_rej = eng.rejkurt(to_matlab_comp(test_glob_dat, eng), 3, [], 3, nargout = 2)
    print "MATLAB Global Done"
    mat_glob_kurt = np.asarray(mat_glob_kurt)
    mat_glob_rej = np.asarray(mat_glob_rej)
    py_glob_kurt, py_glob_rej = kurt_baddetec(test_glob_dat, [3])
    np.savez("/home/nitin/hopkins/neurodata/nicolas/numpy/" + name + "_kurt.npz", py_kurt=load_dat['py_kurt'], py_rej=load_dat['py_rej'], mat_kurt=load_dat['mat_kurt'], mat_rej=load_dat['mat_rej'], py_glob_kurt=py_glob_kurt, py_glob_rej=py_glob_rej, mat_glob_kurt=mat_glob_kurt, mat_glob_rej=mat_glob_rej)
