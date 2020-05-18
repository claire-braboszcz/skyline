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
                    ica_bandpass_fmax, erp_bandpass_fmin,
                    erp_bandpass_fmax)



DOIT_CONFIG = dict(
    default_tasks=['epoch_pv', 'evoked_pv'],
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
            
           filt_ica_fname=fname.filt_ica(  subject='sub-'+ str(subj), 
                                            session='ses-'+str(sess), 
                                            fmin= ica_bandpass_fmin, 
                                            fmax= ica_bandpass_fmax)
    
           ica_fname = fname.ica(subject='sub-'+ str(subj),
                                  session='ses-'+str(sess))
            
           yield dict(
                    name = "%s-%s" % (subj, sess),  
                   # file_dep =['02-Run-ICA.py'], #filt_ica_fname, 
                    targets=[ica_fname], 
                    actions=['python3 02-Run-ICA.py %s %s' % (subj, sess)],                
                    )
    

    



def task_filter_erp():
    """Step 03: Bandpass-filter the data for ERP """

    for subj in subject_ids:
        for sess in sessions:
            
            raw_fname = fname.raw( subject='sub-'+ str(subj), 
                                   session='ses-'+str(sess))
            
            
            filt_erp_fname=fname.filt_erp(  subject='sub-'+ str(subj), 
                                            session='ses-'+str(sess), 
                                            fmin= erp_bandpass_fmin, 
                                            fmax= erp_bandpass_fmax)
    
            yield dict(
                    name = "%s-%s" % (subj, sess),  
                    file_dep =[raw_fname, '03-Filter-ERP.py'], 
                    targets=[filt_erp_fname], 
                    actions=['python3 03-Filter-ERP.py %s %s' % (subj, sess)],                
                    )
     
    
    



def task_epoch_pv():
    """Step 04: Epoch data for Passive viewing task  """

    for subj in subject_ids:
        for sess in sessions:
            
           
            filt_erp_fname = fname.filt_erp(subject='sub-'+ str(subj), 
                                            session='ses-'+str(sess), 
                                            fmin= erp_bandpass_fmin, 
                                            fmax= erp_bandpass_fmax)
            
            
            epochs_pv_fname = fname.epochs_pv(subject='sub-'+ str(subj), 
                                            session='ses-'+str(sess)
                                            )
            
        
            
            ica_fname = fname.ica(subject='sub-'+ str(subj),
                                  session='ses-'+str(sess))
            
            
            yield dict(
                    name = "%s-%s" % (subj, sess),  
                    file_dep =[filt_erp_fname, '04-Epochs-PV.py'], 
                    targets=[epochs_pv_fname,], 
                    actions=['python3 04-Epochs-PV.py %s %s' % (subj, sess)],                
                    )

def task_evoked_pv():
    """Step 05: Compute Evoked data for Passive viewing task  """

    for subj in subject_ids:
        for sess in sessions:
            
                      
            
           # epochs_pv_fname = fname.epochs_pv(subject='sub-'+ str(subj), 
           #                                 session='ses-'+str(sess)
           #                                 )
            
        
            evoked_pv_fname = fname.evoked_pv(subject='sub-'+ str(subj), 
                                            session='ses-'+str(sess)
                                            )
            
          
            
            
            yield dict(
                    name = "%s-%s" % (subj, sess),  
                    file_dep =[ '05-Evoked-PV.py'], #epochs_pv_fname,
                    targets=[evoked_pv_fname,], 
                    actions=['python3 05-Evoked-PV.py %s %s' % (subj, sess)],                
                    )




def task_epoch_gng():
    """Step 05: Epoch data for Go-NoGO task  """

    for subj in subject_ids:
        for sess in sessions:
            
           
            filt_erp_fname = fname.filt_erp(subject='sub-'+ str(subj), 
                                            session='ses-'+str(sess), 
                                            fmin= erp_bandpass_fmin, 
                                            fmax= erp_bandpass_fmax)
            
            
                       
            epochs_gng_fname = fname.epochs_gng(subject='sub-'+ str(subj), 
                                            session='ses-'+str(sess)
                                            )
            
            ica_fname = fname.ica(subject='sub-'+ str(subj),
                                  session='ses-'+str(sess))
            
            
            yield dict(
                    name = "%s-%s" % (subj, sess),  
                    file_dep =[filt_erp_fname, ica_fname,  '05-Epochs-GNG.py'], 
                    targets=[epochs_gng_fname], 
                    actions=['python3 05-Epochs-GNG.py %s %s' % (subj, sess)],                
                    )
   

   
