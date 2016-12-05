import utils.plots as plt
import pandas as pd

def subset_chans(T, S, title):
  r"""Return plot of a subset of the channels.
  
  Parameters
  ----------
  T : eeg_panda_format dictionary (https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/PANDA_data_format.md)
  S : list
    list of the indicies of the subset.
  title : string
    title of the plot

  Returns
  -------
  plot : html of the plot, or a paragraph if there are no channels in the subset.

  """
  cct = [pd.DataFrame(data=T['eeg'][:, c]) for c in S]
  if len(cct) > 0:
    df = pd.concat(cct, axis=1)
    df.columns = [str(c) for c in S]
    df.index = map(lambda t: t[0]/1000.0, T['times'])
    return plt.plotly_hack(plt.sparklines(df, title=title))
  else:
    return'<p>No bad channels!</p>'

def zeroed(T):
  r"""Return plot of zeroed channels.
  
  Parameters
  ----------
  T : eeg_panda_format dictionary (https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/PANDA_data_format.md)

  Returns
  -------
  plot : html of the plot.

  """
  return subset_chans(T, T['meta']['zeroed_chans'], "Zeroed Channels")

def bad_electrodes(T):
  r"""Return plot of bad channels.
  
  Parameters
  ----------
  T : eeg_panda_format dictionary (https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/PANDA_data_format.md)

  Returns
  -------
  plot : html of the plot.

  """
  return subset_chans(T, T['meta']['bad_chans'], "Bad Channels")

def interp_electrodes(T):
  r"""Return plot of interpolated channels.
  
  Parameters
  ----------
  T : eeg_panda_format dictionary (https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/PANDA_data_format.md)

  Returns
  -------
  plot : html of the plot.

  """
  return subset_chans(T, T['meta']['bad_chans'], "Interpolations")

