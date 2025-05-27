
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Arrow import Arrow
from Geometry.Primitives.Line import Line
from config import config
from Geometry.Matrix import RotationMatrix, TranslationMatrix
from .node import Node

from .load import Load
class DistributedForce(Load):
    def __init__(self, id:int, node:Node, direction: Vector, lenght: float):
        super().__init__(id, node, direction)

        self.lenght = lenght

        self.ctrlPoints.append(Point(-self.lenght/2, -2))
        self.ctrlPoints.append(Point(self.lenght/2, -2))
        
        n = 4
        step = self.lenght/n
        for i in range(-n//2, n//2+1):
            self.ctrlPoints.append(Point(i * step, 0))
            self.ctrlPoints.append(Point(i * step, -2))
            
    def __str__(self):
        return f"Element: {self.node}, Direction: {self.direction}, Lenght: {self.lenght}, Force: {self.force}"

    def __repr__(self):
        return self.__str__()

         
    def __dict__(self):
        return {"lenght": self.lenght}
    
    def geometry(self):
        self.primitives.clear()

        mt = TranslationMatrix(self.node.point)
        mr = RotationMatrix()
        for i in range(len(self.ctrlPoints)):
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mr
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mt
            
        self.primitives.append(Line(self.ctrlPoints[0].asList(), self.ctrlPoints[1].asList(), eval(config("ForceColor")), 5))

        for i in range(2, len(self.ctrlPoints), 2):
            self.primitives.append(Arrow(self.ctrlPoints[i].asList(), self.ctrlPoints[i+1].asList(), eval(config("ForceColor")), 1))

        return self.primitives