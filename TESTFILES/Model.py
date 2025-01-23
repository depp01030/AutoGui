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
#%%
def main(CONFIG):
    try: 
        gen_object = genClasses.Top()
        # job_name = os.environ['JOB']
        # job_object = genClasses.Job(os.environ['JOB'])    
        # step_object = genClasses.Step(job_object, 'pcb')  
        # matrix_info = step_object.job.matrix.getInfo()
        record.info('中文info') 
        record.check_info('這是 checkinfo 1') 
        record.check_info('This is checkinfo 2') 
        record.check('中文 is checkinfo 2') 
        record.check_info('This is checkinfo 3') 

        record.note('這是 note') 
        record.check_point('This is checkinfo 3') 
        record.warning('這是警告') 

        record.warning('''
jdsiofjoasd
jsdoifjsdiofjsd
sjdofidjsiofjdsojsd
sjdoifjsdiofjosdfij''') 

    except Exception, e:
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