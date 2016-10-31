# Team Orange Panda
## EEG Pipeline

## Adding an analysis or pre-processing routine:
* The input of the function should be a (n, c, p) shaped ndarray (numpy array
  * n is the number of timesteps (~170k for eeg)
  * c is the number of channels (111)
  * p is the number of patients (you can just test with one)
* The output of the function is  a tuple (d, o, ...)
  * d is the updated ndarray (e.g. if you put through interpolation, d is the original data array with the interpolated columns filled in)
  * o is some kind of output text (what happened? e.g. for bad electrode detect, maybe say 'detected 10 bad electrodes)... This return is not currently used but likely will be in the future.
* Documentation should be added with a docstring right underneath the function definition. for an example, look in utils/example.py... just copy paste that one then change it to match what your function does.
* Plotting functions can be added for your routine in utils/meda.py...
  * make a function which takes as argument a pandas dataframe (and any additional arguments). This should return a plotly figure object. Look at the many functions for examples of using cufflinks. Cufflinks is a productivity tool for plotly which lets you use a bunch of basic plotting functionality with one line of code. Just be sure to add the `asFigure = True` argument. Once this is finished, go to the `full_report` function and wrap your function in the `plotly_hack` and add it to the html string (it should be clear how to do this from the rest of the function). Also, make sure to test with both small data (stocks example) and big data (a full EEG dataset). Sometimes functions will work on small data but are too inefficient to run on big data.

* read the docs - [https://neurodatadesign.github.io/orange-panda]
