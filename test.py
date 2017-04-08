# coding: utf-8
import bench.dataset_creation as dc
import bench.disc_set as d_set
import bench.utilities as ut
import bench.discriminibility as disc
import methods.denoise as den
import methods.viz as viz
import methods.bad_chans as bad_chans
import os
from pathos.multiprocessing import ProcessingPool as Pool
import numpy as np

os.chdir('../data')
factory, labels = ut.data_generator_factory('fake_data')
params = {
	'p_global': {
	     'hpf': {
	         'order': 4,
	         'Fs': 500,
	         'cutoff': .1
	     },
	     'bsf': {
	         'order': 4,
	         'Fs': 500,
	         'cutoff': [59, 61]
	     },
		'rpca': {
		    'max_iter': 15,
		    'verbose': True,
		    'pca_method': 'randomized',
		    'delta': 1e-5,
		    'mu': .75
		},
		'bad_detec': {
		    'thresh': 3,
		    'measure': ['prob', 'kurtosis'],
		    'normalize': 0,
		    'discret': 1000,
		    'verbose': False,
		    'trim': .1
		}
	}
}
level_discs = []

def my_disc(D):
	return disc.disc_all(D, labels, d_set.TRANSFORMS,
		                 d_set.METRICS, d_set.NAMES)

def round(D, f, pars):
	D = [f(d[0], d[1], pars) for d in D]
	step_discs = my_disc([d[0] for d in D])
	D = [viz.visualize_matrix(d[0], d[1], pars) for d in D]
	return (D, step_discs)

def setup(D, p_local, p_global):
	D = D - np.mean(D, axis = 1).reshape(-1, 1)
	p_local['max'] = np.max(D)
	p_local['min'] = np.min(D)
	return (D, p_local)

#fs = [setup, den.highpass, den.bandstop, den.eog_regress, den.rpca_denoise]
fs = [setup,
      den.highpass,
      den.bandstop,
      den.eog_regress,
      bad_chans.bad_detec]

D = [d for d in factory()]

for f in fs:
	D, step_disc = round(D, f, params['p_global'])
	level_discs.append(step_disc)
	for d in D:
		d[1]['step'] = d[1]['step'] + 1

print level_discs

