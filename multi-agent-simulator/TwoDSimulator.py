import numpy as np
from numpy import random
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


NumAgents=10
WorldDimension = 100

agent_coordinates1 = WorldDimension*(random.rand(2,NumAgents)-0.5)
agent_coordinates2 = WorldDimension*(random.rand(2,NumAgents)-0.5)
coordinates = [agent_coordinates1, agent_coordinates2]

pg.setConfigOptions(antialias=True)
app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
win = pg.GraphicsWindow(title='Simulation environment')
win.resize(800,800)

p1 = win.addPlot()
p1.setRange(xRange=[-50,50],yRange=[-50,50])
data = coordinates
ptr = 0
def update():
    global points, data, ptr
    p1.clear()
    points = pg.ScatterPlotItem(x=data[ptr%2][0], y=data[(ptr)%2][1],
                                pen=pg.mkPen(None), symbolBrush=(255, 255, 255, 120), 
                                size=1, pxMode=False)
    p1.addItem(points)
    ptr += 1
    
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(250)
QtGui.QApplication.instance().exec_()