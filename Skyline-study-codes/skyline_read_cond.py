#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:14:01 2019

@author: claire
"""

import pandas as pd

#-------------- Parameters -----------------

# enter participant ID
pp_id = 330

# Enter participant's experimental group, chose from:
#'Study ID EEG Female'
#'Study ID EEG Male'
#'Study ID Main Male'
#'Study ID Main Female'

pp_group = 'Study ID EEG Male'
pp_cond = 'Cond EEG Male'
#---------------------------------------------



condfile = '/home/claire/Documents/STUDY/EEG-Tobacco/Skyline Participants Forms/skyline_study_id_cond.csv'


cond = pd.read_csv(condfile)

eeg_m = cond[[pp_group, pp_cond]]


eeg_m.loc[eeg_m[pp_group] == pp_id]
