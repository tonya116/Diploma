
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Arrow import Arrow
from Geometry.Primitives.Line import Line
from config import config
from Geometry.Matrix import RotationMatrix, TranslationMatrix
from .node import Node
from .element import Element

class DistributedForce:
    def __init__(self, node:Node, direction: Vector, lenght: float):
        self.node: Node = node
        self.direction = direction
        self.lenght = lenght
        self.force = self.direction.norm()
        self.primitives = []
        self.ctrlPoints:list[Point] = []
        self.ctrlPoints.append(Point(-self.lenght/2, -2, 0))
        self.ctrlPoints.append(Point(self.lenght/2, -2, 0))
        
        n = 4
        step = self.lenght/4
        for i in range(-2, 3):
            self.ctrlPoints.append(Point(i * step, 0, 0))
            self.ctrlPoints.append(Point(i * step, -2, 0))
            
    def __str__(self):
        return f"Element: {self.element}, Offset: {self.offset}, Direction: {self.direction}, Lenght: {self.lenght}, Force: {self.force}"

    def __repr__(self):
        print(self.__str__())
        
    def geometry(self):

        mt = TranslationMatrix(self.node.point)
        mr = RotationMatrix(3.1415/2)
        for i in range(len(self.ctrlPoints)):
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mr
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mt
            print(self.ctrlPoints[i])
            
        self.primitives.append(Line(self.ctrlPoints[0].asList(), self.ctrlPoints[1].asList(), eval(config("ForceColor")), 5))

        for i in range(2, len(self.ctrlPoints), 2):
            self.primitives.append(Arrow(self.ctrlPoints[i].asList(), self.ctrlPoints[i+1].asList(), eval(config("ForceColor")), 1))

        return self.primitives