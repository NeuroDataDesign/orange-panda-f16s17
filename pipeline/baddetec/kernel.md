## Kernel Distribution:

- Nonparametric representation of prob density funciton of random var
- **Use kernel when** parametric function will not properly describe the data
	- Or not assuming stuff about data
- **Defined by:**
	- Smoothing function
	- Bandwith value that controls smoothness of density curve


#### Kernel Density Estimator
- Estimated probability density function of random var
- [**Equation here**](https://www.mathworks.com/help/stats/kernel-distribution.html)

#### Kernel Smoothing Function
- Kernel is called a kernel because it's a small base that's used to determine a distribution at each point
- Represents distribution of weights that sum to original point
- Define shape of curve
- Build function using sample data
- Sum component smoothing functions for each data value to produce a smooth continuous probability curve
- **Smoothing functions can be continuous shapes including:**
	- normal
	- epanechnikov
	- box
	- triangle
	- Varies slightly, not sure to what extent

#### Bandwith
- Bandwith value controls smoothness of resulting probability density curve
	- Smaller = less smooth, more peaks
	- Larger = closer to kernel function
- Selection:
	- **Reference Rules:**
		- Estimated from theoretical forms based on assumptions about distribution
		- From what I understand, takes away from some advantage of KDE by assuming (?)
	-  **Cross-Validation:**
		- Model is fit a part of the data
		- Tested against another by a decided metric
		- "Empirical approach to model parameter selection = very flexible"
		- Note: All this from 1 source, potential bias

#### Pseudo:
[Equation Here](http://rafalab.github.io/pages/649/section-06.pdf)
- N(x0) = neighborhood of points around x0 (set of all points)
- h = bandwith
- Kh = kernel function in terms of h

## Kernel Density in Python:
- [2013 comparison of different methods and advantages/disadvantages](https://jakevdp.github.io/blog/2013/12/01/kernel-density-estimation/)
- From above blog:
	- **SCI.PY HAS LIMITATIONS ON WHAT IT CAN DO. IT ONLY CAN USE A GAUSSIAN KERNEL AND REFERENCE RULES FOR BANDWITH SELECTION.**
	- ***StatsModels*** does bandwith selection via leave-one-out cross-validation, and can handle more kernels with similar computational efficiency.

### References
- [Basic explanation via MATLAB functionality](http://scikit-learn.org/stable/developers/contributing.html#documentation)
- [More in depth explanation, including bandwith selection methods](http://research.cs.tamu.edu/prism/lectures/pr/pr_l7.pdf)

### Extra Notes
- Seems like the original preprocessing pipeline used a histogram method (constructing a histogram manually via data and bins) to predict probability. While also unparameterized has same issues that Jovo brought up, large gains in space with increased dimensions, etc