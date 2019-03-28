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
    
'''

import random
import os
#import csv
import numpy
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

is_go = yellowframe
is_nogo = blueframe

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



#---------------------------
# Passive viewing Task parameters
#---------------------------

HW = 4
NEG = 5
NEUT = 6

nHW = 41
nNEG = 41
nNEUT = 41

n_rep_pv = 2




def health_warning(stim):
    return True if 'HW' in stim  else False

def neg_pic (stim):
    return True if 'Neg' in stim  else False

def neut_pic (stim):
    return True if 'Neut' in stim  else False





def genTrialList():
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
    
    all_go_b1 = all_go[0:nGO_bloc]
    all_go_b2 = all_go[nGO_bloc :]
    
    all_nogo_b1 = all_nogo[0:nNG_bloc]
    all_nogo_b2 = all_nogo[nNG_bloc :]
    
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
    random.shuffle(all_neg_stim)
    random.shuffle(all_neut_stim)
    
    
    all_hw_b1 = all_hw[0:nHW]
    all_hw_b2 = all_hw[nHW:]

    all_neg_b1 = all_neg[0:nNEG]
    all_neg_b2 = all_neg[nNEG:]
    
    all_neut_b1 = all_neut[0:nNEUT]
    all_neut_b2 = all_neut[nNEUT:]
    
    
     #-----------------------------------------
     # create list of trial type 
     #-----------------------------------------
  
    # go nogo
    trial_type_gonogo_b1=[]
    trial_type_gonogo_b2=[]

    #trial_type = [[GO]  + [NOGO]] * nNoGo + [[GO] + [GO]] * int((nGo-nNoGo)/2)
    
    trial_type_gonogo_b1 = [[GO]  + [NOGO]] * nNG_bloc + [GO] * (nGO_bloc-nNG_bloc)   
    trial_type_gonogo_b2 = [[GO]  + [NOGO]] * nNG_bloc + [GO] * (nGO_bloc-nNG_bloc)
    random.shuffle(trial_type_gonogo_b1)
    random.shuffle(trial_type_gonogo_b2)


    # passive viewing
    #---------------------

    trial_type_pass_view_b1 =[]
    trial_type_pass_view_b2 =[]

    trial_type_pass_view_b1 =[HW] * nHW + [NEG] * nNEG + [NEUT] * nNEUT  
    trial_type_pass_view_b2 =[HW] * nHW + [NEG] * nNEG + [NEUT] * nNEUT  

    random.shuffle(trial_type_pass_view_b1)
    random.shuffle(trial_type_pass_view_b2)


    
    #-----------------------------------------
    # Generate Lists for Inter Stim Intervals
    #-----------------------------------------    
    
    isi_gonogo_1 = random.sample(range(500, 800), len(trial_type_gonogo_b1)) # bloc 1 go nogo
    isi_gonogo_2 = random.sample(range(500, 800), len(trial_type_gonogo_b2)) # bloc 2 go nogo
    
    isi_pass_view_1 = random.sample(range(1500, 3000), len(trial_type_pass_view_b1)) # bloc 1 passive viewing
    isi_pass_view_2 = random.sample(range(1500, 3000), len(trial_type_pass_view_b2)) # bloc 2 passive viewing

    
   #--------------------------
   # Assign stim to to trial
   #--------------------------
   
   trig_GO = 101
   trig_NOGO = 103
   
   
   stim_trial_b1=[]
   trigger_code_b1=[]
  
   for i in range(len(trial_type_gonogo_b1)):
        if trial_type_gonogo_b1[i] == GO:
            stim_trial_b1 += [all_go_b1[i]]
            trigger_code_b1 += [trig_GO]
        
        if trial_type_gonogo_b1[i] == NOGO:
            stim_trial_b1 += [all_nogo_b1[i]]    
            trigger_code_b1 += [trig_NOGO]

   gng_b1 = {'Stim': stim_trial_b1, 'ISI': isi_gonogo_1, 'Code': trigger_code_b1}
    
   stim_trial_b2=[]
   trigger_code_b2=[]
  
   for i in range(len(trial_type_gonogo_b2)):
        if trial_type_gonogo_b2[i] == GO:
            stim_trial_b2 += [all_go_b2[i]]
            trigger_code_b2 += [trig_GO]
        
        if trial_type_gonogo_b2[i] == NOGO:
            stim_trial_b2 += [all_nogo_b2[i]]    
            trigger_code_b2 += [trig_NOGO]

   gng_b1 = {'Stim': stim_trial_b2, 'ISI': isi_gonogo_2, 'Code': trigger_code_b2}
   
                
            
genTrialList()        
    










