import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("dark")


from auto_bench.utils import (iterdim,
	                          get_param_dims,
	                          dict_index)

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

def compare_results(result_pairs, title):
    results, names = zip(*result_pairs)
    results = pd.DataFrame(data = np.array(results).T, columns = names)

    # Violin Plot
    sns.violinplot(data=results, bw = .2)
    plt.ylabel('Discriminibility')
    plt.xlabel('Processing condition')
    plt.title('Voilin Plots: ' + title)
    plt.show()

    # Boxplot
    sns.boxplot(data=results)
    plt.ylabel('Discriminibility')
    plt.xlabel('Processing condition')
    plt.title('Box Plots: ' + title)
    plt.show()

    #Pairsplot
    sns.pairplot(data=results, kind='reg', diag_kind='hist')
    plt.ylabel('Discriminibility')
    plt.xlabel('Processing condition')
    plt.show()

