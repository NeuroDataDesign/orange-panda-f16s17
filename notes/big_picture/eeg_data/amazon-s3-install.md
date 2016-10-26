# Installing:

## [CloudyR aws.s3:](https://github.com/cloudyr/aws.s3)
install.packages("aws.s3", repos = c("cloudyr" = "http://cloudyr.github.io/drat"))
### Install this after installing dependencies below

Dependencies:

## [Rtools:](https://cran.r-project.org/bin/windows/Rtools/)
No automated way to install this. Need to install version of this so it can build xml2 package off of Github.
    - During install, leave change PATH checked for potential console use later
    - Otherwise, default settings work

## devtools
install.packages("devtools")

## [xml2:](https://github.com/hadley/xml2)
install.packages("devtools")
devtools::install_github("hadley/xml2")
^need to use this way of getting xml2, as need development version of xml2, [see here](https://github.com/cloudyr/aws.s3/issues/61).