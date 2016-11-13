import os
import pickle
from main import (set_args,
                  clean) 
from utils.clean_data import (get_eeg_data,
                              get_times,
                              get_electrode_coords)
from preprocessing.interp import interpolate
from preprocessing.baddetec import bad_chan_detect
from preprocessing.noise_reduct import reduce_noise
from utils.get_data import make_h5py_object
import pandas as pd

def prep_data(file_path, token):
	f_name, ext = os.path.splitext(file_path)
	if token == "pickled_pandas":
		return
	if token == "fcp_indi_eeg":
		return eeg_prep(f_name, ext)


def eeg_prep(f_name, ext):
    html = ''
    set_args()
    d = make_h5py_object(f_name + ext)
    html += "<h1> Preprocessing Report for " + os.path.basename(f_name) + "</h1>"
    # Wrap this patient's data.
    D = [d]
    # Clean the data
    clean_data, clean_report = clean(D)
    html += clean_report
    eeg_data, times, coords = clean_data
    # simulate a time / channes / trials / patients data frame
    eeg_data = eeg_data.reshape(eeg_data.shape[0], eeg_data.shape[1],
                                1, eeg_data.shape[2])
    bad_chans, bad_report = bad_chan_detect(eeg_data[::1000], "KDE", threshold=3)
    html += bad_report
    pool = 10 # How many electrodes to interp against?
    int_data, int_report = interpolate(eeg_data,
                                      'Inv_GC',
                                      bad_chans,
                                      coords = coords,
                                      times = times,
                                      npts = pool)
    html += int_report
    eeg_data, red_report = reduce_noise(eeg_data, 'placeholder')
    html += red_report
    d = eeg_data[:, :, -1]
    t = times[:, :, -1]
    cct = [pd.DataFrame(data=d[:, x]) for x in range(d.shape[1])]
    df = pd.concat(cct, axis=1)
    df.columns = [str(x) for x in range(d.shape[1])]
    df.index = map(lambda x: x[0]/1000.0, t)
    with open(f_name + '.pkl', 'wb') as f:
    	pickle.dump(df, f)
    return html

