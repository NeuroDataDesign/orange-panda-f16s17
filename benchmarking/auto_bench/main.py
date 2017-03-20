# Public
import numpy as np
import time
import pickle as pkl
import pandas as pd
from pathos.multiprocessing import ProcessingPool as Pool

# Ours
from utils import (iterdim,
                   dict_index,
                   get_param_dims,
                   time_str,
                   apply_all)

from discriminibility import discriminibility

PROG_STRING = "Finished %d / %d iterations.\nTime since start:    %s.\nPredicted time left: %s.\n"

def parallel_map(funct, D, n_cores):
    par = Pool(n_cores)
    return par.map(funct, D)

def single_bench(data, labels, params, metric, transform, prep):
    if prep is not None:
        preprocessed_data = map(lambda d: prep(d, params), data)
    else:
        preprocessed_data = data
    if transform is not None:
        transformed_data = map(lambda d: transform(d), preprocessed_data)
    else:
        transformed_data = preprocessed_data
    return metric_test(transformed_data, labels, metric)

def disc_all(factory, labels, transforms, metrics, names):
    discs = []
    for i in range(len(transforms)):
        print names[i]
        D = factory()
        p = Pool(8)
        D = apply_all(D, [transforms[i]], p.map)
        disc = discriminibility(
                    D,
                    labels,
                    metrics[i]
                )
        discs.append(disc)
    return discs


def bench(factory, labels, param_map, metric, transform, prep,
          n_cores = 2, name = 'bench'):
    pkl.dump(param_map, open('results/' + name + '_param_map.pkl', 'wb'))
    param_dimensions = get_param_dims(param_map)
    print 'Got a parameter space of dimension', param_dimensions
    R = np.zeros(param_dimensions)
    try:
        R_load = pkl.load(open('results/' + name + '.pkl', 'rb'))
        print 'Found partially completed run for the name', name, '... loading that.'
        R = R + R_load
    except:
        pass
    start = time.time()
    count = 0
    total = np.cumprod(param_dimensions)[-1]
    for index, x in np.ndenumerate(R):
        data = factory()
        map_func = None
        if R[index] != 0:
            print 'Already found param combination', dict_index(param_map, index)
            total = total - 1
        else:
            theta = dict_index(param_map, index)
            if PARALLEL:
                data = apply(lambda d: transform(prep(d, theta)), data, n_cores)
            else:
                data = map(lambda d: transform(prep(d, theta)), data, n_cores)
            R[index] = discriminibility(data,
                                        labels,
                                        metric)
            count += 1
            pkl.dump(R, open('results/' + name + '.pkl', 'wb'))
            print 'Completed calculation for', dict_index(param_map, index)
            print 'Saved progress at', name + '.pkl'
            curr_time = time.time()
            so_far = curr_time - start
            expected = (so_far / count) * (total - count)
            print PROG_STRING % (count, total, time_str(so_far), time_str(expected)) 
    return R



def metric_test(data, labels, theta, metric, transform, prep, n_cores = 2):
    print 'Best Disc:', 
    print discriminibility(data, labels, metric)
    idx = np.arange(len(data))
    results = []
    for leave_out in range(len(data)):
        loop_idx = np.setdiff1d(idx, [leave_out])
        loop_data = [data[i] for i in loop_idx]
        loop_labels = [labels[i] for i in loop_idx]
        print loop_idx
        results.append(discriminibility(loop_data, loop_labels, metric))
    return results

def metric_benchmark(data, labels, transforms, metrics, names, title):
    parallel = Pool(4)
    results = []
    for i in range(len(metrics)):
        print names[i]
        transformed_data = [transforms[i](d) for d in data]
        values = metric_test(transformed_data, labels, metrics[i])
        results.append(values)
    df = pd.DataFrame(data = np.array(results).T, columns = names)
    sns.violinplot(df)
    plt.ylabel('Discriminibility')
    plt.xlabel('Metrics')
    plt.title(title)
    plt.show()
    return df

def best_param_combo(R, param_map):
    param_dims = get_param_dims(param_map)
    best = np.unravel_index(np.argmax(R), param_dims)
    return dict_index(param_map, best), best
