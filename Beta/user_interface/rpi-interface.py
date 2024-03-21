import sys
import time
import csv
import matplotlib as mpl
import matplotlib.animation as animation
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget, QLabel, QToolBar
)

class MainWindow(QMainWindow):

    # Graph variables
    fig = mpl.figure()
    ax1 = fig.add_subplot(1,1,1)

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

    def animate(self, i):
        graph_data = open('graph/graph_data.csv', 'r').read()
        lines = graph_data.split('\n')
        x_axis = []
        y_axis = []
        for line in lines:
            if len(line) > 1:
                measured_time, duration = line.split(',')
                x_axis.append(float(measured_time))
                y_axis.appen(float(duration))
        self.ax1.clear()
        self.ax1.plot(x_axis, y_axis)
        return
    
    # Animation variables
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    mpl.show()


# Every qt program must have an app
app = QApplication(sys.argv)

# Adds a test button
window = MainWindow()
window.show()

# Starts the event loop
app.exec()