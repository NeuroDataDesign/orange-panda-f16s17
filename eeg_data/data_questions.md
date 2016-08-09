Questions for Data Keepers:

1. Some of the full .mat files are missing fields/have empty fields. Have these not been filled yet/will more metadata be added later, or is that intentionally not added because they were defualt fields in the processing (eg for icasphere, icaact, etc)? Is the "x" in xmin and xmax time, or another variable?

2. For the numbered user events (ie the numbers representing user messages, button presses, etc.), is there a legend that connects numbers with a particular prompt for the subject/action from the subject?

3. SurrSupp_Block1 eye tracking data is missing from the CMI_share (note: only for A00051826, need to check others). Some other patients are missing data occasionally throughout. Some include:
    1. A00051826 - missing SurrSupp_Block 1 and video eyetracking data
    2. A00051886 - missing video eyetracking data
    3. A00051955 - missing SurrSupp_Block2 Samples eye tracking data and has a file called A00051955rSupp_Block 1.txt
    4. Additional slight issues across the data. Was this intentional/was the data not measured, or was it missing?

4. A more general question about the subjects and the experiment, when test participants were written as "typically developing", does that mean developing normally (with no condition) or had a slightly developed form of the disease?

5. The order we think the EEG full_xxx.mat files are in is in the attached Excel file. Are we right about which file number corresponds with which paradgim, and is that true for each patient, and is there a reason the tests were run in that order?

6. What is TargOnT (it's an array in multiple of the metadata .mat files from the CMI_share folder)?

7. There are some par. objects left blank in the CMI_share folder .mat files. Were they left like that intentionally?

8. Where does the actual resting eyetracking data end and the visual begin, and will the 2 files be eventually separated?