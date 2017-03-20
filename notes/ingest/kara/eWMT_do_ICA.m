
% This script has multiple preprocessing steps that need to be run
% individually by highlighting the section and "Evaluating the selection"
load ALL.mat

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% STEP 1: take note of potentially bad channels
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cfg          = [];
cfg.method   = 'trial'; % other options = 'trial' 'channel' or 'summary'
cfg.eegscale = 1;
cfg.latency     = [0  5.5]; % whole trial
ft_data2        = ft_rejectvisual(cfg,ft_data); % just go through and see 
% which channels are potentially bad and remove any that are problematic

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% STEP 2: ICA to identify blinks and eye movements
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% run ICA
cfg = []; 
cfg.method  = 'runica';
cfg.numcomponent = 40;
datacomp = ft_componentanalysis(cfg, ft_data2); % this takes ~20 minutes
 
datacomp.dimord = 'chan_time';

save companalysis datacomp

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% STEP 3: visualize ICA components
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Take note on which components look like blink and/or eye movements
cfg = [];
cfg.layout = 'DUKE47_2.mat';
cfg.component = [1:20];
cfg.colormap = 'jet';
ft_topoplotIC(cfg, datacomp)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% STEP 4: visualize artifact components.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Identify components that represents blink by looking at real trial data
cfg = [];
cfg.channel = {datacomp.label{1} datacomp.label{2} datacomp.label{3} datacomp.label{8} datacomp.label{20}};
cfg.layout = 'DUKE47_2.mat'; 
cfg.viewmode = 'vertical';
artf = ft_databrowser(cfg, datacomp);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% STEP 5: remove blink component (usually the 1st or 2nd component)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cfg=[];
cfg.component = [2 3]; % note blink comp can be different by participant and more than one component can be blinks
dummy = ft_rejectcomponent(cfg, datacomp);
close all

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% STEP 6: visualize EOG channels.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Go though trials and click on segments of trials that contain lateral eye movements
sacc = 25;
cfg = [];
cfg.lpfilter                = 'yes';
cfg.lpfreq                  = 30;
HEG                        = ft_preprocessing(cfg, dummy);
for i=1:length(HEG.trial)
    HEG.trial{i}(1,:) = HEG.trial{i}(2,:) - HEG.trial{i}(44,:); % overwrite chan 1 w/ HEOG. 2 = LE1, 44 = RE1
end

cfg = [];
cfg.channel = {'LE1','RE1'}; % channels above eyes
cfg.layout = 'DUKE47_2.mat';
cfg.viewmode = 'vertical';
cfg.zscale = [-sacc*1.5,sacc*1.5];
artf2 = ft_databrowser(cfg, HEG);
marked = artf2.artfctdef.visual.artifact;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% STEP 7: remove trials with lateral eye movements marked in Step 6
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cfg=[];
cfg.artfctdef.reject = 'complete'; % this rejects complete trials, use 'partial' if you want to do partial artifact rejection
cfg.artfctdef.visual.artifact = artf2.artfctdef.visual.artifact;
dummy2 = ft_rejectartifact(cfg,dummy);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% STEP 8: remove any trials with spikes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cfg          = [];
cfg.method   = 'trial';
cfg.megscale = 1;
cfg.latency     = [0 5.5];
ft_data        = ft_rejectvisual(cfg,dummy2);

save data_clean ft_data dummy marked dummy2
clear all


% run eWMT_trialsort to sort into diff conditions
