# EEG PANDA
## A pipeline for automated EEG data analysis.

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
