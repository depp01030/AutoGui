#!/usr/bin/python
# -*- coding: utf-8 -*-
import os 
try:
    import requests
except:
    pass
import datetime
import traceback
# SERVICE_ROOT = 'http://ws125:3114/cam/info_converter/dev/'
# SERVICE_ROOT = 'http://ws125:3124/cam/info_converter/test/'
# SERVICE_ROOT = 'http://ws125:31251/cam/info_converter/'
# SERVICE_ROOT = 'http://ws125:3125/cam/info_converter/'
# SERVICE_ROOT= 'http://ws125:3124/cam/info_converter/test/'
SERVICE_ROOT = os.environ['GEOM_SERVICE'] + 'cam/info_converter/'
# SERVICE_ROOT = 'http://ws125:3114/cam/info_converter/dev/'
# db_job_logs_dict = load_job_logs_from_db(DB, TRVer, JobID, IsSave = 1 )
def load_job_logs_from_db(DB, TRVer, JobID, job_name, IsSave = 1 ):
    '''
    DB = 'User'
    TRVer = 'Release'
    JobID = '5137974'
    IsSave = 1
    job_name = 'rd-202400414-a1d01'
    '''
    db_job_logs_dict = {}
    try:
        output_dict = {
            'DB': DB,
            'TRVer': TRVer,
            'JobID' : JobID,
            'JobName' : job_name,
            'IsSave' : IsSave,}
        

        data_dict = {'data_dict' : str(output_dict)}
        service_function_name = 'load_job_logs_from_db'
        url = SERVICE_ROOT + service_function_name
        r = requests.post(url, data = data_dict, timeout=5)
        db_job_logs_dict = eval(r.text)
    
    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)
    return db_job_logs_dict

def load_perm_db_txt_log(DB, TRVer, JobID, job_name, IsSave = 1 ):
    '''
    DB = 'Dev'
    TRVer = 'Release'
    JobID = '1174073'
    IsSave = 1
    job_name = 'advt-db011q'
    '''
    perm_db_txt_logs = []
    try:
        output_dict = {
            'DB': DB,
            'TRVer': TRVer,
            'JobID' : JobID,
            'JobName' : job_name,
            'IsSave' : IsSave,}
        

        data_dict = {'data_dict' : str(output_dict)}
        service_function_name = 'load_perm_db_txt_log'
        url = SERVICE_ROOT + service_function_name
        r = requests.post(url, data = data_dict, timeout=5)
        # db_job_logs_dict = eval(r.text.decode('unicode_escape').encode('utf-8'))
        # db_job_logs_dict = eval(r.text.decode('unicode_escape'))
        byte_perm_db_txt_logs = eval(r.text)
        for byte_db_log in byte_perm_db_txt_logs:
            try:
                perm_db_log = eval(byte_db_log)
            except:
                continue
            perm_db_txt_logs.append(perm_db_log)
    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)
    return perm_db_txt_logs

#%%
def insert_job_logs_to_db(insert_job_logs):
    '''
    single_log =  {
        'UserName': 'incam-incam',
        'LogTime': '2024-10-07 18:20:05',
        'DB': 'Dev',
        'JobName': 'asme-pd0004-v1d02-auto',
        'StateCode': '200',
        'ProgramState': 'Pass',
        'JobID': '6482769',
        
        'Software': 'incam',
        'ExecID': '522183',
        'TRVer': 'Test',
        'ProgramVer': u'240102',
        'ExecMode': 'Manual',

        'ProgramName': u'Pass',
        'RunTime': 10.0198,
        'IsSave': 0,
        }


    insert_job_logs = []
    for i in range(1):
        insert_job_logs.append(single_log)


        
    '''
    try:
        data_dict = {'data_dict' : str(insert_job_logs)} 
        # data_dict = {'data_dict' : str(insert_job_logs)} 
        service_function_name = 'insert_job_logs_to_db'
        url = SERVICE_ROOT + service_function_name
        r = requests.post(url, data = data_dict, timeout=5) 
        
        # job_logs = eval()
        print(r.text) 
        return True
    except Exception as e: 
        err_msg = traceback.format_exc()
        print(err_msg)
        return False



#%%
if __name__ == '__main__':
    
    insert_job_logs = []
    form = {'DB': 'Dev',
            'UserName':'IES',
            'JobID' : 3345678,
            'JobName': 'real-lb021j-a1d01',
            'ProgramID': 39527,
            'ProgramName': 'CreateJob',
            'ProgramState': 'PASS',
            'LogTime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    for i in range(3):
        insert_job_logs.append(form)



    '''
    
    @app.route('/cam/call_load_job_logs_from_db', methods=['GET', 'POST'])
    @cross_origin()
    def call_load_job_logs_from_db(): 
        params = request.form
        DB = str(params['DB'])
        TRVer = str(params['TRVer'])
        JobID = str(params['JobID'])
        job_logs_dict = load_job_logs_from_db(DB, TRVer, JobID)
        
        return str(job_logs_dict)
        
    @app.route('/cam/call_insert_job_logs_to_db', methods=['GET', 'POST'])
    @cross_origin()
    def call_insert_job_logs_to_db(): 
        
        str_job_logs = request.values.get('job_logs')  
        job_logs = eval(str_job_logs)
        
        job_log_dict = insert_job_logs_to_db(job_logs)
        
        return str(job_log_dict)
    
    
    ''' 
#     unicode_string = '\u9019\u908a' 
 
    text = 'I am' + 'Warning : \xe9\x80\x99 '
    text.decode('utf-8')
    # text.encode('utf-8')
#     unicode_string.encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')

# decoded_string = unicode_string.encode('utf-8').decode('unicode_escape')
    # insert_job_logs = [
    #     {'UserName': 'incam-incam', 'IsSave': 1, 'ExecID': '863258', 'TRVer': 'Test', 'ProgramName': 'RecordCheck', 'ProgramVer': '241017-1-1408', 'ExecMode': 'Manual', 'LogMsg': [{'msg_list': ['\xe4\xb8\xad\xe6\x96\x87info '], 'type': 'Info', 'datetime': '2024-11-12 10:16:40'}, {'msg_list': ['\xe9\x80\x99\xe6\x98\xaf checkinfo 1 '], 'type': 'Checked', 'datetime': '2024-11-12 10:16:40'}, {'msg_list': ['This is checkinfo 2 '], 'type': 'Checked', 'datetime': '2024-11-12 10:16:40'}, {'msg_list': ['\xe4\xb8\xad\xe6\x96\x87 is checkinfo 2 '], 'type': 'Checked', 'datetime': '2024-11-12 10:16:40'}, {'msg_list': ['This is checkinfo 3 '], 'type': 'Checked', 'datetime': '2024-11-12 10:16:41'}, {'msg_list': ['\xe9\x80\x99\xe6\x98\xaf note '], 'type': 'Note', 'datetime': '2024-11-12 10:16:41'}, {'msg_list': ['\xe9\x80\x99\xe6\x98\xaf\xe8\xad\xa6\xe5\x91\x8a '], 'type': 'Warning', 'datetime': '2024-11-12 10:16:42'}, {'msg_list': ['End File 300 ', ''], 'type': 'Info', 'datetime': '2024-11-12 10:16:43'}], 'DB': 'Dev', 'JobID': '1174073', 'JobName': 'advt-db011q', 'StateCode': '300', 'LogTime': '2024-11-12 10:16:40', 'ProgramState': 'Warning', 'RunTime': '1.99521112442', 'Software': 'incam'},
    #     {'UserName': 'incam-incam', 'IsSave': 1, 'ExecID': '156385', 'TRVer': 'Test', 'LogTime': '2024-11-12 10:16:59', 'ProgramVer': '241017-1-1408', 'ExecMode': 'Manual', 'LogMsg': [{'msg_list': ['\xe4\xb8\xad\xe6\x96\x87 info '], 'type': 'Info', 'datetime': '2024-11-12 10:16:59'}, {'msg_list': ['\xe9\x80\x99\xe6\x98\xaf checkinfo 1 '], 'type': 'Checked', 'datetime': '2024-11-12 10:16:59'}, {'msg_list': ['This is checkinfo 2 '], 'type': 'Checked', 'datetime': '2024-11-12 10:16:59'}, {'msg_list': ['\xe4\xb8\xad\xe6\x96\x87 is checkinfo 2 '], 'type': 'Checked', 'datetime': '2024-11-12 10:16:59'}, {'msg_list': ['This is checkinfo 3 '], 'type': 'Checked', 'datetime': '2024-11-12 10:17:01'}, {'msg_list': ['\xe9\x80\x99\xe6\x98\xaf note '], 'type': 'Note', 'datetime': '2024-11-12 10:17:01'}, {'msg_list': ['\xe9\x80\x99\xe6\x98\xaf\xe8\xad\xa6\xe5\x91\x8a '], 'type': 'Warning', 'datetime': '2024-11-12 10:17:02'}, {'msg_list': ['End File 300 ', ''], 'type': 'Info', 'datetime': '2024-11-12 10:17:03'}], 'DB': 'Dev', 'JobID': '1174073', 'Software': 'incam', 'StateCode': '300', 'ProgramName': 'RecordCheck', 'ProgramState': 'Warning', 'RunTime': '2.97250914574', 'JobName': 'advt-db011q'}
    # ]

#     import json
#     byte_sequence = '\xe9\x80\x99\xe6\x98\xaf'
#     # bstr =byte_sequence.encode('latin1').decode('utf-8')
#     output_dict = {
#         'DB': 'DB',
#         'TRVer': 'TRVer',
#         'JobID' : 'JobID',
#         'JobName' : byte_sequence,
#         'IsSave' : 'IsSave',}
    
#     json.dumps(output_dict)
# encode_list = []
# for db_log in insert_job_logs:
#     pass
#     str(db_log['LogMsg']).encode('latin1').decode('utf-8')

# b"{byte_sequence}".decode('utf-8')
# # Decode the byte sequence using UTF-8
# byte_sequence.encode('latin1').decode('utf-8')
# import os 
# file_name = '1174073_advt-db011q'
# file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
#                          'TESTFILES', file_name)

# with open(file_path, "r", encoding='utf-8') as f:
#     perm_db_txt_logs = f.readlines()
# with open(file_path, "rb") as f:
#     perm_db_txt_logs = f.readlines()

# perm_db_txt_logs[0].decode('utf-8', errors='replace')
# 'ä¸\\xadæ\\x96\\x87info '
# print(decoded_character)  # Output: 這 (the character corresponding to the byte sequence)

# byte_sequence
# data_dict = {'data_dict' : insert_job_logs} 
# service_function_name = 'insert_job_logs_to_db'
# url = SERVICE_ROOT + service_function_name
# r = requests.post(url, data = data_dict, timeout=5) 
# Sample log data (as provided)
# db_logs = [
#     {'msg_list': ['ä¸\xadæ\x96\x87info '], 'type': 'Info', 'datetime': '2024-11-12 10:16:59'},
#     {'msg_list': ['é\x80\x99æ\x98¯checkinfo 1 '], 'type': 'Checked', 'datetime': '2024-11-12 10:16:59'},
#     {'msg_list': ['This is checkinfo 2 '], 'type': 'Checked', 'datetime': '2024-11-12 10:16:59'},
#     {'msg_list': ['ä¸\xadæ\x96\x87is checkinfo 2 '], 'type': 'Checked', 'datetime': '2024-11-12 10:16:59'},
#     {'msg_list': ['This is checkinfo 3 '], 'type': 'Checked', 'datetime': '2024-11-12 10:17:01'},
#     {'msg_list': ['é\x80\x99æ\x98¯ note '], 'type': 'Note', 'datetime': '2024-11-12 10:17:01'},
#     {'msg_list': ['é\x80\x99æ\x98¯è\xad¦å\x91\x8a '], 'type': 'Warning', 'datetime': '2024-11-12 10:17:02'},
#     {'msg_list': ['End File 300 ', ''], 'type': 'Info', 'datetime': '2024-11-12 10:17:03'}
# ]

# # Process each log message
# for log in db_logs:
#     for msg in log['msg_list']:
#         try:
#             # Decode using latin1 and then encode to utf-8 if necessary
#             decoded_msg = msg.encode('latin1').decode('utf-8')
#             print(decoded_msg)  # Print the correctly decoded message
#         except UnicodeDecodeError as e:
#             print("Decoding error:", e)
# %%
