import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

def plot_timeseries(data, time = None, selector = "all", start = 0, end = None, skip = 1, randno = 10, title = 'unnamed figure', xlab = '', ylab=''):
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
        plt.plot(times, d)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.show()

