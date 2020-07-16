#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 18:02:09 2020


use the events.tsv file to create an epoch metadata file to read with mne python


@author: claire
"""

from config import (fname, erp_bandpass_fmin, erp_bandpass_fmax, 
                    events_dict, 
                    sfreq,
                    tmin_gng, tmax_gng, event_dict_gng,
                    screen_offset,
                    reject_criteria, 
                    flat_criteria, 
                    baseline_gng, 
                    n_jobs)

import pandas as pd


subj=146
sess=1

logfile=pd.read_csv(fname.logfile(subject='sub-'+ str(subj), 
                                   session='ses-'+str(sess)), sep='\t')


# find indexes of task start - go no go was done in 2nd and 3rd
ind_bloc=logfile[logfile["value"]==55].index.tolist()


df=logfile.iloc[ind_bloc[1]:ind_bloc[2], :]

df=df.append(logfile.iloc[ind_bloc[3]:ind_bloc[4], :])


