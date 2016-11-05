import os
import pickle
from main import (set_args,
                  clean,
                  detect_bad_channels,
                  interpolate,
                  reduce_noise,
                  acquire_data) 
from utils.clean_data import (get_eeg_data,
                              get_times,
                              get_electrode_coords)
from preprocessing.interp import (fit_sphere,
                                  gc,
                                  gc_invdist_interp)
from utils.get_data import make_h5py_object
import pandas as pd

def format_data(file_path, token):
	f_name, ext = os.path.splitext(file_path)
	if token == "pickled_pandas":
		return
	if token == "fcp_indi_eeg":
		eeg_format(f_name, ext)


def eeg_format(f_name, ext):
    set_args()
    d = make_h5py_object(f_name + ext)
    # Wrap this patient's data.
    D = [d]
    # Clean the data
    clean_data, clean_report = clean(D)
    eeg_data, times, coords = clean_data
    cart = get_electrode_coords(D[0], coords = "euclidian")
    # We only have one patient for this example
    d = eeg_data[::100, :, -1]
    t = times[::100, :, -1]
    cct = [pd.DataFrame(data=d[:, x]) for x in range(d.shape[1])]
    df = pd.concat(cct, axis=1)
    df.columns = [str(x) for x in range(d.shape[1])]
    print t.shape
    df.index = map(str, t)
    with open(f_name + '.pkl', 'wb') as f:
    	pickle.dump(df, f)

    #bad_chans, bad_report = detect_bad_channels(ed)
    #pool = 10 # How many electrodes to interp against?
    #int_data, int_report = interpolate(ed, coords,
    #               bad_chans, npts = pool)
