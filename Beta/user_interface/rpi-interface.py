import sys
import time
import csv
import matplotlib as mlp
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget, QLabel, QToolBar
)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Monitoring")

        label = QLabel("Toggle Toolbar")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("Graph View")
        self.addToolBar(toolbar)


    def onToolBarButtonClick(self, s):
        print("clicked", s)


# Every qt program must have an app
app = QApplication(sys.argv)

# Adds a test button
window = MainWindow()
window.show()

# Starts the event loop
app.exec()