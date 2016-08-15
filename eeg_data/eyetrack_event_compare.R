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