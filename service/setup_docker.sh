docker logs "$(cat .docker_container_id.txt)"
docker rm -f "$(cat .docker_container_id.txt)"
docker rmi -f rymarr/eeg_panda_image
docker build -t rymarr/eeg_panda_image .
docker run  --name eeg_panda_container -p 127.0.0.1:8888:80 rymarr/eeg_panda_image > .docker_container_id.txt
