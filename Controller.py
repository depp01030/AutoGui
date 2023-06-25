# -*- coding: utf-8 -*-


#%%

import os 
import sys
import json
import traceback
import shutil
import subprocess
import datetime 
from PyQt4 import QtGui, QtCore

#try:
#    _fromUtf8 = QtCore.QString.fromUtf8
#except AttributeError:
#    def _fromUtf8(s):
#        return s

from MainWindow.view import Ui_MainWindow
os.chdir('D:\AutoCam')
import random


#%%
#class DraggableFrame(QtGui.QFrame):
#    def __init__(self, title):
#        super(DraggableFrame, self).__init__()
#        self.text = title
#        # Set the frame style
#        self.setFrameStyle(QtGui.QFrame.Box)
#        
#        
#        horizontalLayout = QtGui.QHBoxLayout(self) 
#        label = QtGui.QLabel(self) 
#        label.setText(title)
#        horizontalLayout.addWidget(label)
#        pushButton = QtGui.QPushButton(self) 
#        pushButton.setText(title)
#        horizontalLayout.addWidget(pushButton)
#        comboBox = QtGui.QComboBox(self) 
#        horizontalLayout.addWidget(comboBox)
#        horizontalLayout.addStretch()

PROCESS_LIST = [['Preprocess', 'Preprocess'], ['Drill','Drill'],
                ['Inner','Inner'], ['Shipping', 'Shipping'], ['Panel','Panel']]

class ProcessTab(QtGui.QWidget):    
    def __init__(self):
        super(ProcessTab, self).__init__()
#        self.tab_tmp = QtGui.QWidget()
        self.verticalLayout_5 = QtGui.QVBoxLayout(self) 
        self.listWidget = QtGui.QListWidget(self)
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection) 
        self.listWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        
        self.verticalLayout_5.addWidget(self.listWidget)
class ProgramStateLabel(QtGui.QLabel):
    def __init__(self, state):
        super(ProgramStateLabel, self).__init__()
        self.exec_state = state
        self.state = state
        self.setText(state) 
#        self.mousePressEvent = self.mousePressEvent
        
    def mousePressEvent(self,event):
        self.switch_state()
    def switch_state(self):        
        if self.state != 'Wait':
            self.set_state('Wait')
        else:
            self.set_state(self.exec_state)
            
    def set_state(self, state):
        state_style_dict = {}
        state_style_dict['Wait'] = "QLabel { \
                                border : 1px solid #298DFF;\
                                border-radius : 3px;\
                                background-color : rgb(105, 235, 157);\
                                color : rgb(54, 54, 54);\
                                font-size : 12pt;\
                                }"
                                
                                
        self.state = state
        self.setText(state) 
        if state in state_style_dict.keys():
            self.setStyleSheet(state_style_dict[state])
class ProgramButton(QtGui.QPushButton):
    def __init__(self, text):
        super(ProgramButton, self).__init__()        
        self.setText(text)

class ProgramVerComboBox(QtGui.QComboBox):
    def __init__(self):
        super(ProgramVerComboBox, self).__init__()        
        self.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
                
        
class ProgramFrame(QtGui.QFrame):
    def __init__(self,
                 mode,              
                 button_name,
                 main_folder_path,
                 program_name,
                 state = 'None'):
        super(ProgramFrame, self).__init__()
        self.mode = mode          
        self.main_folder_path = main_folder_path
        self.program_name = program_name
        self.setObjectName(program_name)
        self.root_path = os.path.dirname( os.path.dirname(main_folder_path) )
        self.label = ProgramStateLabel(state)   
        self.pushButton = ProgramButton(button_name)  
        self.comboBox = ProgramVerComboBox()
        # Set the frame style
        self.setFrameStyle(QtGui.QFrame.Box)
        
        
        self._setupUi()
        self.set_mode(self.mode)
        self.setup_click_event()
    def _setupUi(self):        
        horizontalLayout = QtGui.QHBoxLayout(self) 
        horizontalLayout.addWidget(self.label)
        horizontalLayout.addWidget(self.pushButton)
        horizontalLayout.addWidget(self.comboBox)
        horizontalLayout.addStretch()
        
    def setup_click_event(self):                
        self.pushButton.clicked.connect(self.run)
        
    def run(self, exec_info):
        '''
        Run program
        Parse tmp Log
        Update permanent program log
        Update tmp job log
        Set label state
        return : True, False -> Whether run next program.
        '''
        ''' ======================= get file_path ======================= '''
        ver_path = os.path.join(self.main_folder_path, self.mode)  
#        ver_path = 'D:\AutoCam\Preprocess\Main_tmp_3339\Test'
        ver_folder = str(self.comboBox.currentText())
        ver_folder_path = os.path.join(ver_path, self.program_name + '-' + ver_folder) 
#        #open text/ release folder
#        if os.path.isdir(ver_path): 
#            os.startfile(ver_path) 
#        ver_folder_path = 'D:\AutoCam\Preprocess\Main_tmp_890\Test\tmp_890-20513'
        file_path = os.path.join(ver_folder_path, 'main.py')
    
        ''' ======================== run program ======================== '''
        exec_id = exec_info['exec_id']
        args = 'arg'
        if os.path.isfile(file_path): 
            cmd = 'python {0} {1} {2}'.format(file_path, exec_id, args)
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
    
            # Print the output and error messages
            print("Output:")
            print(output.decode())
            
            print("Error:")
            print(error.decode())
        else:
            print('File {0} not found'.format(file_path))
        ''' ======================= call log_parser ====================== '''        
        tmp_log_folder = os.path.join(self.main_folder_path, 'Tmp')  
        file_name = '{0}_{1}.txt'.format(self.mode, exec_id)    
        file_path = os.path.join(tmp_log_folder,file_name) 
        program_state, perm_prog_log, tmp_job_log = self.program_log_parser(exec_info,
                                                                            file_path)   
        # Update permanent program log
        perm_prog_log_name = self.mode + '_' + self.program_name
        perm_prog_log_file_path = os.path.join(self.main_folder_path, 'Log', perm_prog_log_name)
        with open(perm_prog_log_file_path, "a") as f:
            f.write(perm_prog_log)
            
        # Update tmp job log 
        tmp_job_log_folder = os.path.join(self.root_path, 'Tmp')
        if not os.path.isdir(tmp_job_log_folder) :
            os.mkdir(tmp_job_log_folder)
        tmp_job_log_name = self.mode + '_' + exec_info['job_id'] + '_' + exec_info['job_name']
        tmp_job_log_file_path = os.path.join(tmp_job_log_folder, tmp_job_log_name)
        with open(tmp_job_log_file_path, "a") as f:
            f.write(tmp_job_log)
            
        ''' ======================= Set Label State ======================= '''
        self.label.exec_state = program_state        
        self.label.switch_state()
    def program_log_parser(self,
                           exec_info,
                           file_path):
                               
        with open(file_path, "r") as f:
            prog_log = f.readlines()
            
        state_dict = { 1 : 'Info',
                       2 : 'Warning',
                       3 : 'Error'}        
        
        msg_dict = {'Info'    : [],
                    'Warning' : [],
                    'Error'   : []}
             
        state_level = 1
        for log in prog_log:
            if 'Info' in log:
                state_level = max(state_level, 1)
                msg_dict['Info'].append(log.strip())
         
            elif 'Warning' in log:
                state_level = max(state_level, 2)
                msg_dict['Warning'].append(log.strip())
         
            elif 'Error' in log:
                state_level = max(state_level, 3)
                msg_dict['Error'].append(log.strip())
        if 'EndFile' not in prog_log[-1]:
            state_level = 3
        ''' =================== Construct Log Format ==================== '''       
        # common info        
        exec_id  = exec_info['exec_id']
        program_state = state_dict[state_level] 
        time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        job_id   = exec_info['job_id']
        job_name = exec_info['job_name']
        # permanent program log
        user_name= exec_info['user_name']
        log_msgs = str(msg_dict)
        perm_prog_log = '{0};{1};{2};{3};{4};{5};{6} \n'.\
                        format(exec_id,
                               job_id,
                               job_name,
                               program_state,
                               user_name,
                               log_msgs,
                               time_stamp)
                
        # job log  
        log_id = random.randint(100000000,999999999)
        program_name = self.program_name
        tmp_job_log = '{0};{1};{2};{3};{4};{5};{6} \n'.\
                        format(log_id,
                               exec_id,
                               program_name,
                               job_id,
                               job_name,
                               program_state,
                               user_name, 
                               time_stamp)
        
        return program_state, perm_prog_log, tmp_job_log

    def set_mode(self, mode):
        if mode == 'Test':
            self.mode = 'Test'
            self.comboBox.setVisible(False)
        else:
            self.mode = 'Release'
            self.comboBox.setVisible(True)
        self.comboBox.clear()
        
        #get version folder list
        ver_path = os.path.join(self.main_folder_path, self.mode)
        if os.path.isdir(ver_path):
            ver_list = os.listdir(ver_path)
            
            #add all version folder to combobox
            for ver_folder in ver_list:
                self.comboBox.addItem(ver_folder.split('-')[1])
        else:
            print('Path {0} is not exist'.format(ver_path))
 
''' ******************************* main ui ******************************* '''
class MainUi(Ui_MainWindow, QtGui.QMainWindow):
    def __init__(self, mode = 'Test'):
        super(MainUi, self).__init__()
        #get basic info
        self.setup_attr(mode)
        #load_config
        
        self._setupUi()
        self.setup_ui_state()
        self.setup_click_event()
    def setup_attr(self, mode):
        self.mode = mode        
        
        self.root_path = 'D:\AutoCam'
        self.user_name = 'user' #210605-CAM_SUER  
        self.priority_level = ''
        
        self.job_id    = 'job_id'
        self.job_name  = os.environ['JOB'] if 'JOB' in os.environ.keys() else 'None'
        
#        self.job_object = 
        self.config = load_config()
    def setup_click_event(self):
        #push button
        self.pushButton_test.clicked.connect(self.test_clicked)
        self.pushButton_test2.clicked.connect(self.test_clicked2)
        
        #menu bar
        self.actionCreateProgram.triggered.connect(self.create_program)
        self.actionSaveConfig.triggered.connect(self.save_config)
        
        #short cut
        self.actionCreateProgram.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_N))
        self.actionSaveConfig.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S))
    
    def _setupUi(self):
        self.setupUi(self)
        self.setup_tabWidget_process()
#        self.frame_optional.hide()
    def setup_tabWidget_process(self):
        self.tabWidget_process.clear()
        #setup Process sheet
        for process_key, tab_name in PROCESS_LIST:
            tab = ProcessTab()
            tab.setObjectName(process_key)
            self.tabWidget_process.addTab(tab, tab_name)
        #setup program_frame of each Process
        for program_key, program_dict in self.config.items():
            process_key = program_dict['process']
            tab = self.tabWidget_process.findChild(QtGui.QWidget, process_key)
            # loading check
            if not tab:
                print ('[Warning] : No process_key : {0}, Failed to load Program {1}'.format(process_key, program_key))
                continue
            is_main_folder_valid = check_main_folder_valid(program_dict['main_folder_path'])
            if not is_main_folder_valid:
                print('[Warning] : Failed to load Program {0}'.format(program_key))
                
            #create frame
            frame = ProgramFrame(mode = self.mode,
                                 button_name = program_dict['button_name'],
                                 main_folder_path = program_dict['main_folder_path'],
                                 program_name = program_key
                                 )
                                 
            order = int(program_dict['order'])
            
            while order >= tab.listWidget.count():
                item  = QtGui.QListWidgetItem(tab.listWidget)
                item.setSizeHint(frame.sizeHint())
                
                tab.listWidget.addItem(item)
#            tab.listWidget.insertItem(program_dict['order'], item)
            cur_item = tab.listWidget.item(order)            
            tab.listWidget.setItemWidget(cur_item, frame)            
        
        self.tabWidget_process.setCurrentIndex(0)
    def setup_ui_state(self):
        state_config = {}
        tmp_job_log = []
        # load db
        pass
        # load tmp_job_log
        tmp_job_log_folder = os.path.join(self.root_path, 'Tmp')
        if not os.path.isdir(tmp_job_log_folder) :
            os.mkdir(tmp_job_log_folder)
            
        tmp_job_log_name = self.mode + '_' + self.job_id + '_' + self.job_name 
        tmp_job_log_file_path = os.path.join(tmp_job_log_folder, tmp_job_log_name)
        if os.path.isfile(tmp_job_log_file_path ):
            with open(tmp_job_log_file_path, "r") as f:
                tmp_job_log = f.readlines()

        for log in tmp_job_log:
            program_name  = log.split(';')[2]
            program_state = log.split(';')[5]
            state_config[program_name] = program_state
        # update state
        for program_key, program_state in state_config.items():
            if program_key not in self.config.keys():
                print(' {0} not in config '.format(program_key ))
            process_key = self.config[program_key]['process']
            
            print(process_key)
            tab = self.tabWidget_process.findChild(QtGui.QWidget, process_key)
            frame = tab.listWidget.findChild(QtGui.QWidget, program_key)
            frame.label.exec_state = program_state           
            frame.label.set_state(program_state)
       
#            order = int(program_dict['order'])
#            
#            while order >= tab.listWidget.count():
#                item  = QtGui.QListWidgetItem(tab.listWidget)
#                item.setSizeHint(frame.sizeHint())
#                
#                tab.listWidget.addItem(item)
##            tab.listWidget.insertItem(program_dict['order'], item)
#            cur_item = tab.listWidget.item(order)            
#            tab.listWidget.setItemWidget(cur_item, frame)    
        
        
    def test_clicked(self):
        self.exec_program_queue()
    def test_clicked2(self):
        self.set_mode()
    def exec_program_queue(self):
        ''' ================== set_program_queue ==================== '''
        #loop all process tab and program on listwidget
        program_wait_queue = [] #put frame object 
        for i in range(self.tabWidget_process.count()):
            tab  = self.tabWidget_process.widget(i)    
            for index in range(tab.listWidget.count()):
                item = tab.listWidget.item(index)
                frame = tab.listWidget.itemWidget(item)
                if frame.label.state == 'Wait':
                    program_wait_queue.append(frame)
        ''' ===================== run program ===================== '''
        #pack exec_dict : some base infomation for log.
        exec_info = {}
        exec_info['exec_id'] = random.randint(100000,999999)
        exec_info['job_id']  = self.job_id
        exec_info['job_name']= self.job_name
        exec_info['user_name'] = self.user_name
        for frame in program_wait_queue:
            frame.run(exec_info)
        
    def set_mode(self):
        if self.mode == 'Test':
            self.mode = 'Release'
            
#            self.frame_optional.show()
        else:
            self.mode = 'Test'
#        
#            self.frame_optional.hide()
        for i in range(self.tabWidget_process.count()): 
            tab  = self.tabWidget_process.widget(i) 
    
            for index in range(tab.listWidget.count()):
                item = tab.listWidget.item(index)
                frame = tab.listWidget.itemWidget(item)
                frame.set_mode(self.mode)
    def delete_program(self):
        tab  = self.tabWidget_process.currentWidget()
        row = tab.listWidget.currentRow()
 
        tab.listWidget.takeItem(row)
 
            
    def create_program(self):
        #get current process sheet
        tab = self.tabWidget_process.currentWidget()
        rint = random.randint(0,10000)
        program = 'tmp_' + str(rint)
        
        create_standard_folder(str(tab.objectName()), program )
        
        
        main_folder_path = os.path.join(self.root_path, str(tab.objectName()), 'Main_' + program)
        frame = ProgramFrame(mode = self.mode,
                             button_name = program ,
                             main_folder_path = main_folder_path,
                             program_name = program 
                             )
        #add item
        item  = QtGui.QListWidgetItem(tab.listWidget)
        item.setSizeHint(frame.sizeHint())                
        tab.listWidget.addItem(item)
        #set frame
        order = tab.listWidget.count() - 1 
        cur_item = tab.listWidget.item(order)            
        tab.listWidget.setItemWidget(cur_item, frame) 

        
    def save_config(self):
        new_config = self.etl_ui_config()
        with open("config.json", "w") as file:
            json.dump(new_config, file, indent=4)
            
    def etl_ui_config(self):
        new_config = {}
        try:
            for i in range(self.tabWidget_process.count()):
    #            process_text = str(self.tabWidget_process.tabText(i))
                tab  = self.tabWidget_process.widget(i)
                process_key  = str(tab.objectName())
        
                for index in range(tab.listWidget.count()):
                    item = tab.listWidget.item(index)
                    frame = tab.listWidget.itemWidget(item)
                    program_key = str(frame.objectName())
                    new_config[program_key] = {'button_name': str(frame.pushButton.text()),
                                               'main_folder_path': frame.main_folder_path,
                                               'process': process_key,
                                               'order'  : index
                                                }
        except Exception as e:
            err_msg = traceback.format_exc()
            print(err_msg)
        return new_config                                        
        
    def tmp(self): 
        pass
#        # Set the selection mode to SingleSelection for easier handling
#        self.listWidget_tmp.setSelectionMode(QtGui.QAbstractItemView.SingleSelection) 
#        self.listWidget_tmp.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
#        
# 
#        for program_key, prgram_dict in self.config.items():
#            
#            is_main_folder_valid = check_main_folder_valid(prgram_dict['main_folder'])
#            if not is_main_folder_valid:
#                print('[Warning] : Failed to load Program {0}'.format(program_key))
#            #create frame
#            frame = ProgramFrame(button_name = prgram_dict['button_name'],
#                                 main_folder = os.path.join(self.root_path, prgram_dict['main_folder']),
#                                 )
#            item  = QtGui.QListWidgetItem(self.listWidget_tmp)
#            item.setSizeHint(frame.sizeHint())
#            self.listWidget_tmp.setItemWidget(item, frame)
#            
#        for index in range(self.listWidget_tmp.count()):
#            item = self.listWidget_tmp.item(index)
#            frame = self.listWidget_tmp.itemWidget(item)
#            print("Item:", frame.button_name ,type(item))
##        
        
def check_main_folder_valid(main_folder_path):
#    print(main_folder)
    pass
    return True
def load_config():
    try:
        if os.path.isfile("config.json"):
            with open("config.json", "r") as file:
                config = json.load(file)
                
            return config    
        else:
            with open("config.json", "w") as file:
                json.dump({}, file, indent=4)
            print('no config.json')
            return {}
    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)
        print('Failed to load config' )
        return {}
        
        

def create_standard_folder(process, program):
    
    root_path = os.getcwd()
    process_path = os.path.join(root_path, process)
    main_program_folder = os.path.join(process, 'Main_' + program)
    sub_folder_list = ['Release', 'Test', 'Tmp', 'Log']    
    if not os.path.isdir(process_path ):
        os.mkdir(process_path)
    if not os.path.isdir(main_program_folder):
        os.mkdir(main_program_folder)
    for sub_folder in sub_folder_list:
        sub_folder_path = os.path.join(main_program_folder, sub_folder)
        if not os.path.isdir(sub_folder_path):
            os.mkdir(sub_folder_path)
    
    ## random create ver_folder
    for _ in range(4):
        ver_name = program + '-' + str(random.randint(10000,99999))
        ver_folder = os.path.join(main_program_folder,'Test',ver_name)
        os.mkdir(ver_folder)
        shutil.copy('main.py', ver_folder)
    
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
    import sys
    app = QtGui.QApplication(sys.argv)
    window = MainUi()
    window.show()
    sys.exit(app.exec_())