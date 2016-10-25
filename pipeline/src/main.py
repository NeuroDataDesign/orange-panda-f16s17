"""This is the docstring for the example.py module.  Modules names should
have short, all-lowercase names.  The module name may have underscores if
this improves readability.

Every module should have a docstring at the very top of the file.  The
module's docstring may extend over multiple lines.  If your docstring does
extend over multiple lines, the closing three quotation marks must be on
a line by itself, preferably preceded by a blank line.

"""
import numpy as np
import ast
from utils.get_data import get_record, get_patients, make_h5py_object
from utils.clean_data import get_eeg_data, get_times, get_electrode_coords
from utils.fourier import butter_highpass_filter, butter_lowpass_filter, butter_bandstop_filter
from preprocessing.interp import fit_sphere, gc, gc_invdist_interp

NUM_PATIENTS = 59 # Half of total, randomly selected


def acquire_data(loc_path = 'utils/tmp'):
    r"""A one-line summary that does not use variable names or the
    function name.
    Several sentences providing an extended description. Refer to
    variables using back-ticks, e.g. `var`.
    Parameters
    ----------
    var1 : array_like
        Array_like means all those objects -- lists, nested lists, etc. --
        that can be converted to an array.  We can also refer to
        variables like `var1`.
    var2 : int
        The type above can either refer to an actual Python type
        (e.g. ``int``), or describe the type of the variable in more
        detail, e.g. ``(N,) ndarray`` or ``array_like``.
    long_var_name : {'hi', 'ho'}, optional
        Choices in brackets, default first when optional.
    Returns
    -------
    type
        Explanation of anonymous return value of type ``type``.
    describe : type
        Explanation of return value named `describe`.
    out : type
        Explanation of `out`.
    Other Parameters
    ----------------
    only_seldom_used_keywords : type
        Explanation
    common_parameters_listed_above : type
        Explanation
    Raises
    ------
    BadException
        Because you shouldn't have done that.
    See Also
    --------
    otherfunc : relationship (optional)
    newfunc : Relationship (optional), which could be fairly long, in which
              case the line wraps here.
    thirdfunc, fourthfunc, fifthfunc
    Notes
    -----
    Notes about the implementation algorithm (if needed).
    This can have multiple paragraphs.
    You may include some math:
    .. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}
    And even use a greek symbol like :math:`omega` inline.
    References
    ----------
    Cite the relevant literature, e.g. [1]_.  You may also cite these
    references in the notes section above.
    .. [1] O. McNoleg, "The integration of GIS, remote sensing,
       expert systems and adaptive co-kriging for environmental habitat
       modelling of the Highland Haggis using object-oriented, fuzzy-logic
       and neural-network techniques," Computers & Geosciences, vol. 22,
       pp. 585-588, 1996.
    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.
    >>> a = [1, 2, 3]
    >>> print [x + 3 for x in a]
    [4, 5, 6]
    >>> print "a\n\nb"
    a
    b
    """
    pat_map = get_patients()
    patients = None
    if args["patients"] is not None:
        patients = args["patients"]
    else:
        patients = range(NUM_PATIENTS)
    d = [] * len(patients)
    for p in patients:
        p_filepath = get_record(pat_map[p], args["record_num"],
                            args["record_type"], loc_path) 
        d.append(make_h5py_object(p_filepath))
    return d

def clean(D):
    # Extract for each patient
    C = []
    for d in D:
        tmp = {}
        tmp["eeg"] = get_eeg_data(d)
        tmp["times"] = get_times(d)
        tmp["coords"] = get_electrode_coords(d, args["coords"])
        C.append(tmp)

    # Go from python base list to numpy ndarray
    eeg_data = np.dstack(subject["eeg"] for subject in C)
    times = np.dstack(subject["times"] for subject in C)
    electrodes = np.dstack(subject["coords"] for subject in C)

    # Make sure the dimensions make sense
    assert eeg_data.ndim == 3
    assert times.ndim == 3
    assert electrodes.ndim == 3

    # Create a report for the cleaning procedure
    out = ''
    out += "## CLEANING DATA...\n"
    out += "* Extracted EEG data with " + str(eeg_data.shape[1]) + \
            " channels and " + str(eeg_data.shape[0]) + \
            " observations.\n"
    out += "* Extracted timing data with " + str(times.shape[0]) + \
            " timesteps.\n"
    out += "* Extracted electrode coordinate data.\n\n"

    return (eeg_data, times, electrodes), out

def detect_bad_channels(eeg_data):
    out = ''
    out +=  "## DETECTING BAD CHANNELS...\n"
    bad_chans_list = []

    # Finding list of bad channels for each patient
    # (list of lists)
    for patient in range(eeg_data.shape[2]):
        d = eeg_data[:, :, patient]
        assert d.ndim == 2
        L = []
        for i in range(d.shape[1]):
            if sum(d[:, i]**2) == 0:
                L.append(i)
        bad_chans_list.append(L)
        out +=  "* There were " + str(len(L)) + \
                " bad channels detected for patient " + \
                str(patient) + ".\n\n"
    # Numpify the python array
    bad_chans_list = np.array(bad_chans_list)
    # Some testing
    assert len(bad_chans_list) == eeg_data.shape[2]
    return bad_chans_list, out

def interpolate(eeg_data, coords, bad_chans, npts = 3):
    out = ""
    out += "## INTERPOLATING BAD CHANNELS...\n"
    closest = []
    for patient in range(eeg_data.shape[2]):
        r = fit_sphere(coords[:, 2, patient])
        out += "* Fit sphere of radius " + str(r) + " to head."
        eeg_data_fixed, close = gc_invdist_interp(eeg_data[:, :, patient],
                    bad_chans[patient], coords[:, :, patient],
                    r, numpts = npts)
        eeg_data[:, :, patient] = eeg_data_fixed
        closest.append(close)
    return (eeg_data, closest), out


def reduce_noise(F):
    out = ""
    out +=  "## REDUCING NOISE...\n"
    D = F.copy()
    for patient in range(D.shape[2]):
        d = D[:, :, patient]
        out += "* Highpass filtered at .1 Hz threshold.\n"
        out += "* Bandstop filtered at harmonics of 60Hz.\n"
        for channel in range(d.shape[1]):
            D[:, channel, patient] = butter_highpass_filter(
                                d[:, channel], 0.1, 500)
            for k in range(60, 299, 60):
                D[:, channel, patient] = butter_bandstop_filter(
                                    d[:, channel], [k-5,k+5], 500)

    return D, out

def set_args():
    global args
    args = {}
    with open("pipeline.conf") as f:
        args = ast.literal_eval(f.read())


def main():
    print "# EEG PIPELINE TEST!"
    print "## GETTING DATA..."
    D = acquire_data()
    print "## CLEANING DATA..."
    cleaned, o = clean(D)
    print o
    eeg_data, times, coords = cleaned
    print "## DETECTING BAD CHANNELS..."
    bad_chans, o = detect_bad_channels(eeg_data)
    print "## INTERPOLATING BAD CHANNELS..."
    interped, o = interpolate(eeg_data, coords, bad_chans)
    print o
    eeg_data, closest = interped
    print "## REDUCING NOISE..."
    eeg_data, o = reduce_noise(eeg_data)
    print o


if __name__ == '__main__':
    set_args()
    main()
