import pandas as pd
import set_keys
import os, sys
lib_path = os.path.abspath(os.path.join('..', 'pipeline', 'src'))
sys.path.append(lib_path)

from utils import meda

from app import app

from flask import (Flask,
                   redirect,
                   render_template,
                   request,
                   url_for,
                   send_from_directory,
                   jsonify)

import plotly.plotly as py
import plotly.graph_objs as go

from werkzeug import secure_filename

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

from markdown import markdown
import matplotlib.pyplot as plt
from utils.plots import (plot_timeseries,
                         make_3d_scatter,
                         make_spectrogram,
                         my_save_fig,
                         plotly_hack)
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import ast
import h5py
import pypandoc
import zipfile
import shutil

ALLOWED_EXTENSIONS = set(['mat', 'csv', 'txt'])


@app.route('/')
def root():
    return app.send_static_file('views/index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/analyze_data', methods=['GET', 'POST'])
def analyze_data():
    if request.method == 'POST':
        patient = request.json['name']

        set_args()

        out = ''
        #out += '<html><head><script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head><body>'

        # Create folder for results if doesn't exist
        # Also set path variables to save data to later
	res_path = "app/static/results/" + patient + '/'
	img_path = "app/static/results/" + patient + "/imgs/"
	if not os.path.exists(res_path):
	    os.makedirs(res_path)
	if not os.path.exists(img_path):
	    os.makedirs(img_path)

        fn = 'files/' + patient
        
        # Load data from file path
        d = make_h5py_object(fn)
        print "made it past files"

        # Wrap this patient's data.
        # Our functions take an array of patients,
        # but we are only doing one patient here.
        D = [d]

        # Clean the data
        clean_data, clean_report = clean(D)
        #out += clean_report
        eeg_data, times, coords = clean_data
        from utils.clean_data import get_electrode_coords
        cart = get_electrode_coords(D[0], coords = "euclidian")
        print "made it past clean"

        # We only have one patient for this example
        d = eeg_data[:, :, -1]
        t = times[:, :, -1]
        bad_chans, bad_report = detect_bad_channels(eeg_data)
        pool = 10 # How many electrodes to interp against?
        int_data, int_report = interpolate(eeg_data, coords,
				bad_chans, npts = pool)
        cct = [pd.DataFrame(data=d[:, x]) for x in range(d.shape[1])]
        df = pd.concat(cct, axis=1)
        #df.index = t
        df.columns = [str(x) for x in range(d.shape[1])]
        out += meda.full_report(df)

        #out += plotly_hack(fig)
        #correl = np.corrcoef(d.T)
	#data = [
	#    go.Heatmap(
	#	z = correl.T,
        #        colorbar=go.ColorBar(title='Correlation coefficient (rho)')
	#    )
	#]
	#layout = go.Layout(
	#    title='Electrode Pearson Correlation Matrix',
	#    xaxis=dict(
	#	title='Electrode',
	#	titlefont=dict(
	#	    family='Courier New, monospace',
	#	    size=18,
	#	    color='#7f7f7f'
	#	)
	#    ),
	#    yaxis=dict(
	#	title='Electrode',
        #        autorange='reversed',
	#	titlefont=dict(
	#	    family='Courier New, monospace',
	#	    size=18,
	#	    color='#7f7f7f'
	#	)
	#    )
        #)
	#fig = go.Figure(data=data, layout=layout)
	#fig['layout'].update(height = 800, width = 800, autosize=False)
	##out += plotly_hack(fig)
        ## Make and add the brain scatter plot to report
        #print "made it to here"

        #scat = plot_timeseries(data = d,
        #    time = t,
        #    selector = "random",
        #    title = "10 randomly selected electrodes from data.",
        #    start = 1500,
        #    end = 2000,
        #    skip = 1,
        #    randno = 10,
        #    xlab = r'$t$, in milliseconds',
        #    ylab = r'voltage in $mV$')

        ## Detect bad electrodes, plot them.
        #bad_chans, bad_report = detect_bad_channels(eeg_data)
        ##out += bad_report
        #bad_plot = plot_timeseries(data = d[:, bad_chans[0]],
        #    time = t,
        #    selector = "all",
        #    title = "Plot of the bad electrodes.",
        #    start = 1000,
        #    end = 2000,
        #    skip = 1,
        #    randno = 10,
        #    xlab = r'$t$, in milliseconds',
        #    ylab = r'voltage in $mV$')

        ## Interpolate bad electrodes
        #pool = 10 # How many electrodes to interp against?
        #int_data, int_report = interpolate(eeg_data, coords,
	#			bad_chans, npts = pool)
        #eeg_data, closest = int_data
        #print "made it to interp"
        ##out += int_report

        ## Plotting the interpolated electrodes
	##for l in range(len(closest[0])):
	##    #out += "\nInterpolating for channel: " + \
	##    #		str(bad_chans[0][l]) + '\n'
	##    #out +=  "\nInterpolating against: " + str(closest[0][l]) + '\n'
	##    inds = closest[0][l]
	##    d = np.column_stack([eeg_data[:, i, 0] for i in inds])
	##    d = np.column_stack([d, eeg_data[:, bad_chans[0][l], 0]])
	##    cols = ["red"] * pool
	##    cols.append("blue")
	##    tmp_fig = plot_timeseries(data = d,
#	#		  time = t,
#	#		  selector = "all",
#	#		  title = "Interpolated (blue) electrode with " + \
#	#		    " its " + str(pool) + " closest neighbors.",
#	#		  colors = cols,
#	#		  start = 100,
#	#		  end = 2000,
#	#		  skip = 10,
#	#		  xlab = r'$t$, in milliseconds',
#	#		  ylab = r'difference from mean' + \
#	#			    'voltage in $mV$')
#       #     title = "Interpolation of Electrode " + str(l)


        ## Reduce noise on data
        ##eeg_data_filtered, rn_report = reduce_noise(eeg_data)
        ##out += rn_report

        ## Plot spectrograms (before and after) for each channel
	##for i in range(5):#eeg_data.shape[1]):
        ##    fig = plt.figure()
        ##    fig.suptitle("Channel " + str(i), fontsize=10)
        ##    plt.subplot(211)	
        ##    make_spectrogram(eeg_data[:, i, 0], fig)
        ##    plt.subplot(212)	
        ##    make_spectrogram(eeg_data_filtered[:, i, 0], fig)
	##    plt.tight_layout()
	##    #plt.savefig(img_path + "spectrogram_channel_"+str(i)+".png")
        ##    plt.clf()
        ##    plt.close(fig)

        ##out += '</body></html>'

        ## Saving everything
        ##html_text = markdown(out, output_format='html5')
	with open(res_path + "report.html", 'w') as f:
		f.write(out)
        print "made it to writ ehtml"
	ziph = zipfile.ZipFile(res_path + '../full_out.zip',
                'w', zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk(res_path):
	    for file in files:
		print "zipping", root, file
		ziph.write(os.path.join(root, file))
	ziph.close()
        print "past zip"
        res_path = "/results/" + patient + "/"
        res = {
		'f_name': patient,
                'report': res_path + 'report.html',
                'zip': res_path + "full_out.zip"
            }
	return jsonify(res)
    else:
	abort(400)

@app.route('/gets3', methods=['GET', 'POST'])
def get_s3():
    if request.method == 'POST':
        set_args()
        local_path = 'files/' + request.json['name']
        print local_path
        if os.path.isfile(local_path):
            print "  there is already a file named: " + \
                    local_path + ", returned that path instead of pulling data."
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
    else:
	abort(400)

@app.route("/analyze", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return app.send_static_file('views/pages/analyze.html')

@app.route("/getHtml", methods=['GET', 'POST'])
def getHtml():
    if request.method == 'POST':
	with open('app/static/results/' + request.json["name"] + '/report.html', 'r') as f:
		html_data = f.read()
		return html_data
	 
