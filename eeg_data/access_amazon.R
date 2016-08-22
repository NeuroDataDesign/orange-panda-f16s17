# dependency check
# loads all relevant libs for aws.s3
dependency <- function() {
    # check for aws.s3 and dependencies
    
    if(suppressWarnings(!require("aws.s3"))) {
        # if not there, install dependencies
        # check for dependencies in order of req
        
        if(suppressWarnings(!require("devtools"))) {
            # if not there, install
            install.packages("devtools");
            library("devtools");
        }
        
        if(suppressWarnings(!require("xml2"))) {
            # if not there, install
            # via github because needs dev version
            devtools::install_github("hadley/xml2");
            library("xml2");
        }
        
        install.packages("aws.s3");
        library("aws.s3");
    }
}

# access eye data via amazon s3 wrapper
# Saves all data to a temp folder in wd
# to be deleted after behavior has been ran
# Args:
# patientnum = patient number
# datatype = either "Events" or "Samples"
accesseyedata <- function(patientnum, datatype = "Events") {

    # define root path to the patient's files based on given patient numbers
    patientpath = paste0("data/uploads/CMI_share/", patientnum, "/", patientnum);
    pathlist <- vector(mode="character", length = "10");
    eventnames <- vector(mode="character", length = "10");
    # now define a set of other paths to use this with
    for (i in 1:10) {
        eventpath <- "";
        if(i == 1 || i == 2 || i == 3) {
            eventpath <- paste0("_SAIIT_2AFC_Block",i);
            eventnames[i] <- paste0("SAIIT",i);
        } else if (i == 4 || i == 5) {
            eventpath <- paste0("_SurrSupp_Block",i - 3);
            eventnames[i] <- paste0("Surround",i - 3);
        } else if (i == 6 || i == 7 || i == 8) {
            eventpath <- paste0("_Video",i - 5);
            eventnames[i] <- paste0("Video",i - 5);
        } else if (i == 9) {
            eventpath <- "_WISC_ProcSpeed";
            eventnames[i] <- paste0("WISC");
        } else if (i == 10) {
            eventpath <- "_vis_learn";
            eventnames[i] <- paste0("Vis");
        }
        pathlist[i] <- paste0(patientpath, eventpath, "%20", datatype, ".txt");
    }
    
    pathdata <- list(pathlist, eventnames);
    dir.create(file.path(getwd(), "temp"));
    # Potentially need to add something to handle if temp folder already exists
    
    mapply(function(x, y) {
        tosave <- paste0(getwd(), "/temp/", y, ".txt");
        save_object(x, bucket="fcp-indi", tosave);
    }, x = pathlist, y = eventnames);
    
}


# access eeg via amazon s3 wrapper
# Saves all data to a temp folder in wd
# to be deleted after behavior has been ran
# Args:
# patientnum = patient number
# recordtype = either "full" or "reduced"
accesseegdata <- function(patientnum, recordtype = "full") {
    
    # define root path to the patient's files based on given patient numbers
    patientpath = paste0("data/uploads/", patientnum, "/");
    pathlist <- vector(mode="character", length = "10");
    eventnames <- vector(mode="character", length = "10");
    # now define a set of other paths to use this with
    for (i in 1:11) {
        eventnames[i] <- paste0(recordtype, "_", patientnum);
        if(i < 10) {
            eventnames[i] <- paste0(eventnames[i], "00", i, ".mat");
        } else {
            eventnames[i] <- paste0(eventnames[i], "0", i, ".mat");
        }
        pathlist[i] <- paste0(patientpath, eventnames[i]);
    }
    
    pathdata <- list(pathlist, eventnames);
    dir.create(file.path(getwd(), "temp"));
    # Potentially need to add something to handle if temp folder already exists
    
    mapply(function(x, y) {
        tosave <- paste0(getwd(), "/temp/", y, ".mat");
        save_object(x, bucket="fcp-indi", tosave);
    }, x = pathlist, y = eventnames);
    
}


# function to delete temp folder after done with activity
deletetemp <- function() {
    unlink("temp", recursive=TRUE);
}