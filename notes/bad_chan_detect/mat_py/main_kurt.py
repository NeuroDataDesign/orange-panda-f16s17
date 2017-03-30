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
    outfile = open("/home/nitin/hopkins/neurodata/nicolas/analysis/" + name + ".txt", "w")
    
    py_jp = []
    py_rej = []
    mat_jp = []
    mat_rej = []
    if not os.path.isfile("/home/nitin/hopkins/neurodata/nicolas/numpy/" + name + "_kurt.npz"):
        print "From scratch!"
        # get patient data
        patient, time, zero = list(get_patient(name + ".mat")[i] for i in [0, 1, 4])
        # get rid of 0 electrodes
        test_dat = patient[:, list(set(range(111)) - set(zero))]
        # reshape data with trials
        num_trials = 4
        test_dat = trials(test_dat, num_trials)
        mat_test_dat = np.swapaxes(test_dat, 1, 2)
        mat_kurt, mat_rej = eng.rejkurt(to_matlab_comp(mat_test_dat, eng), 3, [], 1, nargout = 2)
        mat_kurt = np.asarray(mat_kurt)
        mat_rej = np.asarray(mat_rej)
        print "MATLAB Local Done"
        py_kurt, py_rej = kurt_baddetec(test_dat[0], [3])
        print "Python Local Done"
        diff_kurt = abs(py_kurt - mat_kurt)
        test_glob_dat = np.reshape(test_dat[0], (test_dat[0].shape[0], test_dat[0].shape[1] * test_dat[0].shape[2]))
        out = StringIO.StringIO()
        mat_glob_kurt, mat_glob_rej = eng.rejkurt(to_matlab_comp(test_glob_dat, eng), 1, [], 3, nargout = 2)
        print "MATLAB Global Done"
        mat_glob_kurt = np.asarray(mat_glob_kurt)
        mat_glob_rej = np.asarray(mat_glob_rej)
        py_glob_kurt, py_glob_rej = kurt_baddetec(test_glob_dat, [1])
        np.savez("/home/nitin/hopkins/neurodata/nicolas/numpy/" + name, py_kurt=py_kurt, py_rej=py_rej, mat_kurt=mat_kurt, mat_rej=mat_rej, py_glob_kurt=py_glob_kurt, py_glob_rej=py_glob_rej, mat_glob_kurt=mat_glob_kurt, mat_glob_rej=mat_glob_rej)
        print "File saved!"
    else:
        print "Grabbing from saved!"
        load_dat = np.load("/home/nitin/hopkins/neurodata/nicolas/numpy/" + name + "_kurt.npz")
        py_jp = load_dat['py_jp']
        py_rej = load_dat['py_rej']
        mat_jp = load_dat['mat_jp']
        mat_rej = load_dat['mat_rej']
        diff_kurt = abs(py_kurt - mat_kurt)
    # See results
    diff_kurt = abs(py_kurt - mat_kurt)
    outfile.write("Max Difference" + str(np.max(diff_kurt)) + "\n")
    outfile.write("Min Difference" + str(np.min(diff_kurt)) + "\n")
    outfile.write("Mean Difference" + str(np.mean(diff_kurt)) + "\n")
    outfile.write("Mean Python" + str(np.mean(abs(py_kurt))) + "\n")
    outfile.write("Mean MATLAB" + str(np.mean(abs(mat_kurt))) + "\n")
    outfile.write("Same bad elecs" + str(np.array_equal(py_rej[0], np.asarray(mat_rej))) + "\n")
    outfile.write(mat_rej.any())
    outfile.write(np.where(np.any(py_rej[0], axis = 1)))
    bad_elecs = np.where(np.any(py_rej[0], axis = 1))
    outfile.write("Global Kurtoses within .1?:" + str(np.isclose(py_glob_kurt, mat_glob_kurt, atol=.1).all()) + "\n")
    outfile.write("Rejected electrodes the same?:" + str(np.array_equal(py_glob_rej[0], mat_glob_rej)) + "\n")
    py_bad = []
    mat_bad = []
    for i in range(py_glob_rej[0].shape[0]):
        if py_glob_rej[0][i].any():
            py_bad.append(i)
    for i in range(mat_glob_rej.shape[0]):
        if mat_glob_rej[i].any():
            mat_bad.append(i)
    outfile.write("Electrodes found by Python but not MATLAB:" + str(set(py_bad) - set(mat_bad)) + "\n")
    outfile.write("Electrodes found by MATLAB but not Python:" + str(set(mat_bad) - set(py_bad)) + "\n")
    outfile.write("Electrodes found by Python:" + str(py_bad) + "\n")
    outfile.write("Electrodes found by MATLAB:" + str(mat_bad) + "\n")

    outfile.close()

outfile = open("/home/nitin/hopkins/neurodata/nicolas/analysis/overall.txt", "w")
outfile.write("Patients with incorrect joint prob:\n")
outfile.write(str(incorrect_patients) + "\n")
outfile.write("Patients with incorrect rejections:\n")
outfile.write(str(incorrect_elec_patients) + "\n")

os.chdir(currwd)
