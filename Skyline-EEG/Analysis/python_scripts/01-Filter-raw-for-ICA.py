#!/usr/bin/env python
# coding: utf-8




"""
Perform bandpass filtering to prep data for ICA - another filter is used for data pre-epochs

"""
    
    
import mne
import os
from mne_bids import make_bids_folders, make_bids_basename

get_ipython().magic('matplotlib qt')



print('Processing subject:', subj, 'session:', sess)

# Keep track of PSD plots before and after filtering
figs_before = []
figs_after = []


preproc_path_folder =  make_bids_folders(subject = str(subj), session= str(sess),
                            kind='eeg', bids_root=preproc_root,make_dir=True, overwrite =False)


# load raw data
bids_basename = make_bids_basename(subject=str(subj), session=str(sess))
bids_fname = bids_basename + '_eeg.vhdr'


fname = os.path.join(bids_root, 'sub-%d' %subj,  'ses-%d' %sess, 'eeg', bids_fname)
raw = mne.io.read_raw_brainvision(fname, preload=True)


# high pass filter data for ICA
filt_raw =  raw.copy()
filt_raw.load_data().filter(l_freq=ica_bandpass_fmin, h_freq=ica_bandpass_fmax, l_trans_bandwidth='auto',
        h_trans_bandwidth='auto', filter_length='auto', phase='zero',
        fir_window='hamming', fir_design='firwin', n_jobs=n_jobs)

filt_raw.save(os.path.join( preproc_path_folder,'filter_ica_raw.fif'))

# Make a plot of the PSD before and after filtering
figs_before.append(raw.plot_psd(show=False))
figs_after.append(raw_filt.plot_psd(show=False))#


# Append PDF plots to report
with mne.open_report(fname.report(subject=subject)) as report:
    report.add_slider_to_section(
        figs_before,
        title='PSD before filtering',
        section='Sensor-level',
        replace=True
    )
    report.add_slider_to_section(
        figs_after,
        title='PSD after filtering',
        section='Sensor-level',
        replace=True
    )
    report.save(bids_basename.report_html(subject=subject), overwrite=True,
                open_browser=False)

