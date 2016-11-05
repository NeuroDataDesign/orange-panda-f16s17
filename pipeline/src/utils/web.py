import pickle
import pandas as pd
from utils.get_data import make_h5py_object
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
from utils.formatting_scripts import format_data

RESULTS='app/static/results/'

def get_s3(req):
    f_name, extension = os.path.splitext(req['fpath'])
    local_path = 'files/' + req['name'] + extension
    if os.path.isfile(local_path):
        format_data(local_path, 'eeg')
        return 'ok!'
    conn = S3Connection(os.environ['AWS_ACCESS_KEY'],
            os.environ['AWS_SECRET_KEY'])
    bucket = conn.get_bucket(req['bucket'], validate=False)
    s3path = req['fpath']
    key = Key(bucket, s3path)
    f = file(local_path, 'wb')
    def callback(togo, total):
        print "Got {0: 10d} Bytes out of {1:10d} Bytes".format(togo, total)
        if togo == total:
            print "Done! The path of the " + req['name'] + \
            		" file was returned."
    key.get_file(f, cb = callback)
    f.close()
    format_data(local_path, req['token'])
    return 'ok !'

def make_meda_html(file_name):
    fn = 'files/' + file_name + '.pkl'
    # Load data from file path
    with open(fn, 'rb') as f:
    	df = pickle.load(f)
    return meda.full_report(df)

def save_analysis(html_report, patient):
    # Create folder for results if doesn't exist
    # Also set path variables to save data to later
    res_path = RESULTS + patient + '/'
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

def _make_res(name):
    res = {
    'f_name': name,
            'report': '/results/' + name + '/report.html',
            'zip': 'results/' + name + '.zip'
        }
    return res
def populate_table():
    for root, dirs, files in os.walk(RESULTS):
        return map(lambda x: _make_res(x), dirs)

