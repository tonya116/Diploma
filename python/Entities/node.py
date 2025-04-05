import configparser
import os
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Circle import Circle

# Создаём парсер
config = configparser.ConfigParser()

# Читаем файл
config.read(os.getcwd() + "/python/config.ini")

def setting(key):
    return config['DEFAULT'].get(key)


class Node:

    def __init__(self, id, point:Point):
        self.id = id
        self.point = point
        self.primitives = []
        
    def __repr__(self):
        return f"ID: {self.id}, point: {self.point}"
    
    def geometry(self):
        self.primitives.append(Circle(self.point.asList(), 5, eval(setting("NodeColor")), 5))
        return self.primitives