from boto.s3.connection import S3Connection
from boto.s3.key import Key
import h5py
import os

def get_patients():
    f = open('PATIENT_NUMBERS.txt', 'rb')
    L = []
    for line in f:
        L.append(line[:-1])
    return L

def get_record(patient, recordnum = 1, recordtype = "full"):
    patientpath = "data/uploads/" + str(patient) + '/'
    eventname = str(recordtype) + "_" + str(patient)
    if recordnum < 10:
        eventname += "00" + str(recordnum) + ".mat"
    else:
        eventname += "0" + str(recordnum) + ".mat"
    localpath = "utils/tmp/" + patient + "_" + \
            str(recordnum) + ".mat"
    if os.path.isfile(localpath):
        print "  there is already a file named: " + \
                localpath + ", returned that path instead of pulling data."
        return localpath
    conn = S3Connection(os.environ['AWS_ACCESS_KEY'],
            os.environ['AWS_SECRET_KEY'])
    bucket = conn.get_bucket('fcp-indi')
    s3path = patientpath + eventname
    key = Key(bucket, s3path)
    f = file(localpath, 'wb')
    def callback(togo, total):
        print "Got {0: 10d} Bytes out of {1:10d} Bytes".format(togo, total)
        if togo == total:
            print "Done! The path of the .mat file was returned."
    key.get_file(f, cb = callback)
    return localpath

def make_h5py_object(filepath):
    f = h5py.File(filepath, 'r')
    return f
