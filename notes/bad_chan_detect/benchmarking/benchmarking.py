import numpy as np
from scipy.stats import kurtosis
from sklearn.neighbors.kde import KernelDensity
from sklearn.grid_search import GridSearchCV
import h5py
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *

# reshape the data
def reshape(inEEG):
    if len(inEEG.shape) == 3:
        electrodes = inEEG.shape[1]
        times = inEEG.shape[0]
        trials = inEEG.shape[2]
        return np.reshape(inEEG, (inEEG.shape[0] * inEEG.shape[2], inEEG.shape[1]))
    elif len(inEEG.shape) != 1 and len(inEEG.shape) != 2:
        # fail case
        print "fail"
    else:
        return inEEG

# kde wrapper func
def kdewrap(indata, kernel):
    grid = GridSearchCV(KernelDensity(),
                    {'bandwidth': np.linspace(0.1, 1.0, 30)},
                    cv=10) # 10-fold cross-validation
    grid.fit(indata[:, None])
    kde = KernelDensity(kernel=kernel, bandwidth=grid.best_params_["bandwidth"]).fit(indata[:, np.newaxis])
    return kde.score_samples(indata[:, np.newaxis])

# silverman for simpler kde
def silverman(data):
    # compute sttddev
    stddev = np.std(data)
    q75, q25 = np.percentile(data, [75 ,25])
    iqr = q75 - q25
    m = min(iqr/1.349, stddev)
    silv = (0.9 * m)/(len(data) ** .2)
    if silv == 0:
        return 0.5
    return silv

# kde simpler wrapper
def kdewrap_simp(indata, kernel):
    kde = KernelDensity(kernel=kernel, bandwidth=silverman(indata)).fit(indata[:, np.newaxis])
    return kde.score_samples(indata[:, np.newaxis])

# prob bad detec
def prob_baddetec(inEEG, threshold, probfunc):
    electrodes = inEEG.shape[1]
    
    # Start by reshaping data (if necessary)
    if len(inEEG.shape) == 3:
        inEEG = np.reshape(inEEG, (inEEG.shape[0] * inEEG.shape[2], inEEG.shape[1]))
    elif len(inEEG.shape) != 1 and len(inEEG.shape) != 2:
        # fail case
        return -1
    
    # Then, initialize a probability vector of electrode length
    probvec = np.zeros(electrodes)
    
    # iterate through electrodes and get joint probs
    for i in range(0, electrodes):
        # get prob distribution
        probdist = probfunc(inEEG[:, i], 'gaussian')
        # using probdist find joint prob
        probvec[i] = np.sum(probdist)

    # normalize probvec
    # first calc mean
    avg = np.mean(probvec)
    # then st, d dev
    stddev = np.std(probvec)
    # then figure out which electrodes are bad
    badelec = []
    #print probvec
    for t in threshold:
        bad_list = []
        for i in range(0, len(probvec)):
            #print i, avg, stddev, (avg - probvec[i]) / stddev
            if abs((avg - probvec[i]) / stddev) >= t:
                bad_list.append(i)
        badelec.append(bad_list)
    return badelec

# kurt bad detec
def kurt_baddetec(inEEG, threshold):
    electrodes = inEEG.shape[1]
    
    # Start by reshaping data (if necessary)
    if len(inEEG.shape) == 3:
        inEEG = np.reshape(inEEG, (inEEG.shape[0] * inEEG.shape[2], inEEG.shape[1]))
    elif len(inEEG.shape) != 1 and len(inEEG.shape) != 2:
        # fail case
        return -1
    
    # Then, initialize a probability vector of electrode length
    kurtvec = np.zeros(electrodes)
    
    # iterate through electrodes and get kurtoses
    for i in range(0, electrodes):
        # add kurtosis to the vector
        kurtvec[i] = kurtosis(inEEG[:, i])
        #print kurtvec[i]
        
    
    # normalize kurtvec
    # first calc mean
    avg = np.mean(kurtvec)
    # then std dev
    stddev = np.std(kurtvec)
    # then figure out which electrodes are bad
    badelec = []
    #print probvec
    for t in threshold:
        bad_list = []
        for i in range(0, len(kurtvec)):
            #print i, avg, stddev, (avg - probvec[i]) / stddev
            if abs((avg - kurtvec[i]) / stddev) >= t:
                bad_list.append(i)
        badelec.append(bad_list)
    return badelec

# spectral analysis bad electrodes
def spec_baddetec(inEEG, posthresh, negthresh):
    electrodes = inEEG.shape[1]

    # Start by reshaping data (if necessary)
    if len(inEEG.shape) == 3:
        inEEG = np.reshape(inEEG, (inEEG.shape[0] * inEEG.shape[2], inEEG.shape[1]))
    elif len(inEEG.shape) != 1 and len(inEEG.shape) != 2:
        # fail case
        return -1

    # initialize badelec as an empty array
    badelec = []

    # iterate through electrodes and get spectral densities
    for i in range(0, electrodes):
        # get frequency spectrum for electrode
        sp = np.fft.fft(inEEG[:, i]).real
        sp = sp - np.mean(sp)
        for power in sp:
            if power > posthresh or power < negthresh:
                badelec.append(i)
                break
        
    return badelec

# Good electrodes
def good_elec(inEEG, badelec):
    return np.delete(inEEG, badelec, 1)

# qualitative and quantitative evaluations
def quant_eval(badelec, expected):
    print "Expected:", expected
    print "Actual:", badelec

def qual_plot(data, title):
    # Setup plotly data
    datasets = []

    for i in range(0, data.shape[1]):
        datasets.append(Scatter(
            x = times,
            y = data[::1000,i],
            name = 'Sample ' + str(i)
        ))

    # Setup layout

    layout = dict(title = title,
                  xaxis = dict(title = 'Time (micro seconds)'),
                  yaxis = dict(title = 'Amplitude (mV)'),
                  )

    # Make figure object

    fig = dict(data=datasets, layout=layout)
    
    plot(fig, filename = "plots/" + title)

def live_reindex(dead, bad):
    new_bad = []
    for bad_elec in bad:
        i = 0
        for dead_elec in dead:
            if dead_elec < bad_elec:
                i += 1
        new_bad.append(bad_elec - i)
    return new_bad

##### Gather all data 

# test data
numvals = 1000
# First, build the relevant linspace to grab 1000 points
times = np.linspace(0, 1, numvals)
# Then define the general sine wave used throughout
sin = np.sin(2 * np.pi * times)
testpatient = np.column_stack([sin] * 50)
# Patient 0 data
D = h5py.File("full_A00051826_01.mat", 'r')
patient0 = D["result"]["data"][:, :]
patient0_0 = patient0[:patient0.shape[0]/2, :]
patient0_1 = patient0[patient0.shape[0]/2:, :]
# Patient 1 data
D1 = h5py.File("test.mat", 'r')
patient1 = D1["result"]["data"][:, :]
patient1_0 = patient1[:patient1.shape[0]/2, :]
patient1_1 = patient1[patient1.shape[0]/2:, :]
# Final data list
all_dat = [testpatient, patient0_0, patient0_1, patient1_0, patient1_1]
# Titles for each data set
titles = ["test", "patient0_0", "patient0_1", "patient1_0", "patient1_1"]

# Get detected bad channels
badchans = D["result"]["auto_badchans"][:]
# Manually add electrodes with dead signals
patient0_dead = [0, 7, 13, 19, 23]
patient0_bad = [int(i) for i in badchans]
patient0_bad.sort()
# Get detected bad channels
badchans = D1["result"]["auto_badchans"][:]
# Manually add electrodes with dead signals
patient1_dead = [0, 7, 19, 23, 30]
patient1_bad  = [int(i) for i in badchans]
patient1_bad.sort()
# create list for these as well
dead_list = [[], patient0_dead, patient0_dead, patient1_dead,  patient1_dead]
bad_list = [[], patient0_bad, patient0_bad, patient1_bad,  patient1_bad]

# list of thresholds to test
thresholds = [3, 2.75, 2.5, 2.25, 2, 1.75, 1.5]
#badchans = live_reindex(dead_elec, badchans)

##### Kurtosis Based Detection

test_dat = [testpatient]
print titles[0]

"""
for i in range(len(all_dat)):
    qual_plot(all_dat[i], titles[i])
 
print "Graphs finished!"

for i in range(len(all_dat)):
    data = all_dat[i]
    dead_elec = dead_list[i]
    badchans = bad_list[i]

    file_name = str(titles[i] + "_live_kurt.txt")
    f = open(file_name, 'w')
    f.write("Kurtosis Based Detection\n")
    f.write(titles[i] + "\n")
    f.write("Actual Badchans\n")
    live_badchans = live_reindex(dead_elec, badchans)
    f.write(str(live_badchans) + '\n')
    f.write("Live Electrode Only Results:\n")
    live = np.delete(data, dead_elec, axis=1)
    live_result = kurt_baddetec(live, thresholds)
    for j in range(len(thresholds)):
        f.write("Threshold " + str(thresholds[j]) + '\n')
        f.write(str(live_result[j]) + '\n') 
    f.close()

    file_name = str(titles[i] + "_kurt.txt")
    f = open(file_name, 'w')
    f.write("Kurtosis Based Detection\n")
    f.write(titles[i] + "\n")
    f.write("Actual Badchans\n")
    f.write(str(badchans) + '\n')
    f.write("All Electrode Results:\n")
    result = kurt_baddetec(data, thresholds)
    for j in range(len(thresholds)):
        f.write("Threshold " + str(thresholds[j]) + '\n')
        f.write(str(result[j]) + '\n') 
    f.close()

print "Kurtosis finished!"


for i in range(len(all_dat)):
    data = all_dat[i]
    dead_elec = dead_list[i]
    badchans = bad_list[i]
file_name = str(titles[i] + "_live_spec.txt")
    f = open(file_name, 'w')
    f.write("Spectral Based Detection\n")
    f.write(titles[i] + "\n")
    f.write("Actual Badchans\n")
    live_badchans = live_reindex(dead_elec, badchans)
    f.write(str(live_badchans) + '\n')
    f.write("Live Electrode Only Results:\n")
    live = np.delete(data, dead_elec, axis=1)
    live_result = spec_baddetec(live, -600, 600)
    f.write(str(live_result) + '\n') 
    f.close()

    file_name = str(titles[i] + "_spec.txt")
    f = open(file_name, 'w')
    f.write("Spectral Based Detection\n")
    f.write(titles[i] + "\n")
    f.write("Actual Badchans\n")
    f.write(str(badchans) + '\n')
    f.write("All Electrode Results:\n")
    result = spec_baddetec(data, -600, 600)
    f.write(str(result) + '\n') 
    f.close()

print "Spec finished!"

"""

for i in range(len(all_dat)):
    if i == 0:
	continue
    else:
    	data = all_dat[i][::1000,:]
    dead_elec = dead_list[i]
    badchans = bad_list[i]
    print data.shape

    file_name = str(titles[i] + "_live_prob.txt")
    f = open(file_name, 'w')
    f.write("Spectral Based Detection\n")
    f.write(titles[i] + "\n")
    f.write("Actual Badchans\n")
    live_badchans = live_reindex(dead_elec, badchans)
    f.write(str(live_badchans) + '\n')
    f.write("Live Electrode Only Results:\n")
    live = np.delete(data, dead_elec, axis=1)
    live_result = prob_baddetec(live, thresholds, kdewrap)
    for j in range(len(thresholds)):
        f.write("Threshold " + str(thresholds[j]) + '\n')
        f.write(str(live_result[j]) + '\n') 
    f.close()

    file_name = str(titles[i] + "_prob.txt")
    f = open(file_name, 'w')
    f.write("Spectral Based Detection\n")
    f.write(titles[i] + "\n")
    f.write("Actual Badchans\n")
    f.write(str(badchans) + '\n')
    f.write("All Electrode Results:\n")
    result = prob_baddetec(data, thresholds, kdewrap)
    for j in range(len(thresholds)):
        f.write("Threshold " + str(thresholds[j]) + '\n')
        f.write(str(result[j]) + '\n') 
    f.close()

print "Prob finished!"


