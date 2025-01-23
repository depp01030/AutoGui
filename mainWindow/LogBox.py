#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from PyQt4 import QtGui, QtCore
# reload(sys)
# sys.setdefaultencoding("utf-8")

class LogBox(QtGui.QTextBrowser):
    def __init__(self,parent=None):
        super(LogBox, self).__init__(parent)   
        self._sysinfo = u'系統資訊 : \n'
        self.set_info()
    def _parse(self, word):
        '''
        conver word into standard string format
        '''
        if type(word) == list:
            parsed_word = ''
            for item in word:
                if not item or isinstance(item, list):
                    continue
                print('item : ', item)
                utf8_data = item.decode('utf-8').encode('utf-8')
                item = QtCore.QTextCodec.codecForName("UTF-8").toUnicode(utf8_data)  
                parsed_word += item
                if '\n' not in item:
                    parsed_word += '\n'
        elif type(word) == QtCore.QString:
            parsed_word = word        
        elif isinstance(word, str): #str unicode Qstring
            print(word)
            # word = '中文'
            # word = 'Warning : \xe9\x80\x99 '
            # utf8_data = word.decode('unicode_escape')
            utf8_data = word.decode('utf-8')
            parsed_word = utf8_data
            # utf8_data = word.decode('utf-8')
            # parsed_word = QtCore.QTextCodec.codecForName("UTF-8").toUnicode(utf8_data)  
            # print('not str ' + str(parsed_word))
            # parsed_word = utf8_data
            # parsed_word = word 

        else: #is unicode (\xe9\x80\x99 '.decode('utf-8') already)
            # word = '\u9019\u908a' 
            # parsed_word = word.decode('unicode_escape')
            parsed_word = word
            # parsed_word = 'ELSE' 
            # parsed_word = 'no'
        return parsed_word

    def append(self, word):   
        parsed_word = self._parse(word)
        super(LogBox,self).append(parsed_word)


    def sys_append(self,word):
        parsed_word = self._parse(word)
        self._sysinfo += parsed_word + '\n'
        super(LogBox,self).append(parsed_word)



    def set_info(self):
        self.clear() 
        super(LogBox,self).append(self._sysinfo)

        # LogBox