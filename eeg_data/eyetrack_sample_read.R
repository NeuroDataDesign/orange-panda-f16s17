readrestvis <- function(inputpath) {
  restvisdata <- readfile(inputpath);
  restendtime <- restvisdata[which(20 == restvisdata$LDiaX, arr.ind = TRUE)[6], "Time"];
  restdata <- restvisdata[which(restvisdata$Time < restendtime),];
  visstarttime <- restvisdata[which(91 == restvisdata$LDiaX, arr.ind = TRUE)[1], "Time"];
  visdata <- restvisdata[which(restvisdata$Time >= visstarttime),];
  returnlist <- list(restdata, visdata);
  names(returnlist) <- c("rest", "visual");
  return(returnlist);
}

## Read in A#########_vis_learnSamples.txt
readfile <- function(inputpath) {
  resting_connection <- file(inputpath);
  open(resting_connection);
  
  samplecols <- unlist(read.table(resting_connection, header=FALSE, sep="\t", skip=38, nrows=1, colClasses="character")); # line 39
  samplecols <- gsub(" ", "", samplecols, fixed = TRUE);
  samplecols <- gsub("\\[.*\\]", "", samplecols);
  
  datatable <- read.table(resting_connection, header=FALSE, sep="\t", fill = TRUE, nrows=40000, comment.char="",
                          col.names = samplecols, stringsAsFactors = FALSE);

  datatable <- datatable[-c(1, nrow(datatable)), ];
  
  datatable$LDiaX <- gsub("^.*?: start_eye_recording","",datatable$LDiaX);
  datatable$LDiaX <- gsub("^.*?: ","",datatable$LDiaX);
  
  # Close connection
  close(resting_connection);

  return(datatable);
}