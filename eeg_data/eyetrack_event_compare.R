# takes in an event data list
# of all the different relevant dataframes
eventcompare <- function(eventdata) {
    library(ggplot2);
    out <- rbind(eventdata$userevent[, c("EventType", "Trial")], eventdata$blink[, c("EventType", "Trial")],
    eventdata$saccade[, c("EventType", "Trial")], eventdata$fixation[, c("EventType", "Trial")]);
    qplot(out$EventType);
}