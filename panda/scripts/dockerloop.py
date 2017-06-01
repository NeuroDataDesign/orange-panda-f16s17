import os
import sys
import shutil
import panda.utils.bids_s3 as bids_s3
from pandas import read_csv



if __name__ == '__main__':
    _, buck, dset = sys.argv
    remote_in_dir = ("data/%s") % (dset)
    local_in_dir = ("temp/%s/") % (dset)
    bids_s3.get_data(
        bucket = buck,
        remote_dir = remote_in_dir + '/participants.tsv',
        local = local_in_dir,
        public=True,
        folder = False)
    participants = read_csv(local_in_dir + '/participants.tsv',
                            sep = '\t')
    subjects = participants['participant_id'].as_matrix()
    n_trials = participants['num_trials'].as_matrix()
    subs = [sub.split('-')[-1] for sub in subjects]
    trials =  [map(lambda x: '%02d' % (x), range(1, n + 1)) for n in n_trials]
    full = ''
    base = 'docker run --rm rymarr/panda_pipeline %s %s %s %s\n'
    for sub in subs:
        for subs_trials in trials:
            for trial in subs_trials:
                full += base % (buck, dset, sub, trial)
    with open(local_in_dir + '/command.txt', 'w') as f:
        f.write(full)
    par = 'time parallel -j 2 :::: %s' % (local_in_dir + '/command.txt')
    os.system(par)    
    shutil.rmtree('temp')

