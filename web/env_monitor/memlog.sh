#!/bin/bash -e
# run this in the background with nohup ./memlog.sh > mem.txt &
# written by eric bridgeford

while true; do
    echo "$(free -m | grep Mem | awk '{print $3}')"
    sleep 1
done
