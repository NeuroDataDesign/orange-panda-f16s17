# coding: utf-8
import matplotlib as mpl
# For Cortex Matplotlib
mpl.use('Agg')

# bae
import numpy as np
import matplotlib.pyplot as plt

# Import benchmarking things
import bench.dataset_creation as dc
import bench.utilities as ut
import bench.discriminibility as disc
import bench.disc_set as d_set

# Import actual methods
import methods.denoise as den
import methods.bad_chans as bad_chans
import methods.viz as viz
import methods.interpolation as inter

# Import operating system utilities
import os
from pathos.multiprocessing import ProcessingPool as Pool
import cPickle as pkl

# Make the current working directory the one with the data
os.chdir('../data')

# True if plot
PLOT = True
DOWNSAMPLE = 1

# Set our dataset
DATASET = "bids_raw_demo"

# Num cores
NCORE = 8

# Get a factory which will generate the data (from disc)
factory, labels = ut.data_generator_factory(DATASET)

# Disc
def my_disc(D):
	return disc.disc_all(D, labels, d_set.TRANSFORMS,
						 d_set.METRICS, d_set.NAMES)

# Define a round function
def round(D, f, pars):
	# A multiprocessor
	par = Pool(NCORE)
	print
	print
	print 'Applying', f.__name__

	D = par.imap(lambda d: f(d[0], d[1], pars), D)
	D = [d for d in D]
	step_discs = my_disc([d[0] for d in D])
	if PLOT:
		D = [viz.visualize_matrix(d[0], d[1], pars) for d in D]
	return (D, step_discs)


# Mean center and record max and min value in matrix (for plotting)
def setup(D, p_local, p_global):
        D = D[:, ::DOWNSAMPLE]
	D = D - np.mean(D, axis = 1).reshape(-1, 1)
        zero_chans = []
	p_local['max'] = np.max(D)
	p_local['min'] = np.min(D)
        eeg_chans = np.setdiff1d(np.arange(D.shape[0]), den.EOG_CHANS)
        p_local['eeg_chans'] = eeg_chans
        p_local['eog_chans'] = den.EOG_CHANS
	return (D, p_local)

# Set pipeline structure (order of functions applied)
fs = [setup,
  den.highpass,
  den.bandstop,
  bad_chans.bad_detec,
  inter.wavelet_coefficient_interp,
  den.eog_regress,
  den.rpca_denoise]

# Get channel locations
with open(DATASET + '/chan_locs.pkl', 'r') as f:
	chan_locs = pkl.load(f)

# Set pipeline parameters
params = {
	'p_global': {
		 'hpf': {
			 'order': 4,
			 'Fs': 500 * DOWNSAMPLE,
			 'cutoff': .1
		 },
		 'bsf': {
			 'order': 4,
			 'Fs': 500 * DOWNSAMPLE,
			 'cutoff': [59, 61]
		 },
		'rpca': {
			'max_iter': 10,
			'verbose': True,
			'pca_method': 'randomized',
			'delta': 1e-7,
			'mu': None
		},
		'bad_detec': {
			'thresh': 3,
			'measure': ['prob', 'kurtosis'],
			'normalize': 0,
			'discret': 1000,
			'verbose': PLOT,
			'trim': None
		},
		'inter': {
		    'chan_locs': chan_locs,
		    'loc_unit': 'radians',
                    'verbose': False,
                    'k': 5,
                    'wave': 'db2'
		}
	}
}

# Unpack the generator to get a 'data array'
# This is actually a list of functions which returns a data
D = [d for d in factory()]

# Keep track of discriminibility as we take steps in the pipeline
level_discs = []

# Apply each function and get the discriminibility.
for f in fs:
	for d in D:
		d[1]['function_name'] = f.__name__

	D, step_disc = round(D, f, params['p_global'])
	level_discs.append(step_disc)

	# Increase the step variable in the metadata
	for d in D:
		d[1]['step'] = d[1]['step'] + 1


f_names = map(lambda x: x.__name__, fs)

# Save disc plot
disc.disc_plot(level_discs, d_set.NAMES, f_names)
plt.savefig('figs/level_discs.png')

# Save the results
with open('results.pkl', 'w') as f:
	import cPickle as pkl
	pkl.dump(level_discs, f)
	print 'Saved at results.pkl'

