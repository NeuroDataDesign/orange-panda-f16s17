import pandas as pd
from main import (set_args,
                  clean,
                  detect_bad_channels,
                  interpolate,
                  reduce_noise,
                  acquire_data) 
from utils.get_data import make_h5py_object
from utils.clean_data import (get_eeg_data,
                              get_times,
                              get_electrode_coords)
from utils.fourier import (butter_highpass_filter,
                           butter_lowpass_filter,
                           butter_bandstop_filter)
from preprocessing.interp import (fit_sphere,
                                  gc,
                                  gc_invdist_interp)
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import h5py
import plotly.plotly as py
import plotly.graph_objs as go
from utils import meda
import set_keys
import os, sys
import ast
import zipfile

def get_s3(req):
    set_args()
    local_path = 'files/' + req['name']
    print local_path
    if os.path.isfile(local_path):
        return 'ok!'
    conn = S3Connection(os.environ['AWS_ACCESS_KEY'],
            os.environ['AWS_SECRET_KEY'])
    bucket = conn.get_bucket(request.json['bucket'], validate=False)
    s3path = request.json['fpath']
    print s3path
    key = Key(bucket, s3path)
    f = file(local_path, 'wb')
    def callback(togo, total):
        print "Got {0: 10d} Bytes out of {1:10d} Bytes".format(togo, total)
        if togo == total:
            print "Done! The path of the .mat file was returned."
    key.get_file(f, cb = callback)
    print request.json
    return 'ok !'

def make_meda_html(patient):
    set_args()
    fn = 'files/' + patient
    # Load data from file path
    d = make_h5py_object(fn)
    # Wrap this patient's data.
    D = [d]
    # Clean the data
    clean_data, clean_report = clean(D)
    eeg_data, times, coords = clean_data
    cart = get_electrode_coords(D[0], coords = "euclidian")
    # We only have one patient for this example
    d = eeg_data[::100, :, -1]
    t = times[::100, :, -1]
    #bad_chans, bad_report = detect_bad_channels(ed)
    #pool = 10 # How many electrodes to interp against?
    #int_data, int_report = interpolate(ed, coords,
    #               bad_chans, npts = pool)
    cct = [pd.DataFrame(data=d[:, x]) for x in range(d.shape[1])]
    df = pd.concat(cct, axis=1)
    df.columns = [str(x) for x in range(d.shape[1])]
    return meda.full_report(df)

def save_analysis(html_report, patient):
    # Create folder for results if doesn't exist
    # Also set path variables to save data to later
    res_path = "app/static/results/" + patient + '/'
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    with open(res_path + "report.html", 'w') as f:
        f.write(html_report)
    ziph = zipfile.ZipFile(res_path + '../' + patient + '.zip',
                'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(res_path):
        for file in files:
            ziph.write(os.path.join(root, file))
    ziph.close()
    res_path = "/results/" + patient + "/"
    res = {
    'f_name': patient,
            'report': res_path + 'report.html',
            'zip': 'results/' + patient + ".zip"
        }
    return res
