from utils.fourier import butter_highpass_filter, butter_lowpass_filter, butter_bandstop_filter
from sklearn.decomposition import FastICA, PCA
import numpy as np
import pandas as pd
from utils.plots import plotly_hack, sparklines, correlation
def reduce_noise(eeg_data, method, **kwargs):
  if method == 'placeholder': # for Minimum Viable Product
    out = ""
    out +=  "<h3>REDUCING NOISE</h3>"
    for p in range(eeg_data.shape[3]):
      print 'Noise reduction for patient ' + str(p)
      for t in range(eeg_data.shape[2]):
        print 'Noise reduction for trial ' + str(t)
        out += '<h4>Actions for patient ' + str(p) + '</h4>'
        out += '<ul>'
        out += "<li>Highpass filtered at .1 Hz threshold.</li>"
        out += "<li>Bandstop filtered at harmonics of 60Hz.</li>"
        out += '</ul>'
        for c in range(eeg_data.shape[1]):
          eeg_data[:, c, t, p] = butter_highpass_filter(
            eeg_data[:, c, t, p], 0.1, 500)
          for k in range(60, 299, 60):
            eeg_data[:, c, t, p] = butter_bandstop_filter(
              eeg_data[:, c, t, p], [k-5,k+5], 500)
    return eeg_data, out
  else:
    return eeg_data, '<h3> Nothing happened </h3>'

def eye_artifact(eeg_data, method, **kwargs):
  out = ''
  if method == 'ICA':
    out += '<h3>DETECTING AND REMOVING ARTIFACTS</h3>'
    out += '<p> Running FastICA to discover independent components.'
    for p in range(eeg_data.shape[3]):
      print 'Eye artifact reduction for patient ' + str(p)
      for t in range(eeg_data.shape[2]):
        print 'Eye artifact reduction for trial ' + str(p)
        ica = FastICA()
        ica.fit(eeg_data[::kwargs['ds'], :, t, p])
        ica_ind_component = ica.transform(eeg_data[:, :, t, p])
        components = ica.components_
        comps_df = pd.DataFrame(data=components.T)
        out += '<h5> Correlation matrix of the independent components </h5>'
        out += plotly_hack(correlation(comps_df))
        correl = np.fliplr(comps_df.corr(method='pearson').as_matrix())
        sum_correl = np.sum(np.abs(correl), axis=1)
        out += '<h5> Sums of row-wise correlations (for ' + str(kwargs['n_rm']) + \
        ' independent components with the lowest correlation): </h5>'
        inds = np.argsort(sum_correl)[:kwargs['n_rm']]
        out += '<ol>'
        for c in range(kwargs['n_rm']):
          out += '<li>' + str(np.round(sum_correl[c], 2)) + '</li>' 
        out += '</ol>'
        ica.mixing_[:, inds] = 0
        eeg_data[:, :, t, p] = ica.inverse_transform(ica_ind_component)
        cct = [pd.DataFrame(data=eeg_data[:, c, t, p]) for c in range(eeg_data.shape[1])]
        if len(cct) > 0:
          df = pd.concat(cct, axis=1)
          df.columns = [str(c) for c in range(eeg_data.shape[1])]
          df.index = map(lambda t: t[0]/1000.0, kwargs['times'][:, :, -1])
          out += '<h5> Sparklines of data with low ' + str(kwargs['n_rm']) + \
          ' independent components removed </h5>'
          out += plotly_hack(sparklines(df, title="Sparklines"))
  return eeg_data, out