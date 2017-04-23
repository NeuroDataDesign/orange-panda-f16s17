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


def create_env():
    """
    Create the definiition in Batch if it hasn't been done yet
    """
    # Check computer environment
    cmd_template = 'aws batch describe-compute-environments  --compute-environments {}'
    env_name = 'pseudo-orange-panda4'
    cmd = cmd_template.format(env_name)
    out, err = execute_cmd(cmd)
    result = json.loads(out)
    if len(result['computeEnvironments']) == 0:
        cmd_template = 'aws batch create-compute-environment --cli-input-json file://{}'
        def_json = 'env_template.json'
        cmd = cmd_template.format(def_json)
        out, err = execute_cmd(cmd)

    # Create queue 
    cmd_template = 'aws batch describe-job-queues--job-queues {}'
    env_name = 'pseudo-job-queue'
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

def submit_jobs(jobs):#, jobdir):
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
        with open(sub_file, 'w') as outfile:
            json.dump(submission, outfile)
    return 0

def create_json(name, bucket, path=None, out_path=None, credentials=None,
                dataset=None, log=False):
    """
    Takes parameters to make jsons
    """
    # Set json template filename
    template = "test.json"

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
    # set data
    if dataset is not None:
        cmd[1] = re.sub('(<DATASET>)', dataset, cmd[1])
    else:
        cmd[1] = re.sub('(<DATASET>)', '', cmd[1])
    # set path
    if path != None:
        print "path not none"
        cmd[2] = re.sub('(<PATH>)', path, cmd[2])
    else:
        cmd[2] = re.sub('(<PATH>)', '', cmd[2])
    # set output path
    if out_path != None:
        cmd[3] = re.sub('(<OUT_PATH>)', out_path, cmd[3])
    else:
        cmd[3] = re.sub('(<OUT_PATH>)', '', cmd[3])
    
    print cmd

    job_json = deepcopy(template)
    job_json['jobName'] = name
    job_json['containerOverrides']['command'] = cmd 
    job = name+'.json'
    with open(job, 'w') as outfile:
        json.dump(job_json, outfile)
    jobs += [job]

    return jobs

