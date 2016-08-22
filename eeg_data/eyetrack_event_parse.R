#readeachtrial:
#Prompts user input for the number of trial and saves data pertaining to that specific trial. 
readeachtrial <- function(restdata) {
  n <- readline(prompt="Enter the resting trial number (from 1-5): ")
  i <- as.integer(n)
  if (i > 1) {
    prevresttime <- restdata$userevent[which(20 == restdata$userevent$Description, arr.ind = TRUE)[i], "Start"];
  } else {
    prevresttime <- restdata$userevent$Start[1];
  }
  restendtime <- restdata$userevent[which(20 == restdata$userevent$Description, arr.ind = TRUE)[i+1], "Start"];
  restingtrial <- lapply(restdata, function(x) x[which(x$Start <= restendtime & x$Start >= prevresttime),]);
  return(restingtrial);
}

#sepopenandclose:
#Separates the trials by if the subject was told "eyes open" and "eyes closed".
sepopenandclose <- function(restdata) {
  turningpoint <- restdata$userevent[which(30 == restdata$userevent$Description, arr.ind = TRUE)[1], "Start"];
  eyesopen <- lapply(restdata, function(x) x[which(x$Start < turningpoint),]);
  eyesclosed <- lapply(restdata, function(x) x[which(x$Start > turningpoint),]);
  returnlist <- list(eyesopen, eyesclosed);
  names(returnlist) <- c("open", "closed");
  return(returnlist)
}

# seprestingtrials
# Take in resting data and separate out into different trials
# Arg: file resting data
# Return 5 lists
seprestingtrials <- function(restdata) {
  trialstarts <- restdata$userevent[which(20 == restdata$userevent$Description, arr.ind = TRUE), "Start"];
  triallist <- list();
  for (i in 1:5) {
   restingtrial <- lapply(restdata, function(x) x[which(x$Start <= trialstarts[i+1] & x$Start >= trialstarts[i]),]);
   triallist[[length(triallist)+1]] <- restingtrial;
  }
  names(triallist) <- c("Trial1","Trial2","Trial3","Trial4","Trial5")
  return(triallist);
}
