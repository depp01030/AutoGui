#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
#os.environ["UTILS_PATH"] = "/InCAM/server/site_data/scripts/gen_py/"
#os.environ["UTILS_PATH"] = r"\\192.168.1.63\ezcam\1.1\resource\python"
import sys
import time
import requests
import re
import copy
from datetime import datetime
import shlex
import math
import random
from PyQt4 import QtGui
import json
import random
import traceback
import socket
hostname = socket.gethostname() 
os.chdir(os.path.dirname(os.path.abspath(__file__)))   

'=====================  Script  ==========================='
IES_USER_LIST = ['210605','220920', '210814', '220741', '220853', '220741', 'IESAdmin']
if os.environ['USER'] in IES_USER_LIST:
    sys.path.append("//192.168.1.63/ezcam/1.1/resource/python")
    os.environ["UTILS_PATH"] = r"\\ezcamls\ezcam\1.1\resource\python"
    os.environ['DISPLACE_DB'] = 'USER'

elif os.environ['USER'] in ['incam', 'root' ]:
    os.environ["UTILS_PATH"] = "/InCAM/server/site_data/scripts/gen_py/"
    os.environ['DISPLACE_DB'] = 'USER'
else:
    if hostname == 'incam4':
        os.environ['DISPLACE_DB'] = 'DEV'
    else:
        os.environ['DISPLACE_DB'] = 'USER'
    os.environ["InCAM_DIR"]  = "/InCAM/2.1SP1"
    os.environ["InCAM_EDIR"] = "/InCAM/2.1SP1/bin"
    os.environ["UTILS_PATH"] = "/sw/sys/scripts/gen_py"
os.environ['PROGRAM_ID'] = ''
sys.path.append(os.environ["UTILS_PATH"])

import genClasses   
from utils import Record
print('===================================')
# from utils import camjob2mes, create_layer


def main(work_layer_list = []):
    try:
        '''
        os.environ['JOB'] = 'syno-ot0001-juri'  #
        os.environ['JOB'] = "mtkx-lb008f-a1d01-juri"
        os.environ['JOB'] = 'zeku-pd0002-v1d01-juri'
        os.environ['JOB'] = 'qctx-pc003n-juri'
        os.environ['JOB'] = "mtkx-ot001b-a1d01-secco2"
        '''




        print(r'enter : {0}'.format(__file__)) 
        
        job_name = 'abcd-xxxxx-vadbc-juri'
        job_id   = '32113'

    #    ver = os.path.basename(os.path.dirname(__file__))
        record = Record(__file__, os.environ['PROGRAM_ID'])
 

        log_list = ['[Info] : xxx \n',
                    '[Warning] : xxx \n',
                    '[Error] : xxx \n']
        

        for _ in range(random.randint(0,3)):
            log = log_list[0]    
            record.info(log) 
        if random.uniform(0,1) > 0.7:
            for _ in range(random.randint(1,2)):
                log = log_list[1]
                record.warning(log) 
        if random.uniform(0,1) > 0.8:
            log = log_list[2]
            record.error(log)
        text =str(os.environ.keys())
        job_object = genClasses.Job(os.environ['JOB'])    
        
        step_object = genClasses.Step(job_object, 'pcb')  



        record.info('EndFile') 
        print(record.file_path)

    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)
        record.error(str(err_msg))
if __name__ == '__main__':
    print(sys.argv)
    PROGRAM_ID = ''
    work_layer_list = []  
    if len(sys.argv) > 2:
        PROGRAM_ID = sys.argv[1] 
        work_layer_list = sys.argv[2]
    os.environ['PROGRAM_ID'] = PROGRAM_ID
    main(work_layer_list)
 