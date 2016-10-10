"""Contains basic signal processing utilities.

"""
from scipy.signal import butter, lfilter, freqz

def _butter_lowpass(cutoff, Fs, order=5):
    nyq = 0.5 * Fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff,
                    btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, Fs, order=5):
    r"""Constructs a lowpass filter at given cutoff

    Parameters
    ----------
    data : numpy array 
        a `t` by 1 numpy array representing a discretely sampled time-series signal with `t` timesteps.

    cutoff : float
        the upper bound frequency let through the filter.
    Fs : float
        the sampling frequency of the signal
    order : int
        the order of the filter

    Returns
    -------
    filtered_signal : numpy matrix
        the filtered signal

    See Also
    --------
    butter_highpass_filter :
    butter_bandpass_filter :
    butter_bandstop_filter :

    Notes
    -----
    Relies on scipy.signal

    Examples
    --------

    >>> T = 10 # Signal lasts 10 seconds
    >>> Fs = 40 # We sample the signal at 40 Hz
    >>> w1 = .1
    >>> w2 = 1
    >>> w3 = 4
    >>> sample_points = np.linspace(0, T, T * Fs)
    >>> sines_w1 = np.sin(w1 * 2 * np.pi * sample_points)
    >>> sines_w2 = np.sin(w2 * 2 * np.pi * sample_points)
    >>> sines_w3 = np.sin(w3 * 2 * np.pi * sample_points)
    >>> signal = sines_w1 + sines_w2 + sines_w3
    >>> new_signal = butter_lowpass_filter(signal, 2, Fs, 5)

    """
    b, a = _butter_lowpass(cutoff, Fs, order=order)
    filtered_signal = lfilter(b, a, data)
    return filtered_signal


def _butter_highpass(cutoff, Fs, order=5):
    nyq = 0.5 * Fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff,
                btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, Fs, order=5):
    r"""Constructs a highpass filter at given cutoff

    Parameters
    ----------
    data : ``ndarray`` 
        a `(t, 1)` ``ndarray`` representing a discretely sampled time-series signal with `t` timesteps.

    cutoff : float
        the upper bound frequency let through the filter.
    Fs : float
        the sampling frequency of the signal
    order : int
        the order of the filter

    Returns
    -------
    filtered_signal : numpy matrix
        the filtered signal

    See Also
    --------
    butter_highpass_filter :
    butter_bandpass_filter :
    butter_bandstop_filter :

    Notes
    -----
    Relies on scipy.signal

    Examples
    --------

    >>> T = 10 # Signal lasts 10 seconds
    >>> Fs = 40 # We sample the signal at 40 Hz
    >>> w1 = .1
    >>> w2 = 1
    >>> w3 = 4
    >>> sample_points = np.linspace(0, T, T * Fs)
    >>> sines_w1 = np.sin(w1 * 2 * np.pi * sample_points)
    >>> sines_w2 = np.sin(w2 * 2 * np.pi * sample_points)
    >>> sines_w3 = np.sin(w3 * 2 * np.pi * sample_points)
    >>> signal = sines_w1 + sines_w2 + sines_w3
    >>> new_signal = butter_highpass_filter(signal, 2, Fs, 5)

    """
    b, a = _butter_highpass(cutoff, Fs, order=order)
    filtered_signal = lfilter(b, a, data)
    return filtered_signal

def _butter_bandpass(cutoff, Fs, order=5):
    nyq = 0.5 * Fs
    lowcut = cutoff[0] / nyq
    highcut = cutoff[1] / nyq
    b, a = butter(order, [lowcut, highcut],
                btype='bandpass', analog=False)
    return b, a

def butter_bandpass_filter(data, cutoff, Fs, order=5):
    r"""Constructs a bandpass filter at given cutoff range

    Parameters
    ----------
    data : ``ndarray`` 
        a `(t, 1)` ``ndarray`` representing a discretely sampled time-series signal with `t` timesteps.

    cutoff : [float, float]
        the [lower, upper] bound frequency let through the filter.
    Fs : float
        the sampling frequency of the signal
    order : int
        the order of the filter

    Returns
    -------
    filtered_signal : numpy matrix
        the filtered signal

    See Also
    --------
    butter_highpass_filter :
    butter_bandpass_filter :
    butter_bandstop_filter :

    Notes
    -----
    Relies on scipy.signal

    Examples
    --------

    >>> T = 10 # Signal lasts 10 seconds
    >>> Fs = 40 # We sample the signal at 40 Hz
    >>> w1 = .1
    >>> w2 = 1
    >>> w3 = 4
    >>> sample_points = np.linspace(0, T, T * Fs)
    >>> sines_w1 = np.sin(w1 * 2 * np.pi * sample_points)
    >>> sines_w2 = np.sin(w2 * 2 * np.pi * sample_points)
    >>> sines_w3 = np.sin(w3 * 2 * np.pi * sample_points)
    >>> signal = sines_w1 + sines_w2 + sines_w3
    >>> new_signal = butter_bandpass_filter(signal, [.6, 2], Fs, 5)

    """
    b, a = _butter_bandpass(cutoff, Fs, order=order)
    filtered_signal = lfilter(b, a, data)
    return filtered_signal

def _butter_bandstop(cutoff, Fs, order=5):
    nyq = 0.5 * Fs
    lowcut = cutoff[0] / nyq
    highcut = cutoff[1] / nyq
    b, a = butter(order, [lowcut, highcut],
                btype='bandstop', analog=False)
    return b, a

def butter_bandstop_filter(data, cutoff, Fs, order=5):
    r"""Constructs a bandstop filter at given cutoff

    Parameters
    ----------
    data : ``ndarray`` 
        a `(t, 1)` ``ndarray`` representing a discretely sampled time-series signal with `t` timesteps.

    cutoff : [float, float]
        the [lower, upper] bound frequency let stop with the filter.
    Fs : float
        the sampling frequency of the signal
    order : int
        the order of the filter

    Returns
    -------
    filtered_signal : numpy matrix
        the filtered signal

    See Also
    --------
    butter_highpass_filter :
    butter_bandpass_filter :
    butter_bandstop_filter :

    Notes
    -----
    Relies on scipy.signal

    Examples
    --------

    >>> T = 10 # Signal lasts 10 seconds
    >>> Fs = 40 # We sample the signal at 40 Hz
    >>> w1 = .1
    >>> w2 = 1
    >>> w3 = 4
    >>> sample_points = np.linspace(0, T, T * Fs)
    >>> sines_w1 = np.sin(w1 * 2 * np.pi * sample_points)
    >>> sines_w2 = np.sin(w2 * 2 * np.pi * sample_points)
    >>> sines_w3 = np.sin(w3 * 2 * np.pi * sample_points)
    >>> signal = sines_w1 + sines_w2 + sines_w3
    >>> new_signal = butter_bandstop_filter(signal, 2, Fs, 5)

    """
    b, a = _butter_bandstop(cutoff, Fs, order=order)
    filtered_signal = lfilter(b, a, data)
    return filtered_signal
