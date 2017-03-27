function [trl, event] = eWMT_trialfun(cfg)

% read the header information and the events from the data
hdr   = ft_read_header(cfg.dataset);
event = ft_read_event(cfg.dataset);

% search for trigger events
for i = 1:length(event)
    yn = event(i).value == str2double(cfg.trialdef.trigchannel);
    match(i) = yn(1);
end
sample = [event(find(match)).sample];


% determine the number of samples before and after the trigger
pretrig  = -cfg.trialdef.prestim  * hdr.Fs;
posttrig =  cfg.trialdef.poststim * hdr.Fs;

trl = [];

for j = 1:length(sample);
    trlbegin = sample(j) + pretrig; % show output here to see that is trial 1, run 1
    trlend   = sample(j) + posttrig;
    offset   = pretrig;
  if trlbegin > 0 % kb added on 11/11/2013
    newtrl   = [trlbegin trlend offset];
    trl      = [trl; newtrl]; 
  end %kb added
end

