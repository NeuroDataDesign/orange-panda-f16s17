# EEG Plot of God knows fucking what
eegplot <- function(eegdata) {
    require(ggplot2);
    eegsubsetting1min <- eegdata[1:30000,,15];
    eegsubsetting1min15 <- eegsubsetting1min[seq(1, nrow(eegsubsetting1min), 15), ];
    ggplot(eegsubsetting1min15, aes(Time, Cz)) + geom_line() + ggtitle("Voltage of the Cz Electrode Every 30 ms") +
        labs(x="Time (ms)",y="Voltage of Cz (??V)");
    fftCz <- fft(eegsubsetting1min15$Cz, inverse = FALSE);
    spectrum(fftCz, xlab = "frequency (Hz)", ylab = "Spectrum (W)");
}