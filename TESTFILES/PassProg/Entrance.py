#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:58:08 2023

@author: Depp
"""
#%%
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
import copy
import datetime
import shlex
import math
import random
import traceback

sys.path.append(r'\\ezcamls\ezcam\sys\scripts\AutoCAM2.0')
sys.path.append("/InCAM/server/site_data/scripts/AutoCAM2.0")
sys.path.append(r"/genesis/sys/scripts/AutoCAM2.0")
#%% SET ROOT_PATH
from Utils import LOGIN
UID_KEY = 'KeyInYourUidHere' #key in uid if useing gateway in ezcam
LOGIN_DICT = LOGIN.get_login_dict(UID_KEY = UID_KEY)
# load ENV
for key , value in LOGIN_DICT.items():
    os.environ[key] = value
# set system PATH
for key in ["ROOT_PATH", "UTILS_PATH", "GEN_PATH"]:
    sys.path.append(os.environ[key])

# PATH CHANGE
os.chdir(os.path.dirname(os.path.abspath(__file__)))   

from Record import Record
from Utils import ENV_CONFIG
from Utils.UILauncher import Ui_Launcher
import genClasses 
#%% Set Enviromennt Variables
##Program call by MainUI. set ENV_VAR and CONFIG from MainUI
if len(sys.argv) > 2: 
    ENV_VAR = eval(sys.argv[1])
    CONFIG  = eval(sys.argv[2])

# set default value to ENV Variable.
else:
    CONFIG = {}
    PROGRAM= 'PassTest'
    LOG_PATH = os.path.join(os.path.dirname(__file__),'Tmp')
    ENV_VAR = ENV_CONFIG.get_enviroment_variable(PROGRAM, LOG_PATH)



for key, value in ENV_VAR.items():
    os.environ[key] = ENV_VAR[key]
#%% Import Main Program
from Model import main
from Controller import Controller


#%% SET Enviroment Variable

if __name__ == '__main__':
    '''==============================================================='''
    record = Record()  
    try:
        if os.environ['EXEC_MODE'] == 'Auto':
            #main model, without ui.
            main(CONFIG)  
            record.show_report()
        elif os.environ['EXEC_MODE'] == 'Manual':
             
            #call ui, if necessarsy.
            main(CONFIG)  
            record.show_report()
        elif os.environ['EXEC_MODE'] == 'Test':
            record.info('{0} : 程式連接正常'.format(ENV_VAR['PROGRAM']))
            record.is_exec = True
    except Exception, e:
        err_msg = traceback.format_exc()
        record.info(err_msg)
        record.error(str(e))



    record.end()
    # record.send_mail(ENV_VAR['PROGRAM'])
    sys.exit()
''' 
    something for debug
        job_name = os.environ['JOB']
        record.info(job_name)
        job_object = genClasses.Job(os.environ['JOB'])    
        step_object = genClasses.Step(job_object, 'pcb')  
        matrix_info = step_object.job.matrix.getInfo()
'''
# %%
