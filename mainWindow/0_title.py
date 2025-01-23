#!/usr/bin/python
# -*- coding: utf-8 -*-

#%%
import os
#os.environ["utils_path"] = "/InCAM/server/site_data/scripts/gen_py/"
import sys
import time
import requests
import re
import copy
from datetime import datetime
import shlex
import json
import math 
'=====================  Script  ==========================='
#print str(sys.argv) False True
sys.path.append(r"\\192.168.1.63\ezcam\1.1\resource\python\debugger")

os.environ['EZCAM_UID'] = r"\\192.168.1.63\ezcam\1.1\bin\gateway.exe g@PC905.210605.150C0B.20312 "

if not os.path.isdir("D:/ezcam_tmp"):
    os.mkdir("D:/ezcam_tmp")
os.environ['GENESIS_TMP'] =r"D:\\ezcam\tmp"

os.environ['GENESIS_EDIR'] =r"\\192.168.1.63\ezcam\1.1"

os.environ['GENESIS_DIR'] =r"\\192.168.1.63\ezcam\1.1"

os.environ['USER']= 'IESAdmin'

'''
os.chdir(os.environ['UTILS_PATH'])
os.getcwd()
os.chdir(r'\\ezcamls\ezcam\sys\scripts\overwrite\0_MultiPCBPanel')
'''
import genClasses
import genCommands
import genBasic

os.environ["UTILS_PATH"] = r"\\192.168.1.63\ezcam\1.1\resource\python"
sys.path.append(os.environ["UTILS_PATH"])


'''
os.environ['JOB'] = 'hslc-lb015t-x-panel-narrordmx-arrow'
'''
#set init path

from utils import create_layer, setting_initialize, send_mail,\
                    camjob2mes, is_multi_press, get_sec_drill_layers

#os.chdir(os.path.dirname(os.path.abspath(__file__)))
#
#sys.path.append('//ezcamls/ezcam/sys/scripts/overwrite/AddInnCuPad')
#os.chdir('//ezcamls/ezcam/sys/scripts/overwrite/AddInnCuPad')
#os.getcwd()
#import UiGenerator
#ui_result = UiGenerator.UiLauncher('YN_Radio')

project = 'multi_panel'
#%%
if project == 'multi_panel':
    from project_utils.get_info_from_mes import get_full_info_dict_from_mes, get_default_parameter_from_mes
    from project_utils.get_info_from_cam import get_default_parameter_from_cam,update_final_dicts_info_from_cam
    from project_utils.project_utils import create_step, change_prof_size, panelize_shipping_panel, get_panel_size_dict,filter_out_by_attr
    from utils import create_layer, setting_initialize, send_mail,\
                        camjob2mes, is_multi_press, get_sec_drill_layers
    from IES_service_utils import update_project_parameters, get_project_parameters       


    
    '''
    os.environ['JOB'] ='yoko-pd000l-v1d01-0110' # " (單壓 有二階雷射)"
    os.environ['JOB'] = 'RENE-LB0009-A1D01' # (單向壓 core 12)
    os.environ['JOB'] = 'MTKX-OT001C-A1D01' # (雙向壓2-23,24-35,1-36)
    os.environ['JOB'] = 'TSMC-DD0224-V2D02' # (單向壓1-14,1-75)
    os.environ['JOB'] = 'MARV-DD000B-V1D01' # (雙向壓+散裝 1-10,47-56,1,56)
    os.environ['JOB'] = 'rd-2019080062-a1d01' #(二壓 中間+雙向增層 4-13,1-16)
    os.environ['JOB'] = 'CHPT-OT001J-A1D01' # (二壓+空core 1-6,7-10,1-10 (7,8之間有空core)
    os.environ['JOB'] = 'hslc-ot000p-b2d01-multipress' # (二壓內層沒銅皮 1-17, 18-32)
    os.environ['JOB'] = 'syno-ot0001'       # (三壓1-14,15-44,1-44,45-52,1-52)
    os.environ['JOB'] = 'tsmc-dd0249-v1d01-juri' # (雙向壓 1-20, 21-46, empty core)
    os.environ['JOB'] = 'mtkx-lb007r-a2d01-juri' # (雙向壓vci 2-27, 28-53, )
    os.environ['JOB'] = 'advt-db009r' #two_empty_core
    job_name = os.environ['JOB']
    '''

#%%
if __name__ == '__main__':
    '''
    os.environ['JOB'] ='yoko-pd000l-v1d01-0110' # " (單壓 有二階雷射)"
    os.environ['JOB'] ='mtkx-lb007r-a2d01-keddy' # " (雙向壓vci 2-27, 28-53, )"
    os.environ['JOB'] = 'mtkx-ot001b-a1d01-secco2' # " (雙向壓2-23,24-35,1-36 / d2-3, d1-2, d35-36) "  

    os.environ['JOB'] = 'RENE-LB0009-A1D01' #1c1p #no_cu
    os.environ['JOB'] = 'mtkx-ot001c-a1d01-keddy' #2c3p #2cu
    os.environ['JOB'] = 'mtkx-lb007r-a2d01-keddy-check' #2c3p #2cu #vci
    
    os.environ['JOB'] = 'yoko-pd000l-v1d01-0110'   #1c1p #2laser
    os.environ['JOB'] = 'tsmc-dd0224-v2d02-keddy' #2c2p
    os.environ['JOB'] = 'tsmc-dd0271-v1d01-cubga' #2c2p #2cu
    os.environ['JOB'] = 'MARV-DD000B-V1D01-keddy' #2c3p_e
    os.environ['JOB'] = 'RD-2019080062-A1D01' #2c2p_b
    os.environ['JOB'] = 'CHPT-OT001J-A1D01' #2c3p
    os.environ['JOB'] = 'hslc-ot000p-b2d01' #2c3p #nocu
    os.environ['JOB'] = 'advt-db009r'       #1c1p
    os.environ['JOB'] = 'TSMC-DD0249-V1D01' #2c3p #1cu
    os.environ['JOB'] = 'syno-ot0001-juri'  #3c5p
    os.environ['JOB'] = 'syna-lb000e-a1d01'  #2c2p #1cu

    os.environ['JOB'] = 'syna-lb000e-a1d01'  #2c2p #1cu
    os.environ['JOB'] = 'RENE-LB0009-A1D01' # (單向壓 core 12)
    os.environ['JOB'] = 'MTKX-OT001C-A1D01' # (雙向壓2-23,24-35,1-36)
    os.environ['JOB'] = 'TSMC-DD0224-V2D02' # (單向壓1-14,1-75)
    os.environ['JOB'] = 'TSMC-DD0249-V1D01' # (經典雙向 1-20, 21-46)
    os.environ['JOB'] = 'MARV-DD000B-V1D01' # (雙向壓+散裝 1-10,47-56,1,56)
    os.environ['JOB'] = 'syno-ot0001-juri'  # (三壓1-14,15-44,1-44,45-52,1-52)
    os.environ['JOB'] = 'RD-2019080062-A1D01' #(二壓 中間+雙向增層 4-13,1-16)
    os.environ['JOB'] = 'CHPT-OT001J-A1D01' # (二壓+空core 1-6,7-10,1-10 (7,8之間有空core)
        
    os.environ['JOB'] = "mtkx-lb008f-a1d01-juri"
    os.environ['JOB'] = 'zeku-pd0002-v1d01-juri'
    os.environ['JOB'] = 'qctx-pc003n-juri'
    
    os.environ['JOB'] = "mtkx-ot001b-a1d01-secco2"
    '''
    
    job_name = os.environ['JOB']
    job_object = genClasses.Job(os.environ['JOB'])    
    step_object = genClasses.Step(job_object, 'pcb')  
    matrix_info = step_object.job.matrix.getInfo()
    matrix_info['gROWname']
    step_object.display('l3')

    
    job_info_dict = get_project_parameters(job_name, 'MultiPCBPanel')

    job_name = 'amba-lb001f-a1d01'
    job_name = os.environ['JOB']
    project_name = 'MultiPCBPanel'
    job_info_dict  = get_project_parameters(job_name, project_name)

# %%

job_name
all_layer_attr_dict = job_info_dict['all_layer_attr_dict']
parsed_stackup_dict = job_info_dict['parsed_stackup_dict'] 
combine_dict = parsed_stackup_dict['combine_dict']
all_press_dict = parsed_stackup_dict['all_press_dict']

parsed_stackup_dict.keys()
all_layer_attr_dict.keys()
parsed_stackup_dict['all_press_dict']['d4-13'].keys()
all_layer_attr_dict['10mil-top-0']
all_layer_attr_dict['l14']['mate_phase_of_manufacture']
all_layer_attr_dict['l44']['mate_phase_of_manufacture']
all_layer_attr_dict['l45']['mate_phase_of_manufacture']
all_layer_attr_dict['l46']['mate_phase_of_manufacture']

job_info_dict
#%% marv
all_layer_attr_dict['l19']
all_layer_attr_dict['l14']
all_layer_attr_dict['l15']
all_layer_attr_dict['l31']
all_layer_attr_dict['l10'] 
cur = root



os.environ['JOB'] = 'rene-lb0009-a1d01' #1c1p l1 roger
os.environ['JOB'] = 'mtkx-ot001c-a1d01-keddy' #2c3p l3
os.environ['JOB'] = 'mtkx-lb007r-a2d01-keddy-check' #2c3p l4 vci
os.environ['JOB'] = 'yoko-pd000l-v1d01' #1c1p l2l2
os.environ['JOB'] = 'tsmc-dd0224-v2d02-keddy' #2c2p1y
os.environ['JOB'] = 'tsmc-dd0271-v1d01-cubga' #2c2p1y l1
os.environ['JOB'] = 'marv-dd000b-v1d01-keddy' #2c3p1y
os.environ['JOB'] = 'rd-2019080062-a1d01' #2c2p l6 build
os.environ['JOB'] = 'hslc-ot000p-b2d01' #2c3p l2
os.environ['JOB'] = 'tsmc-dd0249-v1d01-keddy-co2' #2c3p l1
os.environ['JOB'] = 'syno-ot0001-juri'  #3c5p
os.environ['JOB'] = 'syna-lb000e-a1d01'  #2c2p1y
os.environ['JOB'] = 'chpt-pc0015-v1d03-panel-circle-pcbvalor' #1c1p circle_s
os.environ['JOB'] = 'msun-pc001d-v1d02-panel-circle2' #1c1p circle_b
os.environ['JOB'] = 'qctx-pc0056-juri' #1c1p
os.environ['JOB'] = 'zeku-pd0002-v1d01-juri' #2c3p l2 vci
os.environ['JOB'] = 'advt-db009r' #1c1p


def product_type(job_name):
   ITEMNO, ERP_ITEMVER = camjob2mes(job_name)
   target_job_name = ITEMNO + '-' + ERP_ITEMVER

   is_st = False

   Split_JOb = target_job_name.split('-')
   job_name = '-'.join(Split_JOb[:3])

   if Split_JOb[1][:2].lower() in ["st","uf","tf","ta","am","ap"]:
       is_st = True

   elif 'rd' in Split_JOb[0][:2]:
       if len(Split_JOb) == 2:
           job_name = job_name + '-X'
       
   payload = {'part_num':job_name.upper()}
   r = requests.post("http://10.12.20.149:820/cam/query_part_num", data=payload, timeout=5)
   ItemNumber = r.text

   if len(ItemNumber) != 0 and '-ST-' in ItemNumber  :
       is_st = True
   
   if is_st:
       return 'ST'

   else:      
       return 'PCB'