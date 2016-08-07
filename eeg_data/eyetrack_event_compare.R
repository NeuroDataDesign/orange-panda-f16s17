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
    fixations <- unlist(read.table(resting_connection, header=FALSE, sep="\t", skip=9, nrows=1, colClasses="character"));
    print(class(fixations));
    # Skip header lines
    # read.table(resting_connection, header=FALSE, sep="\t", skip=20, nrows=12);
    # Close connection
    close(resting_connection);
    
}
