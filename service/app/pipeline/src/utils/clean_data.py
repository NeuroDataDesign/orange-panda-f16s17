"""Contains methods to extract numpy array objects from the h5py object extracted from the S3 bucket.

"""
import numpy as np

def get_eeg_data(f):
    r"""Extract an eeg numpy data matrix from the h5py object.

    Parameters
    ----------
    f : h5py object
        a h5py object obtained from the `make_h5py_object` function in the get_data module

    Returns
    -------
    eeg_data : ``ndarray``
        A `(t, c)` ``ndarray`` (`t` is the number of timesteps, `c` is the number of channels).

    See Also
    --------
    utils.get_data.get_record
    utils.get_data.make_h5py_object

    Notes
    -----
    The dataset has 111 channels.

    Timesteps are measured in milliseconds, and values were measured at 500 Hz.

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> from get_data import get_record, get_patients, make_h5py_object
    >>> f = get_record(get_patients()[0])
    >>> data = make_h5py_object(f)
    >>> eeg_data = get_eeg_data(data)

    """
    data = np.array(f['result']['data'])
    assert data.ndim == 2 # time by electrode channels
    assert data.shape[1] == 111 # has 111 electrode channels
    return data
    

def get_times(f):
    r"""Extract times numpy matrix from the h5py object.

    Parameters
    ----------
    f : h5py object
        a h5py object obtained from the `make_h5py_object` function in the get_data module

    Returns
    -------
    times : ``ndarray``
        A (t, 1) ``ndarray`` (`t` is the number of timesteps).

    See Also
    --------
    utils.get_data.get_record
    utils.get_data.make_h5py_object

    Notes
    -----
    The dataset has 111 channels.

    Timesteps are measured in milliseconds, and values were measured at 500 Hz.

    Examples
    --------

    >>> from get_data import get_record, get_patients, make_h5py_object
    >>> f = get_record(get_patients()[0])
    >>> data = make_h5py_object(f)
    >>> times = get_times(data)

    """
    times = np.array(f['result']['times'])
    assert times.ndim == 2
    assert times.shape[1] == 1
    return times

def get_electrode_coords(f, coords = "euclidian"):
    r"""Extract times numpy matrix from the h5py object.

    Parameters
    ----------
    f : h5py object
        a h5py object obtained from the `make_h5py_object` function in the get_data module

    coords : string
        'euclidian' for euclidian coordinates, 'spherical' for spherical coordinates (not really with a variable radius coordinate).

    Returns
    -------
    electrode_coords : ``ndarray``
        A `(t, 3)` ``ndarray`` (`t` is the number of timesteps, columns are `x`, `y`, `z` or :math:`theta`, :math:`phi`, `r`).

    See Also
    --------
    utils.get_data.get_record
    utils.get_data.make_h5py_object

    Notes
    -----
    Spherical has a variable radius parameter.

    Timesteps are measured in milliseconds, and values were measured at 500 Hz.

    Examples
    --------

    >>> from get_data import get_record, get_patients, make_h5py_object
    >>> f = get_record(get_patients()[0])
    >>> data = make_h5py_object(f)
    >>> coords = get_electrode_coords(data, coords = "spherical")

    """
    base = f['result']['chanlocs']
    electrode_coords = None
    if coords == "euclidian":
        x = [base[e[0]][:][0][0] for e in base['X']] 
        y = [base[e[0]][:][0][0] for e in base['Y']]
        z = [base[e[0]][:][0][0] for e in base['Z']] 
        electrode_coords = np.array(zip(x, y, z))
    elif coords == "spherical":
        t = [base[e[0]][:][0][0] for e in base['sph_theta']]
        p = [base[e[0]][:][0][0] for e in base['sph_phi']]
        r = [base[e[0]][:][0][0] for e in base['sph_radius']]
        electrode_coords = np.array(zip(t, p, r))
    else:
        raise Exception("Pick spherical or euclidian coordinates")
    assert electrode_coords.ndim == 2
    assert electrode_coords.shape[1] == 3
    return electrode_coords

    
