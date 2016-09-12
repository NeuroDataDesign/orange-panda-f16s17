### Dependencies

# Get current wd
#orig <- getwd();
# Set wd to executing directory
#dirn <- dirname(parent.frame(2)$ofile)
#dirn <- dirname(sys.frame(1)$ofile)
# setwd(paste0(dirn, "/readdata"))
# print(getwd())
# Do the sourcing
# source('read_data.R')

# Change back to orig
#setwd(orig)
require(ggplot2)
require(reshape)

pupilloc <- function(patientnum = "A00051826", record = "Rest") {
    # Get data
    eyedata <- samplerestvis("C:\\Users\\Nitin\\Documents\\Hopkins\\BCI\\EEG Data Sharing\\A00051826\\A00051826_vis_learn Samples.txt")$rest;
    # Get location data (no scaling)
    locdata <- eyedata[,c("Time", "Type", "LEPOSX", "LEPOSY", "LEPOSZ", "REPOSX", "REPOSY", "REPOSZ")];
    # add column to determine trials
    
    # Make all time in terms of 0
    locdata[,"Time"] <- locdata[,"Time"] - locdata[1,"Time"];
    # Add labels for different trials
    events <- which(locdata$Type == "MSG");
    locdata[events[2]:events[4], "Trial"] <- 1;
    locdata[events[4]:events[6], "Trial"] <- 2;
    locdata[events[6]:events[8], "Trial"] <- 3;
    locdata[events[8]:events[10], "Trial"] <- 4;
    locdata[which(locdata$Type == "MSG")[10]:nrow(locdata), "Trial"] <- 5;
    locdata <- locdata[!is.na(locdata$Trial),];
    locdata <- melt(restsample, id = c("Time", "Type", "Trial"),
                    variable = "DataType", value = "Position");
    # Plot the data
    ggplot(locdata) +
        geom_point(aes(Time, value)) +
        ggtitle(paste("Patient", patientnum, "Eye Movement vs Time (4Hz Samples)")) +
        labs(x="Time (microseconds)",y="Eye Position (px)", color="Eye Distinction:") +
        facet_grid(DataType~Trial, scales = "free_x", labeller=label_both);
}