## Cross Validation

Cross validation is a model validation technique.
- It assesses results of statistical analysis and how will generalize to an independent data set
- Finds the accuracy of a predictive model

### Process
1. Given known data (training dataset)
2. Given unknown data (testing dataset)
3. Test model in training phases to optimize model but limit overfitting

To apply this technique w/ only known data:
- Partition dataset, perform analysis on 1 test subset and validate other subsets

**Exhaustive vs Nonexhaustive**
- Exhaustive = learn and test on all possible ways to divide original sample into training + validation

k-fold non-exhaustive:
k-equal sized sample, 1 is training set, other k-1 are for testing. Try each sample as training
Advantages:
- each data point helps test once
- each used as a test k-1 times

leave-one-out exhaustive:
k-fold but set k to the number of observations in data set.

### Cross Validation for Time Series:
- More difficult, as all partitioned test data is somehow linked/has dependeny on test values
- Find MSE of errors between forecasted timeset values and actual
- All k sets are supersets of their corresponding k-1 sets

#### References:
- [Cross Validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics)#Purpose_of_cross-validation)
- [Sci Kit (implementation I'm using)](http://scikit-learn.org/stable/modules/cross_validation.html)
- [Carnegie Mellon Basic Overview](https://www.cs.cmu.edu/~schneide/tut5/node42.html)
- [Blog on Statistician](http://robjhyndman.com/hyndsight/crossvalidation/)
- [**In depth look, project Euclid Paper**](http://projecteuclid.org/download/pdfview_1/euclid.ssu/1268143839)
- [TAMU Lecture Slides (not sure university but well explained)](http://research.cs.tamu.edu/prism/lectures/iss/iss_l13.pdf)


