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
    return fig

def var_dist(df, axis='Column'): 
    if axis == 'Row':
        df = df.transpose()
    df = df.replace([np.inf, -np.inf], np.nan).dropna(how="all")
    var = df.var()
    mean = var.mean()
    mcvar = var - mean
    mcvar = mcvar.rename(
            columns = {0 : 'Variances'})
    fig = mcvar.iplot(kind='bar',
           legend=False,
           yTitle= 'Variance',
           asFigure=True,
           title='Variance for each ' + axis + ' (mean centered, mean = ' + \
                   str(np.round(mean, 2)) + ',  excluding all NaN and Inf)',
           xTitle= axis,
           fill=True)
    return fig

def my_spectrogram(df, ind, sfreq):
    cols = df.columns
    df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
    col = df.as_matrix()[:, ind]
    f, t, Sxx = spectrogram(col.T, sfreq)
    sp = pd.DataFrame(data=np.log(Sxx.T), index = t, columns = f)
    return sp.iplot(kind='heatmap', colorscale='spectral', asFigure=True,
            title="Spectrogram for " + cols[ind] + ' (log magnitude)',
            xTitle='Time', yTitle = 'Frequency', zTitle="log magnitude")


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
    if len(df.index) > 1000:
        cp = "(time compressed from " + str(len(df.index)) + " to 1000)"
        index = np.floor(np.linspace(0, len(df.index) - 1, 1000))
        df = df.ix[index.astype(int)]
    return df.iplot(kind='heatmap', colorscale='spectral', asFigure=True,
            title="Heatmap over time " + cp, xTitle='Row Index',
            yTitle = 'Column Index')

def correlation(df):
    correl = df.corr(method='pearson').as_matrix()
    data = [
        go.Heatmap(
            z = correl.T,
            colorbar=go.ColorBar(title='Correlation coefficient (rho)'),
            zmin = -1,
            zmax = 1
        )
    ]
    layout = go.Layout(
        title='Pearson Correlation Matrix',
        xaxis=dict(
            title='Columns',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Columns',
            autorange='reversed',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    #fig['layout'].update(height = 800, width = 800, autosize=False)
    return fig

def special_dist(M):
    num_cols = M.shape[1]
    num_rows = M.shape[0]
    npr = map(lambda x: np.sum(np.isnan(M[x, :])),
            xrange(num_rows))
    npc = map(lambda x: np.sum(np.isnan(M[:, x])),
            xrange(num_cols))
    ipr = map(lambda x: np.sum(np.isinf(M[x, :])),
            xrange(num_rows))
    ipc = map(lambda x: np.sum(np.isinf(M[:, x])),
            xrange(num_cols))
    mr = map(lambda x: np.nanmean(M[x, :]),
            xrange(num_rows))
    mc = map(lambda x: np.nanmean(M[:, x]),
            xrange(num_cols))
    vr = map(lambda x: np.nanvar(M[x, :]),
            xrange(num_rows))
    vc = map(lambda x: np.nanvar(M[:, x]),
            xrange(num_cols))
    return npr, npc, ipr, ipc, mr, mc, vr, vc



def plotly_hist(data, x_ticks):
    data = [
        go.Histogram(
            x = data
        )
    ]
    layout = go.Layout(
            xaxis = go.XAxis(dict(ticktext=x_ticks,
                tickvals=range(len(labels))),
                showticklabels=True,
                range=[0, len(labels)],
                mirror=True),
        )
    figure = go.Figure(data=data, layout=layout)
    return plotly_hack(figure)

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
    iris = data.DataReader("yhoo", "yahoo", datetime.datetime(2007, 1, 1), 
                datetime.datetime(2012,1,1))
   # iris = pdr.get_data_yahoo('AAPL')
    iris = iris.drop('Volume', 1)
    #iris = pd.read_csv('iris.csv')
    iris = pd.DataFrame(get_messy_data(iris), index = iris.index, columns = iris.columns)
    iris = iris.apply(lambda x: pd.to_numeric(x, errors='ignore'))
    html = ''
    #html += plotly_hack(type_plot(iris))
    html += plotly_hack(type_plot(iris))
    html += plotly_hack(bad_values(iris, 'NaN', 'Column')) 
    html += plotly_hack(bad_values(iris, 'Inf', 'Column')) 
    html += plotly_hack(bad_values(iris, 'NaN', 'Row')) 
    html += plotly_hack(bad_values(iris, 'Inf', 'Row')) 
    html += plotly_hack(var_dist(iris, 'Column')) 
    #html += var_dist(iris, 'Row') 
    html += plotly_hack(heatmap(iris)) 
    html += plotly_hack(sparklines(iris)) 
    for i in range(len(iris.columns)):
        html += plotly_hack(my_spectrogram(iris, i, 1))
    neg_iris = iris.copy()
    neg_iris.ix[:, :] = np.random.random(iris.shape)
    html += plotly_hack(correlation(neg_iris))
    html = wrap_html(html)
    with open('meda_example.html', 'w') as f:
        f.write(html)
