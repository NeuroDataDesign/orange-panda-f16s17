# Probably a bad idea but matplotlib is annoying
import warnings
warnings.filterwarnings("ignore")

# Bae
import numpy as np
import matplotlib
import seaborn as sns
from pandas import read_csv
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# System utilities
import sys
import cPickle as pkl
import os
import os.path as op
import shutil

# Import pipeline specific utilities
import panda.utils.bids_s3 as bids_s3

import bench.discriminibility as disc
import bench.metrics as metrics

# Import params (dependent on chan_locs)
from panda.config import params


def main(buck, dset):
    # Organize directories

    remote_in_dir = ("data/%s") % (dset)
    local_in_dir = ("temp/%s") % (dset)
    plot_dir = ("results/%s") % (dset)

    # Try to make directories
    try:
        os.makedirs(local_in_dir)
        os.makedirs(plot_dir)
    except:
        print 'Directories already exist, re-doing analysis.'

    print "Saving participants from S3.", "\n"
    bids_s3.get_data(
        bucket = buck,
        remote_dir = remote_in_dir + '/participants.tsv',
        local = local_in_dir,
        public=True,
        folder = False)

    # Load participants into
    print "Loading participants info from disk.", "\n"
    participants = read_csv(local_in_dir + '/participants.tsv',
                            sep = '\t')
    subjects = participants['participant_id'].as_matrix()
    n_trials = participants['num_trials'].as_matrix()
    all_discs = []
    function_names = map(lambda x: x.__name__, params['functions'])
    for der in ['correlation_matrix']:
        der_discs = [] = []
        plot_count = 0
        for funct in function_names:
            derivatives = None
            labels = []
            for sub, trial in zip(subjects, n_trials):
                for tr in range(trial):
                    path = "%s/ses-%02d/eeg/derivatives/%s/%s_%s.pkl" \
                           % (sub, tr + 1, der, der, funct) 
                    bids_s3.get_data(
                        bucket = buck,
                        remote_dir = remote_in_dir + '_out/' + path,
                        local = local_in_dir + '/' + path,
                        public=True,
                        folder = False)
                    with open(local_in_dir + '/' + path, 'rb') as f:
                        D = pkl.load(f)
                        if derivatives is None:
                            derivatives = np.expand_dims(D, axis=2)
                        else:
                            derivatives = np.append(derivatives,
                                          np.expand_dims(D, axis=2), axis=2)
                        labels.append(sub)

            # Calculate and save disc
            dist = disc.distance_matrix(derivatives, metrics.frob)
            myrdf = disc.rdf(dist, labels)
            my_disc = np.mean(myrdf)
            print funct, der, my_disc
            der_discs.append(my_disc)
            
            # Dist plot
            within, outside = disc.intra_inter(dist, labels)
            sns.distplot(within, hist = False, rug = True, label='Intra')
            sns.distplot(outside, hist = False, rug = True, label = 'Inter')
            plt.legend()
            plt.title('Function: %s' % (funct))
            plt.savefig('%s/dists-%s.png' % (plot_dir, funct))
            plt.cla()
            plt.clf()
            plt.close()

            # Heat Map
            sns.heatmap(np.power(dist, 2))
            plt.xlabel('Subjects')
            locs = np.arange(0, dist.shape[0], dist.shape[0] / len(subjects))
            locs = locs + (dist.shape[0] / len(subjects)) / 2
            plt.xticks(locs, subjects)
            plt.yticks(locs, subjects)
            plt.title('Function: %s, Discriminibility: %04f' % (funct, my_disc))
            plt.ylabel('Subjects')
            plt.savefig('%s/disc-heat-_%s.png' % (plot_dir, funct))
            plt.cla()
            plt.clf()
            plt.close()
            plot_count += 1

        all_discs.append((der, der_discs))
    print all_discs
    for der_discs in all_discs:
        name, der_discs = der_discs
        plt.plot(der_discs, label = name)
    plt.xticks(range(len(function_names)), function_names)
    plt.tight_layout()
    ax = plt.gca()
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.06),
          ncol=4, fancybox=True, shadow=True)
    ax.margins(0.1)
    plt.xlabel('Experiment Name')
    plt.ylabel('Discriminibility')
    plt.tight_layout()
    plt.savefig('%s/group_analysis.png' % (plot_dir))
    shutil.rmtree('temp')

if __name__ == "__main__":
    # Get arguments
    _, buck, dset = sys.argv
    main(buck, dset)
