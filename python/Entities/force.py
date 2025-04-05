import configparser
import os
import numpy as np
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Arrow import Arrow

# Создаём парсер
config = configparser.ConfigParser()

# Читаем файл
config.read(os.getcwd() + "/python/config.ini")

def setting(key):
    return config['DEFAULT'].get(key)


class Force:
    def __init__(self, point: Point, direction: Vector):
        self.point = point
        self.direction = direction
        self.force = np.linalg.norm(self.direction.asList())
        self.primitives = []


    def __str__(self):
        return f"Point: {self.point}, Direction: {self.direction}, Force: {self.force}"

    def __repr__(self):
        print(f"Point: {self.point}, Direction: {self.direction}, Force: {self.force}")
        
    def geometry(self):
        self.primitives.append(Arrow(self.point.asList(), (self.point+self.direction).asList(), eval(setting("ForceColor")), 5))
        return self.primitives