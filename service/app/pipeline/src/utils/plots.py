"""Contains basic signal processing utilities.

"""
import sys
import pickle
from plotly.tools import FigureFactory as FF
import scipy.interpolate as interpolate
from scipy.signal import spectrogram
from pandas_datareader import data
import datetime
import cufflinks as cf
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
from collections import Counter
from scipy import signal

def type_summary(df):
  r"""Return statistics on the frequency of each data type in the data frame.

  Parameters
  ----------
  df : a pandas data frame
    Must indicies and column data set to the timestampls and eeg channel names.

  Returns
  -------
  A list of (`type`, `num_of_type`) tuples for each unique data type.

  """
  g = df.columns.to_series().groupby(df.dtypes).groups
  s = {k.name: v for k, v in g.items()}
  return [(kw, len(s[kw])) for kw in s]

def type_plot(df):
  r"""Get a plot of the summary of data types.

  Parameters
   ----------
  df : a pandas data frame
    Must indicies and column data set to the timestampls and eeg channel names.

  Returns
  -------
  html
    HTML code for the plot.

  """
  ts = type_summary(df)
  labels, values = zip(*ts)
  values = np.array(values)
  tot = float(np.sum(values))
  freq = values / float(np.sum(values))
  cols = np.column_stack([values, freq])
  df = pd.DataFrame(data=cols, index=labels, columns=['Freq', 'Density'])
  fig = df.iplot(columns=['Freq', 'Density'],
      title = "Frequency and Density of each data type over columns.",
      xTitle = 'Type',
      asFigure=True,
      theme='solar',
      kind='bar',
      legend=False,
      yTitle='Density',
      secondary_y = ['Freq'])
  fig.layout.update(dict(yaxis2=dict(title="Frequency", side="right")))
  return fig

def bad_values(df, choice='NaN', axis='Column'):  
  r"""Return a plot of frequency of some bad value over some axis.

  Parameters
  ----------
  df : a pandas data frame
    Must indicies and column data set to the timestampls and eeg channel names.
  choice: string
    'NaN' for NaN values of 'Inf' for inf values
  axis : string
    'Column' for column or 'Row' for row.
  Returns
  -------
  html
    HTML code for the plot.

  """
  if axis == 'Row':
    df = df.transpose()
  mis_val = None
  if choice == 'NaN':
    mis_val = df.isnull().sum()
  elif choice == 'Inf':
    df = df.fillna(0)
    df = df.replace(np.inf, np.nan)
    mis_val = df.isnull().sum()
  mis_val_percent = df.isnull().sum()/len(df)
  mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
  mis_val_table_ren_columns = mis_val_table.rename(
  columns = {0 : choice + ' Frequency', 1 : choice + ' Density'})
  fig = mis_val_table_ren_columns.iplot(kind='bar',
      secondary_y=[choice + ' Frequency'],
      legend=False,
      yTitle= choice + " Density",
      asFigure=True,
      theme='solar',
      title='Distribution of ' + choice + ' values over ' + axis,
      xTitle= axis,
      shared_xaxes=True,
      fill=True)
  fig.layout.update(dict(yaxis2=dict(title=choice + " Frequency",
          side="right")))
  return fig

def var_dist(df, axis='Column'):
  r"""Get a plot of the variance of each array on axis.

  Parameters
  ----------
  df : a pandas data frame
    Must indicies and column data set to the timestampls and eeg channel names.
  axis : string
    'Column' for column or 'Row' for row.
  Returns
  -------
  html : string
    HTML code for the plot.

  """
  if axis == 'Row':
    df = df.transpose()
  df = df.replace([np.inf, -np.inf], np.nan).dropna(how="all")
  var = df.var()
  minimum = var.min()
  maximum = var.max()
  logscale = ""
  if float(minimum) / maximum < .01:
    logscale = "logscale"
    var = df.apply(np.log, axis=1).var()
    minimum = var.min()
    maximum = var.max()
  pad = maximum - minimum / 10.0
  var = var.rename(
      columns = {0 : 'Variances'})
  fig = var.iplot(kind='bar',
      legend=False,
      theme='solar',
      asFigure=True,
      title='Variance for each ' +axis+ ' (excluding all NaN and Inf)',
      xTitle= axis,
      fill=True)
  fig.layout.update(dict(yaxis=dict(title = 'Variance ' + logscale,
    range=[minimum - pad, maximum + pad])))
  return fig

def my_spectrogram(df, ind, sfreq):
  r"""Get a plot of the summary of data types. 

  Parameters
  ----------
  df : a pandas data frame
   Must indicies and column data set to the timestampls and eeg channel names.

  Returns
  -------
  html
   HTML code for the plot.

  """
  cols = df.columns
  df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
  col = df.as_matrix()[:, int(ind)]
  f, t, Sxx = spectrogram(col.T, sfreq)
  sp = pd.DataFrame(data=np.log(Sxx.T), index = t, columns = f)
  fig = sp.iplot(kind='heatmap', colorscale='spectral', asFigure=True,
      title="Spectrogram for " + str(cols[ind]), theme='solar',
      xTitle='Time', yTitle = 'Frequency', zTitle="log magnitude")
  fig.data.update(dict(colorbar=dict(title="Magnitude logscale", titleside="right")))
  return fig

def anomaly(df):
  r"""Returns a plot showing the data anomalies in the EEG data..

  Parameters
  ----------
  df : a pandas data frame
    Must indicies and column data set to the timestampls and eeg channel names.

  Returns
  -------
  html
    HTML code for the plot.

  """
  df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
  S, U = np.linalg.eigh((df - df.mean()).cov())
  df = (df).dot(U[:, -1].T)
  df.columns=['Scatter Points']
  spline = df.rolling(window=df.shape[0]/50, center=True, min_periods = 0).mean()
  spline.columns=['Smoothed Values']
  resid = (df - spline).apply(np.abs)
  sd = np.sqrt(resid.var())
  hcb = spline + 5 * sd
  lcb = spline - 5 * sd
  out = (df - hcb > 0) | (df - lcb < 0) 
  fig = df.ix[out].iplot(title="Anomaly Detection Plot (outside 5 SD bands from rolling mean)",
      xTitle='Time', yTitle='Value', theme='solar', 
      kind='line', mode='markers', asFigure=True, legend=True)
  fig.data.update(dict(marker=dict(size = 4)))
  fig.data.extend(spline.iplot(kind='line', title='mean', asFigure=True, color='blue', legend=True).data)
  fig.data.extend(hcb.iplot(kind='line', title='5 Sigma', asFigure=True, color='red', legend=True).data)
  fig.data.extend(lcb.iplot(kind='line', title = '5 Sigma', asFigure=True, color='red', legend=True).data)
  fig.data[0].update(dict(name='Data'))
  fig.data[1].update(dict(name='Rolling Mean'))
  fig.data[2].update(dict(name='+ 5 SD'))
  fig.data[3].update(dict(name='- 5 SD'))
  return fig


def cv(df):
  r"""Returns a plot showing the cumulative variance explained.

  Parameters
  ----------
  df : a pandas data frame
    Must indicies and column data set to the timestampls and eeg channel names.
    
  Returns
  -------
  html
    HTML code for the plot.

  """
  df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
  mcdf = df - df.mean()
  S, U = np.linalg.eigh(mcdf.cov().as_matrix())
  S = S[::-1]
  total = np.sum(S)
  S = np.cumsum(S)
  S = S / total
  S = S[S < .9999]
  index = (np.arange(S.shape[0]) + 1).tolist()
  scree = pd.DataFrame(data = S.tolist(),
      index = range(1, len(S) + 1),
      columns=["eigenvalue"])
  fig = scree.iplot(kind='line', fill = True,
      title="Cumulative Variance Explained",
      asFigure=True, theme='solar')
  ytitle = "Cumulative Proportion of Total Variance Explained"
  xtitle = "Principal Component"
  fig.layout.update(dict(yaxis=dict(tick0=0, title = ytitle,
    titlefont=dict(color='lightgrey'), tickfont=dict(color='lightgrey')),
    xaxis=dict(tickvals=index, title=xtitle,
      titlefont=dict(color='lightgrey'), tickfont=dict(color='lightgrey'))))
  return fig 


def sparklines(df, title = 'Sparklines '):
  r"""Returns a plot showing the sparklines of the channels

  Parameters
  ----------
  df : a pandas data frame
    Must indicies and column data set to the timestampls and eeg channel names.
  title : string
    an alternative title for the plot.
    
  Returns
  -------
  html
    HTML code for the plot.

  """
  cp = ''
  if len(df.index) > 1000:
    cp = "(compressed to 1000 timesteps)"
    index = np.floor(np.linspace(0, len(df.index) - 1, 1000)).astype(np.int64)
    #new_ind = df.index[index]
    df = df.ix[df.index[index]]
    #df.index = new_ind
  df = df.replace([np.inf, -np.inf], np.nan).dropna(how="all")
  colind = np.floor(np.linspace(0, df.shape[1]-1, min(20, df.shape[1]))).astype(int)
  df = df.ix[:, colind]
  fig = df.iplot(kind='line',  asFigure=True,
      title=title + cp, subplots=True, xTitle='Row Index', yTitle='Column Index',
      shape=(len(df.columns), 1), shared_xaxes = True, theme='solar')
  fig.layout.update(height=200 + len(df.columns) * 60)
  return fig

def heatmap(df):
  r"""Returns a heatmap of the data frame.

  Parameters
  ----------
  df : a pandas data frame
    Must indicies and column data set to the timestampls and eeg channel names.
    
  Returns
  -------
  html
    HTML code for the plot.

  """
  df = df.replace([np.inf, -np.inf], np.nan).dropna(how="all")
  cp = ''
  minimum = df.min().min()
  maximum = df.max().max()
  mean = df.mean().mean()
  logscale = ""
  if maximum - mean > 10 * mean or mean - minimum > 10 * minimum:
    logscale = "logscale"
    df = df.apply(np.log, axis=1)
  if len(df.index) > 1000:
    cp = "(compressed to 1000 timesteps)"
    index = np.floor(np.linspace(0, len(df.index) - 1, 1000))
    df = df.ix[index.astype(int)]
  df.index = np.arange(len(df.index))
  fig = df.iplot(kind='heatmap', colorscale='spectral', asFigure=True,
      title="Heatmap over time " + cp, xTitle='Row Index',
      yTitle = 'Column Index', theme='solar')
  fig.data.update(dict(colorbar=dict(title="Magnitude " + logscale, titleside="right")))
  return fig

def correlation(df):
  r"""Returns a plot showing the correlation matrix.

  Parameters
  ----------
  df : a pandas data frame
    Must indicies and column data set to the timestampls and eeg channel names.
    
  Returns
  -------
  html
    HTML code for the plot.

  """
  correl = np.fliplr(df.corr(method='pearson').as_matrix())
  x = df.columns.format()
  y = x[::-1]
  z_text = np.around(correl, 2)
  colorscale = [[-1, '#0000FF'], [1, '#FF0000']]  # custom colorscale
  fig = pd.DataFrame(data=correl).iplot(kind='heatmap',
    theme='solar', asFigure=True)
  fig.layout.update(dict(title="Pearson Correlation Matrix", height = 800, width = 800, autosize = False))
  fig.data.update( 
      dict(colorscale = colorscale, showscale = True,
        colorbar=dict(title="correlation coefficient")))
  return fig

def wrap_html(html):
  r"""Wrapes in a string which includes html pre-requisites for plotly..

  Parameters
  ----------
  html : a string of html code
    
  Returns
  -------
  html
    the wrapped html code.

  """
  out = ''
  out += '<html><head>'
  out += '<title>PANDA Report</title>'
  out += '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">' 
  out += '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
  out += '</head><body style="background-color: rgb(21, 21, 22)">'
  out += html
  out += '</body></html>'
  return out

def get_messy_data(df):
  r"""Function for testing... just messes up the input data with Nans and Infs.

  Parameters
  ----------
  df : a pandas data frame
    
  Returns
  -------
  df
    a messy pandas data frame.

  """
  # Put one 'nan' in 25% of the rows, then one inf in 25%.
  df = df.as_matrix()
  from sklearn import datasets
  rng = np.random.RandomState(2) 
  dataset = datasets.load_boston()
  n_samples = df.shape[0]
  n_features = df.shape[1]
  missing_rate = 0.05
  n_missing_samples = int(np.floor(n_samples * missing_rate))
  missing_samples = np.hstack((np.zeros(n_samples - n_missing_samples),
     np.ones(n_missing_samples)))
  rng.shuffle(missing_samples)
  missing_features = rng.randint(0, n_features, n_missing_samples)
  X_missing = df.copy()
  X_missing[np.where(missing_samples)[0], missing_features] = np.nan
  rng.shuffle(missing_samples)
  X_missing[np.where(missing_samples)[0], missing_features] = np.inf
  return X_missing

def coherence_plot(df):
  r"""Returns a plot showing the coherence matrix.

  Parameters
  ----------
  df : a pandas data frame
    Must indicies and column data set to the timestampls and eeg channel names.
    
  Returns
  -------
  html
    HTML code for the plot.

  """
  df = df.ix[::100]
  currd = df.as_matrix()
  currd = currd.T
  coherearr = []
  for i in range (0, len(currd)):
    temparr = []
    for j in range (0, len(currd)):
      temparr.append(np.mean(
          signal.coherence(currd[i], currd[j], 500)[1]
        ))
    coherearr.append(temparr)
  df = pd.DataFrame(data=np.array(coherearr), index=df.columns, columns=df.columns)
  fig = df.iplot(kind='heatmap',
    theme='solar', asFigure=True)
  fig.layout.update(dict(title="Coherence", height=800, width=800))
  colorscale = [[0, '#0000FF'],[.5, '#FFFFFF'], [1, '#FF0000']]  # custom colorscale
  fig.data.update( 
      dict(colorscale=colorscale, showscale = True,
        colorbar=dict(title="coherence")))
  return fig

def get_stocks():
  r"""Get tech company stock prices for test data.

  Parameters
  ----------
    
  Returns
  -------
  df
    a data frame of the stocks

  """
  start = datetime.datetime(2010, 10, 10)
  end = datetime.datetime(2016,10,10)
  companies = ["goog", "aapl", "yhoo", "msft", "amzn"]
  cnames = ["Google",  "Apple", "Yahoo", "Microsoft", "Amazon"]
  df = pd.concat([data.DataReader(c, "yahoo", start, end).loc[:, "Close"] for c in companies], axis=1)
  df.columns = cnames
  df = pd.DataFrame(get_messy_data(df), index = df.index,
      columns = df.columns)
  df = df.apply(lambda x: pd.to_numeric(x, errors='ignore'))
  pickle.dump(df, open('stocks.pkl', 'wb'))

def plotly_hack(fig):
  r"""Work around to get plotly on html.

  Parameters
  ----------
  fig : plotly figure
    
  Returns
  -------
  html : string
    the html string

  """
  from plotly.offline.offline import _plot_html
  plot_html, plotdivid, width, height = _plot_html(
        fig, False, "", True, '100%', 525, False)
  return plot_html

def full_report(df):
  r"""Make all the plots for a data frame.

  Parameters
  ----------
  df : a pandas data frame
    Must indicies and column data set to the timestampls and eeg channel names.
    
  Returns
  -------
  html : string
    the html string

  """
  html = ''
  html += plotly_hack(type_plot(df))
  print "Making data type bar chart..."
  html += plotly_hack(bad_values(df, 'NaN', 'Column')) 
  print "Making NaNs over columns distribution bar chart..."
  html += plotly_hack(bad_values(df, 'Inf', 'Column')) 
  print "Making Infs over columns distribution bar chart..."
  html += plotly_hack(bad_values(df, 'NaN', 'Row')) 
  print "Making NaNs over rows distribution bar chart..."
  html += plotly_hack(bad_values(df, 'Inf', 'Row')) 
  print "Making Infs over rows distribution bar chart..."
  #html += plotly_hack(var_dist(df, 'Column')) 
  print "Making bar chart of the variance of each column..."
  #html += plotly_hack(heatmap(df)) 
  print "Making a heatmap of the entire dataset..."
  html += plotly_hack(sparklines(df)) 
  print "Making sparklines for each column..."
  d = len(df.columns)
  sp_compress = np.floor(np.linspace(0, d-1, min(d, 10)))
  print "Making spectrograms..."
  for i in sp_compress:
    html += plotly_hack(my_spectrogram(df, int(i), 500))
    print "    spectrogram made for " + str(df.columns[int(i)])
  html += plotly_hack(correlation(df))
  print "Making Pearson Correlation Matrix..."
  html += plotly_hack(cv(df))
  print "Making cumulative variance elbow of Principal Components..."
  html += plotly_hack(anomaly(df))
  print "Making anomaly graph..."
  html = wrap_html(html)
  print "Making coherence plot..."
  html += plotly_hack(coherence_plot(df))
  return html

if __name__ == "__main__":
  cf.go_offline()
  cf.set_config(theme='solar')
  df = None
  f_name = None
  if len(sys.argv) > 1:
    df = pickle.load(open(sys.argv[1], 'rb')) 
    f_name = sys.argv[1] + '.html'
  else:
    print "No Pickle file given, using example data from stocks"
    get_stocks()
    f_name = 'stocks.pkl.html'
    df = pickle.load(open('stocks.pkl', 'rb'))
  html = full_report(df)
  with open(f_name, 'w') as f:
    f.write(html)
  print "DONE! Wrote report to " + f_name


