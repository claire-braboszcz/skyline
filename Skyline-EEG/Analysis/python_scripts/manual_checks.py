#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 14:49:18 2020

@author: claire
"""

import mne
from mne.preprocessing import ICA,  create_eog_epochs

raw=mne.io.read_raw_fif('sub-148_ses-1_filt_1_40_raw.fif')

ica=mne.preprocessing.read_ica('sub-148_ses-1_ica.fif')

eog_epochs = create_eog_epochs(raw,ch_name='Fp1', tmin=-.5, tmax=.5, 
                               preload= True)


eog_epochs.apply_baseline((None, None))
eog_inds, eog_scores = ica.find_bads_eog(eog_epochs, ch_name='Fp1', 
                                         threshold=2)

ica.plot_properties(raw, picks=eog_inds)

eog_evoked = eog_epochs.average()
eog_evoked.apply_baseline(baseline=(None, -0.2))


ica.exclude =eog_inds


ica.plot_sources(eog_evoked)

