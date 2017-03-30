import numpy as np
import h5py
import os
import scipy.io

# return tuple of patient info
def get_patient(filename):
    curr_wd = os.getcwd()
    os.chdir("/home/nitin/hopkins/neurodata/nicolas")
    elec_range = range(0, 111)
    # get data
    D = h5py.File(filename, 'r')
    patient = D["EEG"]["data"][:, :]
    time = D["EEG"]["times"][:]
    nic_auto_bad = D["auto_badchans"][:]
    nic_man_bad = D["man_badchans"][:]
    # get zero elecs
    zero_elec = []
    for i in range(patient.shape[1]):
        is_zero = True
        for j in range(500):
            if patient[j, i] != 0:
                is_zero = False
        if is_zero:
            zero_elec.append(i)
    
    # make it 0-indexed
    nic_auto_bad = [int(x) - 1 for x in nic_auto_bad if x != 0]
    nic_man_bad = [int(x) - 1 for x in nic_man_bad if x != 0]
    # get good electrodes
    good_elec = set(elec_range).difference(nic_auto_bad).difference(nic_man_bad).difference(zero_elec)
    os.chdir(curr_wd)
    return patient, time, nic_auto_bad, nic_man_bad, zero_elec, good_elec

# define function to segregate data into separate trials
def trials(l, n):
    print l.shape[0]
    print l.shape[1]
    num = len(l)/n
    print num * n
    l = l[:(num * n),:]
    ret_arr = np.reshape(l, (n, len(l)/n, l.shape[1]))
    ret_arr = np.rollaxis(ret_arr, 2)
    return ret_arr

def to_matlab_comp(mat, eng):
    currwd = os.getcwd()
    os.chdir("/home/nitin/hopkins/neurodata/orange-panda")
    scipy.io.savemat('notes/bad_chan_detect/temp/test.mat', mdict = {"arr":mat})
    loaded_mat = eng.load(os.getcwd() + '/notes/bad_chan_detect/temp/test.mat')
    data = eng.double(loaded_mat.values()[0])
    os.chdir(currwd)
    return data
