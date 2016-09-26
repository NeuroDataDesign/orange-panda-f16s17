# Robust PCA

## Definition - What is it?
-orthogonal transformation to convert a set of observations of possibly correlated variables into a set of values of linearly uncorrelated variables called "principal components".
-brain signals tend to be redundant, therefore reducing dimension helps with analysis
-separate out types of variables for easier analysis.
-remove sparse noise from the data.

## A simple explanation of how it works
-finds the maximum variance in a set of data using the variance equation and the Lagrange multiplier optimization method.
-will recover a matrix only with larger variances and take away the data with small variances to avoid redundant data.

## inexact Augmented Lagrange Multipliers Method
-the method the researchers used to recover a low-rank matrix, A, from a corrupted data matrix D = A + E, where "some entries of the additive errors E may be arbitrarily large".
-it's the higher dimension version of "take the derivative and set it equal to 0" as a parameter to solve.

## Pros
-can be used to recover an UNKNOWN fraction of its entries being arbitrarily corrupted.
-the ALM method is considerably faster than previously known methods.
-higher precision
-less storage

## Cons
-only recovers a low-rank matrix. 

## Alternative Methods
### Accelerated proxximal gradient method
-it's another optimization method
-but it takes more iterations because it looks at the rank of the matrix- will have a large rank (non-zero rows) if the matrix has large dimensions.

### Factor Analysis
-multiple observed variables have similar patterns of response.
-calculates eigenvalue - how much of the variance of the observed variables a factor explains.

We don't use this because there aren't multiple distinct factors- we have all electodes with voltages.