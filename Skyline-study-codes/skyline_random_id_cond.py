#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 15:37:12 2019

@author: apheia
"""

import random   
import numpy as np
import pandas as pd
import string


# generate random study ID
#def rand_id_gen(size, chars= string.digits):
#    return ''.join(random.choice(chars) for x in range(size))

#--------------------------
# create random study ID
#--------------------------
    
random.seed(a=5)

study_id=[]
#for i in range (1, 141):
study_id = random.sample(range(100, 900), 140) # random list between 100 and 900 without duplicate



screening_id = list(range(1, 141))


#create dictionary
d = {'Screening ID' : screening_id, 'Study ID': study_id}

#create dataframe
df = pd.DataFrame(d)

df.to_csv('skyline_screening_study_id.csv')

#----------------------------
# Randomize study conditions
#----------------------------
# attribute condition
nr_subjects = 75
batch_nr = 10
total_cond = []
for i in range(0, int(nr_subjects/batch_nr)):
    nr = [0,1]*batch_nr
    random.shuffle(nr)
    total_cond += nr


d_cond ={'Study ID': study_id, 'Condition': total_cond }

df_cond = pd.DataFrame(d_cond)

df_cond.to_csv('skyline_study_id_cond.csv')


#-----------------------------------------------
# Study ID + Phone numbers
#-----------------------------------------------

phone =[0]*len(study_id)

d_phone = {'Study ID': study_id, 'Phone':phone}


df_phone = pd.DataFrame(d_phone)

df_phone.to_csv('skyline_study_id_phone_numbers.csv')
