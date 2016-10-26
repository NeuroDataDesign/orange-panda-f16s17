
#The total number of functions called to generate a heatmap of 30 electrodes for the first minute of data

heatmap <- function(eegdata) {
  eeg1min15 <- eebsubset(eegdata)
  eeg1min15cut4 <- eeg1min15[2:200,]
  eeg1min15cut16a <- eeg1min15cut4[seq(1, nrow(eeg1min15cut4), 10), 1:31]
  eeg1min15cut16a$Time <- as.factor(eeg1min15cut16a$Time)
  eeg1min15cut16a.m <- eegmelt(eeg31min15cut16a)
  voltageheatmap(eeg31min15cut16a.m)
}