from scipy.signal import butter, lfilter, freqz

def _butter_lowpass(cutoff, Fs, order=5):
    nyq = 0.5 * Fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff,
                    btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, Fs, order=5):
    b, a = _butter_lowpass(cutoff, Fs, order=order)
    y = lfilter(b, a, data)
    return y


def _butter_highpass(cutoff, Fs, order=5):
    nyq = 0.5 * Fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff,
                btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, Fs, order=5):
    b, a = _butter_highpass(cutoff, Fs, order=order)
    y = lfilter(b, a, data)
    return y

def _butter_bandpass(cutoff, Fs, order=5):
    nyq = 0.5 * Fs
    lowcut = cutoff[0] / nyq
    highcut = cutoff[1] / nyq
    b, a = butter(order, [lowcut, highcut],
                btype='bandpass', analog=False)
    return b, a

def butter_bandpass_filter(data, cutoff, Fs, order=5):
    b, a = _butter_bandpass(cutoff, Fs, order=order)
    y = lfilter(b, a, data)
    return y

def _butter_bandstop(cutoff, Fs, order=5):
    nyq = 0.5 * Fs
    lowcut = cutoff[0] / nyq
    highcut = cutoff[1] / nyq
    b, a = butter(order, [lowcut, highcut],
                btype='bandstop', analog=False)
    return b, a

def butter_bandstop_filter(data, cutoff, Fs, order=5):
    b, a = _butter_bandstop(cutoff, Fs, order=order)
    y = lfilter(b, a, data)
    return y
