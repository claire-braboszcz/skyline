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
                    events_dict, tmin_pv, tmax_pv , event_dict_pv, screen_offset, reject_criteria, 
                    flat_criteria, baseline_pv,  n_jobs)





# Be verbose
mne.set_log_level('INFO')


# Handle command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('subject', metavar='subj', help='The subject to process')
parser.add_argument('session', metavar='sess', help='The session to process')

args = parser.parse_args()
subj= args.subject
sess= args.session


print('Epochs Passive viewing', 'Processing subject:', subj, 'session:', sess)


# get the events from raw brainvision files

raw_bv = mne.io.read_raw_brainvision(fname.raw(
                                   subject='sub-'+ str(subj), 
                                   session='ses-'+str(sess)), preload=True)

raw_bv.resample(sfreq=250)


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

raw.resample(sfreq=250)

# load ica weights
print('Load ICA weights')

ica= read_ica(fname.ica(subject='sub-'+ str(subj), session='ses-'+str(sess)))


# Passive viewing Task
print('Epoch the data - passive viewing')


epochs_pv = mne.Epochs(raw, events2, event_dict_pv, tmin_pv, tmax_pv, baseline=baseline_pv,  preload=True)


print('Interpolating bad channels')
epochs_pv.interpolate_bads()

# Save evoked plot to the report
with mne.open_report(fname.report(subject='sub-'+ str(subj), session='ses-'+str(sess))) as report:
    report.add_figs_to_section(
        [epochs_pv.average().plot(show=False)],
        captions= 'Evoked without ICA - Passive Viewing',
        section='Passive Viewing Evoked',
        replace=True
    )
    report.save(fname.report_html(subject='sub-'+ str(subj), session='ses-'+str(sess)), overwrite=True,
                open_browser=False)


# Now apply ICA weights and drop eye movements ICA

ica.apply(epochs_pv)

# Drop epochs with too large signal (muscles artefacts) and drop flat electrodes

epochs_pv.drop_bad(reject=reject_criteria, flat=flat_criteria) 

print('  Dropped %0.1f%% of epochs' % (epochs_pv.drop_log_stats(),))


# save epochs files 
print('Saving file')
epochs_pv.save(fname.epochs_pv(subject='sub-'+ str(subj), session='ses-'+str(sess)), overwrite = True)

# Save evoked plot to the report
with mne.open_report(fname.report(subject='sub-'+ str(subj), session='ses-'+str(sess))) as report:
    report.add_figs_to_section(
        [epochs_pv.average().plot(show=False)],
        captions= 'Evoked with ICA - Passive Viewing',
        section='Passive Viewing Evoked',
        replace=True
    )
    
  
      
    report.add_figs_to_section(
        [epochs_pv.plot_drop_log(show=False)],
        captions= 'Events Drop Log - Passive Viewing',
        section='Passive Viewing Evoked',
        replace=True
    )
    
    
    report.save(fname.report_html(subject='sub-'+ str(subj), session='ses-'+str(sess)), overwrite=True,
                open_browser=False)


