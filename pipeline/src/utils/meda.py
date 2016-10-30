from plotly.tools import FigureFactory as FF
import scipy.interpolate as interpolate
import colorlover as cl
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
from plots import plotly_hack
# matrix exploratory data analysis
def type_summary(df):
    g = df.columns.to_series().groupby(df.dtypes).groups
    s = {k.name: v for k, v in g.items()}
    return [(kw, len(s[kw])) for kw in s]

def type_plot(df):
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
            kind='bar',
            legend=False,
            yTitle='Density',
            secondary_y = ['Freq'])
    fig.layout.update(dict(yaxis2=dict(title="Frequency", side="right")))
    return fig

def bad_values(df, choice='NaN', axis='Column'): 
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
            title='Distribution of ' + choice + ' values over ' + axis,
            xTitle= axis,
            shared_xaxes=True,
            fill=True)
    fig.layout.update(dict(yaxis2=dict(title=choice + " Frequency",
                    side="right")))
    return fig

def var_dist(df, axis='Column'): 
    if axis == 'Row':
        df = df.transpose()
    df = df.replace([np.inf, -np.inf], np.nan).dropna(how="all")
    var = df.var()
    minimum = var.min()
    maximum = var.max()
    logscale = ""
    if float(minimum) / maximum < .1:
        logscale = "logscale"
        var = df.apply(np.log, axis=1).var()
        minimum = var.min()
        maximum = var.max()
    pad = maximum - minimum / 10.0
    var = var.rename(
            columns = {0 : 'Variances'})
    fig = var.iplot(kind='bar',
           legend=False,
           asFigure=True,
           title='Variance for each ' +axis+ ' (excluding all NaN and Inf)',
           xTitle= axis,
           fill=True)
    fig.layout.update(dict(yaxis=dict(title = 'Variance ' + logscale,
        range=[minimum - pad, maximum + pad])))
    return fig

def my_spectrogram(df, ind, sfreq):
    cols = df.columns
    df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
    col = df.as_matrix()[:, ind]
    f, t, Sxx = spectrogram(col.T, sfreq)
    sp = pd.DataFrame(data=np.log(Sxx.T), index = t, columns = f)
    fig = sp.iplot(kind='heatmap', colorscale='spectral', asFigure=True,
            title="Spectrogram for " + cols[ind],
            xTitle='Time', yTitle = 'Frequency', zTitle="log magnitude")
    fig.data.update(dict(colorbar=dict(title="Magnitude logscale", titleside="right")))
    return fig

def anomaly(df):
    df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
    mcdf = df - df.mean()
    U, S, Vt = np.linalg.svd(mcdf.as_matrix(), full_matrices = False)
    df = (df).dot(U[0, :])
    df.columns=['Scatter Points']
    spline = df.rolling(window=df.shape[0]/50, center=True, min_periods = 0).mean()
    spline.columns=['Smoothed Values']
    resid = (df - spline).apply(np.abs)
    sd = np.sqrt(resid.var())
    hcb = spline + 1 * sd
    lcb = spline - 1 * sd
    fig = df.iplot(title="Anomaly Detection Plot (outside 1 SD bands from rolling mean)",
            xTitle='Time', yTitle='Value', 
            kind='line', mode='markers', asFigure=True, legend=True)
    fig.data.update(dict(marker=dict(size = 6)))
    fig.data.extend(spline.iplot(kind='line', asFigure=True, color='blue', legend=True).data)
    fig.data.extend(hcb.iplot(kind='line', asFigure=True, color='red', legend=True).data)
    fig.data.extend(lcb.iplot(kind='line', asFigure=True, color='red', legend=True).data)
    return fig


def cv(df):
    df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
    mcdf = df - df.mean()
    U, S, Vt = np.linalg.svd(mcdf.as_matrix(), full_matrices = False)
    S = S**2
    total = np.sum(S)
    S = np.cumsum(S)
    S = S / total
    index = (np.arange(S.shape[0]) + 1).tolist()
    scree = pd.DataFrame(data = S.tolist(), index = range(1, len(df.columns) + 1), columns=["eigenvalue"])
    fig = scree.iplot(kind='line', fill = True,
            title="Cumulative Variance Explained",
            asFigure=True)
    ytitle = "Cumulative Proportion of Total Variance Explained"
    xtitle = "Principal Component"
    fig.layout.update(dict(yaxis=dict(tick0=0, title = ytitle),
        xaxis=dict(tickvals=index, title=xtitle)))
    return fig 


def sparklines(df):
    cp = ''
    if len(df.index) > 1000:
        cp = "(time compressed from " + str(len(df.index)) + " to 1000)"
        index = np.floor(np.linspace(0, len(df.index) - 1, 1000))
        df = df.ix[index.astype(int)]
    df = df.replace([np.inf, -np.inf], np.nan).dropna(how="all")
    return df.iplot(kind='line',  asFigure=True,
            title="Sparklines " + cp,  xTitle='Row Index',
            shared_xaxes=True,
            subplots=True,
            shape=(len(df.columns), 1))

def heatmap(df):
    cp = ''
    minimum = df.min().min()
    maximum = df.max().max()
    mean = df.mean().mean()
    logscale = ""
    if float(mean) / maximum < .1 or float(minimum) / mean < .1:
        logscale = "logscale"
        var = df.apply(np.log, axis=1).var()
        minimum = var.min()
        maximum = var.max()
    if len(df.index) > 1000:
        cp = "(time compressed from " + str(len(df.index)) + " to 1000)"
        index = np.floor(np.linspace(0, len(df.index) - 1, 1000))
        df = df.ix[index.astype(int)]
    df = df.apply(np.log, axis=1)
    fig = df.iplot(kind='heatmap', colorscale='spectral', asFigure=True,
            title="Heatmap over time " + cp, xTitle='Row Index',
            yTitle = 'Column Index')
    fig.data.update(dict(colorbar=dict(title="Magnitude " + logscale, titleside="right")))
    return fig

def correlation(df):
    correl = np.fliplr(df.corr(method='pearson').as_matrix())
    x = df.columns.format()
    y = x[::-1]
    z_text = np.around(correl, 2)
    colorscale = [[-1, '#0000FF'], [1, '#FF0000']]  # custom colorscale
    print x
    print y
    print z_text
    fig = FF.create_annotated_heatmap(correl, x=x, y=y, annotation_text=z_text)
    fig.layout.update(dict(title="Pearson Correlation Matrix", height = 800, width = 800, autosize = False))
    fig.data.update( 
            dict(colorscale = colorscale, showscale = True,
                colorbar=dict(title="correlation coefficient")))
    return fig

def wrap_html(html):
    out = ''
    out += '<html><head>'
    out += '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">' 
    out += '<script src="https://cdn.plot.ly/plotly-latest.min.js">'
    out += '</script></head><body>'
    out += html
    out += '</body></html>'
    return out

def get_messy_data(df):
    # Put one 'nan' in 25% of the rows, then one inf in 25%.
    df = df.as_matrix()
    from sklearn import datasets
    rng = np.random.RandomState(2) 
    dataset = datasets.load_boston()
    n_samples = df.shape[0]
    n_features = df.shape[1]
    missing_rate = 0.10
    n_missing_samples = np.floor(n_samples * missing_rate)
    missing_samples = np.hstack((np.zeros(n_samples - n_missing_samples,
					  dtype=np.bool),
				 np.ones(n_missing_samples,
					 dtype=np.bool)))
    rng.shuffle(missing_samples)
    missing_features = rng.randint(0, n_features, n_missing_samples)
    X_missing = df.copy()
    X_missing[np.where(missing_samples)[0], missing_features] = np.nan
    rng.shuffle(missing_samples)
    X_missing[np.where(missing_samples)[0], missing_features] = np.inf
    return X_missing


if __name__ == "__main__":
    cf.go_offline()
    start = datetime.datetime(2010, 10, 10)
    end = datetime.datetime(2016,10,10)
    companies = ["goog", "aapl", "yhoo", "msft", "amzn"]
    cnames = ["Google",  "Apple", "Yahoo", "Microsoft", "Amazon"]
    df = pd.concat([data.DataReader(c, "yahoo", start, end).loc[:, "Close"] for c in companies], axis=1)
    df.columns = cnames
    df = pd.DataFrame(get_messy_data(df), index = df.index, columns = df.columns)
    df = df.apply(lambda x: pd.to_numeric(x, errors='ignore'))
    html = ''
    #html += plotly_hack(type_plot(iris))
    html += plotly_hack(type_plot(df))
    html += plotly_hack(bad_values(df, 'NaN', 'Column')) 
    html += plotly_hack(bad_values(df, 'Inf', 'Column')) 
    html += plotly_hack(bad_values(df, 'NaN', 'Row')) 
    html += plotly_hack(bad_values(df, 'Inf', 'Row')) 
    html += plotly_hack(var_dist(df, 'Column')) 
    #html += var_dist(iris, 'Row') 
    html += plotly_hack(heatmap(df)) 
    html += plotly_hack(sparklines(df)) 
    d = len(df.columns)
    sp_compress = np.floor(np.linspace(0, d-1, min(d, 10)))
    for i in sp_compress:
        html += plotly_hack(my_spectrogram(df, i, 1))
    html += plotly_hack(correlation(df))
    html += plotly_hack(cv(df))
    html += plotly_hack(anomaly(df))
    html = wrap_html(html)
    with open('meda_example.html', 'w') as f:
        f.write(html)
