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

from mainWindow.Frames.Batch.BATCH_JOB_LIST import JOB_LIST
from mainWindow.Frames.Batch.BatchFrame_view import Ui_Frame
from mainWindow.Frames.Batch.batch_utils import (
    do_batch_tasks

)
#%%
class BatchFrame(Ui_Frame, QtGui.QFrame):
      
    def __init__(self, 
                gen_object = None,
                parent = None ): 
        super(BatchFrame, self).__init__()
        self.gen_object = gen_object
        self.parent = parent
        self._setupUi()
        self.setup_click_event()
    def _setupUi(self):
        self.setupUi(self)
        self.load_job_list()
        self.adjustSize()

        
    def setup_click_event(self):
        self.pushButton_batch_exec.clicked.connect(self.batch_exec_clicked)
    ''' ========================================================= '''
    # def XXX(self):
    #     a = ['advt-lb002b-x-outer-pad',
    #         'inde-af0002-v1d01-outer-pad',
    #         'nvid-dd001p-v1d01-outer-pad',
    #         'nvid-dd001q-v2d01-outer-pad',
    #         'nvid-dd001y-v2d01-outer-pad',
    #         'para-lb002x-x-outer-pad',
    #         'sxrt-dd0001-v1d01-outer-pad',
    #         'tsmc-dd029b-v1d01-outer-pad']

    #     a = ['alcp-lb001b-a1d01-outer',
    #         'amba-lb0023-a1d01-outer',
    #         'hslc-dd0052-v1d01-outer',
    #         'hslc-lb013e-a1d01-outer',
    #         'inde-af0002-v1d01-outer',
    #         'mpix-pc0084-x-outer',
    #         'mtkx-lb007f-a1d01-outer',
    #         'mtkx-lb0088-a1d03-outer',
    #         'mtkx-lb009n-a1d01-outer',
    #         'mttc-lb0013-a1d01-outer',
    #         'nvid-dd001q-v1d01-outer',
    #         'para-lb004r-x-outer',
    #         'ztem-lb0021-a1d01-outer']

    def load_job_list(self):
        
        for job_name in JOB_LIST:

            item  = QtGui.QListWidgetItem('{0}'.format(job_name))
            self.listWidget_batch_job_list.addItem(item)
    def etl_batch_job_list(self):
        waiting_job_queue = [] #put frame object  
        
        # for index in range(self.listWidget_batch_job_list.count()):
        #     item = self.listWidget_batch_job_list.item(index) 
        #     if item
        #     waiting_job_queue.append(str(item.text()))
        selected_items = self.listWidget_batch_job_list.selectedItems()
        for item in selected_items:
            waiting_job_queue.append(str(item.text()))
        return waiting_job_queue

    def batch_exec_clicked(self):  
        try:
            waiting_job_queue = self.etl_batch_job_list()
            non_exist_jobs = []
            # self.parent.job_id = job_id    
            top_object = genClasses.Top()
            job_db_list = top_object.listJobs()
            # job_db_list= self.gen_object.listJobs()

            program_wait_queue = self.parent.get_program_queue()
            for job_name in waiting_job_queue: 
                if job_name not in job_db_list:
                    non_exist_jobs.append(job_name)
                    print('[' , job_name, ' ] not in db')
                    continue
                    
                do_batch_tasks(job_name, self.parent, program_wait_queue)
            if len(non_exist_jobs) != 0:
                print(non_exist_jobs)
                self.gen_object.PAUSE('Not Exist Job nums : {0}'.format(len(non_exist_jobs)))
            else:    
                self.gen_object.PAUSE('Batch Finish')
        except Exception as e:
            err_msg = traceback.format_exc()
            print(err_msg)  




