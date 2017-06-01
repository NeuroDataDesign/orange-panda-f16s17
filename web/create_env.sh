#! bin/sh
CSV=$1

printf "AWS_ACCESS_KEY_ID=%s \n" "$(cat ${CSV} | sed -n 2p | cut -d, -f3)" 
printf "AWS_SECRET_ACCESS_KEY=%s \n" "$(cat ${CSV} | sed -n 2p | cut -d, -f4)"

