# EEG PANDA - Automated EEG data analysis.
A summary schematic of what this service offers can be found [here](https://www.lucidchart.com/documents/view/ca99b646-c76a-42ef-8083-cacf3ada2c43).
We are currently live at

##  *How to build and run the pipeline container*
We offer a docker image which runs the numerical software of our pipeline. The workflow is as follows:
1. The user places a credential file in the root directory of the `docker` folder builds the pipeline to create a docker image.
2. The user runs the docker container with four arguments, pointing the container to the correct file in a S3 bucket.
3. The user views the results in the S3 bucket.

We will detail each of these steps below.

#### 1. Adding credentials and building the Docker image.
Clone the `orange-panda` repo and from the root directory, `cd` into the `docker` folder. Here, you will need to add a new file called `credentials.csv` which has the following format:
```
User Name,Access Key Id,Secret Access Key
"name",access-key-id,secret-access-key
```
where `access-key-id` and `secret-access-key` are replaced with your S3 access key and secret access key respectively.

Now, you can successfully build the docker container with the command
`.docker build -t yourname/panda_pipeline .`

This will build a docker image named `yourname/panda_pipeline` on your local machine.

#### 2. Running the docker container.
Using the docker image you built in step 1. is quite simple. Assuming that you have a S3 bucket to which the credentials you provided have access, and that this bucket with name `my-bucket` has a set of EEG data in the [BIDS data format](https://github.com/NeuroDataDesign/orange-panda/blob/master/notes/pipeline/data_format.md) with root folder name `my-dataset`, you can run subject `XXXX` trial `YY` with the command:
```
docker run --rm yourname/panda_pipeline my-bucket my-dataset XXXX YY
```
#### 3. Viewing results
The results will then be pushed to a new directory called `my-dataset_out` in the `my-bucket` bucket.
You can change what derivatives and plots are created from this process in the `docker/panda/config.py` file, by adding to the `plots` and `derivatives` lists functions which you find in the `docker/panda/viz.py` and `docker/panda/derivatives.py` files respectively.

#### Standing up the webservice
1. Install Docker on your machine (https://docs.docker.com/engine/installation/)
2. Pull the official EEG PANDA Docker image with the command `docker pull rymarr/eeg_panda_image`.
3. Launch the webservice with Docker and bind it to port 8888 with the command `docker run -d --name eeg_panda_container -p 8888:80 rymarr/eeg_panda_image`.
3. Congratulations, the web service is now launched at http://127.0.0.1:8888.

#### Using the web service
1. Go to the web service at http://127.0.0.1:8888.
2. Go to the 'Analyze Your Data' tab via the top menu bar.
3. Fill out the 'Get Data' form. The form fields are:
  * Bucket Name - The name of the S3 bucket you are pulling from.
    * For demo data, use the default value `neurodatadesign-test`.
  * File Path - Path to the desired file in the above bucket.
    * For demo data in the format given to us by Nicolas, use the value `test.mat`.
    * For demo data in the general format created by us, use the value `eeg_data.pkl`.
  * Name for Data - a meaningful name for the data.
    * For demo data, use any name you wish!
  * Formatting Token - a token to describe type of data this is.
    * For demo data in the format given to us by Nicolas, use the value `fcp_indi_eeg`.
    * For demo data in the general format created by us, use the value `eeg_panda_format`.
4. Click 'Get Data', and wait for a success message.
5. Click 'Preprocess Data', and wait a success message.
6. Click 'Analyze Data', and wait for a success message.
7. Go to the 'Explore Analyses' tab, and click the links in the table to view the results. 'Prep Report' contains the preprocessing report, 'Post Report' contains the postprocessing report, and 'zip file' contains a zip file of both of these.

##  *How to build and run the development environment*
#### Run a development server:
  1. Slack message @rmarren1 for Amazon Keys, or make an issue and tag @rmarren1.
  2. `git clone https://github.com/NeuroDataDesign/orange-panda`
  3. Go to the 'service' directory.
  4. Create a file named `set_keys.py`, with the following contents:
  ```
  
  import os
  
  os.environ['AWS_ACCESS_KEY']='.........'
  
  os.environ['AWS_SECRET_KEY']='.........'
  
  ```
  5. run ./setup_docker.sh (you must have [docker](https://docs.docker.com/engine/installation/) installed)
  6. The web service will be at http://127.0.0.1:8888. 
  
#### Making changes.
  1. Change any code, or the configuration parameters in service/app/config.txt.
  2. Re-run ./setup_docker.sh.
  3. Re-load the page. The best way to do this is in Google Chrome, by opening the developer tools (f12), right clicking the refresh button and clicking 'Empty Cache and Hard Reload'.

## Current functionality:

### EEG Data Preprocessing:
* Detection of faulty electrodes
  * Outliers of a kernel density based joint probability distribution
* Interpolation of faulty electrodes
  * Inverse great circle distance weighting of neighboring electrodes
* Artifact Rejection
  * FastICA based algorithm
* General noise-reduction
  * Robust PCA
  
### EEG Data Analysis:
* Automatic generation of the following interactive figures:
  * Distribution of NaNs and Infs over columns and rows
  * Sparklines of data dimensions
  * Cumulative variance explained by principal components
  * Anomoly detection figures
  * Pearson Correlation matrix of electrodes
  * Coherence matrix of electrodes
  * Spectrograms of data dimensions

### Documentation
[https://neurodatadesign.github.io/orange-panda]

### About this project
We (rmarren1, mnantez1, nkumarcc, tsunwong123) are undergraduate engineering students at Johns Hopkins University.
The goal of this project is to create a web-service which will allow any scientist or researcher to find, process, and analyze large EEG datasets without the need to install any software or format any data.
