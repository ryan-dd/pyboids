import numpy as np
from numpy import random

class DataGenerator:

    def __init__(self):
        pass

    @staticmethod
    def random_3d_data():
        NumAgents=10
        WorldDimension = 100
        data = []
        for _ in range(1000):
            data.append(WorldDimension*(random.rand(NumAgents,3)-0.5))
        return data
