#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import random
import traceback
sys.path.append(r'\\ezcamls\ezcam\sys\scripts\AutoCAM2.0')
sys.path.append("/InCAM/server/site_data/scripts/AutoCAM2.0")
sys.path.append(r"/genesis/sys/scripts/AutoCAM2.0")
#%% SET ROOT_PATH
from Utils import LOGIN
UID_KEY = 'KeyInYourUidHere' #key in uid if useing gateway in ezcam
LOGIN_DICT = LOGIN.get_login_dict(UID_KEY = UID_KEY)
# load ENV
for key , value in LOGIN_DICT.items():
    os.environ[key] = value
# set system PATH
for key in ["ROOT_PATH", "UTILS_PATH", "GEN_PATH"]:
    sys.path.append(os.environ[key])


import genClasses 

from mainWindow import SQLModel

def get_job_id(gen_object):
    '''get one or create one if not exist'''
    if 'JOB' in os.environ.keys() and os.environ['JOB']:
        
        # gen_object = genClasses.Job(os.environ['JOB'])    
        attr_dict = gen_object.DO_INFO('-t job -e %s -d ATTR' % (gen_object.name))
        
        if '.comment' in attr_dict['gATTRname']:
            idx = attr_dict['gATTRname'].index('.comment')
            comment = attr_dict['gATTRval'][idx]
        else:
            comment = ''
        if not comment:
            job_id = str(random.randint(1000000, 9999999))
            comment_text = "job_id=%s;" % (job_id)
            gen_object.COM("set_attribute, attribute=.comment, \
                            job=%s,name1=,type=Job,value=%s" % (gen_object.name, comment_text))
        else:
            comment_list = comment.split(';')
            for var in comment_list:
                if 'job_id' in var:
                    job_id = var.split('=')[1]
                    break 
    else:                
        job_id = str(404)
    return job_id

def main():
    '''
    Mock CAM save function
    '''
    try:
        if sys.version_info[0] + 0.1 * sys.version_info[1] < 2.6:
            return 
        if 'JOB' in os.environ.keys() and os.environ['JOB']:
            gen_object = genClasses.Job(os.environ['JOB'])   
        else:
            return 
        # gen_object.PAUSE('Save')
        job_id = get_job_id(gen_object)
        if 'JOB' in os.environ.keys():
            job_name = os.environ['JOB']
        else:
            job_name = ''
        if job_name == '':
            return

        file_name = '%s_%s' % (job_id, job_name)
        file_path = os.path.join(os.environ['ROOT_PATH'], 'Tmp', file_name)
        # file_path = r'\\ezcamls\ezcam\sys\scripts\AutoCAM2.0\Tmp\404_NA'
        if os.path.isfile(file_path):
            f = open(file_path)
            job_logs = f.readlines()
            f.close()
            insert_job_logs = []
            for job_log in job_logs:
                try:
                    job_log_dict = eval(job_log)
                except:
                    continue
                job_log_dict['IsSave'] = 1
                insert_job_logs.append(job_log_dict)
            
            if SQLModel.insert_job_logs_to_db(insert_job_logs):

                if os.path.isfile(file_path):
                    os.remove(file_path)
            else: #服務異常打不上去，就存回去(淡紀錄已經被切換了)
                with open(file_path, 'w') as f :
                    for tmp_job_log in insert_job_logs:
                         f.write(str(tmp_job_log) + '\n')

                    

    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)
if __name__ == '__main__':
    main()