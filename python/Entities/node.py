
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Circle import Circle
from config import config
from Geometry.Matrix import TranslationMatrix
from .object import Object

class Node(Object):
    def __init__(self, id, point:Point):
        super().__init__(id)
        self.point = point
        self.primitives = []
        self.ctrlPoints:list[Point] = [Point()]

    def __str__(self):
        return f"ID: {self.id}, Point: {self.point}"
    
    def __repr__(self):
        print(self.__str__())
    
    def geometry(self):
        mt = TranslationMatrix(self.point)
        for i in range(len(self.ctrlPoints)):
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mt
        self.primitives.append(Circle(self.ctrlPoints[0].asList(), 5, eval(config("NodeColor")), 5))

        return self.primitives