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
import requests
import re
import copy
import datetime
import shlex
import math
import json
import traceback




# import Select_layer 
from PyQt4 import QtCore,QtGui

import genClasses
from Record import Record
import Model

from ui.view import Ui_Frame 
record = Record() 
#%%
class Controller(Ui_Frame, QtGui.QFrame):
    def __init__(self, CONFIG=None):
        super(Controller, self).__init__()
        self.CONFIG = CONFIG
        self.set_top_object()
        self._setupUi()
        self.setup_click_event()
        self.record =Record()
    
    def set_top_object(self):
        try:
            # os.environ['JOB'] = 'real-lb021j-juri-bd'
            if 'JOB' in os.environ.keys() and os.environ['JOB']:
                gen_object = genClasses.Job(os.environ['JOB'])   
            else:
                gen_object = genClasses.Top()
        except:
            gen_object = None
        self.gen_object = gen_object

    def _setupUi(self):
        self.setupUi(self) 
        
    ''' =================== click method =================== '''
    def setup_click_event(self):
        self.pushButton_execute.clicked.connect(self.execute_clicked)
        self.pushButton_Test.clicked.connect(self.close)


    def execute_clicked(self):
        Model.main(self.CONFIG) 
        self.record.show_report()
        self.close()


    ''' =================== drag event =================== '''
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.drag:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag = False
    ''' =================== functions =================== '''







    # sys.exit()
#%%
if __name__ == '__main__':
    CONFIG = {} 


# %%
