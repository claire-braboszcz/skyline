#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 18:14:07 2020

@author: claire
"""

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
                    events_dict, tmin_gng, tmax_gng , event_dict_gng,
                    ylim, n_jobs)

import numpy as np
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


print('Compute ERPs Go NoGo', 'Processing subject:', subj, 'session:', sess)

epochs= mne.read_epochs(fname.epochs_gng(subject='sub-'+ str(subj), session='ses-'+str(sess)), preload= True)


# first now that we have removed all bad channels,  re-reference to average reference
epochs.set_eeg_reference(ref_channels='average', projection=False)

# create evoked object for each type of trials: go health warning/ go smoking cue/
# no go health warning/ no go smoking cue
# !! select only trials with correct response

# Correct No-go on Smoking cue
evoked_nogo_smok=epochs['filename.str.startswith("SmoC") and type.str.startswith("nogo") and accuracy.str.startswith("correct")'].average()
evoked_nogo_smok.comment='nogo-smoking cue'

# Correct No-go on health warning
evoked_nogo_hw=epochs['filename.str.startswith("HW") and type.str.startswith("nogo") and accuracy.str.startswith("correct")'].average()
evoked_nogo_hw.comment='nogo-hw'

# Correct Go on Smoking cue
evoked_go_smok=epochs['filename.str.startswith("SmoC") and type.str.startswith("go") and accuracy.str.startswith("correct")'].average()
evoked_go_smok.comment='go-smoking cue'

# Correct Go on health warning
evoked_go_hw=epochs['filename.str.startswith("HW") and type.str.startswith("go") and accuracy.str.startswith("correct")'].average()
evoked_go_hw.comment='go-hw'



topo_times = np.arange(0.150, 0.300, 0.500)


# Save evoked plot to the report
with mne.open_report(fname.report(subject='sub-'+ str(subj), session='ses-'+str(sess))) as report:
    report.add_figs_to_section(
        [evoked_nogo_smok.plot(spatial_colors=True, gfp=True,
               show=False)],
        captions= 'Nogo Smoking cue' ,
        section='Go-Nogo Evoked',
        replace=True
    )

    report.add_figs_to_section(
        [evoked_nogo_hw.plot(spatial_colors=True, gfp=True,
               show=False)],
        captions= 'Nogo Health Warning' ,
        section='Go-Nogo Evoked',
        replace=True
    )
    
    report.add_figs_to_section(
        [evoked_go_smok.plot(spatial_colors=True, gfp=True,
               show=False)],
        captions= 'Go Smoking Cue ',
        section='Go-Nogo Evoked',
        replace=True
    )

    report.add_figs_to_section(
        [evoked_go_hw.plot(spatial_colors=True, gfp=True,
               show=False)],
        captions= 'Go Health Warning' ,
        section='Go-Nogo Evoked',
        replace=True
    )

       
    report.add_figs_to_section(
        [evoked_nogo_smok.plot_topomap(times=topo_times, show=False)],
        captions= 'Topomaps Nogo Smoking cue  ',
        section='Go-Nogo Evoked',
        replace=True
    )
    
    report.add_figs_to_section(
        [evoked_nogo_hw.plot_topomap(times=topo_times, show=False)],
        captions= 'Topomaps Nogo Health Warning ',
        section='Go-Nogo Evoked',
        replace=True
    )
    
    report.add_figs_to_section(
        [evoked_go_smok.plot_topomap(times=topo_times, show=False)],
        captions= 'Topomaps Go Smoking Cue ',
        section='Go-Nogo Evoked',
        replace=True
        
    )   
    report.add_figs_to_section(
        [evoked_go_hw.plot_topomap(times=topo_times, show=False)],
        captions= 'Topomaps Go Health Warning ',
        section='Go-Nogo Evoked',
        replace=True   
        
     )   
    
    
    report.save(fname.report_html(subject='sub-'+ str(subj), session='ses-'+str(sess)), overwrite=True,
                open_browser=False)




# save all evoked files in 1 .fif file
mne.write_evokeds(fname.evoked_gng(subject='sub-'+ str(subj), 
                                  session='ses-'+str(sess)), 
    [evoked_nogo_smok, evoked_nogo_hw, evoked_go_smok, evoked_go_hw] )





