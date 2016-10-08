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


### References
- [Basic explanation via MATLAB functionality](http://scikit-learn.org/stable/developers/contributing.html#documentation)
- [More in depth explanation, including bandwith selection methods](http://research.cs.tamu.edu/prism/lectures/pr/pr_l7.pdf)
x
### Extra Notes
- Seems like the original preprocessing pipeline used a histogram method (constructing a histogram manually via data and bins) to predict probability. While also unparameterized has same issues that Jovo brought up, large gains in space with increased dimensions, etc