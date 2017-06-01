# service -- dockerized flask app launching AWS batch jobs running the panda pipeline

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
