#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 09:40:31 2023

@author: 220853
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
import traceback



def check_list_exist(step_object, chk_list_name):
    """
    確認 check_list 存在
    """
    job_name = step_object.job.name
    step_name = step_object.name
    is_exist = False

    exist_dict = step_object.DO_INFO("-t check -e {0}/{1}/{2} -d EXISTS".format(job_name, step_name, chk_list_name))

    if exist_dict:
        if exist_dict['gEXISTS'] == 'yes':
            is_exist = True
        else:
            is_exist = False

    return is_exist


def get_already_action_num(step_object, check_list_name):

    job_name = step_object.job.name
    step_name = step_object.name

    action_num_dict = step_object.DO_INFO("-t check -e {0}/{1}/{2} -d NUM_ACT -o action=1"\
                                        .format(job_name, step_name, check_list_name))
    # action_num = action_num_dict['gNUM_ACT']
    action_num = action_num_dict.get('gNUM_ACT', 0)

    return action_num


def get_action_title(step_object, check_list_name, action_num):
    job_name = step_object.job.name
    step_name = step_object.name
    action_title = ''
    title_dict = step_object.DO_INFO('-t check -e {0}/{1}/{2} -d TITLE -o action={3}'\
                                    .format(job_name, step_name, check_list_name, action_num))
    if title_dict:
        action_title = title_dict['gTITLE']
    return action_title


def get_check_list_action_info(step_object, check_name, action_num, category = '', layer = ''):

    job_name = step_object.job.name
    step_name = step_object.name
    search_str = ''
    action_info_list = []
    search_str = ''
    if str(action_num) != '':
        search_str = 'action=' + str(action_num)
        if category:
            search_str += '+category=' + category
        if layer:
            search_str += '+layer=' + layer
        action_info_list = step_object.INFO('-t check -e {0}/{1}/{2} -d MEAS -o {3}'\
                                            .format(job_name, step_name, check_name, search_str))
    return action_info_list


def get_all_checklist_info(step_object, check_list_name = 'Temporary'):
    checklist_info_dict = {}
    try:
        is_exist = check_list_exist(step_object, check_list_name)
        if is_exist:
            action_num = get_already_action_num(step_object, check_list_name)
            for num in range(int(action_num)):
                action_num = num + 1
                action_title = get_action_title(step_object, check_list_name, action_num)
                action_info_list = get_check_list_action_info(step_object, check_list_name, action_num)
                key_name = str(action_num) + '_' + str(action_title)
                checklist_info_dict[key_name] = action_info_list

        else:
            step_object.COM('chklist_create,chklist={0}'.format(check_list_name))

    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)

    return checklist_info_dict