# A function for generating memory and cpu summaries for fngs pipeline.
#
# Usage: ./runonesub.sh /path/to/rest /path/to/anat /path/to/output
# written by eric bridgeford

rm -rf $1
mkdir $1

pkill -f memlog
pkill -f cpulog
pkill -f disklog

./memlog.sh > ${1}/mem.txt &
memkey=$!
python cpulog.py ${1}/cpu.txt &
cpukey=$!
./disklog.sh $1 > ${1}/disk.txt &
diskkey=$!

bucket='panda-one-subj'
dataset='bids_raw'
sub='0001'
ses='05'
env_list='/home/nitin/.aws/cred_env_list'

#sudo docker run --env-file $env_list rymarr/panda_pipeline $bucket $dataset $sub $ses 
echo "hello world"

sleep 30

kill $memkey $cpukey $diskkey
