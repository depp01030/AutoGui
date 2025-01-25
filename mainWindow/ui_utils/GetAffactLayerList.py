#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 09:40:31 2023

@author: 220853
"""

import traceback

def get_affact_layer_list(step_object):
    layer_list = []
    try:
        step_object.COM('get_affect_layer')
        affect_layer_string = step_object.COMANS
        layer_list = affect_layer_string.split() 
    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)

    return layer_list
