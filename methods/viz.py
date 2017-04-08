import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def heat_level(C, level, title, left = False, right = False):
    L = np.array([c[level] for c in C])
    L = np.sqrt(np.abs(L)) * np.sign(L)
    ax = sns.heatmap(L, xticklabels = L.shape[1] / 4 + 1,
                     yticklabels = 4)
    plt.xlabel('Wavelet Coefficient k index')
    if left:
        plt.ylabel('Channel Number')
    if right:
        cbar = ax.collections[0].colorbar
        cbar.set_label(r"$sgn(\psi_{j, k})\sqrt{\vert\psi_{j, k}\vert}$", labelpad=20, rotation=270)
    plt.title(title + ', j = ' + str(level))
    
def dist_plot(C, level, label, kde = False):
    L = np.array([c[level] for c in C])
    L = np.nan_to_num(np.sqrt(np.abs(L)) * np.sign(L))
    sns.distplot(L.flatten(), kde = kde, label = label)

def visualize_matrix(D, p_local, p_global):
    plt.figure()
    sns.heatmap(D[:, ::D.shape[1]/10000], xticklabels = 1000, yticklabels=D.shape[0] / 4,
                vmin = p_local['min'], vmax = p_local['max'])
    plt.xlabel('Time compressed to 10,000 timesteps')
    plt.ylabel('Channel')
    plt.title('Step ' + str(p_local['step']) + ' heatmap')
    plt.savefig(p_local['fig_path'] + 'heat' + str(p_local['step']))
    plt.clf()
    plt.close()
    sns.heatmap(np.log(np.abs(D[:, ::D.shape[1]/10000])),
                xticklabels = 1000, yticklabels=D.shape[0] / 4,
                vmin = -4, vmax = 4)
    plt.xlabel('Time compressed to 10,000 timesteps')
    plt.ylabel('Channel')
    plt.title('Step ' + str(p_local['step']) + ' heatmap, log magnitude')
    plt.savefig(p_local['fig_path'] + 'heatlog' + str(p_local['step']))
    plt.clf()
    plt.close()
    #sparklines_bare(D[:, ::D.shape[1]/10000], 'Sparklines 10000 timesteps', p_local, False)
    #plt.xlabel('Time compressed to 10,000 timesteps')
    #plt.ylabel('Channel')
    #plt.savefig(p_local['fig_path'] + 'spark' + str(p_local['step']), dpi=200)
    #plt.clf()
    return (D, p_local)
    
def cross_compare(reg, den, level):
    C_res = [np.array(x[0]) - np.array(x[1]) for x in zip(reg, den)]
    title = 'Raw'
    ax = plt.subplot(131)
    heat_level(reg, level, title, True)
    ax = plt.subplot(132)
    title = 'Denoised'
    heat_level(den, level, title)
    ax = plt.subplot(133)
    title = 'Residual'
    heat_level(C_res, level, title, False, True)
    plt.tight_layout()
    plt.show()
    
    dist_plot(reg, level, label = 'original')
    dist_plot(den, level, label = 'denoised')
    dist_plot(C_res, level, label = 'original - denoised')
    plt.xlabel(r'$sgn(\psi_{j, k})\sqrt{\vert \psi_{j, k} \vert}$')
    plt.ylabel('Frequency')
    plt.title('Distribution of Wavelet Coefficients (all channels) for scale ' + str(level))
    plt.legend()
    plt.show()

def sparklines_bare(d, title, params, nb):
    sns.set_style('whitegrid')
    C = d.shape[0]
    T = d.shape[1]
    first = plt.subplot(C, 1, 1)
    plt.plot(d[0, :])
    plt.title(title)
    plt.setp(first.get_xticklabels(), visible=False)
    plt.setp(first.get_yticklabels(), visible=False)
    plt.ylabel('1')
    for i in range(1, C):
        axes = plt.subplot(C, 1, i + 1, sharex = first)
        plt.plot(d[i, :])
        plt.ylim([params['min'], params['max']])
        plt.setp(axes.get_xticklabels(), visible=False)
        plt.setp(axes.get_yticklabels(), visible=False)
        plt.ylabel(str(i + 1))
    plt.tight_layout()
    plt.xlim([0,T])
    plt.subplots_adjust(top = 1, bottom = 0)
    if nb:
        plt.show()
        return plt.gcf()
    fig = plt.gcf()
    fig.set_size_inches(5, .3 * C)
    plt.tight_layout()
    return plt.gcf()

def sparklines(r, d, den, title, nb):
    import seaborn as sns
    sns.set_style('whitegrid')

    C = d.shape[0]
    T = d.shape[1]
    fig = plt.figure(figsize=(12,1.5 * C))
    first = plt.subplot(C, 1, 1)
    plt.plot(d[0, :], 'b-', label = 'noisy')
    plt.plot(den[0, :], 'r-', label = 'denoised')
    plt.plot(r[0, :], 'g--', label = 'original')
    plt.title(title)
    plt.legend(bbox_to_anchor=(1.2, 1))
    plt.setp(first.get_xticklabels(), visible=False)
    plt.setp(first.get_yticklabels(), visible=False)
    plt.ylabel('1')
    for i in range(1, C):
        axes = plt.subplot(C, 1, i + 1, sharex = first)
        plt.plot(d[i, :], 'b-')
        plt.plot(den[i, :], 'r-')
        plt.plot(r[i, :], 'g--')
        plt.setp(axes.get_xticklabels(), visible=False)
        plt.setp(axes.get_yticklabels(), visible=False)
        plt.ylabel(str(i + 1))
    plt.tight_layout()
    plt.xlim([0,T])
    plt.subplots_adjust(top = 1, bottom = 0)
    if nb:
        plt.show()
        return plt.gcf()
    return plt.gcf()

def chan_errs(real, noisy, den, title):
    C = real.shape[0]
    T = real.shape[1]
    noisy_errs = [np.linalg.norm(real[i, :] - noisy[i, :]) / T for i in range(C)]
    denoised_errs = [np.linalg.norm(den[i, :] - real[i, :]) / T for i in range(C)]
    plt.plot(noisy_errs, label = 'noisy - original MSE')
    plt.plot(denoised_errs, label = 'denoised - original MSE')
    plt.title(title)
    plt.ylabel('MSE')
    plt.xlabel('Channel')
    plt.legend()
    return plt.gcf()

def coef_pyramid_plot(coefs, first=0, scale='uniform', ax=None):
    """
    Parameters
    ----------
    coefs : array-like
        Wavelet Coefficients. Expects an iterable in order Cdn, Cdn-1, ...,
        Cd1, Cd0.
    first : int, optional
        The first level to plot.
    scale : str {'uniform', 'level'}, optional
        Scale the coefficients using the same scale or independently by
        level.
    ax : Axes, optional
        Matplotlib Axes instance

    Returns
    -------
    Figure : Matplotlib figure instance
        Either the parent figure of `ax` or a new pyplot.Figure instance if
        `ax` is None.
    """

    if ax is None:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111, axisbg='lightgrey')
    else:
        fig = ax.figure

    n_levels = len(coefs)
    n = 2**(n_levels - 1) # assumes periodic

    if scale == 'uniform':
        biggest = [np.max(np.abs(np.hstack(coefs)))] * n_levels
    else:
        # multiply by 2 so the highest bars only take up .5
        biggest = [np.max(np.abs(i))*2 for i in coefs]

    for i in range(first,n_levels):
        x = np.linspace(2**(n_levels - 2 - i), n - 2**(n_levels - 2 - i), 2**i)
        ymin = n_levels - i - 1 + first
        yheight = coefs[i]/biggest[i]
        ymax = yheight + ymin
        ax.vlines(x, ymin, ymax, linewidth=4)

    ax.set_xlim(0,n)
    ax.set_ylim(first - 1, n_levels)
    ax.yaxis.set_ticks(np.arange(n_levels-1,first-1,-1))
    ax.yaxis.set_ticklabels(np.arange(first,n_levels))
    ax.tick_params(top=False, right=False, direction='out', pad=6)
    ax.set_ylabel("Levels", fontsize=14)
    ax.grid(True, alpha=.85, color='white', axis='y', linestyle='-')
    ax.set_title('Wavelet Detail Coefficients', fontsize=16,
            position=(.5,1.05))
    fig.subplots_adjust(top=.89)

    return fig
