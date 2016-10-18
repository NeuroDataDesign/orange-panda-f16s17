import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

def plot_timeseries(data, time = None, selector = "all", colors = None, start = 0, end = None, skip = 1, randno = 10, title = 'unnamed figure', xlab = '', ylab='', save_path = ""):
    plt.figure()
    numchan = int(data.shape[1])
    numtimesteps = int(data.shape[0])
    if end is None: end = numtimesteps
    if time is None: time = range(end)
    if selector == "all":
        selector = range(numchan)
    elif selector == "random":
        selector = random.sample(range(numchan), randno)
    times = time[start:end:skip]
    for channel in selector:
        d = data[:, channel][start:end:skip]
        assert len(times) == len(d)
        if colors is None:
            plt.plot(times, d)
        else:
            plt.plot(times, d, colors[channel])
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    if save_path is not "":
        plt.savefig(save_path)
    else:
        plt.show()

