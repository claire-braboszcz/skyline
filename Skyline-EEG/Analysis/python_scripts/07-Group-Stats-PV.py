#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 10:04:06 2020

@author: claire
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

import mne
from mne.channels import find_ch_connectivity, make_1020_channel_selections
from mne.stats import spatio_temporal_cluster_test


