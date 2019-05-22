#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 10:56:03 2019

@author: claire
"""

import pandas as pd
import ptitprince as pt
import seaborn as sns
import os
import matplotlib.pyplot as plt
import numpy as np
import os
#sns.set(style="darkgrid")
#sns.set(style="whitegrid")
#sns.set_style("white")
sns.set(style="whitegrid",font_scale=2)
import matplotlib.collections as clt


#read csv file with data
df = pd.read_csv ("/home/claire/Documents/STUDY/EEG-Tobacco/DATA/Surveys/Skyline - Daily messages - Intervention_7 May 2019_09.54.csv", sep= ",")


df1 = df[['StartDate', 'Finished', 'Q1', 'SC0']]




