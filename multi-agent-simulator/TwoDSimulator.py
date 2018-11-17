import numpy as np
from numpy.linalg import eigvals, eigvalsh
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

# p1 = win.addPlot()
l = pg.GraphicsLayout()
win.setCentralItem(l)
p1 = l.addPlot(1, 1, colspan=3, rowspan=3)
p2 = l.addPlot(4,1)
p3 = l.addPlot(4,2)
p4 = l.addPlot(4,3)
# p1.setRange(xRange=[-20,20],yRange=[-20,20])
# p1.
data = generator.all_positions
p2pp = []
ptr = 0
def update():
    global points, data, ptr
    data = generator.update_boids()

    p1.clear()
    p2.clear()
    p3.clear()
    p4.clear()
    p1.scatterPlot(x=data[:,0], y=data[:,1],
                                pen=pg.mkPen(None), symbolBrush=(255, 255, 255, 205),
                                size=0.05, pxMode=False)
    p2.plot(generator.fevr)
    p3.plot(generator.fevo)
    p4.plot(generator.feva)
    # p1.addItem(l)
    ptr += 1

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)
QtGui.QApplication.instance().exec_()