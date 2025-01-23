# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/InCAM/server/site_data/scripts/AutoCAM2.0/mainWindow/Frames/ToolFrame_view.ui'
#
# Created: Wed Jun 26 08:32:37 2024
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
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_reset_job_id = QtGui.QPushButton(Frame)
        self.pushButton_reset_job_id.setObjectName("pushButton_reset_job_id")
        self.gridLayout.addWidget(self.pushButton_reset_job_id, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QtGui.QApplication.translate("Frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_reset_job_id.setText(QtGui.QApplication.translate("Frame", "ResetJobID", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Frame = QtGui.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())

