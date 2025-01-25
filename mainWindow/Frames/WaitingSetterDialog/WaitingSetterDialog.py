#!/usr/bin/python
# -*- coding: utf-8 -*-
#%%

import os 
import sys
import json
import traceback
import shutil
import subprocess
import datetime 
import time
import random 
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QTableWidgetItem

root_path = os.environ["ROOT_PATH"]
sys.path.append(os.path.join(root_path, "mainWindow/Frames"))

import genClasses 

from mainWindow.Frames.WaitingSetterDialog.view import Ui_Dialog
 
#%%
class WaitingSetterDialog(Ui_Dialog, QtGui.QDialog):
      
    def __init__(self, 
                parent = None,
                gen_object = None,
                process_config = None,
                ): 
        super(WaitingSetterDialog, self).__init__()
        self.gen_object = gen_object
        self.parent = parent
        self.checkbox_state_list = []
        self._setupUi(process_config)
        self.setup_click_event()
        
        
    def _setupUi(self,process_config):
        self.setupUi(self) 
        self.pushButton_check.setText(QtCore.QString(u'確認'))
        self.pushButton_close.setText(QtCore.QString(u'關閉'))
        self.set_checkboxes(process_config)
        self.adjustSize()
    
    def set_checkboxes(self, process_config):
        col_num = 4
        for i, process_info in enumerate(process_config):
            process_key, process_name = process_info
            checkBox = QtGui.QCheckBox()
            checkBox.setText(process_name)
            checkBox.setObjectName(process_key)
            self.gridLayout.addWidget(checkBox, i // col_num + 1, i% col_num, 1, 1)
    def setup_click_event(self): 

        self.pushButton_check.clicked.connect(self.onCheckClicked)
        self.pushButton_close.clicked.connect(self.close)

        checkboxes = self.findChildren(QtGui.QCheckBox)
        for checkbox in checkboxes: 
            checkbox.stateChanged.connect(lambda state, cb=checkbox: self.check_box_state_change(cb))

    def check_box_state_change(self, checkbox):
        # Append the text of the checkbox that changed state
        checkboxes = self.findChildren(QtGui.QCheckBox)
        if checkbox.objectName() == 'All':
            for ref_checkbox in checkboxes: 
                ref_checkbox.setChecked(checkbox.isChecked())
        #self.parent.LogBox.append(str(checkbox.text()))

    def onCheckClicked(self):
        #etl 
        checkboxes = self.findChildren(QtGui.QCheckBox)
        for checkbox in checkboxes: 
            self.checkbox_state_list.append([checkbox.objectName(),  checkbox.isChecked()])
        self.close()

# %%
