#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 16:43:41 2020

@author: claire
"""

#find half-peak latency of the LPP in each condition
# use jackknife leave one out method
import my_jackknife_latency as mjack
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

import pandas as pd

import pingouin as pg
import seaborn as sns

import matplotlib.pyplot as plt


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


elecs= ['Pz']#, 'P3', 'P4']#, 'P3', 'P4']  # electrodes on which we compute the lpp

# lpp to health warning pictures
all_lpp_hw=[all_evokeds_control_1[3], all_evokeds_control_2[3], all_evokeds_interv_1[3], all_evokeds_interv_2[3]]

# lpp to negative stimuli
all_lpp_neg=[all_evokeds_control_1[4], all_evokeds_control_2[4], all_evokeds_interv_1[4], all_evokeds_interv_2[4]]

    
# get the mean of the 3 electrodes of interest to form a ROI
#gd_ave_roi =[]

#for idx, ave in enumerate(gd_ave_erp):
#    gd_ave_roi.append(np.mean(ave.data[:,:], axis=0))


gd_erp_lpp_hw= mjack.get_average_erp_leave_one_out(all_lpp_hw, len(all_lpp_hw), elecs)  


gd_erp_lpp_neg= mjack.get_average_erp_leave_one_out(all_lpp_neg, len(all_lpp_neg), elecs)  
        
    
tmin, tmax = 0.25, 1.0 #0.30
peak_frac=0.5 # fractional latencu peak 
      

lpp_peak_onset_hw = mjack.get_frac_peak_latency(gd_erp_lpp_hw, n_group= len(all_lpp_hw), tmin=tmin, tmax=tmax, peak_frac=peak_frac, sfreq=250)


lpp_peak_onset_neg = mjack.get_frac_peak_latency(gd_erp_lpp_neg, n_group= len(all_lpp_neg), tmin=tmin, tmax=tmax, peak_frac=peak_frac, sfreq=250)
        
##gd_ave_erp.append(mne.grand_average(evokeds).apply_baseline((None, 0)))
#
d={'CTR1': all_onsets_latency[0], 'CTR2': all_onsets_latency[1],
   'INT1':all_onsets_latency[2], 'INT2':all_onsets_latency[3]}

df=pd.concat([pd.Series(v, name=k) for k, v in d.items()], axis=1)



df['id']=df.index

df_long=pd.wide_to_long(df, ["CTR", "INT"], i='id', j="Time")

df_long= pd.melt(df_long.reset_index(), id_vars=['id', 'Time'], 
                 value_vars=['CTR', 'INT'], 
                 var_name='Groupe', 
                 value_name='Latency')

# test for normality
pg.normality(df_long, group='Groupe', dv='Latency')


# statistics - is there an onset difference between the groups/ time of testing
# distribution is not normal so use non parametruc wilcoxon signes rank test




# CTR T1 vs CTR T2
pg.wilcoxon(all_onsets_latency[0],all_onsets_latency[1] )

# CTR T1 vs INT T1
pg.wilcoxon(all_onsets_latency[0],all_onsets_latency[2] )

 # CTR T2 vs INT T2
pg.wilcoxon(all_onsets_latency[1],all_onsets_latency[3] )

# INT T1 vs INT T2
pg.wilcoxon(all_onsets_latency[2],all_onsets_latency[3] )

# correct for multiple comparisons
  
p_vals_all=[0.000043, 0.009397, 0.000043, 0.000043 ] 

reject, pvals_corr = pg.multicomp(p_vals_all, method='bonf')
print(reject, pvals_corr)


# there is significant difference between onsets for the 2 groups x condition`


np.mean(all_onsets_latency[3])





# plot


fig, ax1 = plt.subplots(1, 1, figsize=(5, 4)) 
df_ctr=df_long.query("Groupe == 'CTR'")
ctr_plot=pg.plot_paired(data=df_ctr, dv='Latency', within='Time', subject= 'id', ax=ax1)
 
plt.title('Paired Plot Test-Re Test LPP Latency CTR Groupe')
plt.xticks(ticks=[0, 1], labels=['Pre-Test', 'Post-Test'])


fig2, ax2 = plt.subplots(1, 1, figsize=(5, 4)) 


df_int=df_long.query("Groupe == 'INT'")
int_plot = pg.plot_paired(data=df_int, dv='Latency', within='Time', subject= 'id', ax=ax2)

plt.title('Paired Plot Test-Re Test LPP Latency INT Groupe')
plt.xticks(ticks=[0, 1], labels=['Pre-Test', 'Post-Test'])

fig.savefig(fname.figures_pv + '/ctr_latency.png')
fig2.savefig(fname.figures_pv + '/int_latency.png')




with mne.open_report(fname.group_report) as report:
        
    report.add_figs_to_section(
       fig,               
        captions= 'Increased LPP onset Latency in CTR from T1 to T2' ,
        section='HW Passive Viewing - Group Average ',
        replace=True
    )
    
    report.add_figs_to_section(
        fig2,               
        captions= 'Decreased LPP onset Latency in INT from T1 to T2' ,
        section='HW Passive Viewing - Group Average ',
        replace=True
    )


report.save(fname.group_report_html, overwrite=True,
                open_browser=False)

