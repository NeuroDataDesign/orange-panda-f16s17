# Public
import simplejson as json
import numpy as np
import os
import pickle as pkl
import sys
sys.path.append('../auto_bench')
sys.path.append('../auto_bench/*')

# Ours
import auto_bench as ab
import auto_bench.utils
import auto_bench.main
import auto_bench.metrics
import auto_bench.transforms
import auto_bench.discriminibility
import auto_bench.standard_set as ss
import prep
import prep.noise_reduct

JOB_FILE = sys.argv[1]
job = None
with open(JOB_FILE, 'r') as f:
	job = json.load(f)
	job['prep'] = eval(job['prep'])
	job['params'] = eval(job['params'])

DATASET_PATH = 'datasets/' + job['dataset']

factory, labels = ab.utils.data_generator_factory(DATASET_PATH)

ab.utils.print_info(DATASET_PATH)

results = []
for param in job['params']:
	nfg = ab.utils.nested_generator_factory_factory(factory,
							job['prep'],
							param)

	discs = ab.main.disc_all(nfg,
				 labels,
				 ss.TRANSFORMS,
				 ss.METRICS,
				 ss.NAMES)

	results.append((param,  zip(discs, ss.NAMES)))

with open(DATASET_PATH + '/' + job["job_name"] + '.pkl', 'w') as f:
	pkl.dump(results, f)
