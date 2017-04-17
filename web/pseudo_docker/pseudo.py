# System utilities
import sys
sys.path.append("./*")
import cPickle as pkl
import os
import os.path as op

# Boto 3
import boto3

def pipeline(inFile, outFile):
    f = open(inFile, 'r')
    out = open(outFile, 'w')
    if f.readline() == "Hello World!":
       out.write("WE HAVE FOUND THE NEW WORLD!\n")
    else:
       out.write("No new world, it's just Canada\n")
    f.close()
    out.close()
    

def main():
    bucket_name = sys.argv[1]
    data = sys.argv[2]
    
    # Let's use Amazon S3
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    exists = True

    # get all items in bucket
    inFile = '/src/data/' + data
    outFile = 'out/out_' + data
    bucket.download_file(obj.key, inFile)
    pipeline(inFile, '/src/' + outFile)
    bucket.upload_file('/src/' + outFile, outFile)

if __name__ == "__main__": main()
