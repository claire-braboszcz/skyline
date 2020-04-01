#!/usr/bin/env python
# coding: utf-8

# In[ ]:


´´´
Create BIDS-compatible derivatives folder
´´´

import os



bids_root = '/home/claire/Documents/STUDY/EEG-Tobacco/Skyline-EEG-BIDS'
bids_root_der = os.path.join(bids_root, 'derivatives')
if not os.path.exists(bids_root_der):
    os.makedirs(bids_root_der)

preproc_root = os.path.join(bids_root_der, 'eeg_pre_process')
if not os.path.exists(preproc_root):
    os.makedirs(preproc_root)

pv_root = os.path.join(bids_root_der, 'passive_viewing')
if not os.path.exists(pv_root):
    os.makedirs(pv_root)

gng_root = os.path.join(bids_root_der, 'go_nogo')
if not os.path.exists(gng_root):
    os.makedirs(gng_root)

