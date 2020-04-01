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


# filepath for analysis root folder 
bids_root = '/home/claire/Documents/STUDY/EEG-Tobacco/Skyline-EEG-BIDS'
n_jobs=8

# Analysis parameters

# dataset parameters

events_dict={'go': 11, 'nogo': 13, 'hw': 21, 'neg': 25, 'neut': 22, 'button_press':8, 'fixation':44}  
montage= mne.channels.read_custom_montage(bids_root + '/AC-64.bvef')

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
fname.add('study_path', study_path)
fname.add('archive_dir', '{study_path}/archive')
fname.add('meg_dir', '{study_path}/MEG')
fname.add('subjects_dir', '{study_path}/subjects')
fname.add('subject_dir', '{meg_dir}/{subject}')




