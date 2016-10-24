import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import numpy as np
from scipy.signal import spectrogram

def plot_timeseries(data, time = None, selector = "all", colors = None,
                    start = 0, end = None, skip = 1, randno = 10,
                    title = 'unnamed figure', xlab = '', ylab=''):
    fig = plt.figure()
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
    return fig

def make_3d_scatter(data, coords):
    fig = plt.figure()
    ax = Axes3D(fig)
    x = coords[:, 0]
    y = coords[:, 1]
    z = coords[:, 2]
    ax.scatter(x, y, z, s=np.abs(data[200]), depthshade = True)
    ax.set_xlabel('eyes to back of head')
    ax.set_ylabel('ear to ear')
    ax.set_zlabel('top of head to bottom')
    ax.set_title('Electrodes on the brain.')
    return ax

def make_spectrogram(data, fig, Fs = 500, vmin = 0, vmax = 30):
    f, t, Sxx = spectrogram(data, Fs)
    plt.pcolormesh(t, f, np.log(Sxx))
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    cmap = plt.get_cmap('viridis')
    cmap.set_under(color='k', alpha=None)
    ax = plt.gca()
    NFFT = 256
    pxx,  freq, t, cax = ax.specgram(f/(NFFT/2), Fs=Fs,
            mode='magnitude', NFFT=NFFT, noverlap=NFFT/2,
            vmin=vmin, vmax=vmax, cmap=cmap)
    cbar = plt.colorbar(cax)
    cbar.ax.set_ylabel('Magnitude in mV', rotation=270)
    cbar.ax.get_yaxis().labelpad = 15
    plt.xlim([0, data.shape[0]/Fs])

def my_save_fig(fig, f_name, title):
    plt.savefig(f_name)
    out = ''
    out += '## ' + title + '.\n'
    out +=  '![](' + f_name + ')\n'
    return out

