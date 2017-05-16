import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns
import numpy as np
import scipy.signal
from scipy.signal import spectrogram

def spectrograms(D, p_local, p_global):
    if p_local['eog_in']:
        D = D[p_global['eeg_chans'], :]
    C = D.shape[0]
    T = D.shape[1]
    for c in range(C)[:3]:
        f, t, Sxx = spectrogram(D[c, :], p_global['sample_freq'])
        sns.heatmap(np.log(Sxx[::-1, :]), xticklabels = t.astype(int),
            yticklabels = f.astype(int)[::-1])

        # There is probably a better way to do this
        for label in plt.gca().get_xticklabels():
            label.set_visible(False)
        for label in plt.gca().get_xticklabels()[::Sxx.shape[1] / 6]:
            label.set_visible(True)
        for label in plt.gca().get_yticklabels():
            label.set_visible(False)
        for label in plt.gca().get_yticklabels()[::Sxx.shape[0] / 6]:
            label.set_visible(True)
        cbar = plt.gca().collections[0].colorbar
        plt.title('Spectrogram for channel ' + str(c + 1))
        plt.xlabel('Time in seconds')
        plt.ylabel('Frequency')
        cbar.set_label(r"$\log(\hat{f})$", labelpad=20, rotation=270)
        path = p_global['plot_folders']['spectrogram_dir'] \
               + '/' + 'spectrogram-%03d' % (c + 1)
	if p_global['plotting']['notebook']:
	    show_and_close()
	else:
	    save_and_close(path, p_local)

def correlation(D, p_local, p_global):
    if p_local['eog_in']:
        D = D[p_global['eeg_chans'], :]
    C = D.shape[0]

    with np.errstate(invalid='ignore'):
        D = np.nan_to_num(np.corrcoef(D))

    sns.heatmap(D, xticklabels = C / 10, yticklabels = C / 10, square = True)

    cbar = plt.gca().collections[0].colorbar
    cbar.set_label("Correlation Coefficient", labelpad=20, rotation=270)
    plt.title('Correlation Matrix')
    plt.xlabel('Channels')
    plt.ylabel('Channels')
    path = p_global['plot_folders']['correlation_dir'] \
           + '/' + 'correlation'
    if p_global['plotting']['notebook']:
        show_and_close()
    else:
        save_and_close(path, p_local)

def sym_log(c):
    def f(x):
        return np.sign(x) * np.log(1 + np.abs(x / c))
    return f

def heatmap(D, p_local, p_global):
    if p_local['eog_in']:
        D = D[p_global['eeg_chans'], :]
    C = D.shape[0]
    T = D.shape[1]
    plt.figure()
    compress = T / p_global['plotting']['time_compression']
    x_ticks = max(2, p_global['plotting']['time_compression'] / 10)
    y_ticks = max(2, C / 6)

    f, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(11, 8.5))
    sns.heatmap(data = D[:, ::compress],
                xticklabels = x_ticks,
                yticklabels = y_ticks,
                ax = ax1)
    plt.ylabel('channel')

    cbar = ax1.collections[0].colorbar
    cbar.set_label("raw", labelpad=20, rotation=270)

    sym_log_100 = sym_log(100)

    sns.heatmap(data = sym_log_100(D[:, ::compress]),
                xticklabels = x_ticks,
                yticklabels = y_ticks,
                ax = ax2)
    plt.ylabel('channel')
    cbar = ax2.collections[0].colorbar
    cbar.set_label("symlog100", labelpad=20, rotation=270)

    sym_log_5 = sym_log(5)

    sns.heatmap(data = sym_log_5(D[:, ::compress]),
                xticklabels = x_ticks,
                yticklabels = y_ticks,
                ax = ax3)

    cbar = ax3.collections[0].colorbar
    cbar.set_label("symlog5", labelpad=20,  rotation=270)
    path = p_global['plot_folders']['heatmap_dir'] \
           + '/' + 'heatmap'
    plt.ylabel('channel')
    plt.xlabel('time downsampled to 10,000 timesteps')
    if p_global['plotting']['notebook']:
        show_and_close()
    else:
        save_and_close(path, p_local)

def sparklines(D, p_local, p_global):
    sns.set_style('white')
    C = D.shape[0]
    T = D.shape[1]
    fig = plt.figure()
    fig.set_size_inches(8, .2 * C)
    compress = T / p_global['plotting']['time_compression']

    M = np.max(D)
    m = np.min(D)

    first = plt.subplot(C, 1, 1)
    plt.plot(D[0, ::compress], linewidth=0.75)
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.setp(first.get_xticklabels(), visible=False)
    plt.setp(first.get_yticklabels(), visible=False)
    plt.ylabel('1', fontsize=8, rotation = 0)
    for i in range(1, C):
        ax = plt.subplot(C, 1, i + 1, sharex = first)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        plt.plot(D[i, ::compress], linewidth=0.75)
        plt.ylim([m, M])
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax.get_yticklabels(), visible=False)
        plt.ylabel(str(i + 1), fontsize=8, rotation = 0)
    #plt.tight_layout()
    plt.xlim([0,p_global['plotting']['time_compression']])
    plt.subplots_adjust(wspace=0, hspace=0)
    path = p_global['plot_folders']['sparkline_dir'] \
           + '/' + 'sparklines'
    save_and_close(path, p_local)

def save_and_close(path, p_local):
    try:
        mpl.use('Agg')
    except:
        pass # already loaded
    img = ("%s/%s_%s.png") % (p_local['out_path'], path, p_local['funct'])
    plt.savefig(img)
    plt.cla()
    plt.clf()
    plt.close()


def show_and_close():
    plt.show()
    plt.cla()
    plt.clf()
    plt.close()
