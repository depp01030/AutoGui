#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 09:40:31 2023

@author: 220853
"""

import os
import sys
import time
try:
    # no module in py23
    import requests
    import json
except:
    pass
import re
import traceback

def get_FeatureInfo_AffectLayer(step_object, affect_layer_list, suffix = None):
    # job_name = step_object.job.name
    # step = step_object.name

    software = os.environ['SOFTWARE']
    # 得到當前affect_layer，gateway跑這條有機會爆，而script應該不會
    step_object.COM('get_affect_layer')
    comans_affect_layer = step_object.COMANS
    affect_layer_check = False

    affect_layer_dict = {}

    '''
    if 'genesis' in software:
        if comans_affect_layer != '':
            affect_layer_check = True
    else:
        if comans_affect_layer != ' ':
            affect_layer_check = True

    if affect_layer_check:
        # 'l2 l3 l4 l5'
        affect_layer_list = comans_affect_layer.split()

        for affect_layer in affect_layer_list:
            affect_layer_dict[affect_layer] = \
                step_object.INFO("-t layer -e {0}/{1}/{2} -d FEATURES -m script".\
                                format(step_object.job.name, step_object.name, affect_layer))

    else:
        step_object.PAUSE('no affected layer')
    '''

    if len(affect_layer_list) > 0:
        for affect_layer in affect_layer_list:
            affect_layer_dict[affect_layer] = \
                step_object.INFO("-t layer -e {0}/{1}/{2} -d FEATURES -m script".\
                                format(step_object.job.name, step_object.name, affect_layer))

    else:
        pass
    return affect_layer_dict


'''
matrix_info = step_object.job.matrix.getInfo()

PITCH_DICT = PitchConfig.PITCH_DICT # not need matrix_info

# ===== not need matrix_info =====
# cu_thick_dict # get from mes
job_name = step_object.job.name
cu_thick_dict =  get_cu_thick_dict(job_name)

# press_range # get from mes?

# profile info # get from step info
profile_info_dict = step_object.DO_INFO('-t step -e %s/%s -d PROF_LIMITS -m script'\
                                        % (step_object.job.name, step_object.name))
# is_big_panel # get from step info & from mes
is_big_panel = get_is_big_panel(step_object)

# ===== need matrix_info =====
# drill_layer_dict
drill_layer_dict = get_drill_layer_dict(step_object)
# region_layer_dict
region_layer_dict = get_region_layer_dict(step_object)
# neg_layer_dict
neg_layer_dict = get_neg_layer_dict(step_object)
# # 各層別組抗線資訊



# record.info(' ===== neg_layer_dict ===== ')
# record.info(neg_layer_dict.keys())


'''