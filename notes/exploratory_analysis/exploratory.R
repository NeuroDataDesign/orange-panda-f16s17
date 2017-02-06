# Doesn't get the whole file malleably available
# rather, produces a matrix
# First leftmost column is the time stamps (1)
# The rest to the right are EEG channel inputs (2:112)
eeg_meda <- function(inputpath, outname, start_elec, end_elec, start_time, end_time) {
    
    # first install required package to handle
    # hdf5 format used in the files provided
    if(suppressWarnings(!require("h5"))) {
        install.packages("h5");
        library(h5);
    }
    require(devtools)
    #devtools::install_github("neurodata/meda")
    require(meda)
    require(ggplot2)
    
    file <- h5file(inputpath, "r");
    outFile <- paste0("C:/Users/Nitin/Documents/Hopkins/BCI/orange-panda/notes/exploratory_analysis/",
                      inputpath, "/", outname)
    
    resultdata <- data.matrix(data.frame(file["result/data"][]))
    #timeseries <- data.matrix(data.frame(file["result/times"][], file["result/data"][]));
    #colnames(timeseries) <- c("Time", colnames(timeseries)[2:112]);
    #return(timeseries);
    if(end_time == 0) {
        end_time = nrow(resultdata)
    }
    sample_dat <- resultdata[seq(from=start_time,to=end_time,by=100), start_elec:end_elec]
    bool <- !apply(sample_dat, 2, function(x) sd(x) == 0)
    sample_dat <- sample_dat[, bool]
    meda::genHTML(sample_dat, outFile)
}

run_meda <- function(file_name, start_elec, end_elec, start_time, end_time) {
    eeg_meda(paste0(file_name, ".mat"), 
             paste0("nicolas_", file_name, "_elec",start_elec,"s",
                    end_elec,"e", "_time", start_time, "s", end_time, "e.html"),
             start_elec, end_elec, start_time, end_time)
}

run_scripts <- function() {
    # Half partitions of data
    #run_meda("full_A00051826_01",start_elec=40,end_elec=60,
    #         start_time=0,end_time=10000)
    #run_meda("full_A00051826_01",start_elec=40,end_elec=60,
    #         start_time=10000,end_time=0)
    
    # All partitions 60-80
    #run_meda("full_A00051826_01",start_elec=60,end_elec=80,
    #         start_time=0,end_time=0)
    #run_meda("full_A00051826_01",start_elec=60,end_elec=80,
    #         start_time=0,end_time=10000)
    #run_meda("full_A00051826_01",start_elec=60,end_elec=80,
    #         start_time=10000,end_time=0)
    
    # All partitions 80-111
    #run_meda("full_A00051826_01",start_elec=80,end_elec=111,
    #         start_time=0,end_time=0)
    #run_meda("full_A00051826_01",start_elec=80,end_elec=111,
    #         start_time=0,end_time=10000)
    #run_meda("full_A00051826_01",start_elec=80,end_elec=111,
    #         start_time=10000,end_time=0)
    
    # All partitions 30-70
    #run_meda("full_A00051826_01",start_elec=30,end_elec=80,
    #         start_time=0,end_time=0)
    #run_meda("full_A00051826_01",start_elec=80,end_elec=111,
    #         start_time=10000,end_time=0)
    

    
    #### Test
    
    # Half partitions of data
    #run_meda("test",start_elec=40,end_elec=60,
    #         start_time=0,end_time=0)
    #run_meda("test",start_elec=40,end_elec=60,
    #         start_time=0,end_time=10000)
    #run_meda("test",start_elec=40,end_elec=60,
    #         start_time=10000,end_time=0)
    
    # All partitions 60-80
    #run_meda("test",start_elec=60,end_elec=80,
    #         start_time=0,end_time=0)
    #run_meda("test",start_elec=60,end_elec=80,
    #         start_time=0,end_time=10000)
    #run_meda("test",start_elec=60,end_elec=80,
    #         start_time=10000,end_time=0)
    
    # All partitions 80-111
    #run_meda("test",start_elec=80,end_elec=111,
    #         start_time=0,end_time=0)
    #run_meda("test",start_elec=80,end_elec=111,
    #         start_time=0,end_time=10000)
    #run_meda("test",start_elec=80,end_elec=111,
    #         start_time=10000,end_time=0)
    
    # All partitions 30-70
    #run_meda("test",start_elec=30,end_elec=70,
    #         start_time=0,end_time=0)
    #run_meda("test",start_elec=30,end_elec=70,
    #         start_time=0,end_time=10000)
    #run_meda("test",start_elec=80,end_elec=111,
    #         start_time=10000,end_time=0)
        
}

run_scripts2 <- function() {
    # Paradigm 2
    #run_meda("full_A00051826_02",start_elec=0,end_elec=40,
    #         start_time=0,end_time=0)
    run_meda("full_A00051826_02",start_elec=40,end_elec=80,
             start_time=0,end_time=0)
    run_meda("full_A00051826_02",start_elec=80,end_elec=111,
             start_time=0,end_time=0)
    ### Paradigm 3
    run_meda("full_A00051826_03",start_elec=0,end_elec=40,
             start_time=0,end_time=0)
    run_meda("full_A00051826_03",start_elec=40,end_elec=80,
             start_time=0,end_time=0)
    run_meda("full_A00051826_03",start_elec=80,end_elec=111,
             start_time=0,end_time=0)
    ### Paradigm 4
    run_meda("full_A00051826_04",start_elec=0,end_elec=40,
             start_time=0,end_time=0)
    run_meda("full_A00051826_04",start_elec=40,end_elec=80,
             start_time=0,end_time=0)
    run_meda("full_A00051826_04",start_elec=80,end_elec=111,
             start_time=0,end_time=0)
    ### Paradigm 5
    run_meda("full_A00051826_02",start_elec=0,end_elec=40,
             start_time=0,end_time=0)
    run_meda("full_A00051826_02",start_elec=40,end_elec=80,
             start_time=0,end_time=0)
    run_meda("full_A00051826_02",start_elec=80,end_elec=111,
             start_time=0,end_time=0)    
}