
from Geometry.Matrix import *
from .prop import Support

import numpy as np
from .node import Node
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Line import Line
from Geometry.Primitives.Circle import Circle
from config import config

class Roller(Support):
    def __init__(self, id:int, node:Node, direction: Vector):
        super().__init__(id, node, direction)
        self.dof = 1
        
        self.ctrlPoints.append(Point())
        self.ctrlPoints.append(Point(0, 1))
        n = 2

        self.ctrlPoints.append(Point(-n, 1))
        self.ctrlPoints.append(Point(n, 1))
        for i in range(-n//2, n+1):
            self.ctrlPoints.append(Point(i, 1))
            self.ctrlPoints.append(Point(i-1, 2))
            
    def geometry(self):
        self.primitives.clear()
        
        mt = TranslationMatrix(self.node.point)
        mr = RotationMatrix()
        for i in range(len(self.ctrlPoints)):
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mr
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mt
            
        self.primitives.append(Circle(self.ctrlPoints[0].asList(), 5, eval(config("SupportColor")), 5))
        self.primitives.append(Circle(self.ctrlPoints[0].asList(), 3, (255, 255, 255), 5))
        self.primitives.append(Line(self.ctrlPoints[0].asList(), self.ctrlPoints[1].asList(), eval(config("SupportColor")), 5))

        for i in range(2, len(self.ctrlPoints), 2):
            self.primitives.append(Line(self.ctrlPoints[i].asList(), self.ctrlPoints[i+1].asList(), eval(config("SupportColor")), 5))
        
        return self.primitives