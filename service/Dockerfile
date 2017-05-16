FROM tiangolo/uwsgi-nginx-flask:flask-index

RUN apt-get update && apt-get install -y python-dev python-setuptools python-numpy python-scipy
RUN easy_install pip
run pip install --upgrade pip
RUN pip install cython numpy sklearn boto plotly cufflinks pandas scipy h5py pandas_datareader ipython 
RUN pip install statsmodels
RUN pip install boto3 awscli

COPY ./nginx.conf /etc/nginx/conf.d/
COPY ./app /app
RUN mkdir /.aws && printf "[default]\nregion = us-east-1" > /.aws/config
ADD credentials.csv /credentials.csv
RUN printf "[default]\naws_access_key_id = `tail -n 1 /credentials.csv | cut -d',' -f2`\naws_secret_access_key = `tail -n 1 /credentials.csv | cut -d',' -f3`" > /.aws/credentials && mv /credentials.csv /.aws/ && mv /.aws/  ${HOME}
