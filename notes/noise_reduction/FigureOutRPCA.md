Goal: Robust PCA tries to fit the model using the majority fo the data such that outliers are eliminated and the analysis of data can be performed (since PCA does not perform well towards outliers and will not reduce noise correctly).

Breakdown point of scale estimator S - smallest fraction of observation to be contaminated such that S approcahes infinity or zero.

-Minimum Covariance Determinant estimator - robust, high-breakdown point estimator of covariance. Find the empiricial covariance matrix with the smallest determinant, thus yield a "pure" subset of observations from which to compute standards estimates of location and covariance.  Correction is needed, however, because estimates were learned from only a portion of the initial data.



Useful links
[Summarizing PCA](http://sebastianraschka.com/Articles/2014_pca_step_by_step.html)
[PCA with Outliers and Missing Data](http://www.math.umn.edu/~lerman/Meetings/SIAM2012_Sujay.pdf)

Pseudocode for PCA:
1. Compute the mean for every dimension of the whole data set
2. Covariance matrix for the whole data set
3. Compute eigenvectors and eigenvalues
4. Sort the eigenvectors by decreasing eigenvalues and choose k eigenvectors with the largest eigenvalues to form a n x k dimension matrix W (where every columne is an eigenvector)
5. Use this matrix to transform the samples onto the new subspace. y = w^T * x 