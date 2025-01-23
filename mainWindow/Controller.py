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
from PyQt4 import QtGui, QtCore 
from PyQt4.QtCore import QTimer, QThread, QString
from PyQt4.QtGui import QFileDialog

reload(sys)
sys.setdefaultencoding("utf-8")


from process_config import PROCESS_LIST
# PATH CHANGE
os.chdir(os.path.dirname(os.path.abspath(__file__)))   

from Record import Record
import genClasses 




from view import Ui_MainWindow
import SQLModel
from InfoModel import InfoModel

import mainWindow.SystemConfig as SystemConfig 
from ProcessTab import ProcessTab
from ProgramFrame import ProgramFrame, ParamConfigReader, ParamFrame
import LogParser
from LogBox import LogBox
from ui.dev_frame_controller import DevFrame
from tmp_config import UI_CONFIG
from Frames.Batch.BatchFrame import BatchFrame 
from Frames.Tools.ToolFrame import ToolFrame 
from Frames.WaitingSetterDialog.WaitingSetterDialog import WaitingSetterDialog 

from project_utils import (check_main_folder_valid, is_folder_valid, 
                            get_program_name, get_folder_ver_name, 
                            get_program_key, get_process_by_config, 
                            check_is_program_frame_exist, create_standard_folder, 
                            copy_to_test_folder, copy_to_sub_folder,
                            get_program_frame, get_sub_folder_suffix,
                            get_sub_program_key_list  )
# from Utils.UiMoudule.LayerFrame.LayerFrame import LayerFrame


#%% 

class SignalManager(QtCore.QObject): 
    #attr chgange
    TR_ver_changed = QtCore.pyqtSignal(str)     # TR_ver change
    privilage_changed = QtCore.pyqtSignal(str)  # privilage change
    
    program_selected  = QtCore.pyqtSignal(str, str)  # a program frame is selected. str: program_name


    #program list in tab.
    program_list_clear_selection = QtCore.pyqtSignal()
SIGNAL_MANAGER = SignalManager() 
''' ******************************* main ui ******************************* '''
# class Worker(QThread):
#     update_signal = QtCore.pyqtSignal(int)

#     def __init__(self):
#         super(Worker,self).__init__()
#         self.working = True
#         self.num = 0
#     def __del__(self):
#         self.working=False
#         self.wait()


#     def run(self):
#         while self.working == True: 
#             self.update_signal.emit(1)
#             self.sleep(1)
     
#         self.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
#         self.setMinimumSize(QtCore.QSize(0, 30))


class MainUi(Ui_MainWindow, QtGui.QMainWindow):
    def __init__(self, TR_ver = 'Test'):
        super(MainUi, self).__init__()
        #get basic info
        self.setup_attr(TR_ver)
        #load_config
        self._setupUi()
        self.setup_click_event()
        # self.start_thread()
    # def start_thread(self):
    #     self.thread = Worker()
    #     self.thread.update_signal.connect(self.update_label)      
    #     self.thread.start()

    def setup_attr(self, TR_ver):
        
        self.history_db_logs_dict = {} #key :ProgramName, value : [db_log] 
        self.info_model = InfoModel()
        self.info_model.get_attr(TR_ver)
        ENV_VAR = self.info_model.pack_exec_info(exec_mode = 'UI')
        for key, value in ENV_VAR.items():
            os.environ[key] = ENV_VAR[key]
        ''' =========================================== '''
        self.root_path = os.environ['ROOT_PATH'] 


        self.gen_object = self.info_model.get_gen_object()
        self.user_name = self.info_model.get_user_name()
        self.privilage = self.info_model.get_privilage()
        self.TR_ver    = self.info_model.get_TR_ver(TR_ver)
        self.DB        = self.info_model.get_DB() 
        #cam obj
        self.software   = self.info_model.get_software()
        self.job_name   = self.info_model.get_job_name()
        self.source     = self.info_model.get_source()
        self.job_id     = self.info_model.get_job_id()
  

        self.record = Record(os.path.join(os.environ['ROOT_PATH'], 'mainWindow','Log'))
        self.record.info(self.record._id)
        # load from InfoModel
        self.param_config = self.info_model.load_param_config() 
        self.program_config = self.info_model.load_program_config()  

        #This config is for verifying if program execution conditions match.
        #Note: Keys must match the ExecuteConfig in the program.
        self.program_execute_condition_config ={
            'SOFTWARE' : self.software,
            'SOURCE'   : self.source
        }




    def _setupUi(self):
        self.setupUi(self)
        #hidden cpu label
        self.label_cpu_memory.setHidden(True)
        # set stackwidget_main on home page
        self.stackedWidget_main.setCurrentIndex(0)
        # Set the application icon (logo)
        Logo_path = os.path.join('mainWindow','ui','CHPT_logo.png')
        self.setWindowIcon(QtGui.QIcon(Logo_path))  # Replace with the actual path to your icon image
        
        #add log_box
        self.LogBox = LogBox()
        self.verticalLayout_tab_log.addWidget(self.LogBox)

        # container_widget = 
        # ui_frame = Ui_Frame()
        # self.DevFrame = ui_frame.setupUi(container_widget)  # 设置 Ui_Frame 中的控件

        # dev_frame = QtGui.QFrame(self)
        # self.DevFrame = DevFrame(self, dev_frame)
        # self.verticalLayout_dev.addWidget(dev_frame)
        self.tabWidget.setTabText(0, u"執行紀錄")
        self.tabWidget.setTabText(1, u"專案資訊")
        
        #add Parameter config reader #暫時廢棄這個功能
        # self.tabWidget.setTabText(2, u"專案參數")
        # self.frame_param_configs = ParamConfigReader(self)
        # self.verticalLayout_param_config.addWidget(self.frame_param_configs)

        self.setup_tabWidget_process()
        self.setup_stackedWidget_main()
        # self.setup_ui_state()
        
        self.updateUi_display()





    '''=============================================================='''
    '''                     Sub methods : setup ui                   '''
    '''=============================================================='''
    def setup_tabWidget_process(self):
        self.tabWidget_process.clear()
        #setup Process sheet
        for process_key, tab_name in PROCESS_LIST:
            tab = ProcessTab(process_key, SIGNAL_MANAGER, self)
            tab.setObjectName(process_key)
            tab_name = tab_name
            self.tabWidget_process.addTab(tab, tab_name)

            
        #setup program_frame of each Process
        for program_key, program_dict in self.program_config.items():
            process_key = program_dict['process']
            parent_key = program_dict.get('parent_program', '')
            tab = self.tabWidget_process.findChild(QtGui.QWidget, process_key)
            # loading check
            if not tab:
                self.LogBox.sys_append('[Warning] : No process_key : {0},\
                                        Failed to load Program {1}'\
                                       .format(process_key, program_key))
                continue
            is_main_folder_valid = check_main_folder_valid(program_dict['main_folder_path'])
            if not is_main_folder_valid:
                self.LogBox.sys_append('[Warning] : Failed to load Program {0}'.format(program_key))
            if parent_key != '' and parent_key not in self.program_config.keys():
                self.LogBox.sys_append('找不到 KEY : {0}'.format(parent_key))
                continue
            #create frame
            frame = ProgramFrame(SIGNAL_MANAGER,
                                 button_name = program_dict['button_name'],
                                 main_folder_path = program_dict['main_folder_path'],
                                 program_name = program_key,
                                 process_tab = tab,
                                 parent_program = parent_key,
                                 parent = self
                                 )
                                 
            order = int(program_dict['order'])
            
            while order >= tab.listWidget.count():
                item  = QtGui.QListWidgetItem(tab.listWidget)
                item.setSizeHint(frame.sizeHint())
                
                tab.listWidget.addItem(item)
#            tab.listWidget.insertItem(program_dict['order'], item)
            cur_item = tab.listWidget.item(order)            
            tab.listWidget.setItemWidget(cur_item, frame)            
        
            tab.listWidget.adjustSize()
            
            tab.adjustSize()
        self.tabWidget_process.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)

    def open_page_home(self):
        self.stackedWidget_main.setCurrentIndex(0)
    def open_page_dev_tools(self):
        self.stackedWidget_main.setCurrentIndex(1)
    def open_page_tools(self):
        self.stackedWidget_main.setCurrentIndex(2)
    def open_page_batch(self):
        self.stackedWidget_main.setCurrentIndex(3)
    def setup_stackedWidget_main(self):

        # dev_frame = QtGui.QFrame(self)
        # self.DevFrame = DevFrame(self, dev_frame)
        # self.verticalLayout_dev.addWidget(dev_frame)


        # self.layer_frame = ToolFrame(self.gen_object, self) 
        # self.stackedWidget_main.addWidget(self.layer_frame) 

        self.stackedWidget_main.addWidget(ToolFrame(self.gen_object, self) )

        dev_frame = QtGui.QFrame(self)
        self.DevFrame = DevFrame(self, dev_frame)
        self.verticalLayout_dev.addWidget(dev_frame)
        # self.stackedWidget_main.addWidget(self.DevFrame )

        self.stackedWidget_main.addWidget(BatchFrame(self.gen_object, self) )

    
    def updateUi_display(self):
        s = time.time()
        self.update_program_frame()
        self.preload_history_db_logs()
        self.hidden_object_reset()
        self.disable_object_reset()
        self.setup_title()
        self.update_mechanism()
        # self.LogBox.append(str(time.time() - s ))
    def update_program_frame(self):
        # if self.job_id == '404':
        #     return
        # return  
        job_init_program_log = self.info_model.load_init_program_log() 
        for i in range(self.tabWidget_process.count()):
            # process_text = str(self.tabWidget_process.tabText(i))
            tab  = self.tabWidget_process.widget(i)
            process_key  = str(tab.objectName())
            for index in range(tab.listWidget.count()):
                item = tab.listWidget.item(index)
                frame = tab.listWidget.itemWidget(item)
                if not frame:
                    continue
                #program_name = 'InnerPosAntiPad'
                program_name = str(frame.objectName())
                init_program_log = {}
                if self.job_id == '404':
                    init_program_log = {}
                elif program_name in job_init_program_log.keys():
                    init_program_log = job_init_program_log[program_name]
                frame.update_frame(
                    init_program_log = init_program_log
                    )
    def preload_history_db_logs(self):
        # LogParser.load_db_logs(self.job_id, self.job_name)
        
        self.history_db_logs_dict = self.info_model.load_history_db_logs() 

            

    def hidden_object_reset(self):
        is_user_hidden = False
        if self.privilage == 'User':
            is_user_hidden = True
        self.toolButton_test.setHidden(is_user_hidden)
        self.toolButton_program_info.setHidden(is_user_hidden)
        self.sidebar_button_dev_tools.setHidden(is_user_hidden)
        self.sidebar_button_batch.setHidden(is_user_hidden)
    def disable_object_reset(self):
        is_user_enable = True
        if self.privilage == 'User':
            is_user_enable = False
        self.actionSaveConfig.setEnabled(is_user_enable) 
        self.actionCreateProgram.setEnabled(is_user_enable) 
        self.menuPrivilage.setEnabled(is_user_enable)
        self.menuMode.setEnabled(is_user_enable)



    def setup_title(self):
        title = 'AutoCam - ver1.21 - {0} '.format(self.software)

        mode_color = 'red'
        privilage_color = 'red'

        if self.TR_ver == 'Release':
            mode_color = '#5dc05d'
        if self.privilage == 'User':
            privilage_color = '#5dc05d'
        

        _mode = "<font color='{0}'>{1}</font>".format(mode_color, self.TR_ver)
        _privilage = "<font color='{0}'>{1}</font>".format(privilage_color, self.privilage)
        status = u" &nbsp; 模式 : {0} &nbsp; 權限 : {1} &nbsp; 使用者 : {2} &nbsp; LogDB : {5} &nbsp; 案件 : {3} &nbsp; ID : {4} &nbsp;".\
                format(_mode, _privilage, self.user_name.split('-')[1], self.job_name, self.job_id, self.DB)
        self.setWindowTitle(title)
        self.label_info.setText(status)
    def update_mechanism(self):
        pass
 



    '''=============================================================='''
    '''               Sub methods : setup click event                '''
    '''=============================================================='''

    def setup_click_event(self):
        #side bar buttons
        self.sidebar_button_home.clicked.connect(self.open_page_home)
        self.sidebar_button_tools.clicked.connect(self.open_page_tools)
        self.sidebar_button_dev_tools.clicked.connect(self.open_page_dev_tools)
        self.sidebar_button_batch.clicked.connect(self.open_page_batch)

        #push button 

        
        self.toolButton_test.clicked.connect(self.test_clicked)
        self.toolButton_pause.clicked.connect(self._pause)
        self.toolButton_auto_run.clicked.connect(self.auto_run_clicked)
        self.toolButton_auto_select.clicked.connect(self.auto_select_clicked)
        self.toolButton_program_info.clicked.connect(self.program_info_clicked)
        #StackPage(dev_tools)::push button
        ## DevFrame
        
        # self.pushButton_copy_dev_job_info.clicked.connect(self.set_dev_info_on_clipboard) 
        #menu bar
        self.actionCreateProgram.triggered.connect(self.connect_program)
        self.actionSaveConfig.triggered.connect(self.save_program_config)
        #menu bar::TR_ver
        self.actionTest.triggered.connect(lambda:self.set_TR_ver('Test'))
        self.actionRelease.triggered.connect(lambda:self.set_TR_ver('Release'))
    
        #menu bar::privilage
        self.actionDeveloper.triggered.connect(lambda:self.set_privilage('Dev'))
        self.actionUser.triggered.connect(lambda:self.set_privilage('User'))
        self.actionSupervisor.triggered.connect(lambda:self.set_privilage('Supervisor'))
    
        #TabWidget 
        self.tabWidget_process.currentChanged.connect(self.handle_tab_changed)
        #short cut
        # self.pushButton_test.clicked.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_N))
        self.actionCreateProgram.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_N))
        self.actionSaveConfig.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S))
        # signal
        SIGNAL_MANAGER.TR_ver_changed.connect(self.on_TR_ver_changed)    
        SIGNAL_MANAGER.program_selected.connect(self.on_program_selected) 
        SIGNAL_MANAGER.privilage_changed.connect(self.on_privilage_changed)   
        SIGNAL_MANAGER.program_list_clear_selection.connect(self.on_program_list_clear_selection)


    def closeEvent(self,event): 
        # show message if detect config
        new_config = self.etl_ui_config()
        old = self.info_model.load_program_config()
        if self.is_config_change(new_config, old):
            reply = QtGui.QMessageBox.question(self, 'Confirm Exit', u'CONFIG 有更新, 是否要存檔?',
                                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.save_program_config()
            
        event.accept()
   
    def test_clicked2(self):

        self.delete_program()
        self.clear_selection()
 
    def test_clicked(self):
        # self.update_label()
        exec_info = self.info_model.pack_exec_info('Test')
        self.exec_program_queue(exec_info = exec_info)


    def auto_run_clicked(self): 
        exec_info = self.info_model.pack_exec_info('Auto')
        self.exec_program_queue(exec_info = exec_info)
    
    def auto_select_clicked(self):
        dialog = WaitingSetterDialog(self,
                                    self.gen_object,
                                    PROCESS_LIST)
        # Connect the signal from the dialog to a slot in the main window
        # dialog.user_added.connect(self.add_to_combobox)
        dialog.exec_()  # Use exec_() for modal dialog
        for [process_key, state] in dialog.checkbox_state_list:
            tab = self.tabWidget_process.findChild(ProcessTab, process_key)
            if tab is None:
                continue
 
            for index in range(tab.listWidget.count()):
                item = tab.listWidget.item(index)
                frame = tab.listWidget.itemWidget(item)
                if state == True:
                    frame.label.set_idle_state('Wait')
                else:
                    frame.label.set_result_state()
    def _pause(self): 
        # self.showMinimized()
        # self.gen_object.COM('get_user_name')
        self.gen_object.PAUSE('Pause')  
        if not self.check_pipe():
            self.close()
        # self.showNormal()
    def program_info_clicked(self):

        # self.get_cur_frame()
        tab = self.tabWidget_process.currentWidget() 
        process_key  = str(tab.objectName())
        index = 0 #real index, to avoid empty listItem 
        item = tab.listWidget.currentItem()
        frame = tab.listWidget.itemWidget(item)
        if not frame:
            return 
        frame.show_readme()


    def mousePressEvent(self,event):
        # pos = event.pos()
        # widget = QtGui.QApplication.instance().widgetAt(pos)
        # if widget:
        #     self.textBrowser_tmp_log.append('touch {0}'.format(str(widget.objectName())))
        # else:
        #     self.textBrowser_tmp_log.append('not touch')
        tab  = self.tabWidget_process.currentWidget()
        # process_key  = str(tab.objectName())
        tab.listWidget.clearSelection()  
        self.LogBox.set_info() 

    '''=================='''
    '''   Util Methods   '''
    '''=================='''
        

    def update_label(self,count):
        # def update_ui():
        # cpu_load = self.get_cpu_usage()
        # total_memory, available_memory, used_memory = self.get_memory_usage()
        # self.label_cpu_memory.setText("CPU : {0} %  Memory : {1} %".format(cpu_load, total_memory))
        self.label_cpu_memory.setText('')

        QtCore.QCoreApplication.processEvents() # update in run time
        # QtCore.QMetaObject.invokeMethod(self, update_ui)

    def get_cpu_usage(self):
        load_avg = os.getloadavg()
        return load_avg

    # Memory usage
    def get_memory_usage(self):
        with open('/proc/meminfo') as f:
            lines = f.readlines()
        total_memory = int(lines[0].split()[1])
        available_memory = int(lines[2].split()[1])
        used_memory = total_memory - available_memory
        return total_memory, available_memory, used_memory


    
    def on_program_list_clear_selection(self):
        self.LogBox.clear()

    def handle_tab_changed(self, new_index): 
        if new_index != -1:
            tab = self.tabWidget_process.widget(new_index)
            if isinstance(tab, QtGui.QWidget):
                # Perform actions for unselecting the previous tab's widget
                # tab.listWidget.clearSelection()
                pass



    def set_TR_ver(self, TR_ver):

        if self.TR_ver == TR_ver:
            return
        self.TR_ver = TR_ver
        self.info_model.TR_ver = TR_ver
        self.DB = self.info_model.get_DB()
        SIGNAL_MANAGER.TR_ver_changed.emit(self.TR_ver)
    def set_privilage(self, privilage):
        if self.privilage == privilage:
            return
        self.privilage = privilage
        self.info_model.privilage = privilage
        self.DB = self.info_model.get_DB()
        print(self.TR_ver, self.privilage, self.DB)
        SIGNAL_MANAGER.privilage_changed.emit(self.privilage)
  
    def on_TR_ver_changed(self):
        try:
            self.updateUi_display()
        except Exception as e:
            err_msg = traceback.format_exc()
            self.LogBox.append(err_msg)
    def on_privilage_changed(self):
        try:
            self.updateUi_display()
        except Exception as e:
            err_msg = traceback.format_exc()
            self.LogBox.append(err_msg)
    def on_program_selected(self, program_key, ver_folder):
        # self.frame_program_configs.reset_frame(program_key, ver_folder)
        self.LogBox.append('on_program_selected')
        pass
             
    def clear_selection(self):
        tab  = self.tabWidget_process.widget(0)
        # process_key  = str(tab.objectName())
        tab.listWidget.clearSelection() 

    def get_program_queue(self):
        #loop all process tab and program on listwidget
        program_wait_queue = [] #put frame object 
        for i in range(self.tabWidget_process.count()):
            tab  = self.tabWidget_process.widget(i)    
            for index in range(tab.listWidget.count()):
                item = tab.listWidget.item(index)
                frame = tab.listWidget.itemWidget(item)
                # if not frame.label.is_result and frame.label.idle_state == 'Wait':
                # self.gen_object.PAUSE(frame.label.idle_state)
                # self.gen_object.PAUSE(frame.program_name)
                if frame.label.idle_state == 'Wait':
                    program_wait_queue.append(frame) 
        return program_wait_queue
    def exec_program_queue(self, exec_info, program_wait_queue = None):

        ''' ================== set_program_queue ==================== '''
        if program_wait_queue is None:
            program_wait_queue = self.get_program_queue()
        
        ''' ===================== run program ===================== '''
        #pack exec_dict : some base infomation for log.
        # exec_info = self.info_model.pack_exec_info(exec_mode)
        state_code = '200'
        tot = float(len(program_wait_queue))
        exec_num = 0
        # clear msg box
        tab  = self.tabWidget_process.currentWidget()
        tab.listWidget.clearSelection()   
 
        # self.progressBar.setValue(exec_num)
        QtCore.QCoreApplication.processEvents()  # Allow GUI updates 
        for frame in program_wait_queue:   
            exec_info["LOG_PATH"] = os.path.join(self.root_path, frame.main_folder_path, 'Tmp')  
            exec_info["PROGRAM"] = frame.program_name
            file_path = frame.get_exec_file_path()
            # folder_path = os.path.dirname(file_path)
            exec_info["PROGRAM_VER"] = frame.current_ver
            
            if state_code[0] != '5' or exec_info["EXEC_MODE"] == 'Test': #not 5xx  
                state_code = frame.run(exec_info) 
                # msg = '[Info] : Program {0} Finish \n'.format(state_code)
                # self.LogBox.append(msg)
            else:
                frame.label.set_result_state('Fail')
            exec_num += 1


            self.progressBar.setValue(int((exec_num/tot)*100))
            QtCore.QCoreApplication.processEvents() # update in run time
        # if exec_info['EXEC_MODE'] == 'Auto' and state_code == '200': 
        
        if float(state_code) < 400:
            pass
            # self.gen_object.PAUSE('Finish') 
            # self.gen_object.COM('get_user_name')
        else:
            self.gen_object.PAUSE('Error Please Check') 
        if not self.check_pipe():
            self.close()
    def check_pipe(self):
        try: #check is pipe connect
            self.gen_object.COM('get_user_name')
            return True 
        except Exception as e:
            err_msg = traceback.format_exc()
            print(err_msg) 
            self.LogBox.append(err_msg)
            return False
    def delete_program(self):
        tab  = self.tabWidget_process.currentWidget()
        row = tab.listWidget.currentRow()
        tab.listWidget.takeItem(row)
    def open_process_tab(self,
                        process_key):
        for i in range(self.tabWidget_process.count()):
            cur_tab = self.tabWidget_process.widget(i)    
            if process_key == str(cur_tab.objectName()):
                
                self.tabWidget_process.setCurrentIndex(i)

    def connect_program(self):
        '''
        Connect and create a button
        folder_path = os.path.join(os.getcwd(), 'TESTFILES','PassProg')
        
        '''
        #get current process sheet
        if self.privilage == 'User':
            return 
        if self.TR_ver != 'Test':
            return 
        
        folder_path = str(QFileDialog.getExistingDirectory())
        if not folder_path:
            return 
        
        try:
            program_config = self.program_config

            program_key = get_program_key(folder_path)
            # is_program_frame_exist = check_is_program_frame_exist(program_key, program_config)
            
      
        
            process_key = get_process_by_config(program_key, program_config)
            if process_key == '':
                process_key = str(self.tabWidget_process.currentWidget().objectName())

            main_folder_path = create_standard_folder(process_key, program_key )
            folder_ver_name = get_folder_ver_name(self.root_path, main_folder_path, program_key )

            self.open_process_tab(process_key)

            #show note info
            program_name = get_program_name(program_key, program_config) 

           
            #move old folder to new Main folder
            copy_to_test_folder(folder_path, self.root_path, main_folder_path, folder_ver_name)





            cur_tab = self.tabWidget_process.currentWidget()
            program_frame = get_program_frame(cur_tab, program_key)
           

            if program_frame is None: 
                #create frame
                program_frame = ProgramFrame(SIGNAL_MANAGER,
                                    button_name = program_key ,
                                    main_folder_path = main_folder_path,
                                    program_name = program_key,
                                    process_tab = cur_tab,
                                    parent_program= '',
                                    parent = self 
                                    )
                #add item
                item  = QtGui.QListWidgetItem(cur_tab.listWidget)
                item.setSizeHint(program_frame.sizeHint())                
                cur_tab.listWidget.addItem(item)
                #set frame
                order = cur_tab.listWidget.count() - 1 
                cur_item = cur_tab.listWidget.item(order)            
                cur_tab.listWidget.setItemWidget(cur_item, program_frame)       
                # frame.refresh_combobox()   
                program_frame.comboBox.setCurrentIndex(0) 
            else:
                program_frame.auto_update_flag = False
                program_frame.refresh_combobox()
                program_frame.comboBox.setCurrentIndex(0)
                program_frame.auto_update_flag = True
            msg = '請選擇 "{0}" 的新版本'.format(program_name)# + program_name + u'的新版本'
            self.LogBox.append(msg)

        except Exception as e:
            err_msg = traceback.format_exc()
            print(err_msg)
            self.LogBox.append(err_msg)

    def copy_sub_program(self,
                        src_program_frame, 
                        dest_process_key,
                        TR_ver):
        '''
        root_path = os.getcwd()
        src_program_key = 'OutputAOI'
        src_process_key =  'Tools'
        dest_process_key = 'Test'
        sub_program_key = 'OutputAOI_1'
        TR_ver = 'Test'
        sub_folder = 'SubFolder'
        src_copying_folder_path = os.path.join(root_path, src_process_key,
                                 'Main_' + src_program_key, TR_ver,
                                 src_program_key + '-240829-1-1233', sub_folder)
        dest_folder_path = os.path.join(dest_process_key, 'Main_' + sub_program_key)
        '''
        is_success = False
        #get current process sheet
        if self.privilage == 'User':
            return is_success
        
        try:
            program_config = self.program_config
            src_copying_folder_path = src_program_frame.get_sub_src_copying_folder_path()
            if not os.path.isdir(src_copying_folder_path):
                self.LogBox.append('找不到 SubFolder 資料夾')
                return is_success
            suffix = get_sub_folder_suffix(program_config, src_program_frame.program_name)
            sub_program_key = src_program_frame.program_name + '_' + suffix

            dest_folder_path = create_standard_folder(dest_process_key, sub_program_key, 'Sub_' )
            # folder_ver_name = get_folder_ver_name(self.root_path, dest_folder_path, sub_program_key )

            self.open_process_tab(dest_process_key)


            copy_to_sub_folder(src_copying_folder_path,
                                root_path = self.root_path,
                                dest_folder_path = dest_folder_path,
                                sub_program_key = sub_program_key,
                                TR_ver = TR_ver,
                                LogBox = self.LogBox)

            cur_tab = self.tabWidget_process.currentWidget()
            # program_frame = get_program_frame(cur_tab, program_key)
           
            program_frame = None
            if program_frame is None: 
                #create frame 
                button_text = src_program_frame.pushButton.text()
                program_frame = ProgramFrame(SIGNAL_MANAGER,
                                    button_name = button_text,
                                    main_folder_path = dest_folder_path,
                                    program_name = sub_program_key,
                                    process_tab = cur_tab,
                                    parent_program= src_program_frame.program_name,
                                    parent = self 
                                    )
                #add item
                item  = QtGui.QListWidgetItem(cur_tab.listWidget)
                item.setSizeHint(program_frame.sizeHint())                
                cur_tab.listWidget.addItem(item)
                #set frame
                order = cur_tab.listWidget.count() - 1 
                cur_item = cur_tab.listWidget.item(order)            
                cur_tab.listWidget.setItemWidget(cur_item, program_frame)       
                # frame.refresh_combobox()  
                # program_frame.comboBox.setCurrentIndex(0)
            else:
                pass
                # program_frame.refresh_combobox()
                # program_frame.comboBox.setCurrentIndex(0)

            # self.LogBox.append(u'請選擇"' + QString(program_name) + u'"的新版本' )
            is_success = True
            self.save_program_config()
            return is_success
        except Exception as e:
            err_msg = traceback.format_exc()
            print(err_msg)
            self.LogBox.append(err_msg)

    def update_sub_program(self,
                        src_program_frame, 
                        ):

        is_success = False
        #get current process sheet
        if self.privilage == 'User':
            return is_success
        
        try:
            program_config = self.program_config
            src_copying_folder_path = src_program_frame.get_sub_src_copying_folder_path()
            if not os.path.isdir(src_copying_folder_path):
                self.LogBox.append('找不到 SubFolder 資料夾')
                return is_success


            # sub_program_key_list = ['Pass_1', 'Pass_2', 'Pass_3']
            sub_program_key_list = get_sub_program_key_list(program_config,
                                                            src_program_frame.program_name )
            for sub_program_key in sub_program_key_list:
                if sub_program_key not in program_config.keys():
                    continue
                sub_program_info = program_config[sub_program_key]
                dest_folder_path = sub_program_info['main_folder_path']
                sub_process = sub_program_info['process']
            

                copy_to_sub_folder(src_copying_folder_path,
                                    root_path = self.root_path,
                                    dest_folder_path = dest_folder_path,
                                    sub_program_key = sub_program_key,
                                    TR_ver = self.TR_ver,
                                    LogBox = self.LogBox)

                msg = "{0} 更新完成 ver : {1}".format(sub_program_key, src_program_frame.current_ver)
                self.LogBox.sys_append( msg )
            is_success = True
            return is_success
        except Exception as e:
            err_msg = traceback.format_exc()
            print(err_msg)
            self.LogBox.append(err_msg)            
    def is_config_change(self, new, old):
        return False
    def save_program_config(self):
        try:
            if self.privilage == 'User':
                return 
            new_config = self.etl_ui_config()
            self.program_config = new_config
            backup_config(new_config)
            with open("program_config.json", "w") as file:
                json.dump(new_config, file, indent=4)
                
            with open("tmp_config.json", "w") as file:
                json.dump(self.param_config, file, indent=4)
        except Exception as e:
            err_msg = traceback.format_exc()
            print(err_msg)
            self.LogBox.append(err_msg) 
            msg = "Save Config error"
            self.LogBox.sys_append(msg) 
    def etl_ui_config(self):
        new_config = {}

        for i in range(self.tabWidget_process.count()):
#            process_text = str(self.tabWidget_process.tabText(i))
            tab  = self.tabWidget_process.widget(i)
            process_key  = str(tab.objectName())
            index = 0 #real index, to avoid empty listItem
            for list_idx in range(tab.listWidget.count()):
                try:
                    item = tab.listWidget.item(list_idx)
                    frame = tab.listWidget.itemWidget(item)
                    if not frame:
                        continue
                    program_key = str(frame.objectName())
                    button_text = str(frame.pushButton.text().toUtf8())
#                    str(frame.pushButton.text()).encode('utf-8',errors='ignore')
                    program_config = copy.deepcopy(SystemConfig.ProgramConfig)
                    program_config['button_name'] = button_text
                    program_config['main_folder_path'] = frame.main_folder_path
                    program_config['process'] = process_key
                    program_config['order']   = index
                    program_config['parent_program'] = frame.parent_program #default ''
                    program_config['TR_ver_folder'] = frame.TR_ver_folder
                    program_ver = str(frame.current_ver)
                    if frame.comboBox is None:
                        program_ver = ''
                    program_config['TR_ver_folder'][self.TR_ver] = program_ver
                    frame.TR_ver_folder = program_config['TR_ver_folder']
                    
                    new_config[program_key] =  program_config
                    index += 1 
                    # new_config[program_key] = {'button_name': button_text,
                    #                            'main_folder_path': frame.main_folder_path,
                    #                            'process': process_key,
                    #                            'order'  : index
                    #                             }
                except Exception as e:
                    err_msg = traceback.format_exc()
                    print(err_msg)
                    msg = "Program {0} etl error".format(program_key)
                    self.LogBox.sys_append(msg)
                    self.record.info(err_msg)
        return new_config                                        

def backup_config(config):
    '''
    tmp = {
        'a' : 'hi',
        'b' : 'b',
    }
    config = {
        'file_name' : 'hi',
        'data' : tmp,
        'folder': 'AutoCAMUiConfig'
    }
    
    '''
    try:
        # SERVICE_ROOT = 'http://ws125:3114/dev/' #old
        # SERVICE_ROOT = 'http://ws125:3124/cam/info_converter/test/'
        if 'GEOM_SERVICE' in os.environ.keys():
            SERVICE_ROOT = os.environ['GEOM_SERVICE'] + 'cam/info_converter/'
        else:
            SERVICE_ROOT = 'http://ws125:3125/cam/info_converter/' #main
        # SERVICE_ROOT = 'http://ws125:3114/cam/info_converter/dev/'
        
        _id = random.randint(100000,999999)
 
        data_dict =  {'data_dict' : str({
                'file_name' : 'UiConfig_{0}'.format(str(_id)),
                'folder' : 'AutoCAMUiConfig_{0}'.format(os.environ['DATABASE']),
                'data' : config,
            })
        }
    
        service_function_name = 'json_backup_service'
        url = SERVICE_ROOT + service_function_name

        r = requests.post(url, data = data_dict)


    except Exception as err_msg:
        err_msg = traceback.format_exc()
        print(err_msg)

'''  


class ob:
    def __init__(self):
        pass
    
self  = ob()



mode = 'Test'
config = load_config()

for prog_key, prog_dict in config.items():
    main_folder_path = prog_dict['main_folder_path']


for program_key, program_dict in config.items():
    process = program_dict['process']    
    create_standard_folder(process, program_key)
        


'''
      
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    window = MainUi('Test')
    window.show()
    sys.exit(app.exec_())
# %%
{'bottomlayer': [['coupon', ['l46-enig'], [''], ''],
 ['coupon-10', ['l46-enig'], '']],
'nonvop': [['panel', ['l1-enig', 'l46-enig'], 'donut_r154.11x124.11']],
'pofile': [['panel', [], '']],
'toplayer': [['coupon', ['l1-enig'], ''], ['coupon-10', ['l1-enig'], '']],
'vop': [['panel', ['l1-enig', 'l46-enig'], 'r78.74']]}


{'key_name': {'Step':'coupon',
              'Layer':['l1','l2','l3'],
              'is_ReturnAllLayer':True, #To decide get all layer info , or loop until find valid layer.
              'Feature':[''] ,      # empty default all feature. Optional : #P, #L, #A, #S
              'Symbol':['']  ,      # empty default all. Optional pad name or r* , s*
              'Attr':['']    ,      # empty default all. Optional string attr* , ex: cu-*
              }

}