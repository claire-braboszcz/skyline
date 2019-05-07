#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 14:07:59 2019

@author: claire
"""

import os.path as op
import mne

import numpy as np

file_path = '/media/claire/Skyline EEG/Data/Pilot_04_10/pilot_10_04.vhdr'

raw = mne.io.read_raw_brainvision(file_path, preload=True)

events, _ = mne.events_from_annotations(raw)
