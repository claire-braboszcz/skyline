#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 14:49:18 2020

@author: claire
"""

import mne
from mne.preprocessing import ICA,  create_eog_epochs
from config import fname

subj = str(753)
session=str(1)

raw=mne.io.read_raw_fif('/home/claire/Documents/STUDY/EEG-Tobacco/Skyline-EEG-BIDS/derivatives/eeg_preprocess/sub-'+subj+'/ses-'+session+'/eeg/sub-'+subj+'_ses-'+session+'_filt_1_40_raw.fif')

ica=mne.preprocessing.read_ica('/home/claire/Documents/STUDY/EEG-Tobacco/Skyline-EEG-BIDS/derivatives/eeg_preprocess/sub-'+subj+'/ses-'+session+'/eeg/sub-'+ subj+'_ses-'+session+'_ica.fif')



raw.plot()



eog_epochs = create_eog_epochs(raw,ch_name='Fp1', tmin=-.5, tmax=.5, 
                               preload= True)


eog_epochs.apply_baseline((None, None))
eog_inds, eog_scores = ica.find_bads_eog(eog_epochs, ch_name='Fp1', 
                                         threshold=2)


eog_inds=[0,1, 4]

ica.plot_properties(raw, picks=eog_inds)

eog_evoked = eog_epochs.average()
eog_evoked.apply_baseline(baseline=(None, -0.2))


ica.exclude =eog_inds

ica.plot_sources(eog_evoked)


# save modif if needed 

ica.save(fname.ica(subject='sub-'+ subj, session='ses-'+session))

# Save plots of the ICA components to the report

with mne.open_report(fname.report(subject='sub-'+ subj, session='ses-'+session)) as report:
    report.add_figs_to_section(
        ica.plot_components(show=False),
        captions='ICA components',
        section='Sensor-level',
        replace=True
    )
    report.add_figs_to_section(
        ica.plot_scores(eog_scores, show=False),
        captions='Component correlation with EOG',
        section='Sensor-level',
        replace=True
        
     )   
    report.add_figs_to_section(
        ica.plot_sources(eog_evoked, show=False),
        captions='EOG component activity removed - on averaged EOG epoch',
        section='Sensor-level',
        replace=True
    )
    report.save(fname.report_html(subject='sub-'+ subj, session='ses-'+session), overwrite=True,
                open_browser=False)






#### check for bad channels
    
subj=148
sess=2
raw = mne.io.read_raw_fif(
    fname.filt_erp(subject='sub-'+ str(subj), 
                   session='ses-'+str(sess), 
                   fmin=erp_bandpass_fmin, 
                   fmax=erp_bandpass_fmax),
    preload=True)

raw.plot(n_channels=32)

f=fname.filt_erp(subject='sub-'+ str(subj), session='ses-'+str(sess), fmin=erp_bandpass_fmin, fmax=erp_bandpass_fmax)

raw.save(f, overwrite = True)



filt=raw.filter(l_freq=0.01, h_freq=40, l_trans_bandwidth='auto',
h_trans_bandwidth='auto', filter_length='auto', phase='zero',
fir_window='hamming', fir_design='firwin', n_jobs=n_jobs)

epochs_pv = mne.Epochs(filt, events2, event_dict_pv, tmin_pv, tmax_pv, baseline=baseline_pv,  preload=True)


