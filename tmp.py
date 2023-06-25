# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:07:05 2023

@author: User
"""
import json
config = {'TestA' : {
                    'process' : 'Preprocess',
                    'button_name': 'TestA',
                    'main_folder': 'TestA',
                    'order' : 0},
          'TestB' : {
                    'process' : 'Preprocess',
                    'button_name': 'TestB',
                    'main_folder': 'TestB',
                    'order' : 1},
          'TestC' : {
                    'process' : 'Preprocess',
                    'button_name': 'TestC',
                    'main_folder': 'TestC',
                    'order' : 2},
          'TestD' : {
                    'process' : 'Drill',
                    'button_name': 'TestB',
                    'main_folder': 'TestB',
                    'order' : 1},
        } 
with open("config.json", "w") as file:
    json.dump(config, file, indent=4)

# 从文件中读取 JSON 数据并解析为 Python 数据
with open("config.json", "r") as file:
    config = json.load(file)

