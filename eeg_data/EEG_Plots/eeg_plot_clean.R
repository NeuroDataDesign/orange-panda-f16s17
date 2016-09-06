eegsubset <- function(eegdata) {
  eegsubsetting1min <- eeg[1:30000,];
  eegsubsetting1min15 <- eegsubsetting1min[seq(1, nrow(eegsubsetting1min), 15), ];
  labels <- c('Time','E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12','E13','E14','E15','E16','E18','E19','E20','E21','E22','E23','E24','E25','E26','E27','E28','E29','E30','E31','E32','E33','E34','E35','E36','E37','E38','E39','E40','E41','E42','E43','E44','E45','E46','E47','E50','E51','E52','E53','E54','E55','E57','E58','E59','E60','E61','E62','E64','E65','E66','E67','E69','E70','E71','E72','E74','E75','E76','E77','E78','E79','E80','E82','E83','E84','E85','E86','E87','E89','E90','E91','E92','E93','E95','E96','E97','E98','E100','E101','E102','E103','E104','E105','E106','E108','E109','E110','E111','E112','E114','E115','E116','E117','E118','E120','E121','E122','E123','E124','Cz')
  colnames(eegsubsetting1min15) <- labels
}

eegplot <- function(eegdata) {
  library(ggplot2)
  ggplot(eegsubsetting1min15, aes(Time, Cz)) + geom_line() + ggtitle("Voltage of the Cz Electrode Every 30 ms") +
    labs(x="Time (ms)",y="Voltage of Cz (??V)");
}

powerspecplot <- function(eegdata) {
  fftCz <- fft(eegdata$Cz);
  spectrum(fftCz, xlab = "frequency (kHz)", ylab = "Power (W)");
}

#convert.fft is a courtesy of http://www.di.fc.ul.pt/~jpn/r/fourier/fourier.html
convert.fft <- function(cs, sample.rate=500) {
  cs <- cs / length(cs) # normalize
  
  distance.center <- function(c)signif( Mod(c),        4)
  angle           <- function(c)signif( 180*Arg(c)/pi, 3)
  
  df <- data.frame(cycle    = 0:(length(cs)-1),
                   freq     = 0:(length(cs)-1) * sample.rate / length(cs),
                   strength = sapply(cs, distance.center),
                   delay    = sapply(cs, angle))
  return(df);
}

ampspecplot <- function(fftdata) {
  AmpCz <- Mod(fftdata)
  spectrum(AmpCz, xlab = "frequency (kHz)", ylab = "Amplitude (dB)");
}

phasespecplot <- function(fftdata) {
  phaseCz <- Arg(fftdata)
  spectrum(phaseCz, xlab = "frequency (kHz)", ylab = "Phase");
}