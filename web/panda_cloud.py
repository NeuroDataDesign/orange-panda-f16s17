from argparse import ArgumentParser
from copy import deepcopy
from subprocess import Popen, PIPE
import sys
import os
import re
import csv
import boto3
import json
import ast

def batch_submit(bucket, path, jobdir, credentials=None, state='participant',
                 debug=False, dataset=None, log=False):
    """
    Searches through an S3 bucket, gets all subject-ids, creates json files
    for each, submits batch jobs, and returns list of job ids to query status
    upon later.
    """
    group = state == 'group'
    print("Getting list from s3://{}/{}/...".format(bucket, path))
    threads = crawl_bucket(bucket, path, group)

    print("Generating job for each subject...")
    jobs = create_json(bucket, path, threads, jobdir, group, credentials,
                       debug, dataset, log)

    print("Submitting jobs to the queue...")
    ids = submit_jobs(jobs, jobdir)

def execute_cmd(cmd):
    """
    Given a bash command, it is executed and the response piped back to the
    calling script
    """
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = p.communicate()
    code = p.returncode
    if code:
        sys.exit("Error  " + str(code) + ": " + err)
    return out, err

