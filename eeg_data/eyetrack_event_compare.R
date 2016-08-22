# takes in an event data list
# of all the different relevant dataframes
eventcompare <- function(eventdata) {
    library(ggplot2);
    out <- rbind(eventdata$userevent[, c("EventType", "Trial")], eventdata$blink[, c("EventType", "Trial")],
    eventdata$saccade[, c("EventType", "Trial")], eventdata$fixation[, c("EventType", "Trial")]);
    qplot(out$EventType, xlab = "Event Type", ylab = "Occurrences", main = "Event Occurrences");
}

bytime <- function(eventdata) {
    library(ggplot2);
    # First, get the R user event timestamps
    usertable <- eventdata$userevent[, c("Start", "Description")];
    lowerbound <- usertable$Start[1];
    upperbound <- usertable$Start[2];
    out <- rbind(eventdata$blink[, c("EventType", "Trial")], eventdata$saccade[, c("EventType", "Trial")],
                 eventdata$fixation[, c("EventType", "Trial")]);
}


#Shows the duration of saccades via the chronological trial numbers
saccadeduration <- function(eventdata) {
  library(ggplot2)
  out1 <- rbind(eventdata$saccade[, c("EventType", "Number", "Duration")]);
  g <- ggplot(out1, aes(Number, Duration))
  g + geom_point() + facet_grid(.~ EventType)
}

#Shows the speed of a saccade via the chronological trial numbers
saccadespeed <- function(eventdata) {
  library(ggplot2)
  out1 <- rbind(eventdata$saccade[, c("EventType", "Number", "AverageSpeed")]);
  g <- ggplot(out1, aes(Number, AverageSpeed))
  g + geom_point() + facet_grid(.~ EventType)
}

#Shows how far the subject's eyes have moved during a saccade
saccadedistance <- function(eventdata) {
  library(ggplot2)
  out1 <- rbind(eventdata$saccade[, c("EventType","Number","StartLoc.X", "StartLoc.Y", "EndLoc.X", "EndLoc.Y")]);
  out1$distance <- sqrt((out1$EndLoc.X-out1$StartLoc.X)^2+(out1$EndLoc.Y - out1$StartLoc.Y)^2)
  g <- ggplot(out1, aes(Number, distance))
  g + geom_point() + facet_grid(.~ EventType) + labs(x = "Trial Number", y = "Distance Traveled by Eye")
}

#Shows how much of the subject's time spent with fixation, saccade, or blink.
eventdurationcompare <- function(eventdata) {
  library(ggplot2)
  totalblinkduration <- sum(eventdata$blink$Duration)
  totalsaccadeduration <- sum(eventdata$saccade$Duration)
  totalfixationduration <- sum(eventdata$fixation$Duration)
  individualduration <- c(totalblinkduration, totalsaccadeduration, totalfixationduration)
  labeling <- c("Blink", "Saccade", "Fixation")
  durationdata <- data.frame(individualduration, labeling)
  #begintime <- eventdata$userevent[which(20 == eventdata$userevent$Description, arr.ind = TRUE)[1], "Start"];
 # endtime <- eventdata$userevent[which(rev(20 == eventdata$userevent$Description, arr.ind = TRUE))[1], "Start"];
  #totaltimeelapsed <- endtime - begintime
  qplot(durationdata$labeling,durationdata$individualduration, xlab="Event Type", ylab="Duration")
}

#Shows Pupil Size during fixations as trials go on
pupilsize <- function(eventdata) {
  library(ggplot2)
  out <- rbind(eventdata$fixation[, c("EventType","Number","Avg.PupilSizeX")]);
  g <- ggplot() +
    geom_point(data = out, aes(x = Number, y = Avg.PupilSizeX, color = "blue")) +
    facet_grid(.~ EventType) +
    xlab("Number of Trial") +
    ylab("Average Pupil Size")
  print(g);
}
