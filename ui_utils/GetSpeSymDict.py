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
# sys.path.append("/InCAM/server/site_data/scripts/AutoCAM2.0")
from InfoConverter.CAMClass import cam_tools
# from a import b
def get_spe_sym_dict(step_object, layer_list):
    spe_sym_dict = {}
    try:
        software = os.environ['SOFTWARE']
        # 得到當前affect_layer，gateway跑這條有機會爆，而script應該不會
        step_object.COM('get_affect_layer')
        affect_layer_string = step_object.COMANS

        layer_list = affect_layer_string.split()

        if len(layer_list) < 1:
            step_object.PAUSE('Not affect layer')
        else:
            spe_sym_dict = cam_tools.get_spe_sym_mapping_dict_from_cam(step_object, layer_list)

    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)

    return spe_sym_dict