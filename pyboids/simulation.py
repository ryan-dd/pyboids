import numpy as np
from numpy import random
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

from pyboids.boids_model import Boids


boids = Boids()

pg.setConfigOptions(antialias=True)
app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
win = pg.GraphicsWindow(title='Simulation environment')
win.resize(800,800)

p1 = win.addPlot()
p1.setRange(xRange=[-20,20],yRange=[-20,20])
data = boids.all_positions
ptr = 0
def update():
    global points, data, ptr
    p1.clear()
    data = boids.update_boids()
    points = pg.ScatterPlotItem(x=data[:,0], y=data[:,1],
                                pen=pg.mkPen(None), symbolBrush=(255, 255, 255, 120), 
                                size=0.1, pxMode=False)
    p1.addItem(points)
    ptr += 1

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)
QtGui.QApplication.instance().exec_()
