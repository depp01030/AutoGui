#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu May 25 09:23:14 2023

@author: incam
"""
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

import genClasses
from Record import Record

root_path = os.environ["ROOT_PATH"]
sys.path.append(os.path.join(root_path, "mainWindow/ui_utils"))

#%%
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QListWidget, QMessageBox
from dev_frame import Ui_Frame

# 0205 chen
import GetAffactLayerList
import GetAffectedInfo
import GetCheckListInfo
import GetSpeSymDict


SERVICE_ROOT = 'http://ws125:3114/cam/info_converter/dev/'
# SERVICE_ROOT = 'http://ws125:3114/cam/info_converter/test/'
# SERVICE_ROOT = os.environ['GEOM_SERVICE'] + 'cam/info_converter/'
#%%
class DevFrame(Ui_Frame, QtGui.QFrame):
    '''
    self.parent.LogBox :
        .append('xxx')
    '''
    def __init__(self, parent, frame_toput):
        
        super(DevFrame, self).__init__()   
        if 'JOB' in os.environ.keys():
            self.job_name = os.environ['JOB']
        else:
            self.job_name = 'no_job'
        self.parent = parent
        self.setupUi(frame_toput)      
        self.setup_click_event()   
        self.lineEdit_folder_name.setText(self.job_name)
        self.lineEdit_file_name.setText('output_info')
            
    def setup_click_event(self):
        self.pushButton_copy_dev_job_info.clicked.connect(self.set_dev_info_on_clipboard) 
        self.pushButton_post_affected_layer.clicked.connect(self.post_affected_layer) 

    def etl_from_ui(self):
        etl_dict = {}
        if self.checkBox_layers.isChecked():
            etl_dict.update({self.checkBox_layers.text(): True})
        else:
            etl_dict.update({self.checkBox_layers.text(): False})
            
        if self.checkBox_check_list.isChecked():
            etl_dict.update({self.checkBox_check_list.text(): True})
        else:
            etl_dict.update({self.checkBox_check_list.text(): False})
            
        if self.checkBox_spe_sym_dict.isChecked():
            etl_dict.update({self.checkBox_spe_sym_dict.text(): True})
        else:
            etl_dict.update({self.checkBox_spe_sym_dict.text(): False})
            
        if self.checkBox_matrix.isChecked():
            etl_dict.update({self.checkBox_matrix.text(): True})
        else:
            etl_dict.update({self.checkBox_matrix.text(): False})
        
        return etl_dict
        
    def post_affected_layer(self):
        etl_from_ui = self.etl_from_ui()
        suffix = ''
        output_folder_name = str(self.lineEdit_folder_name.text())
        file_name = str(self.lineEdit_file_name.text())
        
        json_file_name = '{0}_{1}.json'.format(file_name, suffix)
        
        print(json_file_name)
        job_name = self.job_name
        job_object = genClasses.Job(job_name)
        step_name = os.environ['STEP']
        step_object = job_object.steps[step_name]
        output_dict = {'layers': {},
                       'check_list': {},
                       'spe_sym_dict' :{},
                       'matrix': {}}
        # 0205 chen
        affect_layer_list = GetAffactLayerList.get_affact_layer_list(step_object)

        if etl_from_ui[self.checkBox_layers.text()]:
            output_dict['layers'] = GetAffectedInfo.get_FeatureInfo_AffectLayer(step_object, affect_layer_list, suffix)
        if etl_from_ui[self.checkBox_check_list.text()]:
            output_dict['check_list'] = GetCheckListInfo.get_all_checklist_info(step_object, check_list_name = 'Temporary')
        if etl_from_ui[self.checkBox_spe_sym_dict.text()]:
            output_dict['spe_sym_dict'] = GetSpeSymDict.get_spe_sym_dict(step_object, affect_layer_list)
        if etl_from_ui[self.checkBox_matrix.text()]:
            output_dict['matrix'] = step_object.job.matrix.getInfo()
        
        
        
        self.output_and_post_dict(step_object, suffix, output_dict, output_folder_name, json_file_name)

        self.parent.LogBox.append('File has been post.')
        
    def set_dev_info_on_clipboard(self):
        
        # self.LogBox.append('hi')
        try :
            text = '''
            os.environ['JOB'] = "{0}"
            job_name = "{0}"
            job_object = genClasses.Job(os.environ['JOB'])    
            step_object = genClasses.Step(job_object, 'pcb')  
            matrix_info = step_object.job.matrix.getInfo()'''.\
            format(os.environ['JOB'])
            clipboard = QtGui.QApplication.clipboard()
            clipboard.setText(text)
            self.parent.LogBox.append(text)
        except Exception as e:
            err_msg = traceback.format_exc()
            print(err_msg)
            self.parent.LogBox.append(err_msg)

    def output_and_post_dict(self, step_object, suffix, output_dict, output_folder_name, json_file_name):
        '''
        未來可以改：檔案名稱的後綴、資料夾名稱
        '''
        
        folder_name1 = step_object.job.name

        script_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(script_path)
        

        folder_path_affect_layer = os.path.join(current_directory, folder_name1)
        if not os.path.exists(folder_path_affect_layer):
            os.makedirs(folder_path_affect_layer)

        json_file_path = os.path.join(folder_path_affect_layer, json_file_name)
        output_dict['folder_name'] = output_folder_name
        output_dict['job_name'] = output_folder_name
        output_dict['file_name'] = json_file_name
        with open(json_file_path, 'w') as json_file:
            json.dump(output_dict, json_file, indent=4)
        
    
        data_dict = {'data_dict' : str(output_dict)}
        service_function_name = 'dump_data_service'
        url = SERVICE_ROOT + service_function_name
        r = requests.post(url, data = data_dict)
  
        return_dict = eval(r.text)
 

        if type(return_dict) == dict and  'Traceback' in return_dict.keys():
            self.parent.LogBox.append('Post got error')
        else: 
            self.parent.LogBox.append('File has been post.')