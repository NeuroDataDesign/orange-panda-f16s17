from argparse import ArgumentParser
from collections import OrderedDict
from copy import deepcopy
from subprocess import Popen, PIPE
import sys
import os
import re
import csv
import boto3
import json
import ast

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

def get_id():
    out, err = execute_cmd('aws iam get-user')
    result = json.loads(out)['User']['Arn']
    result_list = result.split(":")
    return result_list[4]

def create_env():
    """
    Create compute environment, job queue, and job definition if doesn't exist yet.
    """

    # Create env jsons
    env = "env_template.json"
    template = []

    # Open template, set account IDs 
    with open('{}'.format(env), 'r') as inf:
        template = json.load(inf)
    template['serviceRole'] = re.sub('<ACCT_ID>', get_id(), template['serviceRole'])
    template['computeResources']['instanceRole'] = re.sub('<ACCT_ID>', get_id(), template['computeResources']['instanceRole'])

    # Write template back out
    with open('env_out.json', 'w') as outfile:
        json.dump(template, outfile)

    # Check computer environment
    cmd_template = 'aws batch describe-compute-environments  --compute-environments {}'
    env_name = 'pseudo-orange-panda8'
    cmd = cmd_template.format(env_name)
    out, err = execute_cmd(cmd)
    result = json.loads(out)
    if len(result['computeEnvironments']) == 0:
        cmd_template = 'aws batch create-compute-environment --cli-input-json file://{}'
        def_json = 'env_out.json'
        cmd = cmd_template.format(def_json)
        out, err = execute_cmd(cmd)

    # Create queue 
    cmd_template = 'aws batch describe-job-queues --job-queues {}'
    env_name = 'pseudo-job-queue2'
    cmd = cmd_template.format(env_name)
    out, err = execute_cmd(cmd)
    result = json.loads(out)
    if len(result['jobQueues']) == 0:
        cmd_template = 'aws batch create-job-queue --cli-input-json file://{}'
        def_json = 'queue_template.json'
        cmd = cmd_template.format(def_json)
        out, err = execute_cmd(cmd)

    # Create job definition
    cmd_template = 'aws batch register-job-definition --cli-input-json file://{}'
    def_json = 'pseudo-pipeline.json'
    cmd = cmd_template.format(def_json)
    out, err = execute_cmd(cmd)
    submission = ast.literal_eval(out)
    print("Job Definition Name: {}, Revision: {}".format(submission['jobDefinitionName'], submission['revision']))

    return 0

def crawl_bucket(bucket, path):
    """
    Gets subject list for a given S3 bucket and path
    """
    cmd = 'aws s3 ls s3://{}/data/{}/'.format(bucket, path)
    out, err = execute_cmd(cmd)
    subjs = re.findall('PRE sub-(.+)/', out)
    cmd = 'aws s3 ls s3://{}/data/{}/sub-{}/'
    seshs = OrderedDict()
    for subj in subjs:
        out, err = execute_cmd(cmd.format(bucket, path, subj))
        print "here"
        sesh = re.findall('ses-(.+)/', out)
        seshs[subj] = sesh if sesh != [] else [None]
    print("Session IDs: " + ", ".join([subj+'-'+sesh if sesh is not None
                                       else subj
                                       for subj in subjs
                                       for sesh in seshs[subj]]))
    return seshs


def create_json(bucket, threads, jobdir, dataset, credentials=None, log=False):
    """
    Takes parameters to make jsons
    """

    # make jobdirs
    execute_cmd("mkdir -p {}".format(jobdir))
    execute_cmd("mkdir -p {}/jobs/".format(jobdir))
    execute_cmd("mkdir -p {}/ids/".format(jobdir))

    # Set json template filename
    template = "panda_job.json"
    seshs = threads 

    # Open template, grab overrides we need to set 
    with open('{}'.format(template), 'r') as inf:
        template = json.load(inf)
    cmd = template['containerOverrides']['command']
    env = template['containerOverrides']['environment']

    # Put credentials in environment variable override
    if credentials is not None:
        cred = [line for line in csv.reader(open(credentials))]
        env[0]['value'] = [cred[1][idx]
                           for idx, val in enumerate(cred[0])
                           if "ID" in val][0]  # Adds public key ID to env
        env[1]['value'] = [cred[1][idx]
                           for idx, val in enumerate(cred[0])
                           if "Secret" in val][0]  # Adds secret key to env
    else:
        env = []
    template['containerOverrides']['environment'] = env

    # make returnable object of different jobs to submit
    jobs = list()
    # set bucket
    cmd[0] = re.sub('(<BUCKET>)', bucket, cmd[0])
    # set path
    cmd[1] = re.sub('(<DATASET>)', dataset, cmd[1])

    for subj in seshs.keys():
        print("... Generating job for sub-{}".format(subj))
        for sesh in seshs[subj]:
            job_cmd = deepcopy(cmd)
            job_cmd[2] = re.sub('(<SUB>)', subj, job_cmd[2])
            job_cmd[3] = re.sub('(<SES>)', sesh, job_cmd[3])
            job_json = deepcopy(template)
            name = 'panda_sub-{}'.format(subj)
            if sesh is not None:
                name = '{}_ses-{}'.format(name, sesh)
            job_json['jobName'] = name
            job_json['containerOverrides']['command'] = job_cmd
            job = os.path.join(jobdir, 'jobs', name+'.json')
            with open(job, 'w') as outfile:
                json.dump(job_json, outfile)
            jobs += [job]

    return jobs

def pseudo_create_json(name, bucket, threads, jobdir, path=None, out_path=None, 
            credentials=None, log=False):
    """
    Takes parameters to make jsons for pseudo pipeline
    """

    # make jobdirs
    execute_cmd("mkdir -p {}".format(jobdir))
    execute_cmd("mkdir -p {}/jobs/".format(jobdir))
    execute_cmd("mkdir -p {}/ids/".format(jobdir))

    # Set json template filename
    template = "panda_job.json"
    seshs = threads 

    # Open template, grab overrides we need to set 
    with open('{}'.format(template), 'r') as inf:
        template = json.load(inf)
    cmd = template['containerOverrides']['command']
    env = template['containerOverrides']['environment']

    # Put credentials in environment variable override
    if credentials is not None:
        cred = [line for line in csv.reader(open(credentials))]
        env[0]['value'] = [cred[1][idx]
                           for idx, val in enumerate(cred[0])
                           if "ID" in val][0]  # Adds public key ID to env
        env[1]['value'] = [cred[1][idx]
                           for idx, val in enumerate(cred[0])
                           if "Secret" in val][0]  # Adds secret key to env
    else:
        env = []
    template['containerOverrides']['environment'] = env

    # make returnable object of different jobs to submit
    jobs = list()
    # set bucket
    cmd[0] = re.sub('(<BUCKET>)', bucket, cmd[0])
    # set out path
    cmd[3] = re.sub('(<OUT_PATH>)', out_path, cmd[3])


    for subj in seshs.keys():
        print("... Generating job for sub-{}".format(subj))
        for sesh in seshs[subj]:
            job_cmd = deepcopy(cmd)
            # set path
            job_cmd[2] = re.sub('(<PATH>)', path + "/sub-" + subj + "/ses-" + sesh + "/eeg", job_cmd[2])
            data_file = "sub-" + subj + "_ses-" + sesh
            job_cmd[1] = re.sub('(<DATASET>)', data_file + ".txt", job_cmd[1])

            job_json = deepcopy(template)
            name = 'panda_sub-{}'.format(subj)
            if sesh is not None:
                name = '{}_ses-{}'.format(name, sesh)
            job_json['jobName'] = name
            job_json['containerOverrides']['command'] = job_cmd
            job = os.path.join(jobdir, 'jobs', name+'.json')
            with open(job, 'w') as outfile:
                json.dump(job_json, outfile)
            jobs += [job]

    return jobs

def submit_jobs(jobs, jobdir):
    """
    Give list of jobs to submit, submits them to AWS Batch
    """
    cmd_template = 'aws batch submit-job --cli-input-json file://{}'

    for job in jobs:
        cmd = cmd_template.format(job)
        print("... Submitting job {}...".format(job))
        out, err = execute_cmd(cmd)
        submission = ast.literal_eval(out)
        print("Job Name: {}, Job ID: {}".format(submission['jobName'], submission['jobId']))
        sub_file = submission['jobName']+'_out.json'
        sub_file = os.path.join(jobdir, 'ids', submission['jobName']+'.json')
        with open(sub_file, 'w') as outfile:
            json.dump(submission, outfile)
    return 0
