function eWMT_preprocess(CNT)

% this fxn runs basic data reading and preprocessing of EEG data for WMT study. 
% run this fxn from where raw data are stored. 
% previously: input e.g. eWMT_preprocess('01','AV_073113.cnt')
% now: input e.g. eWMT_preprocess('path/to/AV_073113.cnt')
% this is because subject ID no longer relevant because NOT currently
% adding behavioral data
% follow this w eWMT_do_ICA.m

warning off

cfg = [];
cfg.dataset = CNT;

cfg.hpfilter                = 'no';
cfg.hpfreq                  = .5;
cfg.dftfilter               = 'no';
cfg.dftfreq                 = [60 120 180];
cfg.continuous              = 'yes';
cfg.trialdef.prestim        = 2; % pre-trial data (often used for baseline correction, later in analysis)
cfg.trialdef.poststim       = 5.5; % length of a trial in seconds
cfg.trialdef.trigchannel    = '1'; % onset of fixation (beg of trial is marked with a '1' trigger
cfg.trialfun                = 'eWMT_trialfun'; 
cfg 						= ft_definetrial(cfg);
cfg.channel                 = 1:47;
cfg.refchannel              = 'all';
cfg.layout                  = 'DUKE47_2.mat'; % 47 electrode equidistant array
ft_data                     = ft_preprocessing(cfg);

%% Use below if there are junk data in .cnt from restarting task.
%  cfg.trials = [1:384];
%  ft_data2 = ft_preprocessing(cfg, ft_data);
% 
% cfg.trials = [450:513];
% ft_data3 = ft_preprocessing(cfg, ft_data);
% 
% cfg = [];
% ft_data = ft_appenddata(cfg, ft_data2, ft_data3);
 

% need to add behav data (can turn this off if you don't want to add behavioral data to EEG data)
%load(['../behav/ID_' subID 'Performance.mat']);
%ft_data.trialinfo = master;

!mkdir -p ../preprocessed
cd ../preprocessed/

save('ALL.mat',  'ft_data');

% eWMT_do_ICA next
