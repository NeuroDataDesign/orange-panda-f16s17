import boto.s3.connection
import boto.s3.key
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import numpy as np
import sys
import os

try:
    import set_keys
except:
    print 'You need to set the file with the secret keys!!!'

REPORT_FMT = "Downloaded %04d / %04d Megabytes."
COUNTER = 0

S3_PREFIX = 'data/Projects/EEG_Eyetracking_CMI_data/compressed/'

def get_key_name_pairs(bucket):
    pairs = []
    L = bucket.list(prefix=S3_PREFIX)
    for key in L:
        pairs.append((key, str(key).split('/')[-1][:-1]))
    return pairs


def main():
    BASE_PATH = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    conn = S3Connection(os.environ['AWS_ACCESS_KEY'], os.environ['AWS_SECRET_KEY'])
    bucket = conn.get_bucket('fcp-indi')
    pairs = get_key_name_pairs(bucket)
    if not os.path.exists(BASE_PATH):
        os.mkdir(BASE_PATH)
        print 'Creating directory at', BASE_PATH
    for pair in pairs[start:end]:
        key, f_name = pair
        print 'Downloading file', f_name
        key.get_contents_to_filename(BASE_PATH + f_name,
                                    cb = call, num_cb = 100)
        floc = BASE_PATH + str(f_name)
        print 'file location is', floc
        subj = f_name.split('.')[0]
        print 'unzipping', f_name
        os.system('tar -zxf ' + floc + ' -C ' + BASE_PATH)
        print 'removing old zip of', floc
        os.system('rm ' + floc)

def call(sofar, total):
    sofarmb = int(float(sofar) / 1e6)
    totalmb = int(float(total) / 1e6)
    print REPORT_FMT % (sofarmb, totalmb)

if __name__ == '__main__':
    main()
