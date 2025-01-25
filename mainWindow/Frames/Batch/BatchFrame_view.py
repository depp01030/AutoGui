# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/InCAM/server/site_data/scripts/AutoCAM2.0/mainWindow/Frames/Batch/BatchFrame_view.ui'
#
# Created: Wed Oct  9 17:35:53 2024
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(463, 459)
        Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout = QtGui.QVBoxLayout(Frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listWidget_batch_job_list = QtGui.QListWidget(Frame)
        self.listWidget_batch_job_list.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidget_batch_job_list.setObjectName("listWidget_batch_job_list")
        self.verticalLayout_2.addWidget(self.listWidget_batch_job_list)
        self.pushButton_batch_exec = QtGui.QPushButton(Frame)
        self.pushButton_batch_exec.setObjectName("pushButton_batch_exec")
        self.verticalLayout_2.addWidget(self.pushButton_batch_exec)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QtGui.QApplication.translate("Frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_batch_exec.setText(QtGui.QApplication.translate("Frame", "Batch Run ", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Frame = QtGui.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())

