import numpy as np
import cPickle as pkl
import scipy
import scipy.signal

def correlation(D, p_local, p_global):
    if p_local['eog_in']:
        D = D[p_global['eeg_chans'], :]
    with np.errstate(invalid='ignore'):
        D = np.nan_to_num(np.corrcoef(D))

    path = p_global['derivatives']['correlation_matrix'] \
           + '/' + 'correlation_matrix'
    save_and_close(D, path, p_local)

def svd(D, p_local, p_global):
    if p_local['eog_in']:
        D = D[p_global['eeg_chans'], :]
    U, s, _ = np.linalg.svd(D, full_matrices=False)

    path_spectrum = p_global['derivatives']['spectrum'] \
                    + '/' + 'spectrum'
    path_lsv = p_global['derivatives']['left_singular_vectors'] \
               + '/' + 'left_singular_vectors'
    save_and_close(s, path_spectrum, p_local)
    save_and_close(U, path_lsv, p_local)

def coherence(D, p_local, p_global):
    if p_local['eog_in']:
        D = D[p_global['eeg_chans'], :]
    C = D.shape[0]
    coh = np.zeros([C, C])
    for i in range(C):
        for j in range(i):
            x = D[i, :]
            y = D[j, :]
            x_y_coh = scipy.signal.coherence(x, y, p_global['sample_freq']) 
            x_y_coh = np.mean(x_y_coh[1])
            coh[i, j] = x_y_coh
            coh[j, i] = x_y_coh
    coh = coh + np.eye(C)
    path = p_global['derivatives']['coherence_matrix'] \
               + '/' + 'coherence'
    save_and_close(coh, path, p_local)

def save_and_close(D, path, p_local):
    der = ("%s/%s_%s.pkl") % (p_local['out_path'], path, p_local['funct'])
    with open(der, 'wb') as f:
        pkl.dump(D, f, -1)
