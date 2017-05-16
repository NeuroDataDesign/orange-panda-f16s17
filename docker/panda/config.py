import cPickle as pkl

# Import pipeline methods
import panda.methods.denoise as den
import panda.methods.bad_chans as bad_chans
import panda.methods.derivatives as der
import panda.methods.viz as viz
import panda.methods.interpolation as inter
import panda.methods.misc as misc

params = {
    'p_global': {
         'hpf': {
             'order': 6,
             'Fs': 500,
             'cutoff': 1
         },
         'lpf': {
             'order': 6,
             'Fs': 500,
             'cutoff': 230
         },
         'bsf': {
             'order': 6,
             'Fs': 500,
             'cutoffs': [[50, 70], 
                         [95, 105], 
                         [115, 125],
                         [175, 185],
                         [195, 205]]
         },
	'wave_visu': {
	    'wave': 'db2',
	    'verbose': False
	},
	'wave_rej': {
	    'wave': 'db2',
	    'thresh': 16,
            'rec': True
	},
        'amp_rej': {
            'thresh': 8,
            'method': 'shrink'
        },
        'rpca': {
            'max_iter': 60,
            'verbose': False,
            'pca_method': 'randomized',
            'delta': 1e-7,
            'mu': None
        },
        'bad_detec': {
            'thresh': 3,
            'measure': ['prob', 'kurtosis'],
            'normalize': 0,
            'discret': 1000,
            'verbose': False,
            'trim': None
        },
        'inter': {
            'loc_unit': 'radians',
                    'verbose': False,
                    'k': 3,
                    's' : 1000,
                    'wave': 'db2'
        },
        'sample_freq': 500,
        'eog_chans': [48, 49, 56, 63, 68,
                      73, 81, 88, 94, 99,
                      107, 113, 119, 125,
                      125, 126, 127, 128], # 0 indexed
        'plotting': {
            'time_compression': 10000,
            'notebook': False
        },
        'plot_folders': {
            'spectrogram_dir' : 'qa/spectrograms',
            'heatmap_dir' : 'qa/heatmaps',
            'correlation_dir' : 'qa/correlations',
            'sparkline_dir' : 'qa/sparklines'
        },
        'derivatives': {
            'correlation_matrix': 'derivatives/correlation_matrix',
            'spectrum': 'derivatives/spectrum',
            'coherence_matrix': 'derivatives/coherence_matrix',
            'left_singular_vectors': 'derivatives/left_singular_vectors'
        }
    },
    'functions': [misc.setup,
                  den.highpass,
#                  den.bandstop,
                  den.eog_regress,
                  den.wave_rejection,
                  den.amp_shrinkage,
                  bad_chans.bad_detec,
                  inter.wave_interp
                  ],

    'derivatives': [der.correlation],#, der.svd, der.coherence],
    'plots':[viz.heatmap, viz.spectrograms, viz.correlation]
}
