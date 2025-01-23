# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:05:24 2023

@author: Depp
"""
import os 
import json
import random
import traceback
import platform
import subprocess
import shutil
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer, QThread, QString
from PyQt4.QtGui import QFileDialog 
import LogParser
from project_utils import (create_standard_folder  )
from Utils.UiMoudule.ConfigUI.View_ParamConfigReader import Ui_Frame as View_ParamConfigReader
from Utils.utils import get_step_list
from process_config import PROCESS_LIST
from SystemConfig import UI_MSG, FORCE_SWITCH_SAVE_STATUS_PROGRAM_LIST
''' ========================================================================== '''
'''                                ProgramFrame                                '''
''' ========================================================================== '''
class ProgramFrame(QtGui.QWidget):
    '''
    release 
    copy_to
    connect 
    '''
    def __init__(self,   
                 SIGNAL_MANAGER,       
                 button_name,
                 main_folder_path,
                 program_name,
                 process_tab,
                 parent_program,
                 state = 'None',
                 parent=None,
                 ):
        super(ProgramFrame, self).__init__(parent) 
        self.SIGNAL_MANAGER = SIGNAL_MANAGER
        self.parent = parent
        self.program_name = program_name
        self.setObjectName(program_name) 
        
        
        self.main_folder_path = main_folder_path  #'/Preprocess/Main_xxx'
        self.process_tab = process_tab
        self.parent_program = parent_program
        self.auto_update_flag = True
        self._frame_title = None #
        self._button_text = None
        self._current_ver = None #
        self.has_load_hitory_execute_log = False
        self.history_execute_log = [] #this is for show on 2.0 UI


        self.label = ProgramStateLabel(state)   
        self.pushButton = ProgramButton(button_name)  
        self.comboBox = None
        if self.parent_program == '':
            self.comboBox = ProgramVerComboBox()

        self.setup_attr()
        self.setupUi()
        self.setup_click_event()
    def setupUi(self):        
        self._setupUi()
        self.menu = ProgramFrameMenu(self)    
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
    def _setupUi(self):   
        self.set_TR_ver(self.parent.TR_ver)
        self.set_privilage(self.parent.privilage)
        # Set the frame style
        # self.setFrameStyle(QtGui.QFrame.Box)
        # qss = """
        #     QFrame {
        #             padding :4px;
        #             border :2px solid #d9d9d9;
        #             border-radius : 3px;
        #             background-color : #333333;
        #             color : #12a3f7; 
        #             font-size : 8pt;
        #             font-weight: bold;
        #             }
        #     QFrame:hover {
        #             padding :4px;
        #             border :2px solid #d9d9d9;
        #             border-radius : 3px;
        #             background-color: #81939e;
        #             font-size : 8pt;
        #             font-weight: bold;
        #             }
        # """

        # self.setStyleSheet(qss)

        self._set_style('unselect')
        horizontalLayout = QtGui.QHBoxLayout(self) 
        horizontalLayout.addWidget(self.label)
        # horizontalLayout.addItem(QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum))
        horizontalLayout.addWidget(self.pushButton)
        
        horizontalLayout.addItem(QtGui.QSpacerItem(80, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        if self.comboBox is not None:
            horizontalLayout.addWidget(self.comboBox)
    @property
    def button_text(self):
        self._button_text = str(self.pushButton.text().toUtf8())
        return self._button_text
    @property
    def current_ver(self):
        if self.comboBox is not None:
            if self._current_ver is None or self.parent.privilage == 'User':
                self._current_ver = str(self.TR_ver_folder[self.parent.TR_ver])
            else:
                self._current_ver = str(self.comboBox.currentText()).replace(' ', '')
        else:
            self._current_ver = self.parent.program_config[self.parent_program]['TR_ver_folder'][self.parent.TR_ver]
        return self._current_ver
    @property
    def frame_title(self):
        title = "Program : {0}-{1}-{2} Log : ".format(
            self.pushButton.text().toUtf8(),
            self.program_name,
            self.current_ver
        )
        self._frame_title = title
        return self._frame_title
    def setup_attr(self):
        #set cur TR version folder
        if self.program_name in self.parent.program_config.keys():
            self.TR_ver_folder =  self.parent.program_config[self.program_name]['TR_ver_folder']
        else:
            self.TR_ver_folder =  {'Test':'', 'Release':''}
        self.last_exec_id = '' 
        self.program_log = []
        self.release_log = ''
        self.description = ''
        self.available = True
    def setup_click_event(self):                
        self.pushButton.clicked.connect(self.exec_clicked)
        # signal
        self.SIGNAL_MANAGER.TR_ver_changed.connect(self.on_parent_TR_ver_changed)    
        # self.parent.privilage_changed.connect(self.on_parent_privilage_changed)   
        self.SIGNAL_MANAGER.privilage_changed.connect(self.on_parent_privilage_changed)  
        if self.comboBox is not None:
            self.comboBox.currentIndexChanged.connect(self.on_combobox_changed) 
    def on_combobox_changed(self):
        self.update_frame()
        if self.auto_update_flag:
            src_copying_folder_path = self.get_sub_src_copying_folder_path()
            if os.path.isdir(src_copying_folder_path):
                self.update_sub_clicked()
    def update_sub_clicked(self):
        # sub_program_copying(process_key,
        #                     self.button)
        # self.parent.LogBox.append("{0}_{1}".format(self.program_name, self.current_ver))
  
        is_success = self.parent.update_sub_program(self)
        if not is_success:
            self.parent.LogBox.append('update sub fail') 
            return  
        
        # self.parent.parent.LogBox.append(msg)
    def update_frame(self, cur_idx=0, init_program_log = {}):
        ## set state and last_exec_id ##
        if init_program_log:
            #set state
            self.label.set_result_state(init_program_log['ProgramState'])
            #set last_exec_id
            self.last_exec_id = init_program_log['ExecID'] 

        #init last_exec_id, otherwise might be the one of the other TRver.
        # 嘗試註解這段，為了確保得到last_exec_id 24/08/12 depp
        # self.last_exec_id = ''
        ## get cur program version folder ##
        file_path = self.get_exec_file_path()
        ver_folder_path = os.path.dirname(file_path)

        ## load readme ##
        readme_info = self.parent.info_model.load_readme(ver_folder_path)
        if readme_info:
            ## set project name ##
            project = readme_info['project_name']
            
            ## set description ##
            description = readme_info['description']
            ## set program_info ## : release log...
            release_log = readme_info['release_log']
            self.release_log = release_log

            utf8_data = description.decode('utf-8').encode('utf-8')
            self.description = QtCore.QTextCodec.codecForName("UTF-8").toUnicode(utf8_data)
            self.setToolTip(self.description )
        
        ## set available ##  
        if self.current_ver == '':
            self.set_available(False)
        else:
            is_available = True #default
            # json_path = os.path.join(ver_folder_path,'ExecuteConfig.json') 
            # if os.path.isfile(json_path):    
            #     with open(json_path, "r") as file:
            #         ExecuteConfig = json.load(file)
            #     is_available =  self.is_program_work(ExecuteConfig)
            
            self.set_available(is_available)
    def set_available(self, available):
        self.available = available
        self.label.set_available(available)
        self.pushButton.setEnabled(available)
    ''' ================== '''
    '''    On Selection    '''
    ''' ================== '''
    def show_readme(self):
        self.parent.LogBox.append(self.description)
        self.parent.LogBox.append(self.release_log)
    def unselect(self):
        self._set_style('unselect')
    def select(self):
        try:
            self._set_style('select')
            # trigger by listwidget itemClicked
            # ver_folder = os.path.dirname(self.get_exec_file_path())
            # self.SIGNAL_MANAGER.program_selected.emit(self.program_name,ver_folder) 
            self.parent.LogBox.clear()
            
            # msg = "Program : " + self.pushButton.text()  + ' - ' + \
            #     self.program_name + ' - ' +\
            #     str(self.comboBox.currentText()) + ' Log : '

            # msg = msg.decode('utf-8').encode('utf-8') 
            # self.setToolTip(self.description )
            
            self.parent.LogBox.append(self.frame_title)  
            self.show_history_execute_log()
            # self.show_program_log()
            # self.get_program_log()  
            # if self.program_log: 
            #     self.parent.LogBox.append(self.program_log)
                # self.parent.record.check(self.program_log, box = True)

        except Exception as e:
            err_msg = traceback.format_exc()
            self.parent.LogBox.sys_append(err_msg)
    def update_execute_log(self, db_log):
        if not self.has_load_hitory_execute_log: #first clicked
        # if self.history_execute_log == []: 
            self.has_load_hitory_execute_log = True
            #try get from parent
            if self.program_name in self.parent.history_db_logs_dict.keys():
                hist_db_logs = self.parent.history_db_logs_dict[self.program_name]
                for hist_db_log in hist_db_logs:
                    self.update_execute_log(hist_db_log)
        execute_log = LogParser.parse_db_log_to_execute_log(db_log)
        
        self.history_execute_log.insert(0,str(execute_log))
    def show_history_execute_log(self):
        if not self.has_load_hitory_execute_log: #first clicked
        # if self.history_execute_log == []: 
            self.has_load_hitory_execute_log = True
            #try get from parent
            if self.program_name in self.parent.history_db_logs_dict.keys():
                hist_db_logs = self.parent.history_db_logs_dict[self.program_name]
                for hist_db_log in hist_db_logs:
                    self.update_execute_log(hist_db_log)
            
        for log in self.history_execute_log:
            self.parent.LogBox.append(log)
        self.parent.LogBox.verticalScrollBar().setValue(0)
    ''' ==================== old read perm log start ===================== '''
    # def _show_program_log(self,perm_prog_log_dict = None): 
    #     # self.parent.LogBox.append(self.last_exec_id)
    #     try:
    #         if perm_prog_log_dict is not None:
    #             self.parse_perm_prog_log_dict(perm_prog_log_dict)
    #         else:
    #             if self.program_log == []:
    #                 perm_prog_log_dict = self.get_perm_prog_log_dict()  
    #                 self.parse_perm_prog_log_dict(perm_prog_log_dict)
            
    #         reversed_log = sorted(self.program_log, reverse = True)
    #         for log in reversed_log:
    #             self.parent.LogBox.append(log)
    
    #     # for log in msg_log:
    #     #     self.parent.LogBox.append(log)
    #     except Exception as e:
    #         err_msg = traceback.format_exc()
    #         self.parent.LogBox.sys_append(err_msg)

    # def make_base_info(self, perm_prog_log_dict):
    #     '''
    #     ------------------------------------
    #     perm_prog_log_dict = {'UserName': 'incam-incam',
    #                 'JobName': 'cype-pc0002-v1d01-antipos',
    #                 'StateCode': '200',
    #                 'ProgramState': 'Pass',
    #                 'Software': 'incam',
    #                 'IsSave': 0,
    #                 'ExecID': '705686',
    #                 'TRVer': 'Test',
    #                 'ProgramVer': '240704',
    #                 'ExecMode': 'Manual',
    #                 'LogMsg': '[]',
    #                 'LogTime': '2024-07-04 13:25:35',
    #                 'RunTime': 0.00269985198975
    #                 }
        
    #     '''
        
    #     base_info_list = [' ------- {0} ------- '.format(perm_prog_log_dict['LogTime'])]
    #     base_info_list.append('使用者 : ' + perm_prog_log_dict['UserName'].split('-')[1])
    #     base_info_list.append('執行結果 : ' + perm_prog_log_dict['ProgramState'])
    #     return base_info_list
    # def parse_perm_prog_log_dict(self,perm_prog_log_dict): 
    #     '''
    #     This method parse perm_prog_log_dict and 
    #     set to self.program_log
    #     '''
    #     if perm_prog_log_dict == {}:
    #         return 
    #     base_info_list = self.make_base_info(perm_prog_log_dict)

    #     # base_info = 'Program : {0} 執行完畢, Code : {1}'.format(self.program_name, '200')

    #     raw_log_msg = perm_prog_log_dict['LogMsg']
    #     parsed_log_list = raw_log_msg
    #     if len(parsed_log_list) == 0:
    #         parsed_log_list = [] 
    #     base_info_list.extend(parsed_log_list)
    #     self.program_log.append(base_info_list)

    ''' ==================== old read perm log end ===================== '''
    def get_newest_perm_log_dict(self, perm_log_list):
        '''
        cur_job_nmae = 'cype-pc0002-v1d01-antipos'
        i =
        '''
        newest_perm_log_dict = {}
        if len(perm_log_list) == 0:
            return {}
        cur_job_nmae = self.parent.job_name
        for i in range(len(perm_log_list)-1, -1, -1):
            try:
                newest_perm_log_dict = eval(perm_log_list[i])
                if cur_job_nmae == newest_perm_log_dict['JobName'] and\
                      self.last_exec_id == newest_perm_log_dict['ExecID']:
                    return newest_perm_log_dict
                 
            except:
                pass
        return {}
    
    def get_perm_prog_log_dict(self):
        '''
        
        file_name = 'Release_3716207.txt'
        file_path = os.path.join(os.getcwd(), 'TESTFILES', file_name)
        '''
        perm_prog_log_dict = {}
        # if self.program_log :
        #     #already got program_log.
        #     return 
        # if not self.last_exec_id:
        #     #havent executed before.
        #     return 
        
        #search by TR_ver, JobID and last_exec_id
        # self.program_log = ''
        folder_path = os.path.join(self.main_folder_path, 'Log')
        file_name = '{0}_{1}.txt'.format(self.parent.TR_ver, self.parent.job_id)
        file_path = os.path.join(folder_path, file_name)

        if not os.path.isfile(file_path):
            return perm_prog_log_dict
        with open(file_path, 'r') as f:
            perm_log_list = f.readlines()
        
        if len(perm_log_list) == 0:
            return perm_prog_log_dict  
           
        perm_prog_log_dict =  self.get_newest_perm_log_dict(perm_log_list)
        return perm_prog_log_dict

            # parsed_log_list = LogParser.program_log2ui(log_list)
        # for log_line in parsed_log_list:
        #     self.program_log.append(log_line)
        ''' ========================================================= '''
        # for log in perm_log:
        #     log = eval(log)
        #     if self.last_exec_id == log['ExecID'] and self.parent.TR_ver == log['TRVer']:
        #         print( '************ : ' + str(self.parent.TR_ver) + log['TRVer'])
        #         if  log['LogMsg'] != '[]':
        #             log_msg = log['LogMsg']
        #         break
        # self.program_log.extend(log_msg)

        ''' ========================================================= '''
        # full log mechanism ##
        # self.parent.LogBox.append(file_path)
        # if os.path.isfile(file_path):
        #     with open(file_path, 'r') as f:
        #         perm_log = f.readlines()
        #     log_msg = ''
        #     for log in perm_log:
        #         log = eval(log)
        #         # if self.last_exec_id == log['ExecID'] and self.parent.TR_ver == log['TRVer']:
        #         if self.parent.TR_ver == log['TRVer']:
        #             print( '************ : ' + str(self.parent.TR_ver) + log['TRVer'])
        #             if  log['LogMsg'] != '[]':
        #                 log_msg = log['LogMsg']
                        
        #                 ''' =========== make log list ============== '''
        #                 log_list = eval(log_msg)
        #                 for log_line in log_list:
        #                     self.program_log.append(log_line)


    ''' ================== '''
    '''    Click Method    '''
    ''' ================== '''
    def release_clicked(self):
        try:
            if self.label.result_state in ['Error', 'Fail']:
                msg = "{0} 執行錯誤, 無法發佈".format(self.button_text)
                self.parent.LogBox.append(msg)
                self.program_log.append(msg)
                return 
            main_folder_path = os.path.join(self.parent.root_path,
                                            self.main_folder_path)
            
            msg = release_program(main_folder_path,
                            self.program_name,
                            self.current_ver,
                            self.button_text)
            
            self.auto_update_flag = True
            
            self.parent.LogBox.sys_append(msg)
            self.program_log.append(msg)
        except Exception as e:
            err_msg = traceback.format_exc()
            self.parent.LogBox.sys_append(err_msg)
    def delete_clicked(self): 
        extra_msg = u''
        if has_release_ver(self.main_folder_path):
            extra_msg += u"正是區有程式\n"
        msg_box = QtGui.QMessageBox(2, u'警告', extra_msg + u'請確認是否要刪除程式',
                                     QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        reply = msg_box.exec_() 

        if reply == QtGui.QMessageBox.Yes:
            print('Confirmed')
        else:
            return 
        try:
            # get cur ListWidgetItem.
            for i in range(self.process_tab.listWidget.count()):
                item = self.process_tab.listWidget.item(i)
                frame = self.process_tab.listWidget.itemWidget(item)
                if frame == self: 
                    self.process_tab.listWidget.takeItem(i)
                    break
            # self.process_tab.listWidget.
            # self.parent.tabWidget_process.findChild(QListWidget,)
            # msg = 'hi'
            # self.parent.LogBox.append(msg)
        except Exception as e:
            err_msg = traceback.format_exc() 
            self.parent.LogBox.append(err_msg)
    def open_folder_clicked(self, force = False):
        try:
            if not force and self.parent.privilage == 'User':
                return 

            file_path = self.get_exec_file_path()
            
            #file_path = r'\\ezcamls\ezcam\sys\scripts\0_TestingProgram\_AutoCamGui\Preprocess\Main_tmp_827\Test\tmp_827-15143\main.py'
            folder_path = os.path.dirname(file_path)
            if not os.path.isdir(folder_path): 
                folder_path = os.path.dirname(folder_path)
                 
            #open test/ release folder
            if os.path.isdir(folder_path): 
                # os.startfile(folder_path)
                open_file_or_directory(folder_path)
                
        except Exception as e:
            err_msg = traceback.format_exc()
            print(err_msg)
            self.parent.LogBox.append(err_msg)
    def sub_copying_clicked(self, action):
        dest_process_key = str(action.objectName())
        # sub_program_copying(process_key,
        #                     self.button)

        
        is_success = self.parent.copy_sub_program(self, dest_process_key, self.parent.TR_ver)
        if not is_success:
            return 
        # msg = '程式 : {0} 已複製到 {1} '.format(self.parent.button_text, str(action.text()))
        # + self.parent.button_text + u'"的新版本'
        msg = '程式 "' + self.button_text + '" 已複製到 ' +str(action.text().toUtf8())
        self.parent.LogBox.append(msg) 
        # self.parent.parent.LogBox.append(msg)



    def on_parent_TR_ver_changed(self):
        self.set_TR_ver(self.parent.TR_ver) 
        self.menu = ProgramFrameMenu(self)
    def set_TR_ver(self, TR_ver):
        self.auto_update_flag = False
        self.refresh_combobox(TR_ver)
        self.auto_update_flag = True
    def refresh_combobox(self, TR_ver = None):
        if self.comboBox is None:
            return 

        if not TR_ver:
            TR_ver = self.parent.TR_ver
        #reset info in readme
        self.release_log = '' 
        self.description = ''
        ''' Reset combobox ''' 
        self.comboBox.clear() 
        #get version folder list
        ver_path = os.path.join(self.main_folder_path, TR_ver)


        if os.path.isdir(ver_path):
            ver_list = os.listdir(ver_path)
            valid_ver_list = get_valid_ver_list(ver_list)

            #add empty
            self.comboBox.addItem(' ')
            #add all version folder to combobox
            for ver_folder in valid_ver_list:
                # self.comboBox.addItem('-'.join(ver_folder.split('-')[1:]))
                self.comboBox.addItem(str(ver_folder))
                
            ### set default value.
            cur_ver = self.TR_ver_folder[TR_ver]
            # Find the index of the desired text in the item list
            index = self.comboBox.findText(cur_ver)
            if index != -1:
                # Set the current index of the combobox to the index of the desired text 
                self.comboBox.setCurrentIndex(index) 

        else:

            msg = 'Path {0} is not exist'.format(ver_path)
            print(msg)
            # self.parent.LogBox.append(msg)
    def on_parent_privilage_changed(self):
        self.set_privilage(self.parent.privilage)
    def set_privilage(self, privilage):
        if privilage == 'User':
            is_visible = False
        else:
            is_visible = True
        if self.comboBox is not None:
            self.comboBox.setVisible(is_visible)
    def contextMenuEvent(self,event): 
        if self.parent.privilage == 'User':  
            return
        try:
            self.select()
            self.menu.exec_(event.globalPos())  
        except Exception as e:
            err_msg = traceback.format_exc()
            print(err_msg)
    def get_exec_file_path(self):
        TR_ver_path = os.path.join(self.parent.root_path, self.main_folder_path, self.parent.TR_ver)  
        if self.comboBox is None:
            ver_folder_path = os.path.join(TR_ver_path, self.program_name ) 
            file_path = os.path.join(ver_folder_path, 'Entrance.py') 
        else:
            # TR_ver_path = 'D:\AutoCam\Preprocess\Main_tmp_3339\Test'
            ver_folder_path = os.path.join(TR_ver_path, self.program_name + '-' + self.current_ver) 
            file_path = os.path.join(ver_folder_path, 'Entrance.py') 
        return file_path
    def get_sub_src_copying_folder_path(self):  
        src_folder_path = os.path.dirname(self.get_exec_file_path())
        sub_folder = 'SubFolder'
        src_copying_folder_path = os.path.join(src_folder_path, sub_folder)
        return src_copying_folder_path
    def get_parent_path(self):
        '''
        r'/InCAM/server/site_data/scripts/AutoCAM2.0/Test/Main_Pass/Test/Pass-240704-1-1105'
        version = '240704-1-1105'
        '''
        parent_path = ''
        TR_ver = self.parent.TR_ver
        parent = self.parent_program
        if parent == '':
            return parent_path
        process = self.parent.program_config[parent]['process']
        version = self.parent.program_config[parent]['TR_ver_folder'][TR_ver]
        TR_ver_path = os.path.join(self.parent.root_path, process, 'Main_' + parent, TR_ver)

        ver_folder_path = os.path.join(TR_ver_path, parent + '-' + version) 
        
        parent_path = os.path.join(TR_ver_path, ver_folder_path)
        return parent_path
    def exec_clicked(self):
        try:
            # get exec_info 
            exec_info = self.parent.info_model.pack_exec_info(exec_mode = 'Manual') 
            exec_info["LOG_PATH"] = os.path.join(self.parent.root_path, self.main_folder_path, 'Tmp')  
            exec_info["PROGRAM"] = self.program_name
            file_path = self.get_exec_file_path()
            # folder_path = os.path.dirname(file_path)
            # exec_info["PROGRAM_VER"] = self.current_ver.split('-')[1]
            exec_info["PROGRAM_VER"] = self.current_ver
            # run
            self.run(exec_info)
            if not self.parent.check_pipe():
                self.parent.close()

        except Exception as e:
            err_msg = traceback.format_exc()
            print(err_msg) 
            self.parent.LogBox.append(err_msg)
    def run(self, exec_info):
        '''
        Run program
        Parse tmp Log
        Update permanent program log
        Update tmp job log
        Set label state
        return : True, False -> Whether run next program.
        '''
        if self.available == False:
            return 
            
        is_shell = True if platform.system() == 'Linux' else False

        program_state, state_code = 'Error', '505' #default
        is_non_open_job = False
        if exec_info["PROGRAM"] in ["CreateJob"]:
            is_non_open_job = True
        if is_non_open_job:
            exec_info["JOB_NAME"] = "Unknown"
            exec_info["JOB_ID"] = str(random.randint(1000000, 9999999))
        # if exec_info["PROGRAM"] in ["CreateJob"]:
        #     os.environ['STEP'] = 'ipc'
        # if exec_info["PROGRAM"] in ["CreateOrg"]:
        #     os.environ["STEP"] = 'org'
        # if exec_info["PROGRAM"] in ["CreatePCB"]:
        #     os.environ["STEP"] = 'pcb'
        try:
            ''' ======================= get file_path ======================= ''' 
            file_path = self.get_exec_file_path()
            ''' ======================== run program ======================== '''
            # get set ENVIRONMENT VARIABLE
            ENV_VAR = str(exec_info) 

            # get PARAMETER CONFIG
            PARAM_CONFIG = parse_param_config()
            PARAM_CONFIG['PARENT_PATH'] = self.get_parent_path()
            if os.path.isfile(file_path): 
                if is_shell:
                    cmd = r'python "{0}" "{1}" "{2}"'.format(file_path, ENV_VAR, PARAM_CONFIG)
                else:
                    cmd = r'\\ezcamls\ezcam\1.1\resource\python\Anaconda2\python.exe "{0}" "{1}" "{2}"'.format(file_path, ENV_VAR, PARAM_CONFIG)
                is_success = os.system(cmd)
            else:
                self.parent.LogBox.sys_append('File {0} not found'.format(file_path)) 
            ''' ======================= call log_parser ====================== '''      
            record_log, file_path = LogParser.record_log_reader(
                                                main_folder_path = self.main_folder_path,
                                                TR_ver   = exec_info['TR_VER'],
                                                exec_id  = exec_info['EXEC_ID'],
                                                job_name = exec_info['JOB_NAME'])
            record_log = record_log.decode('utf-8')
            if record_log == '':
                self.label.set_result_state('Error')
                error_code = 506
                msg = UI_MSG['LOGFILE_NOT_FOUND'].format(self.button_text, file_path, error_code)
                self.parent.LogBox.sys_append(msg) 
                return error_code
            # raw_prog_log, program_state, msg_log, state_code =\
            program_log_dict, is_end_properly = LogParser.record_log_paser(record_log) 
            if not is_end_properly:
                self.label.set_result_state('Error')
                error_code = 507
                msg = UI_MSG['PROGRAM_TERMINATED_ABNORMALLY'].format(self.button_text, error_code)
                
                self.parent.LogBox.sys_append(msg) 
                return error_code
 
            #get JOB_NAME for program "CreateJob" 
            if is_non_open_job:
                '''
                update_window_jobinfo()
                '''
                # self.parent.LogBox.append('=========')
                # self.parent.LogBox.append(str(raw_prog_log))
                # self.parent.LogBox.append('=========')
                job_name = program_log_dict['JobName']
                job_id = program_log_dict['JobID'] 
                if job_name:
                    exec_info["JOB_NAME"] = job_name
                    os.environ["JOB"] = job_name
                    exec_info["JOB_ID"] = job_id
                    #為了解決create job後人員沒關介面的問題
                    self.parent.job_name = os.environ["JOB"]
                    self.parent.info_model.job_name = os.environ["JOB"]

                    self.parent.job_id = job_id
                    self.parent.info_model.job_id = job_id

                    self.parent.setup_title()
                    self.parent.source = self.parent.info_model.get_source()
                    # os.environ["SOURCE"] = self.parent.source
            if program_log_dict['StateCode'] in ['204', '502']:
                return program_log_dict['StateCode']
            

            if exec_info['EXEC_MODE'] == 'Test':
                msg = UI_MSG['EXECUTE_ENDING_MSG'].format(self.button_text, program_log_dict['StateCode'])
            else:
                msg = UI_MSG['TESTING_ENDING_MSG'].format(self.button_text, program_log_dict['StateCode'])
            ## ==================== show msg ==================== ##
            self.parent.LogBox.sys_append(msg)
            self.parent.LogBox.clear()
            self.parent.LogBox.append(self.frame_title)

            if program_log_dict['StateCode'] in ['505', '506'] :
                msg = UI_MSG['ERROR_05_06'].format(self.program_name, program_log_dict['StateCode']) 
                # self.parent.LogBox.sys_append(msg)
                self.label.set_result_state('Error') 
                return program_log_dict['StateCode']
            
            if exec_info['EXEC_MODE'] == 'Test': 
                #in test mode we don't save any permanent log
                if program_log_dict['StateCode'] == '200':
                    program_state = 'PassTest'
                else:
                    program_state = program_log_dict['State']
                self.label.set_result_state(program_state)
                return program_log_dict['StateCode']
          
            
            self.last_exec_id = exec_info["EXEC_ID"]
            # Update permanent program log
            
            
            db_log = LogParser.create_db_log(program_log_dict)
            ## force switch save info

            if check_is_non_save_program(db_log['ProgramName']): 
                db_log['IsSave'] = 1

            


            LogParser.write_perm_prog_log(
                self.main_folder_path, db_log )
            # Update tmp job log 
            LogParser.write_tmp_job_log(
                self.parent.root_path, db_log )

            # self.set_program_log(log_list) #save in frame log 
            self.update_execute_log(db_log)
            self.show_history_execute_log()
            
            # self.show_program_log(perm_prog_log_dict) #show in frame log 
            ''' ======================= Set Label State ======================= '''
            self.label.set_result_state(program_log_dict['State'])
        except Exception as e:
            err_msg = traceback.format_exc() 
            self.parent.LogBox.sys_append(err_msg)
            self.label.set_result_state('Error') 

        


        return program_log_dict['StateCode']
 
    def _set_style(self, selection):
        if selection == 'unselect':
            qss = """
            QFrame {
                    padding :4px;
                    border :2px solid #d9d9d9;
                    border-radius : 3px;
                    background-color : #333333;
                    color : #12a3f7; 
                    font-size : 8pt;
                    font-weight: bold;
                    }
            QFrame:hover {
                    padding :4px;
                    border :2px solid #d9d9d9;
                    border-radius : 3px;
                    background-color: #81939e;
                    font-size : 8pt;
                    font-weight: bold;
                    }
            """
        elif selection == 'select':
            qss = """
            QFrame {
                    padding :4px;
                    border :2px solid #d9d9d9;
                    border-radius : 3px;
                    background-color : #354294;
                    font-size : 8pt;
                    font-weight: bold;
                    }
            QFrame:hover {
                    padding :4px;
                    border :2px solid #d9d9d9;
                    border-radius : 3px;
                    background-color: #81939e;
                    font-size : 8pt;
                    font-weight: bold;
                    }
            """
        self.setStyleSheet(qss)
def check_is_non_save_program(program_name):
    for non_save_program in FORCE_SWITCH_SAVE_STATUS_PROGRAM_LIST:
        if non_save_program.upper() in program_name.upper():
            return True
    return False

            
def has_release_ver(main_folder_path):
    release_folder = os.path.join(main_folder_path, 'Release')
    if os.path.isdir(release_folder) and len(os.listdir(release_folder)) > 0:
        return True
    return False
def release_program(main_folder_path,
                    program_name,
                    current_ver,
                    button_text,):
    '''
    main_folder_path = "AutoCAM2.0/InnerNeg/Main_Pass"
    program_name = 'pass'
    current_ver = '230807-1-1231'
    button_text = '測試'
    '''
    test_folder_path = os.path.join(main_folder_path,
                                    'Test',
                                    program_name + '-' + current_ver)  
    if not os.path.isdir(test_folder_path):
        msg = 'Test folder : {0} 不存在'.format(current_ver)
 
        return msg

    release_folder_path = os.path.join(main_folder_path,
                                    'Release',
                                    program_name + '-' + current_ver)  
    if os.path.isdir(release_folder_path):
        msg = '版本 : {0} {1} 已經存在'.format(button_text, current_ver)
        return msg

    shutil.copytree(test_folder_path, release_folder_path)
    msg = '版本 : {0} {1} 發佈成功'.format(button_text, current_ver)
    return msg

def open_file_or_directory(path):
    if platform.system() == 'Windows':
        subprocess.Popen(['start', '', path], shell=True)
    elif platform.system() == 'Linux':
        subprocess.Popen(['xdg-open', path])
    elif platform.system() == 'Darwin':  # macOS
        subprocess.Popen(['open', path])
def get_valid_ver_list(ver_list):
    '''
    ver_list = ['testProgram-240522-5-1235',
                    'testProgram-240522-2-1235',
                    'testProgram-240522-3-1239']
                    
    '''
    valid_ver_list = []
    for ver_name in ver_list:
        if ''.join(ver_name.split('-')[1:3]).isdigit():
            valid_ver_list.append(ver_name)

    valid_ver_list = sorted(valid_ver_list, key = lambda x: int(''.join(x.split('-')[1:3])), reverse=True)
    valid_ver_list = list(map(lambda x:'-'.join(x.split('-')[1:4]), valid_ver_list))
    return valid_ver_list   
def parse_param_config(ui_param_config = {}):
    '''
    ui_param_config = {
        'job_name':{
        'order' : 0,
        'Widget': '', #maybe use to append some Widget Module.
        'Input' : '', #'' for line text
        'Label' : 'Job Name'
        },
        'gerber_path':{
            'order' : 1,
            'Widget': '', #maybe use to append some Widget Module.
            'Input' : '', #'' for line text
            'Label' : 'Gerber Path'
            }
    }
    '''
    param_config = {}
    # if not ui_param_config:
    #     if self.program_name in self.parent.param_config.keys():
    #         ui_param_config = self.parent.param_config[self.program_name]
        
    # for param_key, param_dict in ui_param_config.items():
    #     param_config[param_key] = str(param_dict['Value'])
    return  param_config

''' ========================================================================== '''
    # ## To parse ExecuteConfig to get is available
    # ## stop use 2024/08/23
    # def is_program_work(self, CONFIG):
    #     for _, config_dict in CONFIG.items():
    #         pass
    #         if not self.check_condition(config_dict):
    #             return False
    #     return True
    # def check_condition(self, config_dict):
    #     #return False if can't work
    #     if config_dict == {}:
    #         return False
    #     key, value_list = config_dict.popitem()
    #     if value_list == ['*']:
    #         return self.check_condition(config_dict)
    #     if key not in self.parent.program_execute_condition_config.keys(): 
    #         self.parent.LogBox.sys_append('{0} no key {1} in ENV_DICT '.format(self.pushButton.text(), key))
            
    #         return self.check_condition(config_dict)

    #     if self.parent.program_execute_condition_config[key] not in value_list:
    #         return True
    #     return self.check_condition(config_dict)
''' ========================================================================== '''



class ProgramStateLabel(QtGui.QLabel):
    _TextMap ={
        'Disable': 'Disable',
        'None': '',
        'Ready': 'Ready',
        'Wait': u'準備執行',
        'PassTest': u'測試通過',
        'Pass': u'通過',
        'Warning': u'警告',
        'Error': u'錯誤',
        'Fail': u'失效',

    }
    _LABEL_STATE_STYLE_DICT = {
                        'Disable' : "QLabel { \
                            border :2px solid #333333;\
                            border-radius : 3px;\
                            background-color : #767778;\
                            color : #005100 ; \
                            font-size : 12pt;\
                            font-weight: bold;\
                            }",
                        'None' : "QLabel { \
                            border :2px solid #333333;\
                            border-radius : 3px;\
                            background-color : #c4c4c4;\
                            color : #333333; \
                            font-size : 12pt;\
                            font-weight: bold;\
                            }",
                        'Ready' : "QLabel { \
                            border :2px solid #333333;\
                            border-radius : 3px;\
                            background-color : #c4c4c4;\
                            color : #333333; \
                            font-size : 12pt;\
                            font-weight: bold;\
                            }",
                        'Wait' : "QLabel { \
                            border :2px solid #333333;\
                            border-radius : 3px;\
                            background-color : #c4c4c4;\
                            color : #333333; \
                            font-size : 12pt;\
                            font-weight: bold;\
                            }",
                        'PassTest' : "QLabel { \
                            border :2px solid #005100;\
                            border-radius : 3px;\
                            background-color : #4CAF50;\
                            color : #005100; \
                            font-size : 12pt;\
                            font-weight: bold;\
                            }",
                        'Pass' : "QLabel { \
                            border :2px solid #005100;\
                            border-radius : 3px;\
                            background-color : #4CAF50;\
                            color : #005100; \
                            font-size : 12pt;\
                            font-weight: bold;\
                            }",
                        'Warning' : "QLabel { \
                            content : 'hi';\
                            border :2px solid #916e00;\
                            border-radius : 3px;\
                            background-color : #FFCC00;\
                            color : #916e00; \
                            font-size : 12pt;\
                            font-weight: bold;\
                            }",
                        'Error' : "QLabel { \
                            border :2px solid #921d2b;\
                            border-radius : 3px;\
                            background-color : #de6365;\
                            color : #921d2b; \
                            font-size : 12pt;\
                            font-weight: bold;\
                            }",
                        'Fail' : "QLabel { \
                            border :2px solid #921d2b;\
                            border-radius : 3px;\
                            background-color : #de6365;\
                            color : #921d2b; \
                            font-size : 12pt;\
                            font-weight: bold;\
                            }",
    }
    def __init__(self, state):
        super(ProgramStateLabel, self).__init__()
        self.available = True
        #distinct, is now label display result or not. False -> idle; True -> result
        self.is_result = False 
        self.result_state = 'None'
        self.idle_state   = 'None'
        self.set_idle_state(self.idle_state) 
#        self.mousePressEvent = self.mousePressEvent
        self._setupUi() 
        self.adjustSize()
    def _setupUi(self):
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(100, 30))
        self.setAlignment(QtCore.Qt.AlignCenter)


    def set_available(self, available):
        self.available = available
        if self.available == False:
            self.setStyleSheet(self._LABEL_STATE_STYLE_DICT['Disable'])
        else:
            if self.result_state != 'None':
                self.setStyleSheet(self._LABEL_STATE_STYLE_DICT[self.result_state])
            else:
                self.setStyleSheet(self._LABEL_STATE_STYLE_DICT[self.idle_state])



    def mousePressEvent(self,event):
        '''
        #executed
        I_None -> I_Wait -> R_state -> I_None
        #not execute yet
        I_None -> I_Wait -> I_None
        '''
        self.on_pressed()
    def on_pressed(self):
        if not self.available:
            return 
        if self.idle_state == 'Wait':
            self.set_result_state(self.result_state)
        elif self.idle_state == 'None': 
            self.set_idle_state('Wait') 
            # if self.is_result: #executed.
            #     self.set_idle_state('None')
            # else: 
            #     if self.result_state == 'None': #not execute yet
            #         if self.idle_state == 'Wait':
            #             self.set_idle_state('None')
            #         else:    
            #             self.set_idle_state('Wait')
            #     else: #executed
            #         if self.idle_state == 'None':
            #             self.set_idle_state('Wait')
            #         elif self.idle_state == 'Wait':
            #             self.set_result_state(self.result_state)
    
    def set_result_state(self,state = None):
        
        if not self.available:
            return 
        # self.is_result = True
        if state is None:
            state = self.result_state
        
        self.result_state = state
        self.idle_state = 'None'

        self.setText(self._TextMap[state]) 
        if self.available == False:
            self.setStyleSheet(self._LABEL_STATE_STYLE_DICT['Disable'])
            return 
        if state in self._LABEL_STATE_STYLE_DICT.keys():
            self.setStyleSheet(self._LABEL_STATE_STYLE_DICT[state])
    def set_idle_state(self, state):

        if not self.available:
            return 
        # self.is_result = False
        self.idle_state = state

        self.setText(self._TextMap[state]) 
        if self.available == False:
            self.setStyleSheet(self._LABEL_STATE_STYLE_DICT['Disable'])
            return 
        if state in self._LABEL_STATE_STYLE_DICT.keys():
            self.setStyleSheet(self._LABEL_STATE_STYLE_DICT[state])
class ProgramButton(QtGui.QPushButton):
    def __init__(self, text,parent=None):
        super(ProgramButton, self).__init__(parent)        
        self.setText(text)
        self.setMinimumSize(QtCore.QSize(0, 30)) 
#    def _setText(self,text):
#        self.setText(QtGui.QApplication.translate("MainWindow", text, None, QtGui.QApplication.UnicodeUTF8))

class ProgramVerComboBox(QtGui.QComboBox):
    def __init__(self,parent=None):
        super(ProgramVerComboBox, self).__init__(parent)        
        # self.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.setMinimumSize(QtCore.QSize(0, 40))
        self.view().setMinimumWidth(200)
    def wheelEvent(self, event):
        pass  # Do nothing when the mouse wheel is scrolled
class ProgramFrameMenu(QtGui.QMenu):
    def __init__(self,parent=None):
        super(ProgramFrameMenu, self).__init__(parent)         
        '''
        parent : frame
        '''
        self.parent = parent
        self.setStyleSheet(self.parent.styleSheet())
        self.setFixedSize(200, 200)


        open_folder = self.addAction(u"開啟資料夾")
        open_folder.triggered.connect(self.parent.open_folder_clicked)
        
        paste = self.addAction(u"貼上程式名稱")
        paste.triggered.connect(self.paste_clicked) 
           

        if self.parent.parent.TR_ver == 'Test':
            release = self.addAction(u"發佈正式版")
            release.triggered.connect(self.parent.release_clicked)

        delete = self.addAction(u"刪除程式")
        delete.triggered.connect(self.parent.delete_clicked)

        update_sub = self.addAction(u"更新子程式接口")
        update_sub.triggered.connect(self.parent.update_sub_clicked)
        
        sub_menu = self.make_sub_copying_menu()
        
        self.addMenu(sub_menu)
        self.addAction(sub_menu.menuAction())

        # move_to.triggered.connect(self.parent.move_to_hover)
    def make_sub_copying_menu(self):

        sub_menu = QtGui.QMenu(self) 
        sub_menu.setTitle(u"複製到..")

        actions = []
        for process_key, process_name in PROCESS_LIST:
            action = QtGui.QAction(process_name, sub_menu)
            action.setObjectName(process_key)
            actions.append(action)
            # action.triggered.connect(self.sub_copying_clicked)
        sub_menu.addActions(actions)

        sub_menu.triggered.connect(self.parent.sub_copying_clicked)
        return sub_menu

    def paste_clicked(self):
        if self.parent.parent.privilage == 'User':
            return 
        print('click paste') 
        clipboard = QtGui.QApplication.clipboard()
        text_list = clipboard.text().toUtf8().data().decode('utf-8')
#        text_list = text_list.encode("ascii", errors="ignore")
 
        
        text_list = text_list.split('\n')
        for text in text_list:
            if text:
                self.parent.pushButton.setText(text)


class ParamConfigReader(View_ParamConfigReader, QtGui.QFrame):

    def __init__(self,parent):
        super(ParamConfigReader, self).__init__(parent)     
        self.parent = parent
        self.setupUi(self)    
        self.pushButton_save.clicked.connect(self.save_clicked)


    def reset_frame(self, program_key,ver_folder):
        program_key = str(program_key)
        # self.setObjectName(program_key)
        self.clear_frame()
        if program_key in self.parent.param_config.keys():
            program_config_dict = self.parent.param_config[str(program_key)]
        else:
            program_config_dict = self.get_n_parse_input_config(str(program_key), ver_folder)
        print('*************** enter reset *******************')
        #update parsed parameter config to parent.param_config
        print('reset update : ',str(program_key))
        self.parent.param_config[str(program_key)] = program_config_dict
        self.setup_input_config(program_config_dict)
        # self.etl_parameters()
    def get_n_parse_input_config(self, program_key, ver_folder):

        '''
        base format for each parameter.
        "job_name": {
            "Input": "", 
            "Widget": "", 
            "order": 1, 
            "Value": "", 
            "Label": "Delete Rout"
        }
        '''
        new_param_config = {}
        json_path = os.path.join(str(ver_folder), 'config.json')
        if os.path.isfile(json_path):    
            with open(json_path, "r") as file:
                raw_param_config = json.load(file)
        
            param_config_key_list = sorted(raw_param_config.keys(), key = lambda x:raw_param_config[x]['order'])
            count = 0
            new_param_config = {}
            for group_key in param_config_key_list:
                if 'Items' in group_key:
                    group_dict = raw_param_config[group_key]

                    parse_group_dict = self.items_parser(group_dict)
                    new_param_config.update(parse_group_dict)

                else:
                    new_param_config[group_key] = raw_param_config[group_key]
        else:
            print('no parameter config : {0}'.format(program_key))
        return new_param_config
    def setup_input_config(self, program_config_dict):
        count = 0 
        for item_key, item_dict in program_config_dict.items():

            frame = ParamFrame(item_key, item_dict)
            self.gridLayout.addWidget(frame, count, 0)
            count +=1
    def clear_frame(self):
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            else:
                self.gridLayout.removeItem(item)
        # for i in reversed(range(self.gridLayout.count())):
        #     item = self.gridLayout.itemAt(i)
        #     widget = item.widget()
        #     if widget and isinstance(widget, QtGui.QFrame):
        #         widget.deleteLater()
        self.gridLayout.setColumnMinimumWidth(0, 0)
        self.gridLayout.setRowMinimumHeight(0, 0)
        self.gridLayout.update()

    def items_parser(self, group_dict):
        new_group_dict = {}
        rule_key =  group_dict['NumRule']['RuleKey'] 
        reg  =  group_dict['NumRule']['Reg'] 
        item_dict = group_dict['Item']
        if rule_key == 'STEP':
            candi_list = ['ipc', 'org','a-pcb1','aapcb2','aapcb2','aapcb2']
        filtered_list = [item for item in candi_list if re.search(reg, item)]
        for item_key in filtered_list:
            item_dict = copy.deepcopy(group_dict['Item'])
            if item_dict['Label'] == 'reg' :
                label_text = item_key
                item_dict['Label'] = label_text
            new_group_dict[item_key] = item_dict

        return new_group_dict
    
    def save_clicked(self):
        '''
        'job_name':{
            'order' : 0,
            'Widget': '', #maybe use to append some Widget Module.
            'Input' : ['a','b'], #'' for line text
            'Value' : '',
            'Label' : 'Arrange'
        },
        '''
        return_dict = {}
        # Loop through all frames in the grid layout
        for row in range(self.gridLayout.rowCount()):
            for col in range(self.gridLayout.columnCount()):
                if self.gridLayout.itemAtPosition(row, col):
                    frame = self.gridLayout.itemAtPosition(row, col).widget()
                    if isinstance(frame, QtGui.QFrame):
                        # Do something with the frame
                        
                        parame_key  = str(frame.objectName())
                        param_value = str(frame.widget.text()) 
                        return_dict[parame_key] = {
                            'Value' : param_value
                        }

        program_name = str(self.objectName())
        # program_param_dict = self.parent.frame_program_configs.etl_parameters()
        for param_key, value_dict in return_dict.items():
            self.parent.param_config[program_name][param_key].update(value_dict)
        return 

class ParamFrame(QtGui.QFrame):
    def __init__(self,  
                 frame_key,        
                 item_dict):
        '''
        frame_key : objectName, also parameter dict key
        label_text: text of label, can be chinese.
        '''
        super(ParamFrame, self).__init__()
        self.frame_key = frame_key
        
        self.setObjectName(self.frame_key)
        self._setupUi(item_dict)
        self.setObjectName(frame_key) 



    def _setupUi(self,item_dict): 
        horizontalLayout = QtGui.QHBoxLayout(self) 
        input = item_dict['Input'] 
        if input == 'String':
            self.widget = QtGui.QLineEdit()
            self.widget.setText(str(item_dict['Value']))
        elif type(input) == list:
            self.widget =  QtGui.QComboBox()
            for item_text in input:
                self.widget.addItem(item_text)
            if item_dict['Value']:
                self.widget.setCurrentText(str(item_dict['Value']))
        elif input == "Bool":
            self.widget = QtGui.QCheckBox()
        
        horizontalLayout.addWidget(QtGui.QLabel(str(item_dict['Label'])))
        horizontalLayout.addWidget(self.widget)
        horizontalLayout.addStretch()
