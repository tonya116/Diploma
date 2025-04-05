import configparser
import os

from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Arrow import Arrow
from Geometry.Line import Line

# Создаём парсер
config = configparser.ConfigParser()

# Читаем файл
config.read(os.getcwd() + "/python/config.ini")

def setting(key):
    return config['DEFAULT'].get(key)

class DistributedForce:
    def __init__(self, element, offset: float, direction: Vector, lenght: float):
        self.element = element
        self.offset = offset
        self.direction = direction
        self.lenght = lenght
        self.force = self.direction.norm()
        self.primitives = []

    def __str__(self):
        return f"Point: {self.point}, Direction: {self.direction}, Force: {self.force}, Lenght: {self.lenght}"

    def __repr__(self):
        print(f"Point: {self.point}, Direction: {self.direction}, Force: {self.force}")
        
    def geometry(self):
        
        N = 5
        t = self.element.end_node.point - self.element.start_node.point
        print(f"Distributed Force : {t}")
        ort = Vector()
        if self.force > 0:
            ort = t / t.norm()
        
        DFPoint = ort * self.offset
        step = self.lenght/(N + 1) 
        force_vector = self.direction
        for i in range(N):
            u = (step * i - self.offset/2)
            at = DFPoint + ort * u + self.element.start_node.point
            self.primitives.append(Arrow(at.asList(), (at + force_vector).asList(), eval(setting("ForceColor")), 2))
        self.primitives.append(Line((self.element.start_node.point + DFPoint + force_vector + (ort * (-self.lenght/2))).asList(), (self.element.start_node.point + DFPoint + force_vector + (ort * self.lenght/2)).asList(), eval(setting("ForceColor")), 2))

        return self.primitives