#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 16:43:41 2020

@author: claire
"""

#find half-peak latency of the LPP in each condition
# use jackknife leave one out method

import util_latency as ul
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

from sklearn.model_selection import LeaveOneOut
import pandas as pd

from scipy import interpolate
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

all_lpp=[all_evokeds_control_1[3], all_evokeds_control_2[3], all_evokeds_interv_1[3], all_evokeds_interv_2[3]]

gd_ave_erp=[list() for _ in range(4)]

loo=LeaveOneOut()


for ind, lpp in enumerate(all_lpp):

    loo.get_n_splits(lpp)
    
    # get series of grand average with leave-one-out
    for idx in loo.split(lpp):
        print(idx)
        evokeds_loo=[]
        
        for j in idx[0]:
            evokeds_loo.append(lpp[j].pick_channels(elecs).
                               apply_baseline((None, 0)))
            print(idx[0])
            
        gd_ave_erp[ind].append(mne.grand_average(evokeds_loo))
    
# get the mean of the 3 electrodes of interest to form a ROI
#gd_ave_roi =[]

#for idx, ave in enumerate(gd_ave_erp):
#    gd_ave_roi.append(np.mean(ave.data[:,:], axis=0))
        
    
        
# find fractional peak latency:
#for each grand average estimate onset latency by identifying peak amplitude
# onset, which is the first point in that time window in which amplitude exceeds
# 50% of peak score       

#min(np.absolute(np.cumsum(erp)-sum(erp)/2))

# centroparietal electrodes (no CPz on montage)
tmin, tmax = 0.25, 1.0 #0.30
peak_frac=0.5 # fractional latencu peak

all_onsets_latency=[list() for _ in range(4)]#*len(gd_ave_erp[0]) #  save onsets for each condition


for n in range(0, len(all_lpp)):

    for idx, erp in enumerate(gd_ave_erp[n]):
        
        #erp=np.mean(erp.data, axis=0)
        
        # get peak latency and amplitude
        channel,  latency, amplitude= erp.get_peak(tmin=tmin, tmax=tmax,  return_amplitude=True)  
       
        onsetCutOff = peak_frac*amplitude     
           
        dataShifted = erp.data - onsetCutOff # substract onsetcutoff from data to find where it reaches 0
    
        interpolator = interpolate.UnivariateSpline(np.arange(-1.004,1.,1./250),dataShifted,s=0)   # interpolate points
        
        print(interpolator.roots())
        latency_onsetCutOff= interpolator.roots().mean()
        
        all_onsets_latency[n].append(latency_onsetCutOff)
            
        
#gd_ave_erp.append(mne.grand_average(evokeds).apply_baseline((None, 0)))

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

