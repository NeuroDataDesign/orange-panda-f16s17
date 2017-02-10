## Nitin’s Question: How did they choose bad electrodes?
-outliers how many standard deviation away from “certain measures” (i.e. frequency and kurtosis)
-EEGLAB functions were implemented in Python by us
-they “visually inspect” as a safety net. A manual step.
-how many do they actually manually check? 50/50. Half by algorithm and half manual.
-really depends on “data quality”
-can build a classifier and pass it on other subjects

To do: try to download data (via AWS or website)

## Nitin's question: Resting data set – looked at correlation between different electrodes, pair clustering as well. Why is it not recorded to auto bad chans?
Clean electrodes are much thinner
Nicholas will take a look at the electrodes. But it is also “subjective impression”
There’s an extra data set: the “impedence” of each electrode.
-Electrodes with high impedence were given a fluid to be lowered.

To do: IMP for impedence (check for in AWS), check out Electrical Impedence Tomography

## Ryan’s Question: Why do we use interpolation?
-Nicholas used spherical splines – is this better than inverse distance weighting? If so, why? Because benchmarking did not show significant difference.
-he thinks interpolation methods are going to be very similar.
-the skulls are covered very well. But there are subjects with only 32 electrodes.
-interpolation works better with less electrodes.
-we can also take away electrodes – but we also need to use the exact electrode location.

To do: Look for data with only 32 electrodes in it or synthesize data by removing electrodes.

-send Nicholas an email regarding everything we need.
