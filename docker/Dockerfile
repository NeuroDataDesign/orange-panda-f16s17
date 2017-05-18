FROM phusion/baseimage

MAINTAINER Ryan Marren <rmarren1@jhu.edu>

# Set language
ENV LANG en_US.UTF-8

RUN apt-get update && apt-get install -y python-dev python-setuptools python-numpy python-scipy
RUN easy_install pip
RUN apt-get install -y pkg-config zip python-vtk
RUN apt-get install -y python-tk
RUN pip install cython numpy wget sklearn awscli boto3 pyvtk pywavelets seaborn
RUN pip install --upgrade ndd-panda

# Some matplotlib bug with fonts on this base image
RUN rm -rf ~/.cache/matplotlib

# Change to the your project name
# Add credentials (copied from Greg's ndmg)
RUN mkdir /.aws && printf "[default]\nregion = us-east-1" > /.aws/config
ADD credentials.csv /credentials.csv
RUN printf "[default]\naws_access_key_id = `tail -n 1 /credentials.csv | cut -d',' -f2`\naws_secret_access_key = `tail -n 1 /credentials.csv | cut -d',' -f3`" > /.aws/credentials && mv /.aws/  ${HOME} && rm /credentials.csv
RUN cat ${HOME}/.aws/credentials

COPY ./entrypoint /

ENTRYPOINT ["/entrypoint"]
