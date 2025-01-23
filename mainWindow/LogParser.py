#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import traceback
import re

SEVERITY_TO_STATE = {
    0 : 'Pass',
    1 : 'Pass',
    2 : 'Warning',
    3 : 'Error'
}    
SEVERITY = {
    'Info'       : 0,
    'Note'       : 1,
    'StepStart'  : 1,
    'StepEnd'    : 1,
    'Pause'      : 0,
    'Checked'    : 0,
    'Check'      : 0,
    'Warning'    : 2,
    'Error'      : 3,
}   


def record_log_reader(main_folder_path,
                       TR_ver,
                       exec_id,
                       job_name ):
    '''
    STATE_DICT : { 1 : 'Pass',
                    2 : 'Warning',
                    3 : 'Error'}     
    file_name = 'Test_239416_mtkx-md0036-a1d01-auto.txt'
    file_path = os.path.join(os.getcwd(), 'TESTFILES', file_name)
    '''
    file_path = ''
    raw_prog_log = ''
    try:
        tmp_log_folder = os.path.join(main_folder_path, 'Tmp')  
        file_name = '{0}_{1}_{2}.txt'.format(TR_ver, exec_id, job_name) #Same from Record.
        file_path = os.path.join(tmp_log_folder,file_name) 
        
        if not os.path.isfile(file_path):    
            return raw_prog_log, file_path
        
        with open(file_path, "r") as f:
            raw_prog_log = f.read()
        return raw_prog_log, file_path
    except Exception as e:
        err_msg = traceback.format_exc() 
        print(err_msg)
        return raw_prog_log, file_path

def record_log_paser(record_log):
    program_log_dict = {
        'Time'       : '',
        'JobID'      : '',
        'JobName'    : '',
        'Time Spend' : '',
        'State'      : 'Error',
        'StateCode'  : '506',
        'User'       : '',
        'Exec_ID'    : '',
        'Program'    : '',
        'ProgramVer' : '',
        'Software'   : '',
        'Source'     : '',
        'EXEC_MODE'  : '',
        'TRversion'  : '',
        'Database'   : '',
        'LogList'     : '',
    }
    if record_log == '':
        return program_log_dict
    record_log_list = record_log.split('\n')

    # =============== Write msg_dict ===============
    idx = -1
    pattern = r"\[(.*)\]"
    is_end_properly = False
    while idx < len(record_log_list):
        idx += 1
        line_text = record_log_list[idx]
        if '====LOG===' in line_text:
            break

        split_text_list = line_text.split(':')
        if len(split_text_list) < 2:
            continue
        #get key
        reg = re.search(pattern, split_text_list[0])
        if reg is None:
            continue
        text_key = reg.group(1)
        #get value
        value = ':'.join(split_text_list[1:]).strip()        
        if text_key not in program_log_dict.keys():
            continue

        #set key value
        print(text_key, value)
        program_log_dict[text_key] = value
    
    program_log_dict['LogList'] = parse_record_log_list(record_log_list[idx:])
    
    if 'End File' in record_log_list[-2] or 'End File' in record_log_list[-1]:
        is_end_properly = True
    return program_log_dict, is_end_properly        
    # msg_log = ''
    # for msg_idx in range(idx, len(raw_prog_log_list)):
    #     log = raw_prog_log_list[msg_idx]
    #     if 'End File' in log: 
    #         state_code = str(int(log.split('End File')[-1].strip()))
    #     if '[Info]' in log:
    #         state_level = max(state_level, 1)
    #         # msg_dict['Info'].append(log.strip())
    #         msg_log += log.strip() + '\n'
    #     elif '[Warning]' in log:
    #         state_level = max(state_level, 2)
    #         # msg_dict['Warning'].append(log.strip())
    #         msg_log += log.strip() + '\n'
    #     elif '[Error]' in log:
    #         state_level = max(state_level, 3)
    #         # msg_dict['Error'].append(log.strip())
    #         # state_code = '500'
    #         msg_log += log.strip() + '\n'

    # if state_code[0] == '5':
    #     state_level = 3
    # program_log_dict['StateCode'] = state_code
    # ##==============================================
    # return raw_prog_log, STATE_DICT[state_level], msg_log, state_code
def create_db_log(program_log_dict):
    #permanent program log
    db_log = {
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
    return db_log
def parse_db_log_to_execute_log(db_log):
    '''
    db_log = {
            'LogTime' : '0',#
            'JobID' : '0',
            'JobName' : '0',
            'RunTime' : '0',
            'ProgramState' : '0',#
            'StateCode' : '0',#
            'UserName' : 'incam-incam',#
            'ExecID' : '0',
            'ProgramName' : '0',
            'ProgramVer' : '0',
            'Software' : '0',
            #'Source : '0',
            'ExecMode' : '0',
            'TRVer' : '0',
            'DB' : '0',
            'LogMsg' : [],#
            'IsSave' : '0',
        } 
    '''
    execute_log = ''
    execute_log_header = '''------- {0} -------
使用者 : {1}
執行時間 : {2}  秒
執行狀態 : {3}, Code : {4}
'''.format(db_log['LogTime'], db_log['UserName'].split('-')[1],
            round(float(db_log['RunTime']), 3),
            db_log['ProgramState'], db_log['StateCode']  
            ) 
    visit_step_mark_list = [] #it should be
    step_state_map = {}
    execute_log_body = ''

    ''' ==================== parse LogMsg ======================= '''
    for msg in db_log['LogMsg']:
        msg_type = msg['type']
        if not execute_log_type_filter(msg_type):
            continue  
        
        #get msg_text
        msg_text = ''
        
        # for text in msg['msg_list']:
        #     msg_text +=  text + '\n' 
        msg_text = '\n'.join(msg['msg_list'])
        #handle step state issue
        if msg_type == 'StepStart':
            cur_step, cur_step_state = msg_text.split(' : ')
            step_state_map[cur_step] = cur_step_state
            visit_step_mark_list.append(cur_step)
            continue
        if msg_type == 'StepEnd':
            cur_step, cur_step_state = msg_text.split(' : ')
            step_state_map[cur_step] = cur_step_state
            continue
    
    
        msg_body = '\n{0} : {1}'
        execute_log_body += msg_body.format(msg_type, msg_text)
    # print('this is log body before : ')
    # print(execute_log_body)
    # execute_log_body = execute_log_body.decode('unicode_escape').encode('utf-8')
    # print('this is log body : ')
    # print(execute_log_body)
    ## add step_state into header ##
    step_state_header = ''
    for step_name in visit_step_mark_list:
        step_state = step_state_map[step_name]
        if 'start' in step_state:
            step_state = 'Error'
        step_state_header += "STEP 狀態 {0} : {1} \n".format(step_name, step_state)

    execute_log += execute_log_header
    execute_log += step_state_header
    execute_log += '執行訊息 : '
    execute_log += execute_log_body 
    
    
    # execute_log = ''     
    # msg_text = '\u9019\u908a' 
    # msg_text.encode('unicode_escape')
    
    # execute_log+= msg_text

    # utf8_data = execute_log.encode('utf-8')
    
    return execute_log

def execute_log_type_filter(msg_type):
    if msg_type in ['StepStart', 'StepEnd', 'Note', 'Warning', 'Error']:
        return True
    return False


def write_perm_prog_log(main_folder_path,
                        db_log):
    try:
        perm_prog_log = str(db_log)  + '\n'
        perm_prog_log_name = '{0}_{1}.txt'.format(db_log['TRVer'], db_log['JobID'])
        perm_prog_log_file_path = os.path.join(main_folder_path, 'Log', perm_prog_log_name)
        with open(perm_prog_log_file_path, "a") as f:
            f.write(perm_prog_log)

    except Exception as e:
        err_msg = traceback.format_exc() 
        print(err_msg)

def write_tmp_job_log(root_path,
                      db_log):
    try:
        
        tmp_job_log = str(db_log) + '\n' 
        
        tmp_job_log_folder = os.path.join(root_path, 'Tmp')
        if not os.path.isdir(tmp_job_log_folder) :
            os.mkdir(tmp_job_log_folder)

        tmp_job_log_name = '{0}_{1}'.format(db_log['JobID'], db_log['JobName'])
        tmp_job_log_file_path = os.path.join(tmp_job_log_folder, tmp_job_log_name)
        with open(tmp_job_log_file_path, "a") as f:
            f.write(tmp_job_log)
    except Exception as e:
        err_msg = traceback.format_exc() 
        print(err_msg)
        
def load_db_logs(
        job_id,
        job_name):  
    
    pass
def load_tmp_db_logs(root_path,
                      job_id,
                      job_name):
    '''
    tmp_job_log_file_path = r'D:\AutoCam\AutoCAM2.0\mainWindow\TESTFILES\1663490_qctx-ot0075-pth-cnc'
    '''
    tmp_db_logs = []
    # load from db

    # load from tmp_job_log
    tmp_job_log_folder = os.path.join(root_path, 'Tmp')
    if not os.path.isdir(tmp_job_log_folder) :
        os.mkdir(tmp_job_log_folder)
        
    tmp_job_log_name = '{0}_{1}'.format(job_id, job_name)
    tmp_job_log_file_path = os.path.join(tmp_job_log_folder, tmp_job_log_name)
    if not os.path.isfile(tmp_job_log_file_path ):
        return tmp_db_logs

    with open(tmp_job_log_file_path, "r") as f:
        tmp_job_logs = f.readlines()

    for tmp_job_log in tmp_job_logs:
        try:
            tmp_db_log = eval(tmp_job_log)
        except:
            continue
        tmp_db_logs.append(tmp_db_log)
    return tmp_db_logs
#%% 
def parse_record_log_list(record_log,
                        pack_info_func = None):
    '''
    input : program_log -> raw string with '\n'

    output: log_list -> '[Warning] : 2023-07-24 15:47:21  war ' -> 'war'
    pack_info_func = pack_to_text_list
    '''

    if pack_info_func is None:
        pack_info_func = pack_to_msg_list

    if isinstance(record_log, list):
        program_log_list = record_log
    else:
        program_log_list = record_log.split('\n') 
    # print('after', 'type : ', type(program_log_list), program_log_list)
    pattern = r'\[(\w+)\]\s*:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*(.*)'
    # Find all matches in the log text
    
    
    log_list = []
    is_in_msg = False
    # for i, log in enumerate(program_log_list):
    length = len(program_log_list)
    cur_info = []
    i = 0
    while (i < length):

        line_text = program_log_list[i]
    
        matches = re.findall(pattern, line_text)
        if len(matches) == 0 or  matches[0][0] == 'Time':
            # handle in msg case
            if is_in_msg:
                cur_info.append(line_text)
            i += 1
            continue        
        # get new info now
        if is_in_msg:
            #handle msg that has been caught
            packed_info = pack_info_func(cur_info)
            if is_not_empty(packed_info):       
                log_list.append(packed_info)
            #refresh cur_info
            cur_info = [] 
             

        if matches[0][0] not in SEVERITY.keys():
            i += 1
            continue
        #handle cur msg
        cur_info.append(matches[0])
        is_in_msg = True
        i += 1
    if is_in_msg:
        #handle msg that has been caught
        packed_info = pack_info_func(cur_info)
        if is_not_empty(packed_info): 
            log_list.append(packed_info)
        #refresh cur_info
        cur_info = [] 

    return log_list

def is_not_empty(packed_info):
    if isinstance(packed_info, dict) and packed_info != {}:

        return True
    
    if isinstance(packed_info,str):
        if (isinstance(packed_info, str) and packed_info.strip() != '') and packed_info != []:
            return True
                
    return False 

def pack_to_msg_list(cur_info):
    '''
    cur_info = [('Warning', '2024-11-04 05:16:10', '未排入step:pcb-1 ')]

    cur_info = [
        (u'Info', u'2024-10-18 08:51:10', u'Traceback (most recent call last):'),
      u'  File "/incam_mnt/server/LocalMain.py", line 393, in step_work',
      u'    return file_path', "UnboundLocalError: local variable 'file_path' referenced before assignment",
      u' ']
    '''
    packed_info = {'type' : '',
                'datetime' : '',
                'msg_list' : []
                }
    FILTER_LEVEL = 1
    for msg in cur_info:
        
        if isinstance(msg, tuple):
            if SEVERITY[msg[0]] < FILTER_LEVEL:
                return {}
            packed_info['type'] = msg[0]
            packed_info['datetime'] = msg[1]
            packed_info['msg_list'].append(msg[2])
        # if isinstance(msg, str):
        else:
            if msg.strip() == '':
                continue
            packed_info['msg_list'].append(msg)
    return packed_info


def pack_to_text_list(cur_info):
    FILTER_LEVEL = 2
    packed_text = ''
    msg = cur_info[0]
    for i, msg in enumerate(cur_info):
        if isinstance(msg, tuple):
            if SEVERITY[msg[0]] < FILTER_LEVEL: #fileter low level
                return packed_text 
            packed_text += '{0} : {1}'.format(msg[0], msg[2])
        # if isinstance(msg, str):
        else:
            if msg.strip() == '':
                continue
            packed_text += '\n' + msg 
        # if i < len(cur_info):
        #     packed_text +=  '\n'
    return packed_text

def filter_n_replace_check_log(record_log): 
    '''
    input : record_log -> raw string with '\n'

    output: 
        filter_log -> list of log with [Check] ('[Check] : ' + msg only)
        replace_log -> full log with [Check] replace to [Checked]
    '''
    # file_path = r'D:\AutoCam\DEV\Ref\Test\TestProgramService\Data/Test_182585_mtkx-lb008x-a1d01-juri.txt'
    # file = open(file_path, "r")
    # program_log = file.read()
    # file.close()

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






# def get_runtime_from_raw_prog_log(raw_prog_log):
#     raw_prog_log_list = raw_prog_log.split('\n')
#     time = 10
#     for log_line in raw_prog_log_list:
#         if '[Time Spend]' in log_line:
#             time = float(log_line.split(':')[1])
#             break


#     return time



# def program_log_parser(self,
#                            exec_info,
#                            file_path):
                               
#         with open(file_path, "r") as f:
#             prog_log = f.readlines()
#         self.program_log = prog_log
    
        
#         msg_dict = {'Info'    : [],
#                     'Warning' : [],
#                     'Error'   : []}
             
#         state_level = 1
#         for log in prog_log:
#             if 'Info' in log:
#                 state_level = max(state_level, 1)
#                 msg_dict['Info'].append(log.strip())
         
#             elif 'Warning' in log:
#                 state_level = max(state_level, 2)
#                 msg_dict['Warning'].append(log.strip())
         
#             elif 'Error' in log:
#                 state_level = max(state_level, 3)
#                 msg_dict['Error'].append(log.strip())
        
#         if 'End File' not in prog_log[-1]: 
#             #not end properly
#             state_level = 3
         
#         ''' =================== Construct Log Format ==================== '''       
#         # common info        
#         exec_id  = exec_info['EXEC_ID']
#         program_state = state_dict[state_level] 
#         time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         job_id   = exec_info['JOB_ID']
#         job_name = exec_info['JOB_NAME']
#         tr_ver = exec_info['TR_VER']
#         exec_mode = exec_info['EXEC_MODE']
#         software = exec_info['SOFTWARE']
#         user_name= exec_info['USER_NAME']

#         program_ver = str(self.comboBox.currentText())
#         DB = self.parent.DB
#         program_name = self.program_name
#         #permanent program log
#         perm_prog_log_dict = {
#             'ExecID'  : exec_id,
#             'ProgramState': program_state,
#             'ProgramVer': program_ver,
#             'UserName': user_name,
#             'TRVer':    tr_ver, 
#             'ExecMode': exec_mode,
#             'Software': software,
#             'LogTime':  time_stamp,
#             'LogMsg' : str(msg_dict)
#             }
#         perm_prog_log = str(perm_prog_log_dict)  + '\n'
                
#         tmp_job_log_dict = {
#             'DB': DB,
#             'UserName': user_name,
#             'JobID'   : job_id,
#             'JobName' : job_name,
#             'ExecID'  : exec_id,
#             'ProgramName' : program_name,
#             'ProgramState': program_state,
#             'ProgramVer': program_ver,
#             'TRVer':    tr_ver, 
#             'ExecMode': exec_mode,
#             'Software': software,
#             'LogTime':  time_stamp
#             }
#         tmp_job_log = str(tmp_job_log_dict) + '\n'
        
#         return program_state, perm_prog_log, tmp_job_log
#%%




# # %%
# def parse_log_to_dict(log_text):
#     # Initialize the dictionary with default values
#     program_log_dict = {
#         'Time': '',
#         'JobID': '',
#         'JobName': '',
#         'Time Spend': '',
#         'State': 'Error',
#         'StateCode': '506',
#         'User': '',
#         'Exec_ID': '',
#         'Program': '',
#         'ProgramVer': '',
#         'Software': '',
#         'Source': '',
#         'EXEC_MODE': '',
#         'TRversion': '',
#         'Database': '',
#         'LogList': []
#     }

#     # Split the log text into lines
#     lines = log_text.strip().split('\n')

#     # Process each line
#     line = lines[1]
#     for line in lines:
#         # Skip lines that are not relevant
#         if line.startswith('===================LOG==================='):
#             continue
        
#         # Check if the line contains a key-value pair
#         if ':' in line:
#             key, value = line.split(':', 1)  # Split only on the first colon
#             key = key.strip()  # Remove leading/trailing whitespace
#             value = value.strip()  # Remove leading/trailing whitespace
            
#             # Handle LogList separately
#             if key.startswith('[Info]') or key.startswith('[Warning]') or key.startswith('[Checked]'):
#                 program_log_dict['LogList'].append(value)
#             elif key in program_log_dict:
#                 program_log_dict[key] = value

#     return program_log_dict

# # Sample log text
