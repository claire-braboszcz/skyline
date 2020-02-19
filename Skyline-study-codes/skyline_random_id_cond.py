#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 15:37:12 2019

@author: apheia
"""

import random   
import pandas as pd


# generate random study ID
#def rand_id_gen(size, chars= string.digits):
#    return ''.join(random.choice(chars) for x in range(size))


savepath ='/home/claire/Documents/scripts-local/skyline/Skyline-study-codes/skyline_screening_study_id.csv'

#--------------------------
# create random study ID
#--------------------------
    
random.seed(a=5)

study_id_all=[]
#for i in range (1, 141):
study_id_all = random.sample(range(100, 800), 400) # random list between 100 and 900 without duplicate


study_id_main_m = study_id_all[0:100]
study_id_main_f = study_id_all[100:200]

study_id_eeg_m = study_id_all[200:300]
study_id_eeg_f = study_id_all[300:400]


screening_id_main_m = ['m'+ str(id) for id in(range(1, 101))]
screening_id_main_f = ['f'+ str(id) for id in(range(1, 101))]
screening_id_eeg_m = ['eeg_m'+ str(id) for id in(range(1, 101))]
screening_id_eeg_f = ['eeg_f'+ str(id) for id in(range(1, 101))]


#create dictionary
d = {'Screening ID Main Male' : screening_id_main_m, 'Study ID Main Male': study_id_main_m, 
     'Screening ID Main Female' : screening_id_main_f, 'Study ID Main Female': study_id_main_f, 
     'Screening ID EEG Male' : screening_id_eeg_m, 'Study ID EEG Male': study_id_eeg_m, 
     'Screening ID EEG Female' : screening_id_eeg_f, 'Study ID EEG Female': study_id_eeg_f
     }

#create dataframe
df = pd.DataFrame(d)

#df.to_csv('skyline_screening_study_id_1812.csv')

#----------------------------
# Randomize study conditions
#----------------------------

# attribute condition
nr_subjects = 200
batch_nr = 10
total_cond = []
for i in range(0, int(nr_subjects/batch_nr)):
    nr = [0,1]*batch_nr
    random.shuffle(nr)
    total_cond += nr


cond_main_m = total_cond[0:100]
cond_main_f = total_cond[100:200]
cond_eeg_m = total_cond[200:300]
cond_eeg_f = total_cond[300:400]


d_cond ={ 'Study ID Main Male': study_id_main_m, 'Cond Main Male': cond_main_m, 
     'Study ID Main Female': study_id_main_f, 'Cond Main Female': cond_main_f, 
    'Study ID EEG Male': study_id_eeg_m, 'Cond EEG Male': cond_eeg_m, 
    'Study ID EEG Female': study_id_eeg_f,'Cond EEG Female': cond_eeg_f
     }

df_cond = pd.DataFrame(d_cond)

#df_cond.to_csv('skyline_study_id_cond_1812.csv')


#-----------------------------------------------
# Study ID + Phone numbers
#-----------------------------------------------

#phone =[0]*len(study_id)

#d_phone = {'Study ID': study_id, 'Phone':phone}


#df_phone = pd.DataFrame(d_phone)

#df_phone.to_csv('skyline_study_id_phone_numbers.csv')








