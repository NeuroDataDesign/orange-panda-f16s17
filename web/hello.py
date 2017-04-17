import boto3
import os

# Let's use Amazon S3
s3 = boto3.resource('s3')

#client = boto3.client(
#    's3',
#    aws_access_key_id=os.environ['ACCESS_KEY'],
#    aws_secret_access_key=os.environ['SECRET_KEY']
#)

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)
# Upload a new file
data = open('input.txt', 'rb')
s3.Bucket('panda.swerve').put_object(Key='input.txt', Body=data)
