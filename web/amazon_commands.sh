#!/bin/sh

# delete all job definitions 
aws batch describe-job-definitions | grep -Po '"jobDefinitionArn":.*?[^\\]",' \
    | cut -d : -f 2- | tr -d '"' | tr -d ',' \
    | xargs -n 1 aws batch deregister-job-definition --job-definition
