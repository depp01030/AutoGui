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

''' ========================================================================== '''
'''                                ProgramFrame                                '''
''' ========================================================================== '''
class DevWidget(QtGui.QFrame):
    def __init__(self,   
                 parent=None,
                 ):
        super(DevWidget, self).__init__(parent) 
        self.parent = parent

        self.setup_attr()
        self.setupUi()
        self.setup_click_event()

    def setupUi(self):        
        self._setupUi()

        self.menu = ProgramFrameMenu(self)    
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        # self.comboBoxOnChange()



    def _setupUi(self):   

        self.set_TR_ver(self.parent.TR_ver)
        self.set_privilage(self.parent.privilage)
        # Set the frame style
        self.setFrameStyle(QtGui.QFrame.Box)
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


        self.setStyleSheet(qss)
        horizontalLayout = QtGui.QHBoxLayout(self) 
        horizontalLayout.addWidget(self.label)
        # horizontalLayout.addItem(QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum))
        horizontalLayout.addWidget(self.pushButton)
        
        horizontalLayout.addItem(QtGui.QSpacerItem(80, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        horizontalLayout.addWidget(self.comboBox)
        
