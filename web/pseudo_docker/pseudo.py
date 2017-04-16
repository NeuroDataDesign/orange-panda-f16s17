# System utilities
import sys
sys.path.append("./*")
import cPickle as pkl
import os
import os.path as op

# Boto 3
import boto3
import botocore

def main():
    s3 = boto3.client(
        's3',
        aws_access_key_id = os.getenv('ACCESS_KEY'),
    )
    print "Running"
    bucket = s3.Bucket('panda.swerve')
    exists = True
    try:
        client.head_bucket(Bucket='panda.swerve')
        print "Swagggy"
    except botocore.exceptions.ClientError as e:
        print "Didn't work"
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            exists = False
    f = open('input.txt', 'r')
    out = open('output.txt', 'w')
    if f.readline() == "Hello World!":
        out.write("WE HAVE FOUND THE NEW WORLD!")
    else:
        out.write("No new world, it's just Canada")
    f.close()
    out.close()

if __name__ == "__main__": main()
