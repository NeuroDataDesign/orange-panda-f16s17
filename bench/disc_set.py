import metrics
import transforms

TRANSFORMS = [transforms.correl,
              transforms.spect,
              transforms.tc_make(.7),
              transforms.tc_make(.7)]

METRICS =    [metrics.frob,
              metrics.frob,
              metrics.diff_num_3cycle,
              metrics.diff_num_4cycle]

NAMES =      ['Frob Corr',
              'Spect Norm',
              'D # c(3) .7',
              'D # c(4) .7']
