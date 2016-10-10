"""Contains methods to extract data from the S3 bucket.

"""
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import h5py
import os

def get_patients():
    r"""Gets a list of patient numbers to query the S3 bucket with.

    Uses a patient list in PATIENT_NUMBERS.txt to construct a python object of strings of patient numbers.

    Returns
    -------
    L : ``list``
        a list of strings of patient numbers.

    See Also
    --------
    get_record : uses these patient numbers.

    Notes
    -----
    patient numbers are extracted from PATIENT_NUMBERS.txt

    Examples
    --------

    >>> from utils.get_data import get_patients
    >>> print get_patients()[0]
    A00055540

    """
    f = open('PATIENT_NUMBERS.txt', 'rb')
    L = []
    for line in f:
        L.append(line[:-1])
    return L

def get_record(patient, record_num = 1, record_type = "full"):
    r"""Pulls a patient record from the S3 bucket.

    Parameters
    ----------
    patient : string
        the patient number of the patient to pull data for.

    record_num : int, optional
        number of the record to pull. This is usually from 1 to around 10.

    record_type : {'full', 'reduced'}, optional
        'full' by default. 'reduced' has less metadata.

    Returns
    -------
    string
        the filepath of the .mat file of the record (will go to the `\tmp`) directory.

    See Also
    --------
    make_h5py_object : uses filepath to create a h5py object.

    Notes
    -----
    You need to set the amazon keys as environment variables. Put the secret key in ``AWS_SECRET_KEY`` and the regular key in ``AWS_ACCESS_KEY``.

    Uses the ``boto`` package to access AWS.

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> from utils.get_data import get_patients, get_record
    >>> print get_patients()[0]
    'A00055540'
    >>> print get_record(get_patients()[0])
    '~/.../src/utils/tmp/{recordname}.mat'

    """
    patient_path = "data/uploads/" + str(patient) + '/'
    event_name = str(record_type) + "_" + str(patient)
    if record_num < 10:
        event_name += "00" + str(record_num) + ".mat"
    else:
        event_name += "0" + str(record_num) + ".mat"
    local_path = "utils/tmp/" + patient + "_" + \
            str(record_num) + ".mat"
    print local_path
    if os.path.isfile(local_path):
        print "  there is already a file named: " + \
                local_path + ", returned that path instead of pulling data."
        return local_path
    conn = S3Connection(os.environ['AWS_ACCESS_KEY'],
            os.environ['AWS_SECRET_KEY'])
    bucket = conn.get_bucket('fcp-indi')
    s3path = patient_path + event_name
    key = Key(bucket, s3path)
    f = file(local_path, 'wb')
    def callback(togo, total):
        print "Got {0: 10d} Bytes out of {1:10d} Bytes".format(togo, total)
        if togo == total:
            print "Done! The path of the .mat file was returned."
    key.get_file(f, cb = callback)
    return local_path

def make_h5py_object(file_path):
    r"""Make a h5py object out of a .mat file from your system.

    Parameters
    ----------
    file_path : string
        absolute path to the .mat file.

    Returns
    -------
    data : h5py object
        a h5py object containing a (messy) copy of the data from S3.

    See Also
    --------
    utils.clean_data : extract data from object returned from this function

    Notes
    -----
    File should be around 80 mb.

    File should be in .mat format.

    Examples
    --------

    >>> from utils.get_data import get_patients, get_record, make_h5py_object
    >>> print get_patients()[0]
    'A00055540'
    >>> print get_record(get_patients()[0])
    '~/.../src/utils/tmp/{recordname}.mat'
    >>> data = make_h5py_object(get_record(get_patients()[0]))

    """
    data = h5py.File(file_path, 'r')
    return data
