import os
import boto3
from argparse import ArgumentParser
import csv
import sys
sys.path.insert(0, '../')

def uploadS3(bucket, data, public_access_key, secret_access_key):
    s3 = boto3.client('s3', aws_access_key_id=public_access_key, aws_secret_access_key=secret_access_key)
    s3.upload_file(data, bucket, data)
    
def submitJob(bucket, folder, patient, trial, public_access_key, secret_access_key, myJobName):
    batch = boto3.client('batch', aws_access_key_id=public_access_key, aws_secret_access_key=secret_access_key)
    myJobQueue = 'orange-panda-queue'
    myJobDefinition = 'orange-panda-pipeline'
    myCommandOverride = [bucket, folder, patient, trial]
    myEnvironmentOverride = [{'name':'AWS_ACCESS_KEY_ID', 'value':public_access_key}, {'name':'AWS_SECRET_ACCESS_KEY', 'value':secret_access_key}, {'name':'AWS_DEFAULT_REGION', 'value':'us-east-1'}]
    response = batch.submit_job(jobName=myJobName, jobQueue=myJobQueue, jobDefinition=myJobDefinition, containerOverrides={'command':myCommandOverride, 'environment':myEnvironmentOverride}) 
    return response
    
def checkJobStatus(public_access_key, secret_access_key, jobId):
    batch = boto3.client('batch', aws_access_key_id=public_access_key, aws_secret_access_key=secret_access_key)
    return batch.describe_jobs(jobs=[jobId])['jobs'][0]['status']

def main():
    parser = ArgumentParser(description="This is a test")
    parser.add_argument('--bucket', help='The S3 bucket with the input dataset formatted according to the BIDS standard.')
    parser.add_argument('--credentials', help='AWS formatted csv of credentials.')
    parser.add_argument('--folder', help='The folder in the bucket to access the data from.')
    parser.add_argument('--patient', help='The patient number we are trying to analyze.')
    parser.add_argument('--trial', help='The trial # of the patient.')
    result = parser.parse_args()
    
    bucket = str(result.bucket)
    credentials = str(result.credentials)
    data = str(result.data)
    folder = str(result.folder)
    patient = str(result.patient)
    trial = str(result.trial)
    
    credfile = open(credentials, 'rb')
    reader = csv.reader(credfile)
    rowcounter = 0
    for row in reader:
        if rowcounter == 1:
            public_access_key = str(row[2])
            secret_access_key = str(row[3])
        rowcounter = rowcounter + 1

    # uploadS3(bucket, data, public_access_key, secret_access_key)

    # get all items in bucket
    s3 = boto3.resource('s3')
    s3_bucket = s3.Bucket(bucket)
    i = 0
    jobId = []
    for obj in s3_bucket.objects.all():
        response = submitJob(bucket, obj.key, public_access_key, secret_access_key, "testjob" + str(i))
        jobId.append(response['jobId'])
        print("JobID = " + jobId[i])
        i += 1
    for i in range(len(jobId)):
        while(checkJobStatus(public_access_key, secret_access_key, jobId[i]) != 'SUCCEEDED'):
            pass
        print("Job " + jobId + " successful!")
    
    
if __name__ == "__main__":
    main()
