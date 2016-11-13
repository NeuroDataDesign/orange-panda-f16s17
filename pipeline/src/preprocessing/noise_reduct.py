from utils.fourier import butter_highpass_filter, butter_lowpass_filter, butter_bandstop_filter
def reduce_noise(eeg_data, method, **kwargs):
	if method == 'placeholder': # for Minimum Viable Product
	    out = ""
	    out +=  "<h3>REDUCING NOISE</h3>"
	    for p in range(eeg_data.shape[3]):
	    	for t in range(eeg_data.shape[2]):
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
