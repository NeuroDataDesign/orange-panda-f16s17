# fftshift code adapted and altered from 
# http://stackoverflow.com/questions/38230794/how-to-write-fftshift-and-ifftshift-in-r
fftshift <- function(input_matrix, dim = -1) {
    cols <- length(input_matrix)
    cols_half <- ceiling(cols/2)
    return(c(input_matrix[(cols_half+1):cols], input_matrix[1:cols_half]))
}

# fft wrapper
# run the fft, fftshift
convert.fft <- function(eegdata) {
    # run fft
    fftdata <- fft(eegdata);
    # fftshift
    fftdata <- fftshift(fftdata);
    return(fftdata);
}

# Subset the data

eegsubsetter <- function(data, timeslice = c(1, nrow(data)), downsample = 1) {
    # incorporate timeslice
    subset <- data[timeslice[1]:timeslice[2],,];
    # then downsample
    return(subset[seq(1, nrow(subset), downsample), ])
}

# Plot functions

# Time domain plot of the eegdata
timeplot <- function(eegdata, electrodes) {
  require(ggplot2)
  ggplot(eegdata, aes(Time, Cz)) +
    geom_line() +
    ggtitle("Voltage of the Cz Electrode Every 30 ms") +
    labs(x="Time (ms)",y="Voltage of Cz (??V)");
}

# Amplitude vs Frequency Plot of given data
ampplot <- function(fftdata, electrodes, dur, upfreq = 500) {
    # dependency
    require(ggplot2);
    fftdata <- apply(fftdata, FUN = Mod, MARGIN = 2);
    amp <- as.data.frame(cbind(Frequency = (1:nrow(fftdata))/dur, fftdata));
    amp <- melt(amp, id.vars = "Frequency", variable_name = "Electrode");
    ggplot(amp, aes(y = value, x = Frequency, color = Electrode)) +
        geom_line() +
        ggtitle(paste(electrodes)) +
        xlim(0,upfreq) +
        ylim(0,1000) +
        labs(x="Frequency (Hz)",y="Amplitude (dB)");
}

# Phase vs Frequency Plot of given data
phasespecplot <- function(fftdata, electrodes) {
    # dependency
    require(ggplot2);
    phase <- as.data.frame(cbind((1:length(fftdata))/dur, Arg(fftdata)));
    colnames(phase) <- c("Frequency", "Amount");
    ggplot(phase, aes(y = Amount, x = Frequency)) +
        geom_line() +
        ggtitle(paste(electrodes, "Amplitude vs Frequency")) +
        xlim(0,100) +
        labs(x="Frequency (Hz)",y="Amplitude (dB)");
}

# Higher level plotter functions

# Look at different electrodes in graph
fourierwrapper <- function(eegdata, electrodes = "Cz", timeslice = c(1, 30000),
                           samplerate = 500, upperfreq = 250) {
    # subset
    eegsubset <- eegsubsetter(eegdata, timeslice = timeslice);
    # make ffts of multiple electrodes
    eegsubset <- as.data.frame(eegsubset[, electrodes]);
    colnames(eegsubset) <- electrodes;
    fftsubset <- apply(eegsubset, FUN = convert.fft, MARGIN = 2);
    # plot the electrodes
    ampplot(fftsubset, electrodes = electrodes, 
            dur = timeslice[2]/samplerate, upfreq = upperfreq)
}