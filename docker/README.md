# docker -- dockerized panda

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
