#!/usr/bin/env python
# coding: utf-8




"""
Perform bandpass filtering to prep data for ICA - another filter is used for data pre-epochs

"""
    
    
import mne
import argparse
from config import (fname, ica_bandpass_fmin, ica_bandpass_fmax, n_jobs)


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

# Keep track of PSD plots before and after filtering
figs_before = []
figs_after = []



raw = mne.io.read_raw_brainvision(fname.raw(
                                   subject='sub-'+ str(subj), 
                                   session='ses-'+str(sess)), preload=True)

# add channel loc info

montage= mne.channels.read_custom_montage(fname.bids_root + '/EEG_montage/AC-64.bvef')
raw.set_montage(montage)
        



# high pass filter data for ICA
filt_raw =  raw.copy()
filt_raw.load_data().filter(l_freq=ica_bandpass_fmin, h_freq=ica_bandpass_fmax, l_trans_bandwidth='auto',
        h_trans_bandwidth='auto', filter_length='auto', phase='zero',
        fir_window='hamming', fir_design='firwin', n_jobs=n_jobs)


f=fname.filt_ica(subject='sub-'+ str(subj), session='ses-'+str(sess), fmin=ica_bandpass_fmin, fmax=ica_bandpass_fmax)

filt_raw.save(f, overwrite = True)

# Make a plot of the PSD before and after filtering
figs_before.append(raw.plot_psd(show=False))
figs_after.append(filt_raw.plot_psd(show=False))#


# Append PDF plots to report
with mne.open_report(fname.report(subject='sub-'+ str(subj), session='ses-'+str(sess))) as report:
    report.add_figs_to_section(
        figs_before,
        captions='PSD before filtering',
        section='Sensor-level',
        replace=True
    )
    report.add_figs_to_section(
        figs_after,
        captions='PSD after filtering',
        section='Sensor-level',
        replace=True
    )
    report.save(fname.report_html(subject='sub-'+ str(subj), session='ses-'+str(sess)), overwrite=True,
                open_browser=False)

