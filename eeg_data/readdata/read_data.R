### Dependencies

# Get current wd
orig <- getwd();
# Set wd to executing directory
dirn <- dirname(parent.frame(2)$ofile)
dirn <- dirname(sys.frame(1)$ofile)
setwd(dirn)
# Do the sourcing
source('access_amazon.R')
source('eeg_read.R')
source('eyetrack_event_read.R')
source('eyetrack_sample_read.R')
# Change back to orig
setwd(orig)

# Read in EEG data.
# 
# This file has the wrapper functions that we will interface with.
# Each will use the amazon functions and the read functions to return
# R usable data based on what's available. The underlying behavior will be
# hidden from any user.

readeeg <- function(patientnum = "A00051826", record = 1, recordtype = "full") {
    # First, load dependencies for Amazon access
    dependency();
    # After dependencies done, grab the eeg data from amazon
    # grab filepath that now holds the data
    filepath <- accesseegdata(patientnum, record, recordtype);
    # now convert eeg data from filepath
    eegdata <- converteeg(filepath);
    # now get rid of the file
    deletetemp();
    return(eegdata);
}

# Read Eyetracking Event data.
# 
# This file has the wrapper functions that we will interface with.
# Each will use the amazon functions and the read functions to return
# R usable data based on what's available. The underlying behavior will be
# hidden from any user.

readeeg <- function(patientnum = "A00051826", record = 1, recordtype = "full") {
    # First, load dependencies for Amazon access
    dependency();
    # After dependencies done, grab the eeg data from amazon
    # grab filepath that now holds the data
    filepath <- accesseegdata(patientnum, record, recordtype);
    # now convert eeg data from filepath
    eegdata <- converteeg(filepath);
    # now get rid of the file
    deletetemp();
    return(eegdata);
}