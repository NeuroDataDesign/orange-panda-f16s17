readeachtrial <- function(restdata) {
  n <- readline(prompt="Enter the resting trial number (from 1-5): ")
  i <- as.integer(n)
  if (i > 1) {
    prevresttime <- restdata$userevent[which(20 == restdata$userevent$Description, arr.ind = TRUE)[i], "Start"];
  } else {
    prevresttime <- restdata$userevent$Start[1];
  }
  restendtime <- restdata$userevent[which(20 == restdata$userevent$Description, arr.ind = TRUE)[i+1], "Start"];
  restingtrial <- lapply(restdata, function(x) x[which(x$Start < restendtime & x$Start > prevresttime),]);
  return(restingtrial);
}

# seprestingtrials
# Take in resting data and separate out into different trials
# Arg: file resting data
# Return 5 lists
#seprestingtrials <- function(restdata) {
#  library(plyr)
#  restdata <- lapply(restdata, cbind, TrialNumber = c("0"))


# for (i in 1:5) {
#   if (i > 1) {
#     prevrestingtime <- restdata$userevent[which(20 == restdata$userevent$Description, arr.ind = TRUE)[i], "Start"];
#   } else {
#    prevrestingtime <- restdata$userevent$Start[1];
#  }
#  restendtime <- restdata$userevent[which(20 == restdata$userevent$Description, arr.ind = TRUE)[i+1], "Start"];
#  x.sub <-subset(restdata$userevent)
#restdata$userevent$TrialNumber <- as.numeric(as.character(restdata$userevent$TrialNumber))
#restdata$userevent$TrialNumber[which(restdata$userevent$Start <= restendtime & restdata$userevent$Start >= prevrestingtime), restdata$userevent$TrialNumber] = i;
#  apply(restdata, 2, function(x) {
#   x[which(x$Start <= restendtime && x$Start >= prevrestingtime), which(x$TrialTime == 0)] = i; 
#  })

# restdatatochange <- lapply(restdata, function(x) x[which(x$Start <= restendtime & x$Start >= prevrestingtime),])
#restdata <- lapply(restdata, function(x) {
# x[which(x$Start <= restendtime & x$Start >= prevrestingtime),] <- restdatatochange
#})
# }
#  return(restingdata$userevent);
#}
