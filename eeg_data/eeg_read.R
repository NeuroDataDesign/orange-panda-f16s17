# convert .mat to .rdsc
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

converteeg <- function(inputpath) {
    # first install required package to handle
    # hdf5 format used in the files provided
    if(suppressWarnings(!require("h5"))) {
        install.packages("h5");
        library(h5);
    }
    file <- h5file(inputpath, "r");
    timeseries <- data.matrix(data.frame(file["result/times"][], file["result/data"][]));
    return(timeseries);
    
}