
from PyQt4 import QtGui, QtCore

class MyListWidget(QtGui.QListWidget): 
    def __init__(self,SIGNAL_MANAGER):
        super(MyListWidget, self).__init__()
        self.SIGNAL_MANAGER = SIGNAL_MANAGER
        # self.setSelectionMode(QListWidget.ExtendedSelection) 
        self.drag_state = 'Wait' #"Wait", "None"

        # self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
    def clearSelection(self):
        super(MyListWidget, self).clearSelection()
        self.SIGNAL_MANAGER.program_list_clear_selection.emit()
        frame = self.itemWidget(self.currentItem())
        if frame:
            frame.unselect()
        # set result state
        for i in range(self.count()):
            item = self.item(i)
            if item is None:                                
                continue
            frame = self.itemWidget(item)
            frame.label.set_result_state()




    def mousePressEvent(self, event):
        if event.modifiers() & QtCore.Qt.ShiftModifier:
            if event.button() == QtCore.Qt.LeftButton:
                current_row = self.currentRow()
                item = self.itemAt(event.pos())
                row_index = self.row(item) 
                self.set_item_waiting(current_row, row_index)
                # self.drag_state = 'Wait' if self.drag_state == 'None' else 'None'
        elif ( event.modifiers() & QtCore.Qt.ControlModifier) and \
             ( event.modifiers() & QtCore.Qt.AltModifier) :
            item = self.itemAt(event.pos())
            frame = self.itemWidget(item)
            frame.open_folder_clicked(force= True)
        else:
            super(MyListWidget, self).mousePressEvent(event)
    def set_item_waiting(self, current_row, row_index):
        begin, end = sorted([current_row, row_index])
        for i in range(begin, end + 1):
            if i > self.count():
                return
            item = self.item(i)
            if item is None:                                
                continue
            frame = self.itemWidget(item)
            frame.label.set_idle_state('Wait')
    # def mouseMoveEvent(self, event):
    #     if (self.start_pos is not None and 
    #         event.modifiers() & QtCore.Qt.ShiftModifier and
    #         event.buttons() == QtCore.Qt.LeftButton):
    #             item = self.itemAt(event.pos())
    #             if item is not None:                                
    #                 frame = self.itemWidget(item)
    #                 frame.label.set_state_on_drag(self.drag_state)
    #             # rect = QRect(self.drag_start_pos, event.pos()).normalized()
    #             # for checkbox in self.checkbox_list:
    #             #     if rect.intersects(checkbox.geometry()):
    #             #         checkbox.setChecked(True)
    #             #     else:
    #             #         checkbox.setChecked(False)
    #     else:
    #         super(MyListWidget, self).mouseMoveEvent(event)

    # def mouseReleaseEvent(self, event):
    #     super(MyListWidget, self).mouseReleaseEvent(event)
    #     if event.button() == QtCore.Qt.LeftButton:
    #         self.start_pos = None 


    


class ProcessTab(QtGui.QWidget):    
    def __init__(self, 
                process_key,
                SIGNAL_MANAGER,
                parent = None):
        super(ProcessTab, self).__init__(parent)
#        self.tab_tmp = QtGui.QWidget()
        self.parent = parent
        # self.setObjectName = process_key
        self.verticalLayout_5 = QtGui.QVBoxLayout(self) 

        self.listWidget = MyListWidget(SIGNAL_MANAGER)
        self.listWidget.setObjectName = process_key
        self.listWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.verticalLayout_5.addWidget(self.listWidget)

        self.on_parent_privilage_changed()
        self.listWidget.itemClicked.connect(self.item_clicked)
        SIGNAL_MANAGER.privilage_changed.connect(self.on_parent_privilage_changed) 
        self.listWidget.currentItemChanged.connect(self.item_changed) 



    def item_changed(self,cur_item, pre_item):
        if isinstance(pre_item, QtGui.QListWidgetItem):
            frame = self.listWidget.itemWidget(pre_item)
            frame.unselect()
        
        # if isinstance(cur_item, QtGui.QListWidgetItem):
        #     frame = self.listWidget.itemWidget(cur_item)
        #     frame.clicked()
        
        

        
    def item_clicked(self, cur_item):
        if isinstance(cur_item, QtGui.QListWidgetItem):
            frame = self.listWidget.itemWidget(cur_item)
            frame.select() 
    #     qss = """
    #     QFrame {
    #             padding :4px;
    #             border :2px solid #d9d9d9;
    #             border-radius : 3px;
    #             background-color : #4db0e9;
    #             font-size : 8pt;
    #             font-weight: bold;
    #             }
    #     """
    #     frame.setStyleSheet(qss)

    # def mousePressEvent(self, event):
    #     if event.button() == QtCore.Qt.LeftButton :
    #         current_widget = self.currentWidget()
    #         if isinstance(current_widget, QtGui.QListWidget):
    #             print('i am list widget : '  + str(current_widget.ObjectName()))
    #         # self.listWidget.clearSelection()
    #     QtGui.QListWidget.mousePressEvent(self, event)

    def on_parent_privilage_changed(self):
        if self.parent.privilage != 'User': 
            # self.listWidget.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
            self.listWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        else: 
            self.listWidget.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)