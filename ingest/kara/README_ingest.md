## Using Kara's Data:

1. Have [FieldTrip](http://www.fieldtriptoolbox.org/) downloaded to your comp and the path saved in the MATLAB path variable. If for repeatability sake we all want to use the same version, I'm using 20170207
2. Grab some of the data located in cortex at /braindrive/data/kara_eeg/, save to some location on your comp
3. Preprocess from the command line
	1. Start the command line
	2. Enter the ingest folder with cd C:/.../orange-panda/ingest
	3. Run the following: C:/path/to/matlab.exe -r eWMT_preprocess_alt.m 'path/to/.cnt/file'
4. Output file should be saved to ../preprocessed/ALL.mat. The data is located in:
	1. ft_data object
	2. trial object
	3. each cell in the trial object is the data for a different trial
