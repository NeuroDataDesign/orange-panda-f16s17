
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
    for i in range(0, len(probvec)):
        bad_list = []
        for t in threshold:
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
    for i in range(0, len(kurtvec)):
        #print i, avg, stddev, (avg - kurtvec[i]) / stddev
        if abs((avg - kurtvec[i]) / stddev) >= threshold:
            badelec.append(i)
            
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
    
    plot(fig)

# run on sample data

D = h5py.File("full_A00051826_01.mat", 'r')
patient0 = D["result"]["data"][:, :]
# Get detected bad channels
badchans = D["result"]["auto_badchans"][:]
# Append electrodes with dead signals
dead_elec = [0, 7, 13, 19, 23]
#badchans = np.append(badchans).tolist()
badchans = [int(i) for i in badchans]
badchans.sort()
print badchans

no_zero = patient0[:, -dead_elec]

#no_zero = prob_baddetec(patient0, [3, 2.75, 2.5, 2.25, 2, 1.75, 1.5], kdewrap)
