# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 13:09:33 2023

@author: User
"""
import os
import sys

import random

if __name__ == '__main__':
    PROGRAM_ID = ''
    work_layer_list = []
    if len(sys.argv) > 1:
        PROGRAM_ID = sys.argv[1]
    if len(sys.argv) > 2:
        work_layer_list = sys.argv[2]
     
    print('enter : {0}'.format(__file__)) 
    
    job_name = 'abcd-xxxxx-vadbc-juri'
    job_id   = '32113'
#    ver = os.path.basename(os.path.dirname(__file__))
    mode  = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
    tmp_folder = os.path.dirname(os.path.dirname(__file__)).replace(mode, 'Tmp')    
    file_name = '{0}_{1}.txt'.format(mode, PROGRAM_ID)
    file_path = os.path.join(tmp_folder,file_name)
    log_list = ['[Info] : xxx \n',
                '[Warning] : xxx \n',
                '[Error] : xxx \n']
    

    for _ in range(random.randint(0,3)):
        log = log_list[0]
        with open(file_path, "a") as file:        
            file.write(log) 
    if random.uniform(0,1) > 0.7:
        for _ in range(random.randint(1,2)):
            log = log_list[1]
            with open(file_path, "a") as file:        
                file.write(log)
    if random.uniform(0,1) > 0.8:
        log = log_list[2]
        with open(file_path, "a") as file:        
            file.write(log)
    
    if random.uniform(0,1) > 0:
        with open(file_path, "a") as file:        
            file.write('EndFile \n')
 