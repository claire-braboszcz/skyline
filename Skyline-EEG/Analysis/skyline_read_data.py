#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 14:07:59 2019

@author: claire
"""

import os.path as op
import mne

import numpy as np

filename = '/home/claire/Documents/STUDY/EEG-Tobacco/DATA/s558/EEG/session_02/s558_02.vhdr'

raw = mne.io.read_raw_brainvision(filename, preload=True)

events, _ = mne.events_from_annotations(raw)

mne.write_events(op.join('/home/claire/Documents/STUDY/EEG-Tobacco/DATA/s558/EEG/session_02/', 's558_s02.eve'), events)

montage= mne.channels.read_montage('standard_1020', path = '/home/claire/Applications/mne-python/mne/channels/data/montages/')# change to where you've put you mne python folder

raw.set_montage(montage)

raw.set_eeg_reference(ref_channels='average') # adjust to the kind of reference you want

raw_fir = raw.filter(1.,40, fir_design='firwin')


raw.plot()


# epoching data

#event_id = {'break' :50, 'start_go':55, 'start_pv':66, 'HW':21, 'NEG':25, 'NEUT':22, 'GO':11, 'NOGO':13}

# only get go and nogo trials
event_id = {'GO':11, 'NOGO':13}


tmin = -0.2
tmax = 0.5

epochs = mne.Epochs(raw, events, event_id, tmin, tmax,
                    baseline=(None, 0), reject=None,
                    verbose=False, detrend=0,  preload=True)

epochs.plot()


# compute evoked data

ep_go, ep_nogo = epochs['GO'].average(), epochs['NOGO'].average()


mne.viz.plot_compare_evokeds([ep_go, ep_nogo], picks= 'eeg')


diff_evoked = mne.combine_evoked([ep_go, -ep_nogo ], weights= 'equal')





