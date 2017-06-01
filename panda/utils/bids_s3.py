from system import execute_cmd
import sys
import boto3
import os

def get_data(bucket, remote_dir, local, subj=None, ses=None, public=True, folder = True):
    """
    Given an s3 bucket, data location on the bucket, and a download location,
    crawls the bucket and recursively pulls all data.
    """
    client = boto3.client('s3')
    if not public:
        bkts = [bk['Name'] for bk in client.list_buckets()['Buckets']]
        if bucket not in bkts:
            sys.exit("Error: could not locate bucket. Available buckets: " +
                     ", ".join(bkts))
    cmd = 'aws'
    if public:
        cmd += ' --no-sign-request'
    if folder:
        cmd = "".join([cmd, ' s3 cp --recursive s3://', bucket, '/',
                       remote_dir])
    else:
        cmd = "".join([cmd, ' s3 cp s3://', bucket, '/',
                       remote_dir])
    if subj is not None:
        cmd = "".join([cmd, '/sub-', subj])
        std, err = execute_cmd('mkdir -p ' + local + '/sub-' + subj)
        local += '/sub-' + subj

        if ses is not None:
            cmd = "".join([cmd, '/ses-', ses])
            std, err = execute_cmd('mkdir -p ' + local + '/ses-' + ses)
            local += '/ses-' + ses
    cmd = "".join([cmd, ' ', local])
    std, err = execute_cmd(cmd)
    return
