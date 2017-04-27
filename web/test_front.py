from argparse import ArgumentParser
import os
import boto3
import csv
import sys
from create_job import *
sys.path.insert(0, '../')

def main():
    # get args
    parser = ArgumentParser(description="This is a test")
    parser.add_argument('--bucket', help='The S3 bucket with the input dataset formatted according to the BIDS standard.')
    parser.add_argument('--path', help='The path in the S3 bucket with the input dataset.')
    parser.add_argument('--out_path', help='The path in the S3 bucket output results.')
    parser.add_argument('--credentials', help='AWS formatted csv of credentials.')
    parser.add_argument('--data', help='The data file to upload to the specified S3 bucket')
    result = parser.parse_args()
    
    # convert args to objs
    bucket = str(result.bucket)
    path = str(result.path)
    out_path = str(result.out_path)
    credentials = str(result.credentials)
    data = str(result.data)
    
    # extract credentials
    credfile = open(credentials, 'rb')
    reader = csv.reader(credfile)
    rowcounter = 0
    for row in reader:
        if rowcounter == 1:
            public_access_key = str(row[1])
            secret_access_key = str(row[2])
        rowcounter = rowcounter + 1

    # set env vars to current credentials
    os.environ['AWS_ACCESS_KEY_ID'] = public_access_key
    os.environ['AWS_SECRET_ACCESS_KEY'] = secret_access_key
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    # iterate through objs and submit jobs
    i = 0
    jobId = []
    # for obj in ["input.txt"]:# s3_bucket.objects.all():
    create_env()
    print "job" + str(i)
    jobs = create_json("job" + str(i), bucket, path, out_path, credentials=credentials, dataset=data, log=False) 
    submit_jobs(jobs)
    # jobId.append(response['jobId'])
    # print("JobID = " + jobId[i])
    print(jobs)
    i += 1
    
    
if __name__ == "__main__":
    main()
