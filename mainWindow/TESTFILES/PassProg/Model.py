#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import shlex
import math
import random

import datetime

import traceback
import socket

import genClasses  
from Record import Record
record = Record() 
sys.path.append(r'D://AutoCAM//Dev')
from InfoConverter.CAMClass import CAMTools, CAMwkt, CAMCollection, CAMPad
from InfoConverter.InfoConverterUtils import (JobInfoCollector, 
                                              FileTools)
from InfoConverter.InfoConverterAPI import create_layer_by_collection


if 'GEOM_SERVICE' in os.environ.keys():
    SERVICE_ROOT =   os.environ['GEOM_SERVICE'] + 'cam/info_converter/'
else:
    SERVICE_ROOT = 'http://ws125:3125/cam/info_converter/' #main    
# SERVICE_ROOT = 'http://ws125:3114/dev/' #old
# SERVICE_ROOT = 'http://ws125:3114/cam/info_converter/dev/'
# SERVICE_ROOT = 'http://ws125:3124/cam/info_converter/test/'
# SERVICE_ROOT = 'http://ws125:3125/cam/info_converter/' #main

#%%
def main(CONFIG):
    try: 
        job_object = genClasses.Job(os.environ['JOB'])
        step_object = job_object.steps[os.environ['STEP']]
        # job_name = os.environ['JOB']
        # job_object = genClasses.Job(os.environ['JOB'])    
        # step_object = genClasses.Step(job_object, 'pcb')  
        # file_name = 'all_return_dict.json'
        # file_path = os.path.join(os.getcwd(), file_name)
        # with open(file_path, 'r') as f:
        #     all_dict = json.load(f)

        # tmp_collection = CAMwkt.load(all_dict['ref_l18_comp'])
        
        # for layer_name, wkt in all_dict.items():
        #     tmp_collection = CAMwkt.load(wkt)
        #     create_layer_by_collection(cur_object, tmp_collection,
        #                                 layer_name,
        #                                 added_attr_list = ['.string'])
        # matrix_info = step_object.job.matrix.getInfo()\


        # sym = 'donut_r90x4'
        # layer_name = 'test_donut'
        # tmp_collection = CAMCollection()
        # tmp_collection.add(CAMPad([3,3],sym = 'donut_r14.6x4'))
        # tmp_collection.add(CAMPad([3,3],sym = 'donut_r13x4'))
        # tmp_collection.add(CAMPad([3,3],sym = 'donut_r15x4'))
        # tmp_collection.add(CAMPad([3,3],sym = 'donut_r90x4')) 
        # create_layer_by_collection(cur_object, tmp_collection,
        #                             layer_name,
        #                             added_attr_list = ['.string'])
        
        r = requests.get(os.environ['GEOM_SERVICE'])
        record.PAUSE(os.environ['GEOM_SERVICE'])
    except Exception as  e:
        err_msg = traceback.format_exc()
        record.info(err_msg)
        record.error(str(e))
        
        print(err_msg)
    return 
    

#%%
if __name__ == '__main__':
    print('*******************************************')
    CONFIG = {}
    main(CONFIG)






