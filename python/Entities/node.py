
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Circle import Circle
from config import config

class Node:
    def __init__(self, id, point:Point):
        self.id = id
        self.point = point
        self.primitives = []
    
    def __str__(self):
        return f"ID: {self.id}, Point: {self.point}"
    
    def __repr__(self):
        print(self.__str__())
    
    def geometry(self):
        self.primitives.append(Circle(Point(), 5, eval(config("NodeColor")), 5))
        
        for prim in self.primitives:
            prim.translate(self.point)
        
        return self.primitives