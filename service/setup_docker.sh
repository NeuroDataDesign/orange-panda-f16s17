sudo docker build -t eeg_panda_image .
sudo docker run --name eeg_panda_container -p 127.0.0.1:8888:80 eeg_panda_image
