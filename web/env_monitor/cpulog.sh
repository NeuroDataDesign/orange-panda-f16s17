#!/bin/bash -e
# run this in the background with nohup ./memlog.sh > cpu.txt &
# written by eric bridgeford

while true; do
    ps -aux | sort -nrk 3,3 | head -1 | awk '{print $3}'
    sleep 1
done
