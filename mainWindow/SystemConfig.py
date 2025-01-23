# -*- coding: utf-8 -*-
"""

@author: Depp
"""
FORCE_SWITCH_SAVE_STATUS_PROGRAM_LIST = [
    'Pass', 'AoiOut','DiLdiSetting','DrlOutInDrill','StackCnc',
    'PanelScaleTable', 'OutputProfileCenter','DrlOutLaserDrill','DrlOutVopDrill','NonVopOut',
    'OutputPTHCNCFile', 'VciDrlOut','GetRunCardInfo','ExportBackDrillPaper','LogoRecognition',
]
EXECUTE_STATE_CODE = {
    '204' : 'Open UI and close without any operation', #or U dont execute record.show_report
    '200' : 'End correctly',
    '300' : 'Warning',
    
    '500' : 'Program error',
    '501' : 'Broken pipe : internal error', 
    '502' : 'Broken pipe : User abort',
    '503' : 'Program error : No "End File"', #might cause by import error
    '505' : 'Main Ui Broken',
    '506' : 'Raw log file not found',
    '507' : 'No End file in log',
    '508' : 'Record msg_box Error',
    '509' : 'Record log_box Error'
}
STATE_TO_CODE = {

}
CODE_TO_STATE = {
    '204' : 'Pass',
    '200' : 'Pass',
    '300' : 'Warning',
    '500' : 'Error',
    '501' : 'Error',
    '502' : 'Error',
    '503' : 'Error',
    '505' : 'Error',
    '506' : 'Error',
    '507' : 'Error',
}
UI_MSG = {
    'LOGFILE_NOT_FOUND' : 'Program : {0} 在 {1} 找不到log file , Code : {2} ',
    'PROGRAM_TERMINATED_ABNORMALLY' : 'Program : {0} 沒有正常完結 , Code : {1} ',
    'EXECUTE_ENDING_MSG' : 'Program : {0} 測試完成, Code : {1} ',
    'TESTING_ENDING_MSG' : 'Program : {0} 執行完畢, Code : {1} ',
    'ERROR_05_06' : 'Program : {0} Error code : {1}\n',
    
}
USER_CONFIG = {
    'DEV_PC_ID': ['210605', '210814', '220741', '220853', '220741', '220812'
                  '220920', '170804', '230914', '231002', '210818', 'IESAdmin']
}
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
#permanent program log dict
perm_prog_log_dict = {
        'LogTime' : '',
        'JobID' : '',
        'JobName' : '',
        'RunTime' : '',
        'ProgramState' : '',
        'StateCode' : '',

        'UserName' : '',
        'ExecID' : '',
        'ProgramName' : '',
        'ProgramVer' : '',
        'Software' : '',
        #'Source : '',
        'ExecMode' : '',
        'TRVer' : '',
        'DB' : '',
        'LogMsg' : '',
        'IsSave' : '',
    }

tmp_job_log_dict = {
    'DB': '',
    'UserName': '',
    'JobID'   : '',
    'JobName' : '',
    'ExecID'  : '',
    'ProgramName' : '',
    'ProgramState': '',
    'ProgramVer': '',
    'TRVer':    '', 
    'ExecMode': '',
    'Software': '',
    'LogTime':  ''
    }
EXEC_INFO = {
        'JOB_ID' : '', 
        'JOB_NAME' : '', 
        'USER_NAME' : '', 
        'EXEC_ID' : '', 
        'LOG_PATH' : '', 
        'PROGRAM' : '',
        'PROGRAM_VER' : '' ,
        'SOFTWARE' : '', 
        'EXEC_MODE' : '', 
        'TR_VER' : '', 
        'DATABASE' : '', 
        'SOURCE' : ''
}


ProgramConfig = {
        'button_name': '',
        'main_folder_path': '',
        'process': '',
        'TR_ver_folder': {'Test':'',
                          'Release':''},
        'order'  : '',
        'parent_program' : '',
}

# '''
# [Time]       : {0}
# [User]       : {1}
# [Exec_ID]    : {2}
# [Program]    : {3}
# [ProgramVer] : {4}
# [JobName]    : {5}
# [Software]   : {6} 
# [EXEC_MODE]  : {7}
# [TRversion]  : {8}
# [Database]   : {9}
# =========================================
# '''.format('$TIME',
#             os.environ['USER_NAME'],
#             os.environ['EXEC_ID'],
#             os.environ['PROGRAM'],
#             os.environ['PROGRAM_VER'],
#             JOBNAME,
#             os.environ['SOFTWARE'],
#             os.environ['EXEC_MODE'],
#             os.environ['TRver'],
#             os.environ['Database'],)






