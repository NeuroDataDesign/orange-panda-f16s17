docker rm -f eeg_panda_container
docker build -t rymarr/eeg_panda_image .
docker run -i --name eeg_panda_container -p 127.0.0.1:8888:80 rymarr/eeg_panda_image
