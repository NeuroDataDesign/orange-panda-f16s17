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

dataprep <- function(patientnum = "A00051826", record = "Rest") {
    # Get data
    eyedata <- readsample(patientnum = patientnum, record = record);
    # Get location data (no scaling)
    locdata <- eyedata[,c("Time", "Type", "LEPOSX", "LEPOSY", "LEPOSZ", "REPOSX", "REPOSY", "REPOSZ")];
    # add column to determine trials
    
    # Make all time in terms of 0
    locdata[,"Time"] <- locdata[,"Time"] - locdata[1,"Time"];
    # Add labels for different trials
    events <- which(locdata$Type == "MSG");
    if (record == "Rest") {
        locdata[events[2]:events[4], "Trial"] <- 1;
        locdata[events[4]:events[6], "Trial"] <- 2;
        locdata[events[6]:events[8], "Trial"] <- 3;
        locdata[events[8]:events[10], "Trial"] <- 4;
        locdata[which(locdata$Type == "MSG")[10]:nrow(locdata), "Trial"] <- 5;
    } else if (record == "Surround2") {
        for (i in seq(1, 61, 3)) {
            if (i + 3 <= 64) {
                locdata[events[1+i]:events[3+i], "Trial"] <- (i+2)/3;
            } else {
                locdata[events[1+i]:nrow(events), "Trial"] <- (i+2)/3;
            }
        }
    }
    locdata <- locdata[!is.na(locdata$Trial),];
    # Melt data for ggplot2 capability
    locdata <- melt(locdata, id = c("Time", "Type", "Trial"),
                    variable = "DataType", value = "Position");
    return(locdata);
}

pupil_patientfull <- function(patientnum = "A00051826", record = "Rest") {
    # Plot the data
    ggplot(dataprep(patientnum = patientnum, record = record)) +
        geom_point(aes(Time, value)) +
        ggtitle(paste("Patient", patientnum, record, "Data: Eye Movement vs Time (120Hz Samples)")) +
        labs(x="Time (microseconds)",y="Eye Position (px)", color="Eye Distinction:") +
        facet_grid(DataType~Trial, scales = "free", labeller="label_both");
}