# coding: utf-8
import matplotlib as mpl
mpl.use('Agg')
import bench.dataset_creation as dc
import bench.disc_set as d_set
import bench.utilities as ut
import bench.discriminibility as disc
import methods.denoise as den
import methods.viz as viz
import os
from pathos.multiprocessing import ProcessingPool as Pool
import numpy as np

os.chdir('../data')
factory, labels = ut.data_generator_factory('bids_raw_demo')
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
		    'delta': 1e-6,
		    'mu': .65
		}
	}
}
level_discs = []

par = Pool(10)

def my_disc(D):
	return disc.disc_all(D, labels, d_set.TRANSFORMS,
		                 d_set.METRICS, d_set.NAMES)

def round(D, f, pars):
        print 'Started round'
	D = par.imap(lambda d: f(d[0], d[1], pars), D)
        D = [d for d in D]
        print 'Finished round, calculating discriminibility'
	step_discs = my_disc([d[0] for d in D])
	D = [viz.visualize_matrix(d[0], d[1], pars) for d in D]
	return (D, step_discs)

def setup(D, p_local, p_global):
	p_local['max'] = np.max(D)
	p_local['min'] = np.min(D)
	return (D, p_local)

fs = [setup, den.highpass, den.bandstop, den.eog_regress, den.rpca_denoise]
#fs = [setup, den.rpca_denoise]

D = [d for d in factory()]

for f in fs:
	D, step_disc = round(D, f, params['p_global'])
	level_discs.append(step_disc)
	for d in D:
		d[1]['step'] = d[1]['step'] + 1

with open('results.pkl', 'w') as f:
    import cPickle as pkl
    pkl.dump(level_discs, f)

