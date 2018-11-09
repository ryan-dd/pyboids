# -*- coding: utf-8 -*-
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
from numpy import random
from DataGenerator import DataGenerator

app = QtGui.QApplication([])
window = gl.GLViewWidget()
window.opts['distance'] = 100
window.show()
window.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
axis = gl.GLAxisItem()
axis.setSize(x=50,y=50,z=50)
window.addItem(axis)

data = DataGenerator.random_3d_data()

# must initialize
positions = data[0]
scatter_points = gl.GLScatterPlotItem(pos=positions, color=(1,1,1,0.5), size=1, pxMode=False)
window.addItem(scatter_points)

iteration = 0
def update(): 
    global scatter_points, positions, iteration
    scatter_points.setData(pos=data[iteration%(len(data))])
    iteration += 1
            
t = QtCore.QTimer()
t.timeout.connect(update)
t.start(250)
QtGui.QApplication.instance().exec_()
