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
    # add in electrode names for column names
    labels <- c('Time','E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12','E13','E14','E15','E16','E18','E19','E20','E21','E22','E23','E24','E25','E26','E27','E28','E29','E30','E31','E32','E33','E34','E35','E36','E37','E38','E39','E40','E41','E42','E43','E44','E45','E46','E47','E50','E51','E52','E53','E54','E55','E57','E58','E59','E60','E61','E62','E64','E65','E66','E67','E69','E70','E71','E72','E74','E75','E76','E77','E78','E79','E80','E82','E83','E84','E85','E86','E87','E89','E90','E91','E92','E93','E95','E96','E97','E98','E100','E101','E102','E103','E104','E105','E106','E108','E109','E110','E111','E112','E114','E115','E116','E117','E118','E120','E121','E122','E123','E124','Cz');
    eegdata <- as.data.frame(eegdata);
    names(eegdata) <- labels;
    return(eegdata);
}

# Read Eyetracking Event data.
# 
# Potential args: Rest, Vis, SAIIT(1,2,3), Surround(1,2), WISC, Video(1,2,3)

readevent <- function(patientnum = "A00051826", record = "Rest", recordtype = "full") {
    # First, load dependencies for Amazon access
    dependency();
    # After dependencies done, grab the eeg data from amazon
    # grab filepath that now holds the data
    filepath <- accesseyedata(patientnum, "Events");
    # now convert eyetracking data from filepath
    # DOESN'T CHECK FOR CORRECT RECORD HERE
    eventdata <- vector();
    if (record == "Rest") {
        eventdata <- eventrestvis(paste0(filepath, "Vis.txt"))$rest;
    } else if (record == "Vis") {
        eventdata <- eventrestvis(paste0(filepath, record))$visual;
    } else {
        eventdata <- eventfile(paste0(filepath, record));
    }
    
    # now get rid of the file
    deletetemp();
    return(eventdata);
}