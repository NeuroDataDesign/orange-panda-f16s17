import numpy as np
import time
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
sns.set_style("dark")

PROG_STRING = "Finished %d / %d iterations.\nTime since start:    %s.\nPredicted time left: %s.\n"
DATE_STRING = '%02d d, %02d h, %02d m, %02d s'

def dict_index(dictionary, tuple):
    values = {}
    for key, number in zip(dictionary.keys(), tuple):
        values.update({key: dictionary[key][number]})
    return values

def bench(data, labels, metric, param_map,
          transform, sampling_method = 'iterative', name = 'bench'):
    param_dimensions = map(lambda x: len(x), param_map.values())
    R = np.zeros(param_dimensions)
    try:
        R_load = pickle.load(open(name + '.pkl', 'rb'))
        print 'Found partially completed run for the name', name, '... loading that.'
        R = R + R_load
    except:
        pass
    start = time.clock()
    count = 0
    total = np.cumprod(param_dimensions)[-1]
    for index, x in np.ndenumerate(R):
        if R[index] != 0:
            print 'Already found param combination', index
            total = total - 1
        else:
            theta = dict_index(param_map, index)
            transformed_data = map(lambda d: transform(d, theta), data)
            R[index] = discriminibility(transformed_data,
                                        labels,
                                        metric)
            count += 1
            pickle.dump(R, open(name + '.pkl', 'wb'))
            print 'Saved progress at', name + '.pkl'
            curr_time = time.clock()
            so_far = curr_time - start
            expected = (so_far / count) * (total - count)
            print PROG_STRING % (count, total, time_str(so_far), time_str(expected)) 

    return R

def time_str(unix_time):
    seconds = np.floor(unix_time / 1)
    minutes = np.floor(seconds / 60)
    seconds -= 60 * minutes
    hours = np.floor(minutes / 60)
    minutes -= 60 * hours
    days = np.floor(hours / 24)
    hours -= 24 * days
    return DATE_STRING % (days, hours, minutes, seconds)

def partial_disc(D, labels, subject, trial1, trial2):
    enum = np.arange(D.shape[0])
    t1 = enum[labels == subject][trial1]
    t2 = enum[labels == subject][trial2]
    d_t1_t2 = D[t1][t2]
    d_ra = [D[t1][x] for x in enum[labels != subject]]
    return np.mean(d_t1_t2 < d_ra)

def distance_matrix(data, metric, symmetric = True):
    n = len(data)
    dist_matrix = np.zeros([n, n])
    if symmetric:
        for i in range(n):
            for j in range(i):
                dist_matrix[i][j] = metric(data[i], data[j])
                dist_matrix[j][i] = metric(data[i], data[j])
    else:
        for i in range(n):
            for j in range(n):
                dist_matrix[i][j] = metric(data[i], data[j])
    return dist_matrix

def discriminibility(data, labels, metric, dist_mat = False):
    dist_matrix = None
    if not dist_mat:
        dist_matrix = distance_matrix(data, metric)
    else:
        dist_matrix = metric
    labels = np.array(labels)
    partials = []
    for s in np.unique(labels):
        num = np.sum(labels == s)
        for t in range(num):
            for tt in range(num):
                if tt != t:
                    p = partial_disc(dist_matrix,
                        labels, s, t, tt)
                    partials.append(p)
    return np.mean(partials)

def bench_report(results, param_map, transformation_name, metric_name):
    for i, param in enumerate(param_map.keys()):
        param_values = param_map[param]
        mean_discs = map(lambda x: np.mean(x), iterdim(results, axis=i))
        max_discs = map(lambda x: np.max(x), iterdim(results, axis=i))
        min_discs = map(lambda x: np.min(x), iterdim(results, axis=i)) 
        plt.plot(param_values, mean_discs, label='mean disc.')
        plt.plot(param_values, max_discs, label='max disc.')
        plt.plot(param_values, min_discs, label='min disc.')
        plt.title('Discriminibility conditioned on parameter ' + param)
        plt.xlabel('Value of ' + param)
        plt.ylabel('Discriminibility')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()

def iterdim(a, axis=0) :
    a = np.asarray(a);
    leading_indices = (slice(None),)*axis
    for i in xrange(a.shape[axis]) :
        yield a[leading_indices+(i,)]

def metric_test(data, labels, metric):
    idx = np.arange(len(data))
    D = distance_matrix(data, metric)
    results = []
    for leave_out in range(len(data)):
        loop_idx = np.setdiff1d(idx, [leave_out])
        loop_data = [data[i] for i in loop_idx]
        loop_labels = [labels[i] for i in loop_idx]
        results.append(discriminibility(loop_data,
                                        loop_labels,
                                        D[loop_idx, :][:, loop_idx],
                                        True))
    return results

def metric_benchmark(data, labels, transforms, metrics, names, title):
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
