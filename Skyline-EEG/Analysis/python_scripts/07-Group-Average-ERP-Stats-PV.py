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
from scipy.stats import ttest_rel # ttest repeated measures




#print('Compute Group ERPs Passive viewing', 'Processing subject:', subj, 'session:', sess)


#evokeds= mne.read_evokeds(fname.evoked_pv(subject='sub-'+ str(subj), session='ses-'+str(sess)))
# group the evoked data in lists by condition and session

for subj in subject_ids:
    for sess in sessions:
        evokeds= mne.read_evokeds(fname.evoked_pv(subject='sub-'+ str(subj), 
                                                  session='ses-'+str(sess)), 
                                    baseline=(None, 0))


        for idx, evoked in enumerate(evokeds):
            evoked.apply_baseline((None, 0))

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

#for idx, evokeds in enumerate(all_evokeds_interv_1):
#    all_evokeds_interv_1[idx] =  mne.combine_evoked(evokeds, weights='equal'
#                        ).apply_baseline((None, 0))   # Combine subjects
#
#for idx, evokeds in enumerate(all_evokeds_interv_2):
#    all_evokeds_interv_2[idx] = mne.combine_evoked(evokeds, weights='equal'
#                        ).apply_baseline((None, 0))   # Combine subjects
#
#for idx, evokeds in enumerate(all_evokeds_control_1):
#    all_evokeds_control_1[idx] = mne.combine_evoked(evokeds, 'equal'
#                         ).apply_baseline((None, 0))   # Combine subjects
#
#for idx, evokeds in enumerate(all_evokeds_control_2):
#    all_evokeds_control_2[idx] = mne.combine_evoked(evokeds, 'equal'
#                         ).apply_baseline((None, 0))   # Combine subjects
##    
#    
#for idx, evokeds in enumerate(all_evokeds_interv_1):
#    all_evokeds_interv_1[idx] =  mne.grand_average(evokeds).apply_baseline((None, 0))   # Combine subjects
#
#for idx, evokeds in enumerate(all_evokeds_interv_2):
#    all_evokeds_interv_2[idx] =  mne.grand_average(evokeds).apply_baseline((None, 0))
#
#for idx, evokeds in enumerate(all_evokeds_control_1):
#    all_evokeds_control_1[idx] =  mne.grand_average(evokeds).apply_baseline((None, 0))
#
#for idx, evokeds in enumerate(all_evokeds_control_2):
#    all_evokeds_control_2[idx] =  mne.grand_average(evokeds).apply_baseline((None, 0))  
    


# add useful comments info

all_evokeds_interv_1[3].comment = 'lpp_hw_int1'    
all_evokeds_interv_2[3].comment = 'lpp_hw_int2'    
all_evokeds_control_1[3].comment = 'lpp_hw_ctr1'    
all_evokeds_control_2[3].comment = 'lpp_hw_ctr2'    


all_evokeds_interv_1[4].comment = 'lpp_neg_int1'    
all_evokeds_interv_2[4].comment = 'lpp_neg_int2'    
all_evokeds_control_1[4].comment = 'lpp_neg_ctr1'    
all_evokeds_control_2[4].comment = 'lpp_neg_ctr2'    




#Experimental group versus controls difference between test and re-test in LPP
# amplitude in response to health warning stimuli


# Computing the differences at the individual level then group level    
# T1
hw_lpp_pre_test=mne.combine_evoked([mne.grand_average(all_evokeds_interv_1[3]), 
                                    mne.grand_average(all_evokeds_control_1[3])],
                                    weights=(-1,1)).apply_baseline((None,0))

#T2    
hw_lpp_post_test=mne.combine_evoked([mne.grand_average(all_evokeds_interv_2[3]), 
                                    mne.grand_average(all_evokeds_control_2[3])],
                                    weights=(-1,1)).apply_baseline((None,0))
   
hw_lpp_pre_test.comment ='lpp diff ctr vs int at T1'

hw_lpp_post_test.comment= 'lpp diff ctr vs int at T2'

hw_lpp_diff =mne.combine_evoked([-hw_lpp_pre_test, hw_lpp_post_test], 'nave')



mne.viz.plot_evoked_topo(test,  background_color='w')


hw_lpp_evokeds={'lpp int t1':all_evokeds_interv_1[3], 
              'lpp int t2':all_evokeds_interv_2[3],
              'lpp ctr t1':all_evokeds_control_1[3], 
              'lpp ctr t2':all_evokeds_control_2[3], 
              #'lpp ctr vs int pre test':  hw_lpp_pre_test, 
              #'lpp ctr vs int post test':  hw_lpp_post_test, 
              #'lpp pre vs post test':  hw_lpp_diff
              }

def custom_func(x):
    return x.max(axis=1)

for combine in ('mean', 'median', 'gfp', custom_func):
    mne.viz.plot_compare_evokeds(
                hw_lpp_evokeds, 
                picks=[ 'Pz', 'P3', 'P4'],
                 combine=combine, 
                 #ci=.95
                ) 




# plot Group Average for each LPP measure

with mne.open_report(fname.group_report) as report:
    
        
          report.add_figs_to_section(
             mne.viz.plot_compare_evokeds(
                 hw_lpp_evokeds, 
                picks=[ 'Pz', 'P3', 'P4'],
                 combine='mean', 
                 ci=.95
                )   ,
            captions= 'HW LPP - mean' ,
            section='HW Passive Viewing - Group Average ',
            replace=True
        )
             
          report.add_figs_to_section(
         mne.viz.plot_compare_evokeds(
            hw_lpp_evokeds, 
            picks=[ 'Pz', 'P3', 'P4'],
             combine='median', 
             ci=.95
            )   ,
        captions= 'HW LPP - median' ,
        section='HW Passive Viewing - Group Average ',
        replace=True
    )
          report.add_figs_to_section(
         mne.viz.plot_compare_evokeds(
             hw_lpp_evokeds, 
            picks=[ 'Pz', 'P3', 'P4'],
             combine='gfp', 
             ci=.95
            )   ,
        captions= 'HW LPP - gfp' ,
        section='HW Passive Viewing - Group Average ',
        replace=True
    )
             

report.save(fname.group_report_html, overwrite=True,
                open_browser=False)

   












# export evoked to pandas dataframe


time_windows = ((.20, .25), (.30, .35), (.40, .45), (.45, .50), (.55, .60))
elecs= ['Pz', 'P3', 'P4'] # centroparietal electrodes (no CPz on montage)
index=['time']


report = "{elec}, time: {tmin}-{tmax} s; t1={t_val1:.3f}, p1={p1:.3f}"#; t2={t_val2:.3f}, p2={p2:.3f}"

print("\nTargeted statistical test results:")

for (tmin, tmax) in time_windows:
    
#    df_lpp_hw_ctr_1=all_evokeds_control_1[3].copy().crop(tmin, tmax).to_data_frame(index=index)[elecs]
#    df_lpp_hw_ctr_2=all_evokeds_control_2[3].copy().crop(tmin, tmax).to_data_frame(index=index)[elecs]
#
#    df_lpp_hw_int_1=all_evokeds_interv_1[3].copy().crop(tmin, tmax).to_data_frame(index=index)[elecs]
#    df_lpp_hw_int_2=all_evokeds_interv_2[3].copy().crop(tmin, tmax).to_data_frame(index=index)[elecs]
         
    df_hw_lpp_pre_test = hw_lpp_pre_test.copy().crop(tmin, tmax).to_data_frame(index=index)[elecs]
    df_hw_lpp_post_test = hw_lpp_post_test.copy().crop(tmin, tmax).to_data_frame(index=index)[elecs]

    
    
    for elec in elecs:
        # extract data
        A= df_hw_lpp_pre_test[elec]
        B= df_hw_lpp_post_test[elec]
        
#        C= df_lpp_hw_int_1[elec]
#        D= df_lpp_hw_int_2[elec]
        
        # cnoduct t test
        t1, p1 = ttest_l(A, B) # control vs int at T1
       # t2, p2= ttest_ind(B, D) # control vs int at T2
        
        # display results
        format_dict = dict(elec=elec, tmin=tmin, tmax=tmax,

                           t_val1=t1, p1=p1) 
        #                   t_val2=t2, p2=p2)
        print(report.format(**format_dict))



hw_lpp_pre_post = mne.combine_evoked([hw_lpp_pre_test, -hw_lpp_post_test], 
                                     weights='equal')

time_unit = dict(time_units = 's')
hw_lpp_pre_post.plot_joint(times=[0.25, 0.30, 0.35, 0.40, 0.45, 0.5], 
                           #picks=['Pz', 'P3', 'P4'],
                           exclude= 'bads',  
                           title= "Diff Int vs Ctr LPP at Pre versus Post test"
                           )


# Create ROIs by checking channel labels
selections = make_1020_channel_selections(evoked.info, midline="Cz")


# Compute and plot group average for the difference between control and 
# intervention groups at T1 and T2

   
mne.viz.plot_compare_evokeds(
        [hw_lpp_pre_test,hw_lpp_post_test,hw_lpp_pre_post], 
        picks=['CP1', 'CP2', 'Pz', 'P3', 'P4'],
        split_legend=True, title="", ci=0.95
        )   
  


hw_lpp_post_pre = mne.combine_evoked([hw_lpp_post_test, 
                                    -hw_lpp_pre_test], weights='equal')   


    

# Diff T1-T2
    
hw_lpp_post_pre = mne.combine_evoked([hw_lpp_post_test, 
                                    -hw_lpp_pre_test], weights='equal')    
    
hw_lpp_post_pre.plot(spatial_colors=True, gfp=True)
    
    
mne.viz.plot_compare_evokeds([hw_lpp_pre_test,hw_lpp_post_test,hw_lpp_post_pre]
, picks=['Pz', 'P3', 'P4'] ) 
                              
    



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
    
    
  

# TFCE

# Calculate statistical thresholds
con = find_ch_connectivity(all_evokeds_interv_1[0][0].info, "eeg")


# Extract data: transpose because the cluster test requires channels to be last
# In this case, inference is done over items. In the same manner, we could
# also conduct the test over, e.g., subjects.
X = [hw_int_t2.get_data().transpose(0, 2, 1),
     hw_ctr_t2.get_data().transpose(0, 2, 1)]
tfce = dict(start=.2, step=.2)



t_obs, clusters, cluster_pv, h0 = spatio_temporal_cluster_test(
    X, tfce, n_permutations=100)  # a more standard number would be 1000+
significant_points = cluster_pv.reshape(t_obs.shape).T < .05
print(str(significant_points.sum()) + " points selected by TFCE ...")


# We need an evoked object to plot the image to be masked
evoked = mne.combine_evoked([hw_int_t1.average(), - hw_ctr_t1.average()],
                            weights='equal')  # calculate difference wave
time_unit = dict(time_unit="s")
evoked.plot_joint(title="HW T2 Int vs. Ctr", ts_args=time_unit,
                  topomap_args=time_unit)  # show difference wave

# Create ROIs by checking channel labels
selections = make_1020_channel_selections(evoked.info, midline="Cz")

# Visualize the results
fig, axes = plt.subplots(nrows=3, figsize=(8, 8))
axes = {sel: ax for sel, ax in zip(selections, axes.ravel())}
evoked.plot_image(axes=axes, group_by=selections, colorbar=False, show=False,
                  mask=significant_points, show_names="all", titles=None,
                  **time_unit)
plt.colorbar(axes["Left"].images[-1], ax=list(axes.values()), shrink=.3,
             label="µV")

plt.show()  
    

