from PyQt4.QtGui import QListWidget, QApplication, QFrame, QMessageBox
from PyQt4.QtCore import Qt, QObject

class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super(CustomListWidget, self).__init__(parent)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.MouseButtonPress and event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            if item and isinstance(self.itemWidget(item), QFrame):
                QMessageBox.information(self, "Mouse Press Event", "Mouse Pressed on item: " + item.text())
                return True
        return super(CustomListWidget, self).eventFilter(obj, event)

# Usage
app = QApplication([])
list_widget = CustomListWidget()
list_widget.setDragDropMode(QListWidget.InternalMove)

# Add items to the list
frame1 = QFrame()
# frame1.setText("Frame 1")
list_widget.addItem("Item 1")
list_widget.setItemWidget(list_widget.item(0), frame1)

frame2 = QFrame()
# frame2.setText("Frame 2")
list_widget.addItem("Item 2")
list_widget.setItemWidget(list_widget.item(1), frame2)

list_widget.show()
app.exec_()