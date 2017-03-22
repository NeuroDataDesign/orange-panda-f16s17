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