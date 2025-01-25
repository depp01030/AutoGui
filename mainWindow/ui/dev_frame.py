# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/InCAM/server/site_data/scripts/AutoCAM2.0/mainWindow/ui/dev_frame.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName(_fromUtf8("Frame"))
        Frame.resize(685, 423)
        Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Frame)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(Frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit_folder_name = QtGui.QLineEdit(Frame)
        self.lineEdit_folder_name.setObjectName(_fromUtf8("lineEdit_folder_name"))
        self.horizontalLayout_2.addWidget(self.lineEdit_folder_name)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(Frame)
        self.label_2.setEnabled(True)
        self.label_2.setSizeIncrement(QtCore.QSize(0, 0))
        self.label_2.setBaseSize(QtCore.QSize(0, 0))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit_file_name = QtGui.QLineEdit(Frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_file_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_file_name.setSizePolicy(sizePolicy)
        self.lineEdit_file_name.setMaximumSize(QtCore.QSize(591, 16777215))
        self.lineEdit_file_name.setObjectName(_fromUtf8("lineEdit_file_name"))
        self.horizontalLayout_3.addWidget(self.lineEdit_file_name)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBox_layers = QtGui.QCheckBox(Frame)
        self.checkBox_layers.setObjectName(_fromUtf8("checkBox_layers"))
        self.horizontalLayout.addWidget(self.checkBox_layers)
        self.checkBox_check_list = QtGui.QCheckBox(Frame)
        self.checkBox_check_list.setObjectName(_fromUtf8("checkBox_check_list"))
        self.horizontalLayout.addWidget(self.checkBox_check_list)
        self.checkBox_spe_sym_dict = QtGui.QCheckBox(Frame)
        self.checkBox_spe_sym_dict.setObjectName(_fromUtf8("checkBox_spe_sym_dict"))
        self.horizontalLayout.addWidget(self.checkBox_spe_sym_dict)
        self.checkBox_matrix = QtGui.QCheckBox(Frame)
        self.checkBox_matrix.setObjectName(_fromUtf8("checkBox_matrix"))
        self.horizontalLayout.addWidget(self.checkBox_matrix)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton_copy_dev_job_info = QtGui.QPushButton(Frame)
        self.pushButton_copy_dev_job_info.setObjectName(_fromUtf8("pushButton_copy_dev_job_info"))
        self.verticalLayout.addWidget(self.pushButton_copy_dev_job_info)
        self.pushButton_post_affected_layer = QtGui.QPushButton(Frame)
        self.pushButton_post_affected_layer.setObjectName(_fromUtf8("pushButton_post_affected_layer"))
        self.verticalLayout.addWidget(self.pushButton_post_affected_layer)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(_translate("Frame", "Frame", None))
        self.label.setText(_translate("Frame", "folder_name", None))
        self.label_2.setText(_translate("Frame", "file_name    ", None))
        self.checkBox_layers.setText(_translate("Frame", "layers", None))
        self.checkBox_check_list.setText(_translate("Frame", "check_list", None))
        self.checkBox_spe_sym_dict.setText(_translate("Frame", "spe_sym_dict", None))
        self.checkBox_matrix.setText(_translate("Frame", "matrix", None))
        self.pushButton_copy_dev_job_info.setText(_translate("Frame", "Copy Job Info", None))
        self.pushButton_post_affected_layer.setText(_translate("Frame", "Post affected layer", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Frame = QtGui.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())

