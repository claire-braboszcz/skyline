#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
===================
Skyline config file
===================

Configuration parameters for the skyline study

"""

from fnames import FileNames
from mne_bids import make_bids_folders, make_bids_basename


# filepath for analysis root folder 
bids_root = '/home/claire/Documents/STUDY/EEG-Tobacco/Skyline-EEG-BIDS'

# filepath for derivatives files
bids_root_der_preproc ='/home/claire/Documents/STUDY/EEG-Tobacco/Skyline-EEG-BIDS/derivatives/eeg_pre_process'



n_jobs=8

# Analysis parameters

# dataset parameters

events_dict={'go': 11, 'nogo': 13, 'hw': 21, 'neg': 25, 'neut': 22, 'button_press':8, 'fixation':44}  

#--------------------
# filter parameters 
#--------------------

# for data used to run ICA

ica_bandpass_fmin = 1
ica_bandpass_fmax = 40


###################################
# filenames and participants ID
###################################


subject_ids=[146,
            148,
            172,
            185,
            188,
            201,
            271,
            276,
            278,
            279,
            295,
            330,
            339,
            365,
            375,
            388,
            428,
            429,
            477,
            487,
            507,
            537,
            545,
            558,
            562,
            572,
            577,
            589,
            594,
            608,
            647,
            667,
            681,
            690,
            701,
            703,
            718,
            726,
            743,
            747,
            750,
            753,
            754,
            763,
            786
            ]

sessions = [1, 2]


###############################################################################
# Templates for filenames
#
# This part of the config file uses the FileNames class. It provides a small
# wrapper around string.format() to keep track of a list of filenames.
# See fnames.py for details on how this class works.
fname = FileNames()

# Some directories
fname.add('bids_root', bids_root)
fname.add('bids_root_der_preproc', '{bids_root_der}/eeg_preprocess')
fname.add('bids_root_der_gonogo', '{bids_root_der}/go_nogo')
fname.add('bids_root_der_passview', '{bids_root_der}/passive_viewing')


# filename for eeg param
fname.add('eeg_montage','{bids_root}/EEG_montage/AC-64.bvef')


#filenames for files generated during analysis

fname.add('raw','{bids_root}/{subject}/{session}/eeg/{subject}_{session}_eeg.vhdr')
fname.add('filt_ica','{bids_root_der_preproc}/{subject}/{session}/eeg/{subject}_{session}_filt_{fmin}_{fmax}_raw.fif')





# Filenames for MNE reports
fname.add('reports_dir', '{bids_root}/reports/')
fname.add('report', '{reports_dir}/{subject}_{session}_report.h5')
fname.add('report_html', '{reports_dir}/{subject}_{session}_report.html')

























