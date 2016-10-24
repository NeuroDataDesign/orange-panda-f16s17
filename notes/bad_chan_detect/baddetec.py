import numpy as np

# Electrode detection via joint probability

# Inputs:
# data: EEG data
# elec: electrode selection list
# disc: discretization factor
# threshold: threshold

def baddetec_prob(data, elec, disc, threshold):
	numchans = len(data)
	numtrials = len(data[0])
	numtimepts = len(data[:,0])
	print numchans
	#print data
	# reshape data
	#data = np.reshape(data, (numchans, numtrials * numtimepts))
	# initialize joint prob array
	#jp = np.zeros((numchans, numtrials))
	# calculate joint prob across each channel
	#print data[:,]
	#for chan in data[:]:
		# get prob distribution
	#	probdist = get_probdist(data[chan], disc)
	#	for trial in 


swag = np.empty((3,4,5))
swag = np.array(([,12,3],[4,5,6, 7], [7,8,9]))
print swag0
#baddetec_prob(swag, 0, 0, 0)