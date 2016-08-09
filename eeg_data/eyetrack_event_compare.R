# Resting vs SAIIT
# Read resting visual tracking data and compare with flickering data (both the event files)
# potentially generalize this later?

# First need to read in both data sets into data frames
readdata <- function() {
    # Resting data
    # Open connection to file
    resting_connection <- file("cmi_share_A00051826/A00051826_vis_learn Events.txt");
    open(resting_connection);
    
    # For now just read user events
    # First, grab column names
    # Fixations
    fixations <- unlist(read.table(resting_connection, header=FALSE, sep="\t", skip=9, nrows=1, colClasses="character")); # line 10
    # Saccade
    saccade <- unlist(read.table(resting_connection, header=FALSE, sep="\t", skip=2, nrows=1, colClasses="character")); # line 13
    # Blinks
    blinks <- unlist(read.table(resting_connection, header=FALSE, sep="\t", skip=2, nrows=1, colClasses="character")); # line 16
    # User Events
    userevents <- unlist(read.table(resting_connection, header=FALSE, sep="\t", skip=2, nrows=1, colClasses="character")); # line 19
    
    # Read in the whole table
    datatable <- read.table(resting_connection, header=FALSE, sep="\t", fill=TRUE, nrows=7000, skip=1, comment.char=""); # line 143
    
    print(sapply(datatable, class));
    # user event data
    usereventdata <- datatable[, ];
    
    
    # print(head(usereventdata));
    # left eye data
    # lefteyedata <- read.table(resting_connection, header=FALSE, sep="\t", skip=130, nrows=553); # line 606
    # left eye separate
    # saccadedata <- lefteyedata;
    
    
    # Close connection
    close(resting_connection);
    
}