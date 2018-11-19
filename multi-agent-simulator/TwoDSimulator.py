import numpy as np
from numpy import random
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from DataGenerator import DataGenerator
from Boids import Boids

# NumAgents=10
# WorldDimension = 100

# agent_coordinates1 = WorldDimension*(random.rand(2,NumAgents)-0.5)
# agent_coordinates2 = WorldDimension*(random.rand(2,NumAgents)-0.5)
# coordinates = [agent_coordinates1, agent_coordinates2]

generator = Boids()
generator.initialize_boids()

pg.setConfigOptions(antialias=True)
app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
win = pg.GraphicsWindow(title='Simulation environment')
win.resize(800,800)

p1 = win.addPlot()
p1.setRange(xRange=[-50,50],yRange=[-50,50])
data = generator.all_positions
ptr = 0
def update():
    global points, points1, data, ptr
    p1.clear()
    data = generator.update_boids()
    rogue_index = 100
    points = pg.ScatterPlotItem(x=data[rogue_index:,0], y=data[rogue_index:,1],
                                pen=pg.mkPen(None), #symbolBrush=((255,100,100)), 
                                size=0.25, pxMode=False)
    points1 = pg.ScatterPlotItem(x=data[0:rogue_index,0], y=data[0:rogue_index,1],
                                pen=pg.mkPen(None), #symbolBrush=('b'), 
                                size=0.5, pxMode=False)
    points.setBrush(QtGui.QBrush(QtGui.QColor(100,100,255)))
    points1.setBrush(QtGui.QBrush(QtGui.QColor(255,0,0)))
    p1.addItem(points)
    p1.addItem(points1)
    ptr += 1

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)
QtGui.QApplication.instance().exec_()