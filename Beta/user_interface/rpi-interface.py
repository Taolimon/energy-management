import sys
import time
import csv
import numpy as np

import matplotlib.pyplot  as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qtagg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget, QLabel, QToolBar, QVBoxLayout
)

class MainWindow(QMainWindow):

    # Graph variables
    # fig = plt.figure()
    # ax1 = fig.add_subplot(1,1,1)

    def __init__(self):
        super().__init__()
        self._main = QWidget()
        self.setCentralWidget(self._main)
        layout = QVBoxLayout(self._main)

        # static_canvas = FigureCanvas(Figure(figsize=(5,3)))
        toolbar = QToolBar("Graph View")
        # layout.addWidget(NavigationToolbar(static_canvas, self))

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        layout.addWidget(NavigationToolbar(dynamic_canvas, self))

        # self._static_ax = static_canvas.figure.subplots()
        x_axis = [0, 1]
        y_axis = [0, 1]
        # self._static_ax.plot(x_axis, y_axis)

        

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._line, = self._dynamic_ax.plot(x_axis, y_axis)
        self._timer = dynamic_canvas.new_timer(1000)
        self._timer.add_callback(self.animate)
        self._timer.start()

        self.setWindowTitle("Monitoring")

        self.show()


    def onToolBarButtonClick(self, s):
        print("clicked", s)

    def animate(self):
        graph_data = open("Beta\\user_interface\\graph\\graph_data.csv", 'r').read()
        lines = graph_data.split('\n')
        x_axis = []
        y_axis = []
        for line in lines:
            if len(line) > 1:
                measured_time, lux = line.split(',')
                x_axis.append(float(measured_time))
                y_axis.append(float(lux))
                # print("MT " + str(float(measured_time)))
                # print("LUX " + str(float(lux)))

        print("LUX " + str(x_axis))
        self._line.set_data(x_axis, y_axis)
        self._line.figure.canvas.draw()

        # t = np.linspace(0, 10, 101)
        # # Shift the sinusoid as a function of time.
        # self._line.set_data(t, np.sin(t + time.time()))
        # self._line.figure.canvas.draw()
        return
    
    # Animation variables
    # ani = animation.FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
    # plt.show()


if __name__ == "__main__":
    # Every qt program must have an app
    # Check if there is an instance already running
    qapp = QApplication.instance()
    if not qapp:
        qapp = QApplication(sys.argv)


    window = MainWindow()
    window.show()
    window.activateWindow()
    window.raise_()

    # Adds a test button
    # window = MainWindow()
    # window.show()

    # Starts the event loop
    qapp.exec()