# EEG PANDA - Automated EEG data analysis.
A summary schematic of what this service offers can be found [here](https://www.lucidchart.com/documents/view/ca99b646-c76a-42ef-8083-cacf3ada2c43).
We are currently live at http://ec2-54-205-199-24.compute-1.amazonaws.com/#/

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

## *How to stand up the PANDA webservice*
We offer a docker image which runs the production webservice launching our pipeline on AWS batch. The workflow is as follows:
1. The user places a credential file in the root directory of the `service` folder and builds the pipeline to create a docker image.
2. The user runs the docker image and binds it to a public facing port (port 80).

We detail each of these steps below.

#### 1.
This step is exactly the same as step 1. in the preceding section, except instead of placing the `credentials.csv` file in the `docker` directory, you place it in the `service` directory. Also, when you build the docker image, the name should change to `yourname/panda_webservice`.

#### 2.
Launch the webservice with Docker and bind it to port 8888 with the command `docker run -d --name webservice -p 8888:80 rymarr/panda_webservice`. Note, if you would just like to launch a local version of the webservice (for testing), you can simply run the `./setup_docker.sh` script instead of going through this step.

Congratulations, your webservice should now be live at `your-url:8888`. In the local case, this will be `127.0.0.1:8888`

## Using the web service
1. Go to the web service at http://127.0.0.1:8888.
2. Go to the 'Analyze Your Data' tab via the top menu bar.
3. Fill out the 'Get Data' form. The form fields are:
  * Bucket Name - The name of the S3 bucket you are pulling from.
    * For demo data, use the default value `neurodatadesign-test`.
  * Input BIDS directory in S3
    * For demo data, use the value `small_test_set`
4. When finished, the results should appear in the bucket, which can be viewed from the demo in the 'View Analyses' tab.

## Current functionality:

In our [schematic](https://www.lucidchart.com/documents/view/ca99b646-c76a-42ef-8083-cacf3ada2c43), an overview of the pipeline is shown. Each box in this overview is a link, which will direct you to a detailed scientific notebook detailing the step.


### About this project
We (rmarren1, nkumarcc) are undergraduate engineering students at Johns Hopkins University.
The goal of this project is to create a web-service which will allow any scientist or researcher to find, process, and analyze large EEG datasets without the need to install any software or format any data.
