#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 11:03:17 2020

Run ICA to remove eye movement artefacts
Save ICA solution 

@author: claire
"""

import argparse
import numpy as np
import mne
from mne.preprocessing import ICA, create_ecg_epochs, create_eog_epochs
from config import (fname, ica_bandpass_fmin, ica_bandpass_fmax, 
                    n_eog_components, n_jobs)


# Be verbose
mne.set_log_level('INFO')


# Handle command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('subject', metavar='subj', help='The subject to process')
parser.add_argument('session', metavar='sess', help='The session to process')

args = parser.parse_args()
subj= args.subject
sess= args.session


print('Run ICA - Processing subject:', subj, 'session:', sess)


# Construct a raw object that will load the highpass-filtered data.
raw = mne.io.read_raw_fif(
    fname.filt_ica(subject='sub-'+ str(subj), 
                   session='ses-'+str(sess), 
                   fmin=ica_bandpass_fmin, 
                   fmax=ica_bandpass_fmax),
    preload=False)


print('Fitting ICA')

ica = ICA(method='fastica', n_components=15, random_state=97)

ica.fit(raw)


# Find onsets of blinks based on Fp1 activity. Create epochs around them
eog_epochs = create_eog_epochs(raw,ch_name='Fp1', tmin=-.5, tmax=.5, preload=False)


#
# Find ICA components that correlate with eye blinks
eog_epochs.load_data()
eog_epochs.apply_baseline((None, None))
eog_inds, eog_scores = ica.find_bads_eog(eog_epochs, 
                                         ch_name='Fp1', 
                                         threshold=2)

ica.exclude =eog_inds
print('    Found %d EOG indices' % (len(eog_inds),))


# create figure with EOG activity
eog_evoked = eog_epochs.average()
eog_evoked.apply_baseline(baseline=(None, -0.2))


# Save the ICA decomposition
ica.save(fname.ica(subject='sub-'+ str(subj), session='ses-'+str(sess)))


# Save plots of the ICA components to the report

with mne.open_report(fname.report(subject='sub-'+ str(subj), session='ses-'+str(sess))) as report:
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
    report.save(fname.report_html(subject='sub-'+ str(subj), session='ses-'+str(sess)), overwrite=True,
                open_browser=False)
