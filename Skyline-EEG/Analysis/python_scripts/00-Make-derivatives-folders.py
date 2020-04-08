#!/usr/bin/env python
# coding: utf-8

# In[ ]:

"""
Create BIDS-compatible derivatives folder for each participant

"""

import os

from config import (fname, bids_root, bids_root_der)
import argparse



# Handle command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('subject', metavar='subj', help='The subject to process')
parser.add_argument('session', metavar='sess', help='The session to process')

args = parser.parse_args()
subj= args.subject
sess= args.session


print('Making folders for subject:', subj, 'session:', sess)


f_preproc=fname.folder_preproc(bids_root_der=bids_root_der, subject='sub-'+ str(subj), session='ses-'+str(sess))
f_gonogo=fname.folder_gonogo(bids_root_der=bids_root_der, subject='sub-'+ str(subj), session='ses-'+str(sess))
f_passview=fname.folder_passview(bids_root_der=bids_root_der, subject='sub-'+ str(subj), session='ses-'+str(sess))



if not os.path.exists(f_preproc):
    os.makedirs(f_preproc)

if not os.path.exists(f_gonogo):
    os.makedirs(f_gonogo)


if not os.path.exists(f_passview):
    os.makedirs(f_passview)


