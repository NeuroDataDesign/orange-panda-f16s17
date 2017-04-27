#!/bin/sh

BUCKET=panda.swerve
IN_PATH=inputs
OUT_PATH=out
DATA=input.txt
CRED_PATH=~/.aws/credentials.csv

# run pseudo pipeline
python test_front.py --bucket $BUCKET --path $IN_PATH --out_path $OUT_PATH --data $DATA --credentials $CRED_PATH 
