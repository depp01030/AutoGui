# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/InCAM/server/site_data/scripts/AutoCAM2.0/Utils/Template/ui/view.ui'
#
# Created: Fri Jul 21 16:03:56 2023
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(190, 207)
        Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout = QtGui.QVBoxLayout(Frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_execute = QtGui.QPushButton(Frame)
        self.pushButton_execute.setObjectName("pushButton_execute")
        self.verticalLayout.addWidget(self.pushButton_execute)
        self.pushButton_Test = QtGui.QPushButton(Frame)
        self.pushButton_Test.setObjectName("pushButton_Test")
        self.verticalLayout.addWidget(self.pushButton_Test)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QtGui.QApplication.translate("Frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_execute.setText(QtGui.QApplication.translate("Frame", "Execute", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Test.setText(QtGui.QApplication.translate("Frame", "Test", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Frame = QtGui.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())

