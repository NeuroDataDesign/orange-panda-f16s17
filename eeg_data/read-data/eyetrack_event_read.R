# Resting vs SAIIT
# Read resting visual tracking data and compare with flickering data (both the event files)
# potentially generalize this later?

# Read the event data in for the different files for an individual patient to make them all comparable
# UNDER CONSTRUCTION... DON'T WORRY ABOUT FOR NOW
readeyedata <- function(rootpath, patientnum, toret) {
    # build filepath
    filepath = paste0(rootpath, "/", patientnum, "/", patientnum);
    wiscdata <- readfile(paste0(filepath, "_WISC_ProcSpeed Events.txt"));
}



# readrestvis
# Take in file path to visual Event.txt file 
# Arg: file input path
# Return list:
#   - list[1,] = $rest = Rest Data
#   - list[2,] = $visual = Visual Data
readrestvis <- function(inputpath) {
    # First visual learning and resting data parse
    restvisdata <- readfile(inputpath);
    # To separate find the timestamp from user events for the 6th number 20 decription
    # That's the cutoff for actual resting data
    restendtime <- restvisdata$userevent[which(20 == restvisdata$userevent$Description, arr.ind = TRUE)[6], "Start"];
    # use cutoff to get resting data
    restdata <- lapply(restvisdata, function(x) x[which(x$Start < restendtime),]);
    # get lower bound for visdata
    # the "start_eye_recording" tag (changed to a 0 in description here) isn't consistently there for resting
    # so can't use it. use 91, start of visual learning message
    visstarttime <- restvisdata$userevent[which(91 == restvisdata$userevent$Description, arr.ind = TRUE)[1], "Start"];
    visdata <- lapply(restvisdata, function(x) x[which(x$Start >= visstarttime),]);
    returnlist <- list(restdata, visdata);
    names(returnlist) <- c("rest", "visual");
    return(returnlist);
}

# readfile
# Take in file path to Event.txt file 
# Arg: file input path
# Return list:
#   - list[1,] = $userevent = User Event Data
#   - list[2,] = $blink = Blink Data
#   - list[3,] = $fixation = Fixation Data
#   - list[4,] = $saccade = Saccade Data
readfile <- function(inputpath) {
    # Resting data
    # Open connection to file
    resting_connection <- file(inputpath);
    open(resting_connection);
    
    # For now just read user events
    # First, grab column names
    # Fixations
    fixationcols <- unlist(read.table(resting_connection, header=FALSE, sep="\t", skip=9, nrows=1, colClasses="character")); # line 10
    fixationcols <- gsub(" ", "", fixationcols, fixed = TRUE);
    fixationcols <- gsub(".", "", fixationcols, fixed = TRUE);
    # Saccade
    saccadecols <- unlist(read.table(resting_connection, header=FALSE, sep="\t", skip=2, nrows=1, colClasses="character")); # line 13
    saccadecols <- gsub(" ", "", saccadecols, fixed = TRUE);
    saccadecols <- gsub(".", "", saccadecols, fixed = TRUE);
    # Blinks
    blinkcols <- unlist(read.table(resting_connection, header=FALSE, sep="\t", skip=2, nrows=1, colClasses="character")); # line 16
    blinkcols <- gsub(" ", "", blinkcols, fixed = TRUE);
    blinkcols <- gsub(".", "", blinkcols, fixed = TRUE);
    # User Events
    usereventcols <- unlist(read.table(resting_connection, header=FALSE, sep="\t", skip=2, nrows=1, colClasses="character")); # line 19
    usereventcols <- gsub(" ", "", usereventcols, fixed = TRUE);
    usereventcols <- gsub(".", "", usereventcols, fixed = TRUE);
    
    # Read in the whole table
    # get max number of cols in a row
    tablelen <- max(length(fixationcols), length(saccadecols), length(blinkcols), length(usereventcols));
    # nrows = 7000 as a failsafe, not actual amount
    # fill and col.names are there for making sure read in all potential columns
    datatable <- read.table(resting_connection, header=FALSE, sep="\t", fill = TRUE, nrows=7000,
                            skip=1, comment.char="", col.names = paste0("V",seq_len(tablelen)),
                            stringsAsFactors = FALSE);
    
    # separate into event-based tables
    
    # user event data
    # separate data out
    usereventdata <- datatable[which("UserEvent" == datatable$V1), ];
    # remove unnecessary columns
    usereventdata <- usereventdata[, unlist(lapply(usereventdata, function(x) !all(is.na(x))))];
    colnames(usereventdata) <- usereventcols;
    # also remove top and bottom rows because just time of taking data; might be looked at later
    usereventdata <- usereventdata[-c(1, nrow(usereventdata)), ];
    # make description easier to process by converting to numbers
    usereventdata$Description <- gsub("^.*?: ","", usereventdata$Description);
    usereventdata$Description <- gsub("start_eye_recording","0", usereventdata$Description);
    usereventdata$Description <- as.numeric(usereventdata$Description);
    
    
    # blink data
    # Using regexes, catch all blink
    blinkdata <- datatable[grep("^(Blink)", datatable$V1),];
    # remove unnecessary columns
    blinkdata <- blinkdata[, unlist(lapply(blinkdata, function(x) !all(is.na(x))))];
    # put col headers
    colnames(blinkdata) <- blinkcols;
    
    
    # fixation data
    # Using regexes, catch all fixation
    fixationdata <- datatable[grep("^(Fixation)", datatable$V1),];
    # remove unnecessary columns
    fixationdata <- fixationdata[, unlist(lapply(fixationdata, function(x) !all(is.na(x))))];
    # put col headers
    colnames(fixationdata) <- fixationcols;
    
    # saccade data
    # Using regexes, catch all saccade
    saccadedata <- datatable[grep("^(Saccade)", datatable$V1),];
    # remove unnecessary columns
    saccadedata <- saccadedata[, unlist(lapply(saccadedata, function(x) !all(is.na(x))))];
    # put col headers
    colnames(saccadedata) <- saccadecols;
    
    
    # Close connection
    #close(resting_connection);
    
    # return list of tables
    returnlist <- list(usereventdata, blinkdata, fixationdata, saccadedata);
    names(returnlist) <- c("userevent", "blink", "fixation", "saccade");
    return(returnlist);
}