import utils.plots as plt
import pandas as pd

def subset_chans(T, S, title):
  cct = [pd.DataFrame(data=T['eeg'][:, c]) for c in S]
  if len(cct) > 0:
    df = pd.concat(cct, axis=1)
    df.columns = [str(c) for c in S]
    df.index = map(lambda t: t[0]/1000.0, T['times'])
    return plt.plotly_hack(plt.sparklines(df, title=title))
  else:
    return'<p>No bad channels!</p>'

def zeroed(T):
  return subset_chans(T, T['meta']['zeroed_chans'], "Zeroed Channels")

def bad_electrodes(T):
  return subset_chans(T, T['meta']['bad_chans'], "Bad Channels")

def interp_electrodes(T):
  return subset_chans(T, T['meta']['bad_chans'], "Interpolations")
