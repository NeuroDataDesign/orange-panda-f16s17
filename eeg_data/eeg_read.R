# Allows to pull in the metadata 
convertmetadata <- function(inputpath) {
    # start by making sure R.matlab is available in environment
    # use suppress warnings because don't want warning if R.matlab
    # isn't present
    if(suppressWarnings(!require("R.matlab"))) {
        install.packages("R.matlab");
        library("R.matlab");
    }
    
    # next, readMat the file in
    return(readMat(file(inputpath), maxLength=NULL, fixNames=TRUE, drop=c("singletonLists"),
            sparseMatrixClass=c("Matrix", "SparseM", "matrix"), verbose=FALSE));
    
}

# Doesn't get the whole file malleably available
# rather, produces a matrix
# First leftmost column is the time stamps (1)
# The rest to the right are EEG channel inputs (2:112)
converteeg <- function(inputpath) {
    
    # first install required package to handle
    # hdf5 format used in the files provided
    #if(suppressWarnings(!require("rhdf5"))) {
    #    source("http://bioconductor.org/biocLite.R");
    #    biocLite("rhdf5");
    #    library(rhdf5);
    #}
    
###### DEPRECATED, UPDATING TO RELY ON SEPARATE PACKAGE ##########    
    # first install required package to handle
    # hdf5 format used in the files provided
    if(suppressWarnings(!require("h5"))) {
        install.packages("h5");
        library(h5);
    }
    file <- h5file(inputpath, "r");
    resultdata <- file["result/chanlocs"];
    timeseries <- data.matrix(data.frame(file["result/times"][], file["result/data"][]));
    colnames(timeseries) <- c("Time", colnames(timeseries)[2:112]);
    return(timeseries);
    
}