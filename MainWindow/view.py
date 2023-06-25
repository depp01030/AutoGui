# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\AutoCam\MainWindow\view.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(696, 581)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(200, 0))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.pushButton_test = QtGui.QPushButton(self.centralwidget)
        self.pushButton_test.setObjectName(_fromUtf8("pushButton_test"))
        self.verticalLayout_4.addWidget(self.pushButton_test)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tabWidget_process = QtGui.QTabWidget(self.frame)
        self.tabWidget_process.setAutoFillBackground(False)
        self.tabWidget_process.setStyleSheet(_fromUtf8("QTabWidget::pane { /* The tab widget frame */\n"
"    border: 1px solid #C2C7CB;  /* here is the line*/\n"
" padding:20px;\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    left: 1px; /* move to the right by 5px */\n"
"}\n"
"QTabWidget{\n"
"    background-color:rgb(126, 126, 126);\n"
"}\n"
"/* Style the tab using the tab sub-control. Note that\n"
"    it reads QTabBar _not_ QTabWidget */\n"
"QTabBar::tab {\n"
"    margin:0px;/*0 这里可以让tab 跟 TabWidget连成一片*/\n"
"    padding:4px;\n"
"    border-radius: 6px;\n"
"    background:#ffffff;\n"
"    border:2px solid #d9d9d9; \n"
"    background-color:rgb(126, 126, 126);\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    border-color: #9B9B9B;\n"
"    background-color:rgb(218, 218, 218);\n"
"    margin-bottom:-1px;    /*here when selected,I want tab to lower a px. so to covery the line.\n"
"                                               but the line is in front of tab*/\n"
"                                         \n"
"}"))
        self.tabWidget_process.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget_process.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget_process.setIconSize(QtCore.QSize(20, 50))
        self.tabWidget_process.setElideMode(QtCore.Qt.ElideMiddle)
        self.tabWidget_process.setUsesScrollButtons(True)
        self.tabWidget_process.setDocumentMode(False)
        self.tabWidget_process.setTabsClosable(False)
        self.tabWidget_process.setMovable(False)
        self.tabWidget_process.setObjectName(_fromUtf8("tabWidget_process"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.listWidget1 = QtGui.QListWidget(self.tab)
        self.listWidget1.setObjectName(_fromUtf8("listWidget1"))
        self.verticalLayout_5.addWidget(self.listWidget1)
        self.tabWidget_process.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listWidget = QtGui.QListWidget(self.tab_2)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)
        self.label_3 = QtGui.QLabel(self.tab_2)
        self.label_3.setStyleSheet(_fromUtf8("QLabel {\n"
"        border : 0px solid #298DFF;    \n"
"        border-radius : 3px;\n"
"        background-color : rgb(105, 235, 157);\n"
"        color : rgb(54, 54, 54);\n"
"        font-size : 12pt;\n"
"}"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.tabWidget_process.addTab(self.tab_2, _fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.tabWidget_process)
        self.frame_optional = QtGui.QFrame(self.frame)
        self.frame_optional.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_optional.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_optional.setObjectName(_fromUtf8("frame_optional"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_optional)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.line = QtGui.QFrame(self.frame_optional)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout.addWidget(self.line)
        self.frame_3 = QtGui.QFrame(self.frame_optional)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(self.frame_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout.addWidget(self.frame_3)
        self.widget = QtGui.QWidget(self.frame_optional)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.pushButton_test2 = QtGui.QPushButton(self.widget)
        self.pushButton_test2.setObjectName(_fromUtf8("pushButton_test2"))
        self.verticalLayout_3.addWidget(self.pushButton_test2)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.horizontalLayout.addWidget(self.widget)
        self.horizontalLayout_2.addWidget(self.frame_optional)
        self.listWidget.raise_()
        self.tabWidget_process.raise_()
        self.frame_optional.raise_()
        self.verticalLayout_4.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 696, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSaveConfig = QtGui.QAction(MainWindow)
        self.actionSaveConfig.setObjectName(_fromUtf8("actionSaveConfig"))
        self.actionCreateProgram = QtGui.QAction(MainWindow)
        self.actionCreateProgram.setObjectName(_fromUtf8("actionCreateProgram"))
        self.menuFile.addAction(self.actionCreateProgram)
        self.menuFile.addAction(self.actionSaveConfig)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget_process.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_test.setText(_translate("MainWindow", "test", None))
        self.tabWidget_process.setTabText(self.tabWidget_process.indexOf(self.tab), _translate("MainWindow", "Tab 1", None))
        self.label_3.setText(_translate("MainWindow", "TextLabel", None))
        self.tabWidget_process.setTabText(self.tabWidget_process.indexOf(self.tab_2), _translate("MainWindow", "Tab 2", None))
        self.label_2.setText(_translate("MainWindow", "LogBoxxxxxxxxxxxxx", None))
        self.pushButton_test2.setText(_translate("MainWindow", "test2", None))
        self.label.setText(_translate("MainWindow", "LayerSelectorrrrrrrrrrrrrrrrrrrrrr", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionSaveConfig.setText(_translate("MainWindow", "Save", None))
        self.actionCreateProgram.setText(_translate("MainWindow", "Create Program", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

