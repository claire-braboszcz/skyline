#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:58:27 2020

@author: claire
"""

from scipy import interpolate
import mne
import numpy as np
from sklearn.model_selection import LeaveOneOut



# for jaccknife approach to erp latency 

def get_average_erp_leave_one_out(evokeds, n_groups, elecs):
    '''
     evokeds: evoked object or list of evoked objects
     n_groups: size of list 
     elecs: 
    '''
   

    
    gd_ave_erp=[list() for _ in range(n_groups)]
        
    loo=LeaveOneOut()      
        
    for ind, erp in enumerate(evokeds):
    
        loo.get_n_splits(erp)
        
        # get series of grand average with leave-one-out
        for idx in loo.split(erp):
            print(idx)
            evokeds_loo=[]
            
            for j in idx[0]:
                evokeds_loo.append(erp[j].pick_channels(elecs).
                                   apply_baseline((None, 0)))
                print(idx[0])
                
            gd_ave_erp[ind].append(mne.grand_average(evokeds_loo))

    return(gd_ave_erp)
    
    
    
def get_frac_peak_latency(gd_ave_erp, n_group, tmin, tmax, peak_frac, sfreq):

    '''
    find fractional peak latency:
    for each grand average estimate onset latency by identifying peak amplitude
    onset, which is the first point in that time window in which amplitude exceeds
    50% of peak score       
    
    
    gd_ave_erp: evoked object or list of evoked objects
    n_groups: size of list 
    tmin, tmax: tmin and tmax for erp window to consider
    sfreq: sampling frequency of the data
    
    '''



#min(np.absolute(np.cumsum(erp)-sum(erp)/2))

# centroparietal electrodes (no CPz on montage)
   
    
    all_onsets_latency=[list() for _ in range(n_group)]#*len(gd_ave_erp[0]) #  save onsets for each condition
    
    
    for n in range(0, len(gd_ave_erp)):
    
        for idx, erp in enumerate(gd_ave_erp[n]):
            
            #erp=np.mean(erp.data, axis=0)
            
            # get peak latency and amplitude
            channel,  latency, amplitude= erp.get_peak(tmin=tmin, tmax=tmax,  return_amplitude=True)  
           
            onsetCutOff = peak_frac*amplitude     
               
            dataShifted = erp.data - onsetCutOff # substract onsetcutoff from data to find where it reaches 0
        
            interpolator = interpolate.UnivariateSpline(np.arange(-1.004,1.,1./sfreq),dataShifted,s=sfreq)   # interpolate points
            
            print(interpolator.roots())
            latency_onsetCutOff= interpolator.roots().mean()
            
            all_onsets_latency[n].append(latency_onsetCutOff)
          
            
    return(all_onsets_latency)
    


