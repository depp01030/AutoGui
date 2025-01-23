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
import shlex
import math
import traceback
    
import shutil
import subprocess
import datetime 
import platform 
import random
#%%
from LogParser import *
#%%
def get_text():
    log_text = """
    =========================================
    [Time]       : 2024-11-15 17:55:06
    [JobID]      : 1174073
    [JobName]    : advt-db011q
    [Time Spend] : 0.00290989875793 
    [State]      : Warning
    [StateCode]  : 300
    [User]       : incam-incam
    [Exec_ID]    : 781622
    [Program]    : Pass
    [ProgramVer] : 241008-4-1029
    [Software]   : incam 
    [Source]     : Customer
    [EXEC_MODE]  : Manual
    [TRversion]  : Test
    [Database]   : Dev
    ===================LOG=================== 
    [Info] : 2024-11-15 17:55:06 This is Program : Pass 
    [StepStart] : 2024-11-15 17:55:06 pcb : start 
    [Note] : 2024-11-15 17:55:06 this is not 
    [StepEnd] : 2024-11-15 17:55:06 pcb : Pass 
    [StepStart] : 2024-11-15 17:55:06 pcb1 : start 
    [Warning] : 2024-11-15 17:55:06 war 
    [Note] : 2024-11-15 17:55:06 this is not 
    [StepEnd] : 2024-11-15 17:55:06 pcb1 : Warning 
    [StepStart] : 2024-11-15 17:55:06 pcb2 : start 
    [Note] : 2024-11-15 17:55:06 this is not 
    [StepEnd] : 2024-11-15 17:55:06 pcb2 : Pass 
    [Note] : 2024-11-15 17:55:06 this is not 
    [Info] : 2024-11-15 17:55:07 End File 300 
    """
    return log_text


# %%

#%%

def get_log():

    file_name = 'Test_563888_ztem-lb002a-a1d01+2' + '.txt'
    folder_name = os.path.join(os.path.dirname(__file__), 'TESTFILES')
    file_path = os.path.join(folder_name, file_name)

    with open(file_path, 'r') as f :
        log = f.read()
    return log
def parse_job_log():    
    file_name = '4821278_hslc-lb016c-ping-line'
    folder_name = os.path.join(os.path.dirname(__file__), 'TESTFILES')
    file_path = os.path.join(folder_name, file_name)
    if os.path.isfile(file_path ):
        with open(file_path, "r") as f:
            tmp_job_logs = f.readlines()

        for tmp_job_log in tmp_job_logs:
            tmp_job_log_dict = eval(tmp_job_log)

            program_name  = tmp_job_log_dict['ProgramName']
            if program_name not in job_log_dict.keys():
                job_log_dict[program_name] = {
                    'ProgramState' : '',
                    'ExecID' : '',
                    'exec_log' : '',

                }    
            job_log_dict[program_name]['ProgramState'] = tmp_job_log_dict['ProgramState']
            job_log_dict[program_name]['ExecID'] = tmp_job_log_dict['ExecID']
def test():

    record_log = get_text()
    record_log.split('\n')
    msg_list = parse_record_log_list(record_log, pack_to_text_list)
    msg_list = parse_record_log_list(record_log)
        
    program_log_dict, is_end_properly = record_log_paser(record_log)
    
    db_log = create_db_log(program_log_dict)
# %%
            
def xxx():
    import re

    tmp_job_log_dict = {
            'LogTime' : program_log_dict["Time"],
            'JobID' : program_log_dict["JobID"],
            'JobName' : program_log_dict["JobName"],
            'RunTime' : program_log_dict["Time Spend"],
            'ProgramState' : program_log_dict["State"],
            'StateCode' : program_log_dict["StateCode"],
            'UserName' : program_log_dict["User"],
            'ExecID' : program_log_dict["Exec_ID"],
            'ProgramName' : program_log_dict["Program"],
            'ProgramVer' : program_log_dict["ProgramVer"],
            'Software' : program_log_dict["Software"],
            #'Source : program_log_dict["Source"],
            'ExecMode' : program_log_dict["EXEC_MODE"],
            'TRVer' : program_log_dict["TRversion"],
            'DB' : program_log_dict["Database"],
            'LogMsg' : program_log_dict["LogList"],
            'IsSave' : 0,
        } 
    tmp_job_log = str(tmp_job_log_dict) + '\n'

    tmp_job_log_folder = os.path.join(root_path, 'Tmp')
    if not os.path.isdir(tmp_job_log_folder) :
        os.mkdir(tmp_job_log_folder)

    tmp_job_log_name = '{0}_{1}'.format(tmp_job_log_dict['JobID'], tmp_job_log_dict['JobName'])
    tmp_job_log_file_path = os.path.join(tmp_job_log_folder, tmp_job_log_name)

    file_name = 'dsadfasdf' + '.txt'
    folder_name = os.path.join(os.path.dirname(__file__), 'TESTFILES')
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, "a") as f:
        f.write(tmp_job_log)
    with open(file_path, 'r') as f :
        job_logs = f.readlines()

#%%
def _replace_check_info(self):
    file = open(self.file_path, "r")
    file_log = file.read()
    file.close()   
    filter_log_list, replaced_log = filter_n_replace_check_log(file_log)
    self.info(filter_log_list)
    file = open(self.file_path, "w")
    file.write(replaced_log)
    file.close()    
    return filter_log_list
def test_filter_check():
 
    record_log = u"""========================================= 
    [Time]       : 2024-10-23 17:58:40
    [JobID]      : 6812081
    [JobName]    : athr-lb003y-a1d01-outersliver
    [Time Spend] : 0.0039370059967 
    [State]      : Error
    [StateCode]  : 500
    [User]       : incam-incam
    [Exec_ID]    : 803304
    [Program]    : LogTest
    [ProgramVer] : 241022-1-1407
    [Software]   : incam 
    [Source]     : Design
    [EXEC_MODE]  : Manual
    [TRversion]  : Test
    [Database]   : Dev
    ===================LOG=================== 
    [StepStart] : 2024-10-23 17:58:40 pcb : start 
    [Warning] : 2024-10-23 17:58:40 This is Warning
    [StepEnd] : 2024-10-23 17:58:40 pcb1 : Pass 
    [StepStart] : 2024-10-23 17:58:40 pcb2 : start 
    [Info] : 2024-10-23 17:58:40 this is info 
    [Note] : 2024-10-23 17:58:40 This is Program : Pass  
    [StepEnd] : 2024-10-23 17:58:40 pcb2 : Warning 
    [StepStart] : 2024-10-23 17:58:40 pcb3 : start 
    [Error] : 2024-10-23 17:58:40 Traceback (most recent call last):
    File "/InCAM/server/site_data/scripts/AutoCAM2.0/Test/Main_LogTest/Test/LogTest-241022-1-1407/Model.py", line 43, in main
        print(10/0)
    ZeroDivisionError: integer division or modulo by zero
    
    [Error] : 2024-10-23 17:58:40 Traceback (most recent call last):
    File "/InCAM/server/site_data/scripts/AutoCAM2.0/Test/Main_LogTest/Test/LogTest-241022-1-1407/Model.py", line 43, in main
        print(10/0)
    ZeroDivisionError: integer division or modulo by zero

    [Check] : 2024-10-23 17:58:41 End File 500 
    [Check] : 2024-09-13 09:05:24 1153415
    63
    [Info] : 2024-09-13 09:05:35 Post data to service start 
    [Info] : 2024-09-13 09:05:50 Post data to service end 
    [Checked] : 2024-09-13 09:05:54 pth-board_thick_5.0736
    [Warning] : 2024-09-13 09:05:54 pth-board_thick_5.07365-
    [Info] : 2024-09-13 09:05:54 Step : panel finish  
    [Check] : 2024-09-13 09:05:54 Output Path : /InCAM/server/site_data/scrip
    [Info] : 2024-09-13 09:06:03 End File 200
    """ 


    record_log_list = record_log.split('\n') 
    replace_log = ''
    filter_log_list = []
    is_in_msg = False
    for i, log in enumerate(record_log_list):        
        if log == '':
            continue
        # if '[Check]' in log:
        #     filter_log_list.append(log)
        #     record_log_list[i] = log.replace('[Check]', '[Checked]')

        if '[Info]' in log :
            is_in_msg = False
        elif '[Check]' in log :     
            is_in_msg = True       
            msg = ' '.join(log.split(' ')[4:])
            msg = '[Check] : ' + msg
            log = log.replace('[Check]', '[Checked]') 
        elif '[Checked]' in log :
            is_in_msg = False
        elif '[Warning]' in log :
            is_in_msg = False 
        elif '[Error]' in log :
            is_in_msg = False 
        else:
            msg = log
            
        if is_in_msg:
            filter_log_list.append(msg)

        replace_log += log +'\n'

    return filter_log_list, replace_log

eval(str('[{"UserName": "incam-incam", "IsSave": 1, "ExecID": "121603", "TRVer": "Test", "LogTime": "2024-11-13 09:19:18", "ProgramVer": "241017-1-1408", "ExecMode": "Manual", "LogMsg": [{"msg_list": ["\xe4\xb8\xad\xe6\x96\x87info "], "type": "Info", "datetime": "2024-11-13 09:19:18"}, {"msg_list": ["\xe9\x80\x99\xe6\x98\xaf checkinfo 1 "], "type": "Checked", "datetime": "2024-11-13 09:19:18"}, {"msg_list": ["This is checkinfo 2 "], "type": "Checked", "datetime": "2024-11-13 09:19:18"}, {"msg_list": ["\xe4\xb8\xad\xe6\x96\x87 is checkinfo 2 "], "type": "Checked", "datetime": "2024-11-13 09:19:18"}, {"msg_list": ["This is checkinfo 3 "], "type": "Checked", "datetime": "2024-11-13 09:19:19"}, {"msg_list": ["\xe9\x80\x99\xe6\x98\xaf note "], "type": "Note", "datetime": "2024-11-13 09:19:19"}, {"msg_list": ["\xe9\x80\x99\xe6\x98\xaf\xe8\xad\xa6\xe5\x91\x8a "], "type": "Warning", "datetime": "2024-11-13 09:19:20"}, {"msg_list": ["", "jdsiofjoasd", "jsdoifjsdiofjsd", "sjdofidjsiofjdsojsd", "sjdoifjsdiofjosdfij "], "type": "Warning", "datetime": "2024-11-13 09:19:20"}, {"msg_list": ["End File 300 ", ""], "type": "Info", "datetime": "2024-11-13 09:19:23"}], "DB": "Dev", "JobID": "1174073", "Software": "incam", "StateCode": "300", "ProgramName": "RecordCheck", "ProgramState": "Warning", "RunTime": "1.78237509727", "JobName": "advt-db011q"}, {"UserName": "incam-incam", "IsSave": 1, "ExecID": "655362", "TRVer": "Test", "LogTime": "2024-11-13 09:24:01", "ProgramVer": "241011-7-1037", "ExecMode": "Manual", "LogMsg": [{"msg_list": ["157815 "], "type": "Info", "datetime": "2024-11-13 09:24:02"}, {"msg_list": ["Traceback (most recent call last):", "  File "/InCAM/server/site_data/scripts/AutoCAM2.0/Test/Main_Error/Test/Error-241011-7-1037/Model.py", line 39, in main", "    print(10/0)", "ZeroDivisionError: integer division or modulo by zero", " "], "type": "Error", "datetime": "2024-11-13 09:24:02"}, {"msg_list": ["End File 500 ", ""], "type": "Info", "datetime": "2024-11-13 09:24:03"}], "DB": "Dev", "JobID": "1174073", "Software": "incam", "StateCode": "500", "ProgramName": "Error", "ProgramState": "Error", "RunTime": "1.06642007828", "JobName": "advt-db011q"}]'))

b = '''[{"ProgramVer": "241011-7-1037", "ExecMode": "Manual", \
"LogMsg": [{"msg_list": ["157815 "], "type": "Info", "datetime": "2024-11-13 09:24:02"},\
    {"msg_list": ["Traceback (most recent call last):", \
    "  File '/InCAM/server/site_data/scripts/AutoCAM2.0/Test/Main_Error/Test/Error-241011-7-1037/Model.py', line 39, in main", "    print(10/0)", "ZeroDivisionError: integer division or modulo by zero", " "],\
        "type": "Error", "datetime": "2024-11-13 09:24:02"}],"Software": "incam", "StateCode": "500"}]'''
a = '''[{"USER" : "  FILE "FILE ", in "}]'''
b = '''[{"USER" : '  FILE "FILE ", in '}]'''
eval(b)