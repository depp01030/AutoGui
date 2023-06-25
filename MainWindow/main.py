#%%
from PyQt4 import QtGui, QtCore

class DraggableFrame(QtGui.QFrame):
    def __init__(self, title):
        super(DraggableFrame, self).__init__()

        # Set the frame style
        self.setFrameStyle(QtGui.QFrame.Box)

        # Create a label to display the title
        self.titleLabel = QtGui.QLabel(title)

        # Create a QVBoxLayout as the main layout
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.titleLabel)
        layout.addStretch()

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Create a QVBoxLayout as the main layout
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        # Create the QListWidget
        self.listWidget = QtGui.QListWidget()

        # Set the selection mode to SingleSelection for easier handling
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        # Set the drag drop mode to InternalMove for reordering within the list
        self.listWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)

        # Add some draggable frames to the QListWidget
        frame1 = DraggableFrame("Frame 1")
        frame2 = DraggableFrame("Frame 2")

        item1 = QtGui.QListWidgetItem(self.listWidget)
        item1.setSizeHint(frame1.sizeHint())
        self.listWidget.setItemWidget(item1, frame1)

        item2 = QtGui.QListWidgetItem(self.listWidget)
        item2.setSizeHint(frame2.sizeHint())
        self.listWidget.setItemWidget(item2, frame2)

        # Add the QListWidget to the layout
        layout.addWidget(self.listWidget)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
# %%
