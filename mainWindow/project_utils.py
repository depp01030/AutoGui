#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:58:08 2023

@author: Depp
"""
#%%
import os 
import json
import random
import traceback
import platform
import subprocess
import datetime 
import shutil

#%%


def check_main_folder_valid(main_folder_path):
#    print(main_folder)
    pass
    return True

        
def is_folder_valid(folder_path):            
    return os.path.isdir(folder_path)
 

def get_program_name(program_key, program_config):
    program_name = program_key
    cur_program_config = program_config.get(program_key, {})
    if cur_program_config != {}:
        program_name = cur_program_config['button_name'] 
        # program_name = QString(program_name)
    
        # utf8_data = program_name.decode('utf-8').encode('utf-8')
        # program_name = QtCore.QTextCodec.codecForName("UTF-8").toUnicode(program_name)
    return program_name

def get_folder_ver_name(
            program_root,
            main_folder_path,
            program_key ):
    '''
    program_root = os.getcwd()
    main_folder_path = 'Preprocess\\Main_SettingProfile'        
    folder_list = ['testProgram-240522-1-1235',
                    'testProgram-240522-2-1235',
                    'testProgram-240522-3-1239']
    
    '''
    test_folder_path = os.path.join(program_root, main_folder_path, 'Test')
    
    date_code = datetime.datetime.now().strftime('%y%m%d')
    time_code = datetime.datetime.now().strftime('%H%M')
    
    ver_folder_name = program_key + '-' + date_code

    folder_list = os.listdir(test_folder_path)
    num_list = list(map(lambda x:x.split('-')[2], folder_list))
    i = 1
    # while ver_folder_name + '-' + str(i) in folder_list:
    while str(i) in num_list:
        i += 1 
    return ver_folder_name + '-' + str(i) + '-' + time_code
def get_program_key(folder_path):
    return os.path.basename(folder_path)
def check_is_program_frame_exist(program_key, program_config):
    
    if program_key in program_config.keys():
        return True
    return False


def get_process_by_config(program_key, program_config):
    '''
    program_key = 'SettingProfile'
    '''
    process_key = ''
    cur_program_config = program_config.get(program_key, {})
    if cur_program_config != {}:
        process_key = cur_program_config['process'] 
    return process_key
def create_standard_folder(process_key, program, prefix = 'Main_'):
    # process = 'process'; program = 'program'
    root_path = os.getcwd()
    
    process_path = os.path.join(root_path, process_key)
    main_program_folder = os.path.join(process_path, prefix + program)
    sub_folder_list = ['Release', 'Test', 'Tmp', 'Log']    
    if not os.path.isdir(process_path ):
        os.mkdir(process_path)
    if not os.path.isdir(main_program_folder):
        os.mkdir(main_program_folder)
    for sub_folder in sub_folder_list:
        sub_folder_path = os.path.join(main_program_folder, sub_folder)
        if not os.path.isdir(sub_folder_path):
            os.mkdir(sub_folder_path)
 
    main_program_folder_path = os.path.join(process_key,prefix + program)
    return main_program_folder_path

def copy_to_test_folder(folder_path,
                        root_path,
                        main_folder_path,
                        folder_ver_name):
    try:
        test_folder_path = os.path.join(root_path, main_folder_path, 'Test')
        print('folder name*********************', test_folder_path, folder_ver_name) 
        shutil.copytree(folder_path, os.path.join(test_folder_path, folder_ver_name))
    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg) 

def copy_to_sub_folder(src_copying_folder_path,
                    root_path,
                    dest_folder_path,
                    sub_program_key,
                    TR_ver,
                    LogBox ): 
    try:
        dest_folder_path = os.path.join(root_path, dest_folder_path,
                                        TR_ver, sub_program_key) 
        if os.path.isdir(dest_folder_path):
            shutil.rmtree(dest_folder_path)
        shutil.copytree(src_copying_folder_path, dest_folder_path)

        copy_ref_files(TR_ver, src_copying_folder_path, dest_folder_path)

    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg) 
def copy_ref_files(TR_ver, src_copying_folder_path, dest_folder_path):
    ref_files_list = ['UiSetting.py']
    src_folder_path = os.path.dirname(src_copying_folder_path)
    dest_folder_path = os.path.dirname(dest_folder_path)

    for ref_file in ref_files_list:
        if os.path.isfile(os.path.join(dest_folder_path, ref_file)):
            continue
        elif TR_ver == 'Release':
            #先看test 有沒有可以copy的
            test_src_folder_path = dest_folder_path.replace('Release', 'Test')
            if os.path.isfile(os.path.join(test_src_folder_path, ref_file)):            
                shutil.copy(os.path.join(test_src_folder_path, ref_file), dest_folder_path)        
            else:
                #test資料夾沒有檔案了話，從原始Main_xx copy
                shutil.copy(os.path.join(src_folder_path, ref_file), dest_folder_path)
        else:
            #test資料夾沒有檔案了話，從原始Main_xx copy
            shutil.copy(os.path.join(src_folder_path, ref_file), dest_folder_path)





def get_program_frame(cur_tab,
                       program_key):
    ##check if program exist in cur tab
    program_frame = None
    for index in range(cur_tab.listWidget.count()):
        item = cur_tab.listWidget.item(index)
        cur_frame = cur_tab.listWidget.itemWidget(item)
        cur_frame_key = str(cur_frame.objectName())
        if program_key == cur_frame_key:
            program_frame = cur_frame
            break
    return program_frame
def get_sub_folder_suffix(program_config, 
                          program_name):
    '''
    
    file_path = os.path.join(os.getcwd(), '..', 'program_config.json')
    with open(file_path, 'r') as f:
        program_config = json.load(f)
    program_name = 'Pass'
    '''
    suffix = 1
    while '{0}_{1}'.format(program_name, suffix) in program_config.keys():
        suffix += 1
    return str(suffix)
def get_sub_program_key_list(program_config, 
                             program_name):
    '''
    program_name = 'Pass'
    '''
    suffix = 1
    sub_program_key_list = []
    while '{0}_{1}'.format(program_name, suffix) in program_config.keys():
        sub_program_key_list.append('{0}_{1}'.format(program_name, suffix))
        suffix += 1
    return sub_program_key_list
 
# %%
