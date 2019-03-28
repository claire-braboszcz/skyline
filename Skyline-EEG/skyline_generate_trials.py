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
    
    - 2 blocks of 212 stimuli; 82 NoGO, 205 GO
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
    
    # passive viewing
    for root, dirs, files in os.walk(filepath_pass_view, topdown=False):  # read files in folder
        pass_view_stimList = files

    hw_stim = [stim for stim in pass_view_stimList if health_warning(stim)]
    neg_stim = [stim for stim in pass_view_stimList if neg_pic(stim)]
    neut_stim = [stim for stim in pass_view_stimList if neut_pic(stim)]
    
    all_hw = hw_stim *n_rep_pv
    all_neg_stim = neg_stim*n_rep_pv
    neut_stim = neut_stim*n_rep_pv
    
    
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

   #--------------------------
   # Assign stim to to trial
   #--------------------------
    
  
    
   
    
    
    
    # create trials type
    #---------------------------------------------------------------------------------
    
    
    
    
    for trial in range(0, len(total_nogo)): # get list of pairs of go and nogo trials
        all_ng_trials += [[total_go[trial]] + [total_nogo[trial]]]  
    
    
    for trial in range(len(total_nogo)+1, nGo+1): # get list of pairs of remaining go trials
        all_other_go += [[total_go[trial]] + [total_go[trial+1]]]
        trial+= trial+1    
    
    all_trials=[]
    all_trials = all_ng_trials + all_other_go
    
    
   # while run_of_2(all_trials):
 #       random.shuffle(all_trials) # !!! need to check for many go between nogo
    
    
    
    
    
    all_trials = []
    all_blocks = []
    for block in range(nBlock):
    
            #writeTrials = csv.writer(open('block' + str(block+1) + '.csv', 'wb'), delimiter = ',', quotechar = '"')
            #header = ['Block', 'Stim', 'Condition']
            #writeTrials.writerow(header)
           
            all_blocks += [block]
            trial_type =[]
            
            #-----------------------------------------------------------------------------------
            # create trials and check for no more than 2 NOGO in a row and not starting by NoGo
            #-----------------------------------------------------------------------------------
            trial_type = [GO] * (nGoTrialBlock) + [NOGO]*nNoGoTrialBlock
            while run_of_2(trial_type, NOGO):
                random.shuffle(trial_type)
                    
            print(trial_type)        
            
            #--------------------------------
            # insert stimuli name in trials
            #-------------------------------
            # indices for stim name list
            indGo = 0
            indNoGo = 0
            trial=[]
            indBlock = str(block+1)
            
            for i in range (len(trial_type)):
                if trial_type[i] == GO :
                    stim = gostim[indGo]
                    trial = [indBlock, stim, 'Go']
                    indGo += 1
                    
                elif trial_type[i] == NOGO :
                    stim = nogostim[indNoGo]
                    trial = [indBlock, stim, 'NoGo']
                    indNoGo += 1 
                        
               all_trials += trial 
                
                #writeTrials.writerow(trial)
                
            
genTrialList()        
    










