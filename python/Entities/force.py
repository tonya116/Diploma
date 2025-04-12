
import numpy as np
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Arrow import Arrow
from config import config

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
        
        self.primitives.append(Arrow(Point(), self.direction, eval(config("ForceColor")), 5))
        
        for prim in self.primitives:
            prim.translate(self.point)
        
        return self.primitives