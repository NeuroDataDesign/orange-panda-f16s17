docker rm -f panda_container_1
docker rm -f panda_container_2
docker rm -f panda_container_3
docker rm -f panda_container_4

for VARIABLE in 1 2 3 4 5 6 7 8
do
        docker run --name=panda_container_1 rymarr/panda_pipeline \
	neurodatadesign-test bids_raw 0001 0$VARIABLE && docker rm panda_container_1 &

        docker run --name=panda_container_2 rymarr/panda_pipeline \
	neurodatadesign-test bids_raw 0002 0$VARIABLE && docker rm panda_container_2 &

        docker run --name=panda_container_3 rymarr/panda_pipeline \
	neurodatadesign-test bids_raw 0003 0$VARIABLE && docker rm panda_container_3 &

        docker run --name=panda_container_4 rymarr/panda_pipeline \
	neurodatadesign-test bids_raw 0004 0$VARIABLE && docker rm panda_container_4 &

        wait
done
