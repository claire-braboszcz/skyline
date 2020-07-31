#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 18:02:09 2020


use the events.tsv file to create an epoch metadata file to read with mne python


@author: claire
"""

from config import (fname, subject_ids, sessions)

import pandas as pd
import numpy as np


for subj in subject_ids:
       for sess in sessions:
            
            print('Processing subject:', subj, 'session:', sess)

           
            logfile=pd.read_csv(fname.logfile(subject='sub-'+ str(subj), 
                                               session='ses-'+str(sess)), sep='\t')
            
            
            # find indexes of task start - go no go was done in 2nd and 3rd
            ind_bloc=logfile[logfile["value"]==55].index.tolist()
            
            if len(ind_bloc) == 5:
            
                df=logfile.iloc[ind_bloc[1]:ind_bloc[2], :]
                
                df=df.append(logfile.iloc[ind_bloc[3]:ind_bloc[4], :])
            
            elif len(ind_bloc) == 4:
                
                df=logfile.iloc[ind_bloc[0]:ind_bloc[1], :]
                
                df=df.append(logfile.iloc[ind_bloc[2]:ind_bloc[3], :])
            
          
            # create column for onset of button press
            df['response_onset'] =np.nan
            
            idx=df.index[df['value']==8]
            df.loc[idx,['response_onset']] = df.loc[idx, ['onset']].values
            
            
            # create column to indicate button press
            df['response']=np.nan
                      
            
            df.loc[df['value']==8, 'response'] = 'button press'
            
            # shift up one cell to align with rest of trial info
            df.response=df.response.shift(-1)
            df.response_onset=df.response_onset.shift(-1)

             
            
            
            
            df.loc[df['value']==11, 'type'] = 'go'
            df.loc[df['value']==13, 'type'] = 'nogo'
            
            df.loc[(df['type']=='go') &( df['response']=='button press'), 'accuracy' ] = 'correct'
            df.loc[(df['type']=='go') &( df['response'].isna()== True), 'accuracy' ] = 'incorrect'
            df.loc[(df['type']=='nogo') &( df['response'].isna()== True), 'accuracy' ] = 'correct'

            df.loc[(df['type']=='nogo') &( df['response']=='button press'), 'accuracy' ] = 'false alarm'
            
            # remove rows that are not go or nogo
            
            df=df[df['type'].notnull()]
            
            df.to_csv(fname.metadata_gng(subject='sub-'+ str(subj), session='ses-'+str(sess)))

            del df, logfile 
