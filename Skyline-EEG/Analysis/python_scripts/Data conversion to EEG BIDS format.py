#!/usr/bin/env python
# coding: utf-8

# Converting Skyline EEG data into EEG-BIDS format

# 1. creating folder structure
# 

# imports

# In[2]:


import os
import shutil as sh
import csv
import pandas as pd
from numpy.testing import assert_array_equal
import numpy as np
import mne

from mne_bids import make_bids_folders, make_bids_basename, write_raw_bids
from mne_bids.utils import print_dir_tree

from mne_bids.copyfiles import copyfile_brainvision


# In[9]:


home = '/home/claire/Documents/STUDY/EEG-Tobacco'
orig_data_dir = os.path.join(home, 'DATA')
bids_root = os.path.join(home, 'Skyline-EEG-BIDS')
if not os.path.exists(bids_root):
    os.makedirs(bids_root)
        
#487, 185, 701, 201, 718, 577, 589,146,365, 172,608, 690,429,558,278,148, 276,647,562,477,703,786,726,743,763,507,388,428,375,747,754,279,572,339,667,594,188,545,681,750,330,753,271,295
subject_ids=[172, 146]
sessions=[1, 2]
# event dictionnary
trial_type = {'go': 11, 'nogo': 13, 'hw': 21, 'neg': 25, 'neut': 22, 'button_press':8, 'fixation':44}  
# will need to add metad data from logfile 



#  step1 : rename some data file to match the structure skyline_subject_session :
#  

# In[4]:


# only needed this once, so commenting out now
# first let's rename some brainvision datasets that were not correcty labelled

#bad_ids = [148, 558, 278, 608]

#bad_ids =[690]
#for subj in bad_ids:
#    for sess in sessions:
#        data_path= os.path.join(orig_data_dir, 's%d' %subj,  'session%02d' %sess)
#        vhdr_file = os.path.join(data_path, 's%d_%02d.vhdr' %(subj, sess)) 
        # for s690 use :
        #vhdr_file = os.path.join(data_path, 'skyline_%d_%02d.vhdr' %(subj, sess)) 
#        vhdr_file_renamed = os.path.join(data_path, 'skyline_s%d_%02d.vhdr' %(subj, sess)) 
#        copyfile_brainvision(vhdr_file, vhdr_file_renamed)
#        raw = mne.io.read_raw_brainvision(vhdr_file)
#        raw_renamed = mne.io.read_raw_brainvision(vhdr_file_renamed)
#        assert_array_equal(raw.get_data(), raw_renamed.get_data())


# In[10]:


# converts data into new BIDS datasets
# need to merge info from logfiles with info from events


for subj in subject_ids:
    for sess in sessions:
        data_path= os.path.join(orig_data_dir, 's%d' %subj,  'session%02d' %sess)
        fname_in = os.path.join(data_path,'skyline_s%d_%02d.vhdr' %(subj, sess))  
        raw = mne.io.read_raw_brainvision(fname_in, preload=False)
        
       
        events, event_id = mne.events_from_annotations(raw)

        bids_basename = make_bids_basename(subject=str(subj), session = str(sess))

        write_raw_bids(raw, bids_basename, bids_root, event_id=trial_type,
               events_data=events, overwrite=True)
        
        # read events and logfile files
        events_file = os.path.join(bids_root,'sub-%d' %subj, 'ses-%d' %sess, 'eeg','sub-%d_' %subj + 'ses-%d_events.tsv' %sess) 

        #read logfile
        logfile_file = os.path.join(data_path, 's%d_%02d_logfile.txt' %(subj, sess) )

        #output_file= os.path.join((bids_root,'sub-%d' %subj, 'ses-%d' %sess, 'eeg','sub-%d_' %subj + 'ses-%d_events.tsv' %sess) 


        MAPPINGS = {"n/a": None,
                    "fixation": None,
                    "neg": ["Neg"],
                    "neut": ["Neut"],
                    "hw": ["HW"],
                    "go": ["HW", "SmoCuDa"],
                    "nogo": ["HW", "SmoCuDa"],
                    "button_press": None
                    }

        csv_details = None
        last_idx = 1
        new_row_list =[]
        
        with open(logfile_file,'r') as csvfile:
            csv_details = list(csv.reader(csvfile, delimiter='\t'))

        def get_file_details(trial_type):
            global last_idx
            if MAPPINGS[trial_type] is None:
                return None

            for idx, row in enumerate(list(csv_details)[last_idx:]):
                for ttype in MAPPINGS[trial_type]:
                    if ttype in row[1]:
                        last_idx += idx + 1
                        return "_".join(row[1].split("_")[-2:])

        with open(events_file,'r') as csvfile:
                events_reader = csv.reader(csvfile, delimiter='\t')
                for row in list(events_reader)[1:]:
                    csvline = ','.join(row)
                    csvline += ','

                    filename = get_file_details(row[2])
                    if filename:
                        csvline += filename

                    new_row_list.append(csvline)
                    print(csvline)


        # create and save dataframe (replaces previous events.tsv file with added column for filename)
        df_full = pd.DataFrame([sub.split(",") for sub in new_row_list], columns =['onset', 'duration', 'trial_type', 'value', 'sample', 'filename' ] )
        df_full.to_csv(events_file, sep = '\t')
        
        del df_full
        
     


# Merge info from events.tsv and logfile.text to get full events meta-data in one single file
# 

# In[ ]:





# In[ ]:




