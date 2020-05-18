#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:50:08 2020

Compute group average ERPs and stats for Skyline Passive viewing task
 - get participant conditions
 - create ERPS for session1 and session2

    - Experimental group versus controls difference between test and re-test
    in LPP amplitude in response to health warning stimuli

- compute the difference between INT and CTR at T1 and the difference at T2¨

@author: claire
"""



import argparse
import mne
from mne.channels import find_ch_connectivity, make_1020_channel_selections
from mne.stats import spatio_temporal_cluster_test

from config import (fname,
                    subject_ids, 
                    sessions, 
                    subj_interv, 
                    subj_control, 
                     all_evokeds_interv_1, 
                     all_evokeds_interv_2, 
                     all_evokeds_control_1, 
                     all_evokeds_control_2)
                     
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind


# Be verbose
mne.set_log_level('INFO')


# Handle command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('subject', metavar='subj', help='The subject to process')
parser.add_argument('session', metavar='sess', help='The session to process')

args = parser.parse_args()
subj= args.subject
sess= args.session



print('Compute Group ERPs Passive viewing', 'Processing subject:', subj, 'session:', sess)





#evokeds= mne.read_evokeds(fname.evoked_pv(subject='sub-'+ str(subj), session='ses-'+str(sess)))
# group the evoked data in lists by condition and session

for subj in subject_ids:
    for sess in sessions:
        evokeds= mne.read_evokeds(fname.evoked_pv(subject='sub-'+ str(subj), session='ses-'+str(sess)))

        for idx, evoked in enumerate(evokeds):
            if subj in subj_interv:
                if sess == 1:
                    assert len(evokeds) == len(all_evokeds_interv_1)
                    all_evokeds_interv_1[idx].append(evoked)
                    
                elif sess==2:
                    assert len(evokeds) == len(all_evokeds_interv_2)
                    all_evokeds_interv_2[idx].append(evoked)
                
            elif subj in subj_control:
    
                if sess == 1:
                    assert len(evokeds) == len(all_evokeds_control_1)
                    all_evokeds_control_1[idx].append(evoked)
                
                elif sess==2:
                    assert len(evokeds) == len(all_evokeds_control_2)
                    all_evokeds_control_2[idx].append(evoked)




# create grand average by condition and session across subject

for idx, evokeds in enumerate(all_evokeds_interv_1):
    all_evokeds_interv_1[idx] =  mne.combine_evoked(evokeds, weights='equal')   # Combine subjects

for idx, evokeds in enumerate(all_evokeds_interv_2):
    all_evokeds_interv_2[idx] = mne.combine_evoked(evokeds, weights='equal')  # Combine subjects

for idx, evokeds in enumerate(all_evokeds_control_1):
    all_evokeds_control_1[idx] = mne.combine_evoked(evokeds, 'equal')  # Combine subjects

for idx, evokeds in enumerate(all_evokeds_control_2):
    all_evokeds_control_2[idx] = mne.combine_evoked(evokeds, 'equal')  # Combine subjects



all_evokeds_interv_1[3].plot(spatial_colors=True, gfp=True, window_title = 'Group averaged HW - Interv - sess 1', show=True)
all_evokeds_interv_1[4].plot(spatial_colors=True, gfp=True, window_title = 'Group averaged Neg - Interv - sess 1', show=True)


topo_times = np.arange(0.05, 1, 0.050)

all_evokeds_interv_1[3].plot_topomap(topo_times)
all_evokeds_interv_1[4].plot_topomap(topo_times)

# plot Group Average for each LPP measure

with mne.open_report(fname.group_report) as report:
    report.add_figs_to_section(
        [all_evokeds_interv_1[3].plot_topomap(topo_times, show=False)],
        captions= 'LPP Health Warnings Interv - session 1' ,
        section='Passive Viewing - Group Average ',
        replace=True
    )
    report.add_figs_to_section(
        [all_evokeds_interv_1[4].plot_topomap(topo_times, show=False)],
        captions= 'LPP Negative Interv - session 1' ,
        section='Passive Viewing - Group Average ',
        replace=True
    )

    report.add_figs_to_section(
            [all_evokeds_interv_2[3].plot_topomap(topo_times, show=False)],
            captions= 'LPP Health Warnings Interv - session 2' ,
        section='Passive Viewing - Group Average ',
            replace=True
        )
    report.add_figs_to_section(
            [all_evokeds_interv_2[4].plot_topomap(topo_times, show=False)],
            captions= 'LPP Negative Interv - session 2' ,
        section='Passive Viewing - Group Average ',
            replace=True
        )
    
    report.add_figs_to_section(
        [all_evokeds_control_1[3].plot_topomap(topo_times, show=False)],
        captions= 'LPP Health Warnings Control - session 1' ,
        section='Passive Viewing - Group Average ',
        replace=True
    )
    report.add_figs_to_section(
        [all_evokeds_control_1[4].plot_topomap(topo_times, show=False)],
        captions= 'LPP Negative Control - session 1' ,
        section='Passive Viewing - Group Average ',
        replace=True
    )
    
    report.add_figs_to_section(
            [all_evokeds_control_2[3].plot_topomap(topo_times, show=False)],
            captions= 'LPP Health Warnings Control - session 2' ,
        section='Passive Viewing - Group Average ',
            replace=True
        )
    report.add_figs_to_section(
            [all_evokeds_control_2[4].plot_topomap(topo_times, show=False)],
            captions= 'LPP Negative Control - session 2' ,
        section='Passive Viewing - Group Average ',
            replace=True
        )


# SAVE 











# Compute and plot group average for the difference between control and 
# intervention groups at T1 and T2

# Computing the differences at the individual level then group level    
# T1
hw_lpp_pre_test=mne.combine_evoked([all_evokeds_interv_1[3], 
                                    -all_evokeds_control_1[3]], weights='equal')  

#T2    
hw_lpp_post_test=mne.combine_evoked([all_evokeds_interv_2[3], 
                                    -all_evokeds_control_2[3]], weights='equal')
      
    

# Diff T1-T2
    
hw_lpp_post_pre = mne.combine_evoked([hw_lpp_post_test, 
                                    -hw_lpp_pre_test], weights='equal')    
    
hw_lpp_post_pre.plot(spatial_colors=True, gfp=True)
    
    
mne.viz.plot_compare_evokeds([hw_lpp_pre_test,hw_lpp_post_test,hw_lpp_post_pre]
, picks=['Pz', 'P3', 'P4'] ) 
                              
    
 
    
# computing the differences at the group level    
    
#Computing LPPs HW-NEUT for each group and sessionm
group_hw_lpp_interv_pre=mne.combine_evoked([all_evokeds_interv_1[0], 
                                    -all_evokeds_interv_1[2]], weights='equal')
    
group_hw_lpp_interv_post=mne.combine_evoked([all_evokeds_interv_2[0], 
                                    -all_evokeds_interv_2[2]], weights='equal') 
    
group_hw_lpp_control_pre=mne.combine_evoked([all_evokeds_control_1[0], 
                                    -all_evokeds_control_1[2]], weights='equal')    
    
group_hw_lpp_control_post=mne.combine_evoked([all_evokeds_control_2[0], 
                                    -all_evokeds_control_2[2]], weights='equal')    

    
# computing the difference between LLP in each group for each session    
    
group_hw_lpp_pre = mne.combine_evoked([group_hw_lpp_interv_pre, 
                                    -group_hw_lpp_control_pre], weights='equal')  

group_hw_lpp_post = mne.combine_evoked([group_hw_lpp_interv_post, 
                                    -group_hw_lpp_control_post], weights='equal')  

    
group_hw_lpp_pre_post = mne.combine_evoked([group_hw_lpp_pre, 
                                    -group_hw_lpp_post], weights='equal')     
    

mne.viz.plot_compare_evokeds([group_hw_lpp_pre,group_hw_lpp_post, group_hw_lpp_pre_post ]
, picks=['Pz'] )     
    
#T2    
hw_lpp_post_test=mne.combine_evoked([all_evokeds_interv_2[3], 
                                    -all_evokeds_control_2[3]], weights='equal')
      
    

# Diff T1-T2
    
hw_lpp_post_pre = mne.combine_evoked([hw_lpp_post_test, 
                                    -hw_lpp_pre_test], weights='equal')    
    
hw_lpp_post_pre.plot(spatial_colors=True, gfp=True)
    
    
mne.viz.plot_compare_evokeds([hw_lpp_pre_test,hw_lpp_post_test,hw_lpp_post_pre]
, picks=['Pz', 'P3', 'P4'] )   
    
    
    
    

