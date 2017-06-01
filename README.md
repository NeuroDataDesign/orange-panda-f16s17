# EEG PANDA - Automated EEG data analysis.
A summary schematic of what this service offers can be found [here](https://www.lucidchart.com/documents/view/ca99b646-c76a-42ef-8083-cacf3ada2c43).

Our service is not currently live, drop an issue if want to play around with a demo

A slideshow presentation of this work can be found [here](https://docs.google.com/presentation/d/1HAwHF6ujEo9bjGjO5hyxkfl_mLDAdqxLPfy7qIrNXcg/edit?usp=sharing)

Our pipeline is pip installable! run `pip install ndd-panda` to get the latest version. This will include all of the code in the panda folder, and some scripts to run the entire pipeline based on our default pipeline configuration.

### Summary of folders
Inside of each folder will be a readme with more details on the code or service in that folder. Following is a short description of each.

dist -- zip files of our panda codebase (just the barebones signal processing algorithms and pipeline, no docker or AWS deployment)

docker -- a Dockerfile to build a docker image which runs our pipeline taking data in from and pushing data out to S3

docs -- documentation generated from docstrings in the panda code (**these docs are not up to date, you can ignore then**)

method_mds -- detailed scientific notebooks explaining each pipeline step, complete with numerical simulations on contrived data and before-and-after results on EEG data

notes -- various markdowns and jupyter notebooks used as scratch work when brainstorming for and creating this pipeline

panda -- contains all of the signal processing algorithms used in the pipeline, our default pipeline configuration, and a script to run our pipeline with the default configuration (can be modified to run with any configuration if desired, and adding your own algorithms as steps is possible, drop an issue if you have trouble doing this).

service -- a web service which serves our pipeline. users will fill out a web form to launch a AWS batch job which will run this pipeline on each datapoint in a dataset in parallel.

web -- methods to deploy in parallel on batch

## Current functionality:

In our [schematic](https://www.lucidchart.com/documents/view/ca99b646-c76a-42ef-8083-cacf3ada2c43), an overview of the pipeline is shown. Each box in this overview is a link, which will direct you to a detailed scientific notebook detailing the step.


### About this project
We (rmarren1, nkumarcc) are undergraduate computer science students at Johns Hopkins University.
The goal of this project is to create a web-service which will allow any scientist or researcher to find, process, and analyze large EEG datasets without the need to install any software, develop learning algorithms, or purchase expensive high performance computing hardware.
