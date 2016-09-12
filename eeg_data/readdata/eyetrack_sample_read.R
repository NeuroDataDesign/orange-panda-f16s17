###Read in Eye Tracking Sample Data

## Create Two Datatables from imported eyetrack data.
## One for Resting and one for Visual Data
samplerestvis <- function(inputpath) {
  restvisdata <- samplefile(inputpath);
  
  #Identify the time stamp of the 6th "Message: 20"
  #The cutoff for resting data is at the beginning of the 6th "Message 20"
  #The data following the 6th "Message 20" is intentionally omitted - deemed irrelevant
  restendtime <- restvisdata[which(20 == restvisdata$LDiaX, arr.ind = TRUE)[6], "Time"];
  
  #Return all data between the first timestamp and the timestamp identified above into restdata table
  restdata <- restvisdata[which(restvisdata$Time < restendtime),];
  
  #Identify the time stamp of the 1st "Message 91" as the start of visual data
  visstarttime <- restvisdata[which(91 == restvisdata$LDiaX, arr.ind = TRUE)[1], "Time"];
  
  #Return all data after the timestamp for "Message 91"
  visdata <- restvisdata[which(restvisdata$Time >= visstarttime),];
  
  #Create Two Lists: 
  ## 1) Resting Samples Data
  ## 2) Visual Samples Data
  returnlist <- list(restdata, visdata);
  names(returnlist) <- c("rest", "visual");
  return(returnlist);
}

## Read in A#########_vis_learnSamples.txt
samplefile <- function(inputpath) {
  resting_connection <- file(inputpath);
  open(resting_connection);
  
  #Read in the labels for each column
  samplecols <- unlist(read.table(resting_connection, header=FALSE, sep="\t", skip=38, nrows=1, colClasses="character")); # line 39
  
  #Substitute all spaces in the data with no space
  samplecols <- gsub(" ", "", samplecols, fixed = TRUE);
  
  #Substitute all content in brackets with no space
  samplecols <- gsub("\\[.*\\]", "", samplecols);
  
  #Read in all of the data from file A#########_vis_learnSamples.txt
  datatable <- read.table(resting_connection, header=FALSE, sep="\t", fill = TRUE, nrows=40000, comment.char="",
                          col.names = samplecols, stringsAsFactors = FALSE);
  
  #Remove the first and last rows from the read in data
  datatable <- datatable[-c(1, nrow(datatable)), ];
  
  #Remove all text "start_eye_recording"
  datatable$LDiaX <- gsub("^.*?: start_eye_recording","",datatable$LDiaX);
  
  #Remove all text before the ":", as well as the ":"
  ###This is necessary so that we can identify the end of resting data and start of visual data by the message #
  datatable$LDiaX <- gsub("^.*?: ","",datatable$LDiaX);
  
  # Close connection
  close(resting_connection);

  return(datatable);
}