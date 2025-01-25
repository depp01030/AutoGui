#%%
import sys
import pymssql
import os 
import re

import pandas as pd
import numpy as np
import datetime
import time
import traceback
#%%
# PERMANENT_TXT_STORAGE_PATH = os.path.join(
#     os.path.dirname(__file__)
#     )

PERMANENT_TXT_STORAGE_PATH = r'\\fs2\GerberData\cam_log' 
def load_job_logs_from_db(data_dict):
    '''
    DB = 'Test'
    TRVer = 'Test'
    JobID = '2319941'
    IsSave = 0
    JobName = 'qctx-ot006d-batch'
    data_dict = {
        'DB': DB,
        'TRVer': TRVer,
        'JobID' : JobID,
        'JobName' : JobName,
        'IsSave' : IsSave}
    '''
    DB = data_dict['DB']
    TRVer = data_dict['TRVer']
    JobID = data_dict['JobID']
    JobName = data_dict['JobName']
    IsSave = data_dict['IsSave']
    cmd = "SELECT * FROM AutoCAMJobLog_{0} WHERE TRVer = '{1}' and JobID = '{2}' and JobName = '{3}' and IsSave = '{4}' ORDER BY LogTime DESC".\
        format(DB, TRVer, JobID, JobName,  IsSave)

    df = _query_db(cmd)
    if len(df) == 0:
        return {}
    
    df_sorted = df.sort_values(['ProgramName', 'LogTime'], ascending=[True, False])

    # Group the sorted DataFrame by ProgramName and select the first row for each group
    last_logtime_rows = df_sorted.groupby('ProgramName').first().reset_index()
    
    # Transfer datetime to string
    for col_name in last_logtime_rows.select_dtypes(include=[np.datetime64]).columns:
        last_logtime_rows[col_name] = last_logtime_rows[col_name].dt.strftime('%Y-%m-%d  %H:%mm:%ss')
    # Transfer bool to int
    for col_name in last_logtime_rows.select_dtypes(include=[bool]).columns:
        last_logtime_rows[col_name] = last_logtime_rows[col_name].astype(int)
    
    job_logs_dict = last_logtime_rows.to_dict()
    return job_logs_dict


def load_perm_db_txt_log(data_dict):
    '''
    DB = 'Dev'
    TRVer = 'Test'
    JobID = '2319941'
    IsSave = 0
    JobName = 'qctx-ot006d-batch'
    file_name = '1838322_qctx-pc005n-x-rachel-0127'
    file_name = '3963004_ztem-lb0021-a1d01-ping-cnc'
    file_name = '1174073_advt-db011q'
    JobID, JobName  = file_name.split('_')
    data_dict = {
        'DB': DB,
        'TRVer': TRVer,
        'JobID' : JobID,
        'JobName' : JobName,
        'IsSave' : IsSave}
    output_dict = data_dict
    '''
    DB = data_dict['DB']
    TRVer = data_dict['TRVer']
    JobID = data_dict['JobID']
    JobName = data_dict['JobName']
    IsSave = data_dict['IsSave']

    perm_db_logs = []

    ## handle perm_db_log
    folder_path = os.path.join(PERMANENT_TXT_STORAGE_PATH, DB, TRVer, JobName)
    file_name = '{0}_{1}.txt'.format(JobID, JobName)
    file_path = os.path.join(folder_path, file_name)

    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
    if not os.path.isfile(file_path):
        return str(perm_db_logs)
    with open(file_path, "rb") as f:
        perm_db_txt_logs = f.readlines()

    for perm_db_txt_log in perm_db_txt_logs:
        # perm_db_log = eval(perm_db_txt_log)
        perm_db_logs.append(perm_db_txt_log)
     
    return str(perm_db_logs)

def insert_job_logs_to_db(job_logs):
    '''
    single_log =  {
        'UserName': 'incam-incam',
        'LogTime': '2025-03-05 08:29:15',
        'RunTime': 30,
        'DB': 'Dev',
        'JobName': 'qctx-pc005n-x-rachel-0127',
        'ProgramState': 'Pass',
        'StateCode': '204',
        'JobID': '1838322',
        'Software': 'incam',
        'ExecID': '522183',
        'TRVer': 'Test',
        'ProgramVer': u'240102',
        'ExecMode': 'Manual',
        'ProgramName': u'Pass',
        'LogMsg' : [],
        'IsSave' : 0
        }

    
    job_logs = []
    for i in range(1):
        job_logs.append(single_log)
    '''
    # print(raw_data)
    # print(raw_data.encode('utf-8').decode('utf-8') )
    # import json
    # job_logs = eval(raw_data)
    
    # job_logs = eval(raw_data.encode('utf-8').decode('utf-8'))
    order_list = ['DB', 'UserName', 'JobID', 'JobName','ExecID', 'ProgramName', 'ProgramState',
                'StateCode', 'ProgramVer', 'TRVer', 'ExecMode', 'Software', 'RunTime', 'LogTime', 'IsSave']
    flag = True
    if len(job_logs) == 0:
        return flag
    if 'JobName' not in job_logs[0].keys() or'JobID' not in job_logs[0].keys():
        return flag
    
    try:
        conn = pymssql.connect(host='192.168.1.138', user='IESDBAdmin', password='IES1qaz2wsx', database='LogDB')
        cur = conn.cursor()

        for log in job_logs:  
            param_list = []
            for key in order_list:
                value = log[key]
                param_list.append(value)
            cmd = "INSERT INTO AutoCAMJobLog_{0}\
                (UserName, JobID, JobName, ExecID, ProgramName, ProgramState, StateCode,\
                ProgramVer, TRVer, ExecMode, Software, RunTime, LogTime, IsSave)\
                Values ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}', '{12}', '{13}', '{14}')".format(*param_list)
            time.sleep(0.001)
            cur.execute(cmd)
        conn.commit()
          
        ## handle perm_db_log 
        folder_path = os.path.join(PERMANENT_TXT_STORAGE_PATH, job_logs[0]['DB'], job_logs[0]['TRVer'], job_logs[0]['JobName'])
        file_name = '{0}_{1}.txt'.format(job_logs[0]['JobID'], job_logs[0]['JobName'])
        file_path = os.path.join(folder_path, file_name)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        # byte_job_logs = raw_data.encode('utf-8') 
        # print(len(byte_job_logs))
        with open(file_path, 'ab') as f:
            for db_log in job_logs:
                if 'IsSave' not in db_log.keys() or db_log['IsSave'] == 0:
                    continue
                str_db_log = (str(db_log) + '\n').encode('utf-8') 
                # str_db_log = db_log 
                f.write(str_db_log)
            
                
        
    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)
        flag = False

        conn.rollback()
    finally:
        conn.close() 
    return str(flag)

def _query_db(cmd):
    try:
        conn = pymssql.connect(host='192.168.1.138', user='IESDBAdmin', password='IES1qaz2wsx', database='LogDB')

        cur = conn.cursor()
        rawData =[]
        cur.execute(cmd) 
        for rowData in (cur.fetchall()):
            rawData.append(rowData)
    except Exception as e:
        line_no = sys.exc_traceback.tb_lineno
        
        if e[1][:19] == 'Invalid object name':                
            # no table           
            pass
        else:
            return pd.DataFrame()
    finally:
        if cur == None:
            
            return pd.DataFrame()
        else:
            if len(rawData)>0:                    
                data_columns = [item[0] for item in cur.description]
                data = pd.DataFrame(rawData, columns = data_columns)
                return data
            else:
              
                return pd.DataFrame()
# %%
# Define the byte sequence
# str_db_log = "{'UserName': 'incam-incam', 'IsSave': 1, 'ExecID': '458831', 'TRVer': 'Test', 'LogTime': '2024-11-12 13:57:31', 'ProgramVer': '241017-1-1408', 'ExecMode': 'Manual', 'LogMsg': [{'msg_list': ['ä¸\xadæ\x96\x87info '], 'type': 'Info', 'datetime': '2024-11-12 13:57:31'}, {'msg_list': ['é\x80\x99æ\x98¯ checkinfo 1 '], 'type': 'Checked', 'datetime': '2024-11-12 13:57:31'}, {'msg_list': ['This is checkinfo 2 '], 'type': 'Checked', 'datetime': '2024-11-12 13:57:31'}, {'msg_list': ['ä¸\xadæ\x96\x87 is checkinfo 2 '], 'type': 'Checked', 'datetime': '2024-11-12 13:57:31'}, {'msg_list': ['This is checkinfo 3 '], 'type': 'Checked', 'datetime': '2024-11-12 13:57:32'}, {'msg_list': ['é\x80\x99æ\x98¯ note '], 'type': 'Note', 'datetime': '2024-11-12 13:57:32'}, {'msg_list': ['é\x80\x99æ\x98¯è\xad¦å\x91\x8a '], 'type': 'Warning', 'datetime': '2024-11-12 13:57:33'}, {'msg_list': ['End File 300 ', ''], 'type': 'Info', 'datetime': '2024-11-12 13:57:34'}], 'DB': 'Dev', 'JobID': '1174073', 'Software': 'incam', 'StateCode': '300', 'ProgramName': 'RecordCheck', 'ProgramState': 'Warning', 'RunTime': '1.99764895439', 'JobName': 'advt-db011q'}"
# str_db_log = str_db_log.encode('utf-8')
# eval(str_db_log.decode('utf-8'))
# %%
# str_db_log = 'ä¸\xadæ\x96\x87info '
# str_db_log
# a = '''[{'UserName': u'incam-incam', 'IsSave': 1, 'ExecID': u'181464', 'TRVer': u'Test', 'LogTime': u'2024-11-13 12:26:22', 'ProgramVer': u'241011-7-1037', 'ExecMode': u'Manual', 'LogMsg': [{'msg_list': [u'986093 '], 'type': u'Info', 'datetime': u'2024-11-13 12:26:23'}, {'msg_list': [u'Traceback (most recent call last):', u'  File "/InCAM/server/site_data/scripts/AutoCAM2.0/Test/Main_Error/Test/Error-241011-7-1037/Model.py", line 39, in main', u'    print(10/0)', u'ZeroDivisionError: integer division or modulo by zero', u' '], 'type': u'Error', 'datetime': u'2024-11-13 12:26:23'}, {'msg_list': [u'End File 500 ', u''], 'type': u'Info', 'datetime': u'2024-11-13 12:26:24'}], 'DB': u'Dev', 'JobID': u'1174073', 'Software': u'incam', 'StateCode': u'500', 'ProgramName': u'Error', 'ProgramState': u'Error', 'RunTime': u'1.16404104233', 'JobName': u'advt-db011q'}, {'UserName': u'incam-incam', 'IsSave': 1, 'ExecID': u'145187', 'TRVer': u'Test', 'LogTime': u'2024-11-13 12:26:30', 'ProgramVer': u'241011-7-1037', 'ExecMode': u'Manual', 'LogMsg': [{'msg_list': [u'947007 '], 'type': u'Info', 'datetime': u'2024-11-13 12:26:31'}, {'msg_list': [u'Traceback (most recent call last):', u'  File "/InCAM/server/site_data/scripts/AutoCAM2.0/Test/Main_Error/Test/Error-241011-7-1037/Model.py", line 39, in main', u'    print(10/0)', u'ZeroDivisionError: integer division or modulo by zero', u' '], 'type': u'Error', 'datetime': u'2024-11-13 12:26:31'}, {'msg_list': [u'End File 500 ', u''], 'type': u'Info', 'datetime': u'2024-11-13 12:26:32'}], 'DB': u'Dev', 'JobID': u'1174073', 'Software': u'incam', 'StateCode': u'500', 'ProgramName': u'Error', 'ProgramState': u'Error', 'RunTime': u'1.24982094765', 'JobName': u'advt-db011q'}]'''

# b = b'[{\'UserName\': u\'incam-incam\', \'IsSave\': 1, \'ExecID\': u\'181464\', \'TRVer\': u\'Test\', \'LogTime\': u\'2024-11-13 12:26:22\', \'ProgramVer\': u\'241011-7-1037\', \'ExecMode\': u\'Manual\', \'LogMsg\': [{\'msg_list\': [u\'986093 \'], \'type\': u\'Info\', \'datetime\': u\'2024-11-13 12:26:23\'}, {\'msg_list\': [u\'Traceback (most recent call last):\', u\'  File "/InCAM/server/site_data/scripts/AutoCAM2.0/Test/Main_Error/Test/Error-241011-7-1037/Model.py", line 39, in main\', u\'    print(10/0)\', u\'ZeroDivisionError: integer division or modulo by zero\', u\' \'], \'type\': u\'Error\', \'datetime\': u\'2024-11-13 12:26:23\'}, {\'msg_list\': [u\'End File 500 \', u\'\'], \'type\': u\'Info\', \'datetime\': u\'2024-11-13 12:26:24\'}], \'DB\': u\'Dev\', \'JobID\': u\'1174073\', \'Software\': u\'incam\', \'StateCode\': u\'500\', \'ProgramName\': u\'Error\', \'ProgramState\': u\'Error\', \'RunTime\': u\'1.16404104233\', \'JobName\': u\'advt-db011q\'}, {\'UserName\': u\'incam-incam\', \'IsSave\': 1, \'ExecID\': u\'145187\', \'TRVer\': u\'Test\', \'LogTime\': u\'2024-11-13 12:26:30\', \'ProgramVer\': u\'241011-7-1037\', \'ExecMode\': u\'Manual\', \'LogMsg\': [{\'msg_list\': [u\'947007 \'], \'type\': u\'Info\', \'datetime\': u\'2024-11-13 12:26:31\'}, {\'msg_list\': [u\'Traceback (most recent call last):\', u\'  File "/InCAM/server/site_data/scripts/AutoCAM2.0/Test/Main_Error/Test/Error-241011-7-1037/Model.py", line 39, in main\', u\'    print(10/0)\', u\'ZeroDivisionError: integer division or modulo by zero\', u\' \'], \'type\': u\'Error\', \'datetime\': u\'2024-11-13 12:26:31\'}, {\'msg_list\': [u\'End File 500 \', u\'\'], \'type\': u\'Info\', \'datetime\': u\'2024-11-13 12:26:32\'}], \'DB\': u\'Dev\', \'JobID\': u\'1174073\', \'Software\': u\'incam\', \'StateCode\': u\'500\', \'ProgramName\': u\'Error\', \'ProgramState\': u\'Error\', \'RunTime\': u\'1.24982094765\', \'JobName\': u\'advt-db011q\'}]'
# job_logs = eval(b)

# # %%
# b = b'[{\'UserName\': u\'incam-incam\', \'IsSave\': 1, \'ExecID\': u\'634291\', \'TRVer\': u\'Test\', \'LogTime\': u\'2024-11-13 12:37:22\', \'ProgramVer\': u\'241011-7-1037\', \'ExecMode\': u\'Manual\', \'LogMsg\': [{\'msg_list\': [u\'621720 \'], \'type\': u\'Info\', \'datetime\': u\'2024-11-13 12:37:23\'}, {\'msg_list\': [u\'Traceback (most recent call last):\', u\'  File "/InCAM/server/site_data/scripts/AutoCAM2.0/Test/Main_Error/Test/Error-241011-7-1037/Model.py", line 39, in main\', u\'    print(10/0)\', u\'ZeroDivisionError: integer division or modulo by zero\', u\' \'], \'type\': u\'Error\', \'datetime\': u\'2024-11-13 12:37:23\'}, {\'msg_list\': [u\'End File 500 \', u\'\'], \'type\': u\'Info\', \'datetime\': u\'2024-11-13 12:37:24\'}], \'DB\': u\'Dev\', \'JobID\': u\'1174073\', \'Software\': u\'incam\', \'StateCode\': u\'500\', \'ProgramName\': u\'Error\', \'ProgramState\': u\'Error\', \'RunTime\': u\'0.736478805542\', \'JobName\': u\'advt-db011q\'}]'

# for data in eval(b.encode('utf-8')):
#     print(data)
# folder_path = os.path.join(PERMANENT_TXT_STORAGE_PATH, )
# file_name = '{0}_{1}.txt'.format('id','test')
# file_path = os.path.join(PERMANENT_TXT_STORAGE_PATH, file_name)
# with open(file_path, 'ab') as f:
#     for db_log in job_logs:
#         if 'IsSave' not in db_log.keys() or db_log['IsSave'] == 0:
#             continue
#         str_db_log = (str(db_log) + '\n').encode('utf-8') 
#         f.write(str_db_log)

 

# %%
