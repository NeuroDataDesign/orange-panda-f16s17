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
    print sys.argv
    bucket_name = sys.argv[1]
    data = sys.argv[2]
    path = sys.argv[3]
    out_path = sys.argv[4]
    
    # Let's use Amazon S3
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    exists = True

    # get all items in bucket
    locInFile = '/src/data/' + data
    inFile = data
    if path != "":
        inFile = path + '/' + data
    locOutFile = '/src/out/out_' + data
    outFile = data
    if out_path != "":
        outFile = out_path + '/out_' + data
    print inFile
    bucket.download_file(inFile, locInFile)
    pipeline(locInFile, locOutFile)
    bucket.upload_file(locOutFile, outFile)

if __name__ == "__main__": main()
