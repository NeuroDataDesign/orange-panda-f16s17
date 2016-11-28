# Lit References
## A master list of EEG prep/analysis papers which might be useful

### Bad Channel Detection
* http://journal.frontiersin.org/article/10.3389/fninf.2015.00016/full - they are using 4 criterions for bad channels: strong deviations, correlations, high noise and predictability, their github page: https://github.com/VisLab/EEG-Clean-Tools
* http://journal.frontiersin.org/article/10.3389/fnhum.2016.00050/full - this is specifically for ERP data
* http://ieeexplore.ieee.org/document/6945365/ - they assume that you have a "clean" training session and based on that calculate online whether the channels deviate from that "normal" value. their measure is also based on correlations with neighbouring electrodes
* https://github.com/mne-tools/mne-python/blob/master/mne/preprocessing/bads.py bad detect based on z scoring

### Toolboxes
* https://github.com/bbci/wyrm
* https://github.com/mne-tools/mne-python/tree/master/mne. h
* https://github.com/amirrezaw/automagic

### EEG Artifact Detection
* Multiple Artifact Rejection Algorithm http://www.user.tu-berlin.de/irene.winkler/artifacts/MARAtutorial.pdf
  * http://www.user.tu-berlin.de/irene.winkler/artifacts/
* http://www.sciencedirect.com/science/article/pii/S098770531630199X

### Analysis
* https://npepjournal.biomedcentral.com/articles/10.1186/s40810-015-0015-7
