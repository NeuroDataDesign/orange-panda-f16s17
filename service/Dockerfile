FROM tiangolo/uwsgi-nginx-flask:flask-index

RUN apt-get update && apt-get install -y python-dev python-setuptools python-numpy python-scipy
RUN easy_install pip
run pip install --upgrade pip
RUN pip install cython numpy sklearn boto plotly cufflinks pandas scipy h5py pandas_datareader ipython 
RUN pip install statsmodels

COPY ./nginx.conf /etc/nginx/conf.d/
COPY ./app /app
COPY ./set_keys.py /app
COPY ./set_keys.py /app/pipeline/src/utils

