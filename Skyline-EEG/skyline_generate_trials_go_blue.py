'''
Generate list of trial blocs for skyline EEG experiement. Includes Go NogO task and passive viewing

Go NoGo task:
   - 41 health warning
   - 41 smoking cue
   - 5*GO and 2*NOGO
   - need to get at least 82 trials as NoGo in each category so total of 164 NoGO trials
   - 
   -
Duration :574*1.4/60 ~ 13 min   
    
    - 2 blocks of 287 stimuli; 82 NoGO, 205 GO
    - never 2 NoGo in a row
    - trial type based on file name "blue" or "orange"

Passive viewing:
    - 41 HW, 41 Neg, 41 Neut
    - Each stim presented 2 times, = 82 trials per category
    - total 246 trials
    - duration 246*4300 ~18min in average
    - 27 trials of each category in each block, except one block with 1 extra trial for each category
    
'''

import random
import os
#import csv
#import numpy
import pandas as pd




filepath_gonogo = '/home/claire/Documents/STUDY/EEG-Tobacco/Stimuli/Stim_Go_NoGo_Stim_norm'
filepath_pass_view =  '/home/claire/Documents/STUDY/EEG-Tobacco/Stimuli/Stim_passive_viewing_norm'

#---------------------------
# Go NoGo Task parameters
#---------------------------


def yellowframe(stim):
    return True if stim[0] in ['O'] else False

def blueframe(stim):
    return True if stim[0] in ['B'] else False

is_go = blueframe
is_nogo = yellowframe

GO = 1
NOGO = 2
END = 3

nNoGo = 82*2
nGo = 82*5

nNG_bloc = 82
nGO_bloc = 205

total_n_bloc = nNG_bloc + nGO_bloc

nBloc= 2

n_rep_go =5
n_rep_nogo = 2
#def run_of_2(trials, obj):
 #   # check if no more than 4 "go"in a row
    
#    for i in range (1, len(trials)-1):
 #       if trials[i:i+1]== obj :
  #          return True
   # return False

BREAK = 10
START_GO = 101
START_PV = 202
THE_END = 999
#---------------------------
# Passive viewing Task parameters
#---------------------------

HW = 4
NEG = 5
NEUT = 6

#stim per block

n_stim_pv_bloc = 82

#
nHW = 41
nNEG = 41
nNEUT = 41

n_rep_pv = 2 # number of repetitions of the same stim for passive viewing


def health_warning(stim):
    return True if 'HW' in stim  else False

def neg_pic (stim):
    return True if 'Neg' in stim  else False

def neut_pic (stim):
    return True if 'Neut' in stim  else False

#-------------------------
# Task Trigger codes   
#--------------------------

trig_GO = 11    
trig_NOGO = 13

trig_HW = 21
trig_NEG = 25
trig_NEUT = 22

trig_BREAK = 50
trig_END =88
trig_start_go = 55

trig_start_pv = 66


"""
generate trial list for skyline go nogo
"""

   

#-------------------------------
# Stim List 
#-------------------------------

# go nogo
for root, dirs, files in os.walk(filepath_gonogo, topdown=False):  # read files in folder
    go_nogo_stimList = files

goStim = [stim for stim in  go_nogo_stimList if is_go(stim)]
nogoStim = [stim for stim in  go_nogo_stimList if is_nogo(stim)]


all_go = goStim*n_rep_go
all_nogo = nogoStim*n_rep_nogo

random.shuffle(all_go)
random.shuffle(all_nogo)

   
# passive viewing
for root, dirs, files in os.walk(filepath_pass_view, topdown=False):  # read files in folder
    pass_view_stimList = files

hw_stim = [stim for stim in pass_view_stimList if health_warning(stim)]
neg_stim = [stim for stim in pass_view_stimList if neg_pic(stim)]
neut_stim = [stim for stim in pass_view_stimList if neut_pic(stim)]

all_hw = hw_stim *n_rep_pv
all_neg = neg_stim*n_rep_pv
all_neut = neut_stim*n_rep_pv

random.shuffle(all_hw)
random.shuffle(all_neg)
random.shuffle(all_neut)



 #-----------------------------------------
 # create list of trial type 
 #-----------------------------------------
  
# go nogo
trial_type_gonogo_b1=[]
trial_type_gonogo_b2=[]

#trial_type = [[GO]  + [NOGO]] * nNoGo + [[GO] + [GO]] * int((nGo-nNoGo)/2)

trial_type_gonogo_b1 = [[GO]  + [NOGO]] * nNG_bloc + [[GO]] * (nGO_bloc-nNG_bloc)   
trial_type_gonogo_b2 = [[GO]  + [NOGO]] * nNG_bloc + [[GO]] * (nGO_bloc-nNG_bloc)
random.shuffle(trial_type_gonogo_b1)
random.shuffle(trial_type_gonogo_b2)

# flatten list of go-nogo
    
trial_type_gonogo_b1 = [val for sublist in trial_type_gonogo_b1 for val in sublist]
trial_type_gonogo_b2 = [val for sublist in trial_type_gonogo_b2 for val in sublist]

# insert breaks halfway through bloc
trial_type_gonogo_b1.insert(len(trial_type_gonogo_b1)//2, BREAK)
trial_type_gonogo_b2.insert(len(trial_type_gonogo_b2)//2, BREAK)

# passive viewing
#---------------------

trial_type_pass_view_b1 =[]
trial_type_pass_view_b2 =[]
trial_type_pass_view_b3 =[]

trial_type_pass_view = []

trial_type_pass_view =[HW] * nHW * n_rep_pv + [NEG] * nNEG * n_rep_pv + [NEUT] * nNEUT * n_rep_pv  
random.shuffle(trial_type_pass_view)


trial_type_pass_view_b1 = trial_type_pass_view[0:82]
trial_type_pass_view_b2 = trial_type_pass_view[82:164]
trial_type_pass_view_b3 = trial_type_pass_view[164:246]


# insert breaks halfway through bloc
trial_type_pass_view_b1.insert(len(trial_type_pass_view_b1)//2, BREAK)
trial_type_pass_view_b2.insert(len(trial_type_pass_view_b2)//2, BREAK)
trial_type_pass_view_b3.insert(len(trial_type_pass_view_b3)//2, BREAK)

#------------------------------
# get full trial list together
#------------------------------

all_trials_type =[]
all_trials_type = [START_PV]+ trial_type_pass_view_b1 + [START_GO] + trial_type_gonogo_b1 + [BREAK] + [START_PV] + trial_type_pass_view_b2 + [BREAK] + [START_GO] + trial_type_gonogo_b2 + [BREAK] + [START_PV] + trial_type_pass_view_b3 + [THE_END]

 
  
#--------------------------
# Assign stim to to trial
#-------------------------- 
 
all_trials=[]
all_triggers=[]
all_isi = []
all_time_pres =[]

ind_go = 0
ind_nogo = 0
ind_hw = 0
ind_neg =0
ind_neut =0



for stim in range(0,len(all_trials_type)):
    if all_trials_type[stim] == GO:
        all_trials += [all_go[ind_go]]
        all_triggers += [trig_GO]
        all_isi += random.sample(range(500, 800), 1)
        all_time_pres += [600]
        ind_go += 1
        
    elif all_trials_type[stim] == NOGO:
        all_trials += [all_nogo[ind_nogo]]
        all_triggers += [trig_NOGO]
        all_isi += random.sample(range(500, 800), 1)
        all_time_pres += [600]
        ind_nogo += 1 
        
    elif all_trials_type[stim] == HW:
        all_trials += [all_hw[ind_hw]]
        all_triggers += [trig_HW]
        all_isi += random.sample(range(1500, 3000), 1)
        all_time_pres += random.sample(range(1000, 1400), 1)
        ind_hw += 1 
        
    elif all_trials_type[stim] == NEG:
        all_trials += [all_neg[ind_neg]]
        all_triggers += [trig_NEG]
        all_isi += random.sample(range(1500, 3000), 1)
        all_time_pres += random.sample(range(1000, 1400), 1)
        ind_neg += 1 
        
    elif all_trials_type[stim] == NEUT:
        all_trials += [all_neut[ind_neut]]
        all_triggers += [trig_NEUT]
        all_isi += random.sample(range(1500, 3000), 1)
        all_time_pres += random.sample(range(1000, 1400), 1)
        ind_neut += 1 
        
    elif all_trials_type[stim] == BREAK:
        all_trials += ['break']
        all_triggers += [trig_BREAK]
        all_isi += ['break']
        all_time_pres += ['break']
        
    elif all_trials_type[stim] == START_GO:
        all_trials += ['start_gonogo']
        all_triggers += [trig_start_go]
        all_isi += ['start_gonogo']
        all_time_pres += ['start_gonogo']
        
    elif all_trials_type[stim] == START_PV:
        all_trials += ['start_pass_view']
        all_triggers += [trig_start_go]
        all_isi += ['start_pass_view']
        all_time_pres += ['start_pass_view']
  

    elif all_trials_type[stim] == THE_END:
        all_trials += ['the_end']
        all_triggers += [trig_END]
        all_isi += [0]
        all_time_pres += [0]
# go nogo bloc 1
   

d_trials = {'Stim': all_trials, 'PresTime': all_time_pres, 'ISI': all_isi, 'Trigger': all_triggers}
df_trials = pd.DataFrame(d_trials)

df_trials.to_csv('skyline_eeg_all_trials_go_blue_0406.csv', index= False)                     
        











