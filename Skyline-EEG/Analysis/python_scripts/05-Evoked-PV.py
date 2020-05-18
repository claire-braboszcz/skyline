#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 17:53:39 2020

Compute ERPs for the passive viewing task
    • Primary measure: For each participant and session, we will compute two
    LPP measures: 
        the LPP evoked by health warnings will be defined as the 
    difference between the ERP response to health warning and neutral picture 
    (LPPHW) 
    the LPP evoked by negative pictures as the difference between 
    the ERP response to negative pictures and neutral pictures (LPPNEG).
    
    The LPP ERP is defined as a midline centroparietal positive ERP appearing 
    from 300ms after stimulus onset and larger for emotionally salient 
    (pleasant or unpleasant) stimuli compared to neutral ones


@author: claire
"""



import argparse
import mne
from mne.preprocessing import read_ica
from config import (fname, erp_bandpass_fmin, erp_bandpass_fmax, 
                    events_dict, tmin_pv, tmax_pv , event_dict_pv,
                    ylim, n_jobs)

import numpy as np

# Be verbose
mne.set_log_level('INFO')


# Handle command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('subject', metavar='subj', help='The subject to process')
parser.add_argument('session', metavar='sess', help='The session to process')

args = parser.parse_args()
subj= args.subject
sess= args.session


print('Compute ERPs Passive viewing', 'Processing subject:', subj, 'session:', sess)

epochs= mne.read_epochs(fname.epochs_pv(subject='sub-'+ str(subj), session='ses-'+str(sess)), preload= True)

 # for the participants who were sampled at 1000Hz, we have 2001 data points. 
 # Due to rounding approximations, by *first* resampling at 500Hz, we bring 
 # down the number of data points to 1001, n line with the pariticpants 
 # originally sampled at 500Hz
#epochs.resample(sfreq=500)


#epochs.resample(sfreq=250)

#for e in epochs:
#    assert(e.times.shape[0] == 501)

# first now that we have removed all bad channels,  re-reference to average reference
epochs.set_eeg_reference(ref_channels='average', projection=False)

# create evoked object for each type of pictures: health warning/ neutral/ negative and keep them in the same object

evoked_hw=epochs['hw'].average()
evoked_neg=epochs['neg'].average()
evoked_neut=epochs['neut'].average()


# define contrast for LPP to health warning and LPP to negative pictures

contrast_lpp_hw= mne.combine_evoked([evoked_hw, -evoked_neut], weights='equal')
contrast_lpp_neg= mne.combine_evoked([evoked_neg, -evoked_neut], weights='equal')

contrast_lpp_hw_neg= mne.combine_evoked([contrast_lpp_hw, contrast_lpp_neg], weights=[1, -1])

contrast_lpp_hw.comment= 'hw-neut'
contrast_lpp_neg.comment= 'neg-neut'

topo_times = np.arange(0.05, 0.8, 0.050)


# Save evoked plot to the report
with mne.open_report(fname.report(subject='sub-'+ str(subj), session='ses-'+str(sess))) as report:
    report.add_figs_to_section(
        [evoked_hw.plot(spatial_colors=True, gfp=True,
               show=False)],
        captions= 'Health Warnings' ,
        section='Passive Viewing Evoked',
        replace=True
    )

    report.add_figs_to_section(
        [evoked_neg.plot(spatial_colors=True, gfp=True,
               show=False)],
        captions= 'Negative' ,
        section='Passive Viewing Evoked',
        replace=True
    )
    
    report.add_figs_to_section(
        [evoked_neut.plot(spatial_colors=True, gfp=True,
               show=False)],
        captions= 'Neutral ',
        section='Passive Viewing Evoked',
        replace=True
    )

    report.add_figs_to_section(
        [contrast_lpp_hw.plot(spatial_colors=True, gfp=True,
               show=False)],
        captions= 'Contrast HW - Neut' ,
        section='Passive Viewing Evoked',
        replace=True
    )

    report.add_figs_to_section(
        [contrast_lpp_neg.plot(spatial_colors=True, gfp=True,
               show=False)],
        captions= 'Contrast Neg - Neut ' ,
        section='Passive Viewing Evoked',
        replace=True
    )
    
    report.add_figs_to_section(
        [evoked_hw.plot_topomap(times=topo_times, show=False)],
        captions= 'Topomaps Health warning  ',
        section='Passive Viewing Evoked',
        replace=True
    )
    
    report.add_figs_to_section(
        [evoked_neg.plot_topomap(times=topo_times, show=False)],
        captions= 'Topomaps Negatives ',
        section='Passive Viewing Evoked',
        replace=True
    )
    
    report.add_figs_to_section(
        [evoked_neut.plot_topomap(times=topo_times, show=False)],
        captions= 'Topomaps Neutrals ',
        section='Passive Viewing Evoked',
        replace=True
        
    )   
    report.add_figs_to_section(
        [contrast_lpp_hw.plot_topomap(times=topo_times, show=False)],
        captions= 'Topomaps HW-Neut ',
        section='Passive Viewing Evoked',
        replace=True   
        
     )   
    report.add_figs_to_section(
        [contrast_lpp_neg.plot_topomap(times=topo_times, show=False)],
        captions= 'Topomaps Neg-Neut ',
        section='Passive Viewing Evoked',
        replace=True      
    )
    
    
    report.save(fname.report_html(subject='sub-'+ str(subj), session='ses-'+str(sess)), overwrite=True,
                open_browser=False)

#fdgdfg


# save all evoked files in 1 .fif file
mne.write_evokeds(fname.evoked_pv(subject='sub-'+ str(subj), 
                                  session='ses-'+str(sess)), 
    [evoked_hw, evoked_neg, evoked_neut, 
     contrast_lpp_hw, contrast_lpp_neg] )





