docker rm -f eeg_panda_container 
docker build -t eeg_panda_container .
docker run -i --name eeg_panda_container -p 127.0.0.1:8888:80 eeg_panda_container
