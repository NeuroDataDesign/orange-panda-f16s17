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
    "gp_A00051826001",
    "bip_A00053375001",
    "gip_A00051955001",
    "gip_A00053440001",
    "gip_A00054417001",
    "bip_A00054215001",
    "gip_A00054207001",
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
    if not os.path.isfile("/home/nitin/hopkins/neurodata/nicolas/numpy/" + name + ".npz"):
        print "From scratch!"
        # get patient data
        patient, time, zero = list(get_patient(name + ".mat")[i] for i in [0, 1, 4])
        # get rid of 0 electrodes
        test_dat = patient[:, list(set(range(111)) - set(zero))]
        # reshape data with trials
        num_trials = 4
        test_dat = trials(test_dat, num_trials)
        mat_test_dat = np.swapaxes(test_dat, 1, 2)

        mat_jp, mat_rej = eng.jointprob(to_matlab_comp(mat_test_dat, eng), 3, [], 1, 1000.0, nargout = 2, stdout = out)
        print "MATLAB Done"
        py_jp, py_rej = jointprob(test_dat, [3], np.asarray([]), 1, 1000)
        print "Python Done"
        mat_jp = np.asarray(mat_jp)
        mat_rej = np.asarray(mat_rej)
        np.savez("/home/nitin/hopkins/neurodata/nicolas/numpy/" + name, py_jp=py_jp, py_rej=py_rej, mat_jp=mat_jp, mat_rej=mat_rej)
        print "File saved!"
    else:
        print "Grabbing from saved!"
        load_dat = np.load("/home/nitin/hopkins/neurodata/nicolas/numpy/" + name + ".npz")
        py_jp = load_dat['py_jp']
        py_rej = load_dat['py_rej']
        mat_jp = load_dat['mat_jp']
        mat_rej = load_dat['mat_rej']
    # See results
    outfile.write(name)
    outfile.write("Shapes Equal?: " + str(py_jp.shape == mat_jp.shape) + "\n")
    outfile.write("Python head\n")
    outfile.write(str(py_jp[0:2,:]) + "\n");
    outfile.write("MATLAB Head\n");
    outfile.write(str(mat_jp[0:2,:]) + "\n");
    outfile.write("MATLAB has any NaNs?: " + str(np.isnan(mat_jp).any()) + "\n")
    outfile.write("Python has any NaNs?:" + str(np.isnan(py_jp).any()) + "\n")
    outfile.write("Arrays close (.1) tolerance?: " + str(np.isclose(py_jp, mat_jp, atol=.1).all()) + "\n")
    if not np.isclose(py_jp, mat_jp, atol=.1).all():
        incorrect_patients.append(name)
    outfile.write("All electrode/trial rejections the same?: " + str(np.array_equal(py_rej, mat_rej)) + "\n")
    if not np.array_equal(py_rej, mat_rej):
        incorrect_elec_patients.append(name)
    py_bad = []
    mat_bad = []
    for i in range(py_rej.shape[0]):
        if py_rej[i].any():
            py_bad.append(i)
        else:
            mat_bad.append(i)
    outfile.write("Python bad: " + str(py_bad) + "\n")
    outfile.write("MATLAB bad: " + str(mat_bad) + "\n")

    outfile.close()

outfile = open("/home/nitin/hopkins/neurodata/nicolas/analysis/overall.txt", "w")
outfile.write("Patients with incorrect joint prob:\n")
outfile.write(str(incorrect_patients) + "\n")
outfile.write("Patients with incorrect rejections:\n")
outfile.write(str(incorrect_elec_patients) + "\n")

os.chdir(currwd)
