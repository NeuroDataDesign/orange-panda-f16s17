from argparse import ArgumentParser
import os
import boto3
import csv
import sys
from create_job import *
sys.path.insert(0, '../')

def uploadS3(bucket, data, public_access_key, secret_access_key):
    s3 = boto3.client('s3', aws_access_key_id=public_access_key, aws_secret_access_key=secret_access_key)
    s3.upload_file(data, bucket, data)
    
def submitJob(bucket, data, public_access_key, secret_access_key, myJobName):
    batch = boto3.client('batch', aws_access_key_id=public_access_key, aws_secret_access_key=secret_access_key)
    myJobQueue = 'pseudo-job-queue'
    myJobDefinition = 'actual-pseudo-pipeline'
    myCommandOverride = [bucket, data]
    myEnvironmentOverride = [{'name':'AWS_ACCESS_KEY_ID', 'value':public_access_key}, {'name':'AWS_SECRET_ACCESS_KEY', 'value':secret_access_key}, {'name':'AWS_DEFAULT_REGION', 'value':'us-east-1'}]
    response = batch.submit_job(jobName=myJobName, jobQueue=myJobQueue, jobDefinition=myJobDefinition, containerOverrides={'command':myCommandOverride, 'environment':myEnvironmentOverride}) 
    return response
    
def checkJobStatus(public_access_key, secret_access_key, jobId):
    batch = boto3.client('batch', aws_access_key_id=public_access_key, aws_secret_access_key=secret_access_key)
    return batch.describe_jobs(jobs=[jobId])['jobs'][0]['status']

def main():
    # get args
    parser = ArgumentParser(description="This is a test")
    parser.add_argument('--bucket', help='The S3 bucket with the input dataset formatted according to the BIDS standard.')
    parser.add_argument('--dataset', help='The dataset.')
    parser.add_argument('--subject', help='Subject.')
    parser.add_argument('--session', help='Session.')
    parser.add_argument('--credentials', help='AWS formatted csv of credentials.')
    result = parser.parse_args()
    
    # convert args to objs
    bucket = str(result.bucket)
    dataset = str(result.dataset)
    subject = str(result.subject)
    session = str(result.session)

    credentials = str(result.credentials)
    
    # extract from csv
    credfile = open(credentials, 'rb')
    reader = csv.reader(credfile)
    rowcounter = 0
    for row in reader:
        if rowcounter == 1:
            public_access_key = str(row[1])
            secret_access_key = str(row[2])
        rowcounter = rowcounter + 1

    # TO implement: upload local data

    # set env vars to current credentials
    os.environ['AWS_ACCESS_KEY_ID'] = public_access_key
    os.environ['AWS_SECRET_ACCESS_KEY'] = secret_access_key
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    # connect to bucket 
    # s3 = boto3.resource('s3')
    # s3_bucket = s3.Bucket(bucket)

    # iterate through objs and submit jobs
    i = 0
    jobId = []
    # for obj in ["input.txt"]:# s3_bucket.objects.all():
    create_env()
    print "job" + str(i)
    jobs = create_json("job" + str(i), bucket, dataset, subject, session, credentials=credentials, log=False) 
    submit_jobs(jobs)
    # jobId.append(response['jobId'])
    # print("JobID = " + jobId[i])
    print(jobs)
    i += 1
    
    
if __name__ == "__main__":
    main()
