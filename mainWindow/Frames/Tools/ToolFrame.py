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

from ToolFrame_view import Ui_Frame
#%%
class ToolFrame(Ui_Frame, QtGui.QFrame):
      
    def __init__(self, 
                gen_object = None,
                parent = None ): 
        super(ToolFrame, self).__init__()
        self.gen_object = gen_object
        self.parent = parent
        self._setupUi()
        self.setup_click_event()
    def _setupUi(self):
        self.setupUi(self)
        self.adjustSize()

        
    def setup_click_event(self):
        self.pushButton_reset_job_id.clicked.connect(self.reset_job_id_clicked)
    ''' ========================================================= '''
    
    def reset_job_id_clicked(self): 
        job_id = str(random.randint(1000000, 9999999))
        comment_text = "job_id={0};".format(job_id)
        self.gen_object.COM("set_attribute, attribute=.comment, \
                        job={0},name1=,type=Job,value={1}".format(self.gen_object.name, comment_text))
        self.parent.job_id = job_id
        self.parent.setup_title()