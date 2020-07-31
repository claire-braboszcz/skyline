#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 10:43:02 2020

@author: claire
"""


import argparse
import mne
from mne.preprocessing import read_ica
from config import (fname, erp_bandpass_fmin, erp_bandpass_fmax, 
                    events_dict, 
                    sfreq,
                    tmin_gng, tmax_gng, event_dict_gng,
                    screen_offset,
                    reject_criteria, 
                    flat_criteria, 
                    baseline_gng, 
                    n_jobs)

import pandas as pd


# Be verbose
mne.set_log_level('INFO')


# Handle command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('subject', metavar='subj', help='The subject to process')
parser.add_argument('session', metavar='sess', help='The session to process')

args = parser.parse_args()
subj= args.subject
sess= args.session


print('Processing subject:', subj, 'session:', sess)


# get the events from raw brainvision files

raw_bv = mne.io.read_raw_brainvision(fname.raw(
                                   subject='sub-'+ str(subj), 
                                   session='ses-'+str(sess)), preload=True)


raw_bv.resample(sfreq=sfreq)


events,_ = mne.events_from_annotations(raw_bv)

events2=events.copy()


events2[:, 0] += int(round(screen_offset * raw_bv.info['sfreq']))

# Construct a raw object that will load the highpass-filtered data.
raw = mne.io.read_raw_fif(
    fname.filt_erp(subject='sub-'+ str(subj), 
                   session='ses-'+str(sess), 
                   fmin=erp_bandpass_fmin, 
                   fmax=erp_bandpass_fmax),
    preload=True)


raw.resample(sfreq=sfreq)


# load ica weights
print('Load ICA weights')

ica = read_ica(fname.ica(subject='sub-'+ str(subj), session='ses-'+str(sess)))




# Go=NoGo Task
print('Load trials metadata')

metadata = pd.read_csv(fname.metadata_gng(subject='sub-'+ str(subj), session='ses-'+str(sess)))


print('Epoch the data - go-nogo')
epochs_gng = mne.Epochs(raw, events, event_dict_gng, tmin_gng, tmax_gng, baseline=baseline_gng, preload=True)

# add metadata to epochs object
epochs_gng.metadata = metadata

print('Interpolating bad channels')
epochs_gng.interpolate_bads()

# Save evoked plot to the report
#with mne.open_report(fname.report(subject='sub-'+ str(subj), session='ses-'+str(sess))) as report:
#    report.add_figs_to_section(
#        [epochs_gng.average().plot(show=False)],
#        captions= 'Evoked without ICA - Go-Nogo',
#        section=' Go-Nogo Evoked',
#        replace=True
#    )
##    report.save(fname.report_html(subject='sub-'+ str(subj), session='ses-'+str(sess)), overwrite=True,
 #               open_browser=False)


# Now apply ICA weights and drop eye movements ICA

ica.apply(epochs_gng)

# Drop epochs with too large signal (muscles artefacts) and drop flat electrodes

epochs_gng.drop_bad(reject=reject_criteria, flat=flat_criteria) 

print('  Dropped %0.1f%% of epochs' % (epochs_gng.drop_log_stats(),))


# save epochs files 
print('Saving file')
epochs_gng.save(fname.epochs_gng(subject='sub-'+ str(subj), session='ses-'+str(sess)), overwrite = True)

# Save evoked plot to the report
#with mne.open_report(fname.report(subject='sub-'+ str(subj), session='ses-'+str(sess))) as report:
#    report.add_figs_to_section(
#        [epochs_gng.average().plot(show=False)],
#        captions= 'Evoked with ICA - Go-Nogo',
#        section='Go-Nogo Evoked',
#        replace=True
#    )
#    
#  
#      
#    report.add_figs_to_section(
#        [epochs_gng.plot_drop_log(show=False)],
#        captions= 'Events Drop Log - Go-Nogo',
#        section='Go-Nogo Evoked',
#        replace=True
#    )
    
    
#    report.save(fname.report_html(subject='sub-'+ str(subj), session='ses-'+str(sess)), overwrite=True,
 #               open_browser=False)
#

