#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
Execute the Skyline EEG analysis pipeline

Uses do-it

http://pydoit.org

filenames are defined in config.py

Author: Claire Braboszcz
Adapted from Marijn van Vliet


"""



from config import (fname, subject_ids, sessions, ica_bandpass_fmin,
                    ica_bandpass_fmax)



DOIT_CONFIG = dict(
    default_tasks=['run_ica'],
    verbosity=2, sort='alphabetical',
)


def task_make_derivative_folders():
        """Step 00: Create folder architecture """
        
        for subj in subject_ids:
            for sess in sessions:
                #import pdb; pdb.set_trace()
                
                yield dict(
                        name = "%s-%s" % (subj, sess), 
                        actions=['python3 00-Make-derivatives-folders.py %s %s' % (subj, sess)],
                        
                                               
                        
                        )



def task_filter_ica():
    """Step 01: Bandpass-filter the data for ICA """

    for subj in subject_ids:
        for sess in sessions:
            
            raw_fname = fname.raw( subject='sub-'+ str(subj), 
                                   session='ses-'+str(sess))
            
            
            filt_ica_fname=fname.filt_ica(  subject='sub-'+ str(subj), 
                                            session='ses-'+str(sess), 
                                            fmin= ica_bandpass_fmin, 
                                            fmax= ica_bandpass_fmax)
    
            yield dict(
                    name = "%s-%s" % (subj, sess),  
                    file_dep =[raw_fname, '01-Filter-raw-for-ICA.py'], 
                    targets=[filt_ica_fname], 
                    actions=['python3 01-Filter-raw-for-ICA.py %s %s' % (subj, sess)],                
                    )
    



def task_run_ica():
    """Step 02: Run ICA and reject eye-movements related IC """

    for subj in subject_ids:
        for sess in sessions:
            
            filt_ica_fname = fname.filt_ica(subject='sub-'+ str(subj), 
                                            session='ses-'+str(sess), 
                                            fmin= ica_bandpass_fmin, 
                                            fmax= ica_bandpass_fmax)
    
            ica_fname = fname.ica(subject='sub-'+ str(subj),
                                  session='ses-'+str(sess))
            
            yield dict(
                    name = "%s-%s" % (subj, sess),  
                    file_dep =[filt_ica_fname, '02-Run-ICA.py'], 
                    targets=[ica_fname], 
                    actions=['python3 02-Run-ICA.py %s %s' % (subj, sess)],                
                    )
    




