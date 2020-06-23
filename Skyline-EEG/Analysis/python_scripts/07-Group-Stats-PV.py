#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 10:04:06 2020

@author: claire
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

import mne
from mne.channels import find_ch_connectivity, make_1020_channel_selections
from mne.stats import spatio_temporal_cluster_test


from config import (fname, 
                    erp_bandpass_fmin, erp_bandpass_fmax, 
                    tmin_pv, tmax_pv , 
                    subject_ids, 
                    sessions, 
                    subj_interv, 
                    subj_control
                    )




all_events=['hw/int/t1',
            'neg/int/t1', 
            'neut/int/t1',
            'hw/int/t2',
            'neg/int/t2', 
            'neut/int/t2',
            'hw/ctr/t1',
            'neg/ctr/t1', 
            'neut/ctr/t1',
            'hw/ctr/t2',
            'neg/ctr/t2', 
            'neut/ctr/t2']

all_epochs = []


for subj in subject_ids:
    for sess in sessions:
        epochs= mne.read_epochs(fname.epochs_pv(subject='sub-'+ str(subj), 
                                                session='ses-'+str(sess)))
  
        all_epochs.append(epochs)
        

all_evokeds = {cond: [epochs[cond].average().apply_baseline((None, 0))
                      for epochs in all_epochs] for cond in all_events}
all_evokeds
        

# create a pandas dataset with all hw, neg and neut stim for each session and
# group
                
#1. concatenate epochs for all pp in each group and session
all_int_t1 = mne.concatenate_epochs(all_epochs_interv_1)
all_int_t2 = mne.concatenate_epochs(all_epochs_interv_2)

all_ctr_t1 = mne.concatenate_epochs(all_epochs_control_1)
all_ctr_t2 = mne.concatenate_epochs(all_epochs_control_2)





hw_int_t1=all_int_t1['hw']
neg_int_t1=all_int_t1['neg']
neut_int_t1=all_int_t1['neut']

hw_int_t2=all_int_t2['hw']
neg_int_2=all_int_t2['neg']
neut_int_t2=all_int_t2['neut']
           
hw_ctr_t1=all_ctr_t1['hw']
neg_ctr_t1=all_ctr_t1['neg']
neut_ctr_t1=all_ctr_t1['neut']     
         
hw_ctr_t2=all_ctr_t2['hw']
neg_ctr_t2=all_ctr_t2['neg']
neut_ctr_t2=all_ctr_t2['neut']     



# TFCE

# Calculate statistical thresholds
con = find_ch_connectivity(all_int_t1.info, "eeg")


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

