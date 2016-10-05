import numpy as np
import ast
from utils.get_data import get_record, get_patients, make_h5py_object
from utils.clean_data import get_eeg_data, get_times, get_electrode_coords

NUM_PATIENTS = 59 # Half of total, randomly selected


def acquire_data():
    """
        Getting the data from AWS, or from local /utils/tmp. 
        Require: patients list, record_num, record_type args
        Ensure: list of h5py data objects of EEG data
    """
    pat_map = get_patients()
    patients = None
    if args["patients"] is not None:
        patients = args["patients"]
    else:
        patients = range(NUM_PATIENTS)
    d = [] * len(patients)
    for p in patients:
        p_filepath = get_record(pat_map[p], args["record_num"],
                            args["record_type"]) 
        d.append(make_h5py_object(p_filepath))
    return d

def clean(D):
    C = []
    for d in D:
        tmp = {}
        tmp["eeg"] = get_eeg_data(d)
        print "  cleaned eeg data..."
        tmp["times"] = get_times(d)
        print "  cleaned timescale data..."
        tmp["coords"] = get_electrode_coords(d, args["coords"])
        print "  cleaned electrode " + args["coords"] +\
                    " coordinate data..."
        C.append(tmp)
    print "  shaping data..."
    eeg_data = np.dstack([subject["eeg"] for subject in C])
    times = np.dstack([subject["times"] for subject in C])
    electrodes = np.dstack([subject["coords"] for subject in C])
    return eeg_data, times, electrodes

def detect_bad_channels(D):
    """
        DETECT BAD CHANNELS...
        Require: D
        Ensure: L - list of bad electrode channels
    """
    L = []
    return L

def interpolate(D, L):
    """
        INTERPOLATE BAD CHANNELS...
        Require: D, L
        Ensure: D' - D with bad channels interpolated
    """
    return D

def EOG_regress():
    pass

def reduce_noise(D):
    D_with_less_noise = D
    return D_with_less_noise


def main():
    start = """
TEAM ORANGE PANDA
EEG PIPELINE
...
BEGIN

"""
    print start
    print "GETTING DATA..."
    D = acquire_data()
    print "CLEANING DATA..."
    eeg_data, times, electrodes = clean(D)
    np.testing.assert_equal(eeg_data.shape, (176000, 111, 1))
    np.testing.assert_equal(times.shape, (176000, 1, 1))
    np.testing.assert_equal(electrodes.shape, (111, 3, 1))

if __name__ == '__main__':
    global args
    args = {}
    with open("pipeline.conf") as f:
        args = ast.literal_eval(f.read())
    main()
