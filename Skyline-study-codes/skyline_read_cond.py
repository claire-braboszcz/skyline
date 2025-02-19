                                                                                                                                                                                  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:14:01 2019

This script reads the file with participant's random condition attribution.

You need to provide the participant's id (pp_id), as well as the column for participant's group (pp_group) and condition (pp_cond)
ie. need to specify if male/female and main only or eeg study. 

@author: claire
"""

import pandas as pd

#-------------- Parameters -----------------

# enter participant ID
pp_id = 711
# Enter participant's experimental group, chose from:
#'Study ID EEG Female'
#'Study ID EEG Male'
#'Study ID Main Male'
#'Study ID Main Female'

pp_group = 'Study ID EEG Male'
pp_cond = 'Cond EEG Male'
#---------------------------------------------



condfile = '/home/claire/Documents/scripts-local/skyline/Skyline-study-codes/skyline_study_id_cond.csv'


cond = pd.read_csv(condfile)

eeg_m = cond[[pp_group, pp_cond]]


print(eeg_m.loc[eeg_m[pp_group] == pp_id])
