#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
===================
Skyline config file
===================

Configuration parameters for the skyline study


adapted from https://github.com/AaltoImagingLanguage/conpy/tree/master/scripts

"""

from fnames import FileNames


# filepath for analysis root folder 
#bids_root = '/home/claire/Documents/STUDY/EEG-Tobacco/Skyline-EEG-BIDS'

# filepath for derivatives files
#bids_root_der='/home/claire/Documents/STUDY/EEG-Tobacco/Skyline-EEG-BIDS/derivatives'


n_jobs=8

# Analysis parameters

# dataset parameters





###################################
# filenames and participants ID
###################################

#558 (1st participant) is excluded due to error in stimuli timing 

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
           #558,
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

subj_interv=[#558,
            278,
            148,
            276,
            786,
            726,
            743,
            763,
            507,
            375,
            754,
            594,
            188,
            545,
            750,
            330,
            365,
            487,
            201,
            718,
            577,
            589,
            146]


subj_control=[608,
            690,
            429,
            647,
            562,
            477,
            703,
            388,
            428,
            747,
            279,
            572,
            339,
            667,
            681,
            753,
            271,
            295,
            172,
            185,
            701,
            537]



###############################################################################

# STUDY Pre processing and analysis parameters




# filter parameters for data used to run ICA and ERPs analysis

ica_bandpass_fmin = 1
ica_bandpass_fmax = 40


erp_bandpass_fmin= None
erp_bandpass_fmax= 40

# re-sampling frequency
sfreq=250

# Maximum number of ICA components to reject
n_ecg_components = 2  # ICA components that correlate with heart beats
n_eog_components = 2  # ICA components that correlate with eye blinks


#########################################################################################
 # Parameters for creating epochs

#########################################################################################
# epochs characteristics
events_dict={'go': 11, 'nogo': 13, 'hw': 21, 'neg': 25, 'neut': 22, 'button_press':8, 'fixation':44}  


tmin_pv, tmax_pv = -1.0001, 1.0001
event_dict_pv = {'hw': 21, 'neg': 25, 'neut': 22}


baseline_pv=(-1, 0)

tmin_gng, tmax_gng = -0.5, 0.6
event_dict_gng = {'go': 11, 'nogo': 13}
baseline_gng=(-0.5, 0)

# screen offset - delay between picture and trigger
screen_offset=0.008


# Thresholds to use for rejecting epochs that have a too large signal amplitude
reject_criteria =  dict(eeg=200e-6)  #200 µV
flat_criteria= dict(eeg=1e-6) # 1 µV




#########################################################################################
 # Parameters for ERPs

#########################################################################################
# plot individual erps
ylim=30




all_evokeds_interv_1 = [list() for _ in range(5)]
all_evokeds_interv_2 = [list() for _ in range(5)]

all_evokeds_control_1= [list() for _ in range(5)]
all_evokeds_control_2= [list() for _ in range(5)]



all_evokeds_interv_1_gng = [list() for _ in range(4)]
all_evokeds_interv_2_gng = [list() for _ in range(4)]

all_evokeds_control_1_gng= [list() for _ in range(4)]
all_evokeds_control_2_gng= [list() for _ in range(4)]




###############################################################################
# Templates for filenames
#############################################################################
# This part of the config file uses the FileNames class. It provides a small
# wrapper around string.format() to keep track of a list of filenames.
# See fnames.py for details on how this class works.
fname = FileNames()

# Some directories
fname.add('bids_root', '/home/claire/Documents/STUDY/EEG-Tobacco/Skyline-EEG-BIDS/')
fname.add('bids_root_der', '/home/claire/Documents/STUDY/EEG-Tobacco/Skyline-EEG-BIDS/derivatives')


fname.add('folder_preproc', '{bids_root_der}/eeg_preprocess/{subject}/{session}/eeg/')
fname.add('folder_gonogo', '{bids_root_der}/go_nogo/{subject}/{session}/eeg/')
fname.add('folder_passview', '{bids_root_der}/passive_viewing/{subject}/{session}/eeg/')


# filename for eeg param
fname.add('eeg_montage','{bids_root}/EEG_montage/AC-64.bvef')


#filenames for files generated during analysis

fname.add('raw','{bids_root}/{subject}/{session}/eeg/{subject}_{session}_eeg.vhdr')
fname.add('filt_ica','{folder_preproc}/{subject}_{session}_filt_{fmin}_{fmax}_raw.fif')
fname.add('ica', '{folder_preproc}/{subject}_{session}_ica.fif')

fname.add('logfile','{bids_root}/{subject}/{session}/eeg/{subject}_{session}_events.tsv')

#fname.add('ica_on_epochs', '{folder_preproc}/{subject}_{session}_epochs_ica.fif')
#fname.add('epochs_ica','{folder_preproc}/{subject}_{session}_filt_{fmin}_{fmax}_epo.fif')
fname.add('filt_erp','{folder_preproc}/{subject}_{session}_filt_{fmin}_{fmax}_raw.fif')

fname.add('epochs_pv','{folder_passview}/{subject}_{session}_pv_epo.fif')
fname.add('epochs_gng','{folder_gonogo}/{subject}_{session}_gng_epo.fif')

fname.add('evoked_pv','{folder_passview}/{subject}_{session}_pv_ave.fif')
fname.add('evoked_gng','{folder_gonogo}/{subject}_{session}_gng_ave.fif')

fname.add('metadata_gng','{folder_gonogo}/{subject}_{session}_gng_metadata.csv')


fname.add('evoked_pv','{folder_passview}/{subject}_{session}_pv_ave.fif')



# Filenames for MNE reports

fname.add('reports_dir', '{bids_root_der}/reports/')
fname.add('report', '{reports_dir}/{subject}_{session}_report.h5')
fname.add('report_html', '{reports_dir}/{subject}_{session}_report.html')
fname.add('group_report', '{reports_dir}/group_report.h5')
fname.add('group_report_html', '{reports_dir}/group_report.html')



# filepath for figures

fname.add('figures_pv', '{bids_root_der}/figures/passive_viewing/')
fname.add('figures_gng' , '{bids_root_der}/figures/gonogo/')

















