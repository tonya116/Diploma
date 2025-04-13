
from Geometry.Matrix import *
from .prop import Support

import numpy as np
from .node import Node
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Line import Line
from Geometry.Primitives.Circle import Circle
from config import config

class Pinned(Support):
    def __init__(self, id:int, node:Node, direction: Vector):
        super().__init__(id, node, direction)
        self.dof = 2

        self.primitives = []
        self.ctrlPoints:list[Point] = []
        
        self.ctrlPoints.append(Point(0, 0, 0))
        self.ctrlPoints.append(Point(-1, 1, 0))
        self.ctrlPoints.append(Point(1, 1, 0))

        self.ctrlPoints.append(Point(-2, 1, 0))
        self.ctrlPoints.append(Point(2, 1, 0))
        for i in range(-1, 3):
            self.ctrlPoints.append(Point(i, 1, 0))
            self.ctrlPoints.append(Point(i-1, 2, 0))
            
    def geometry(self):
        mt = TranslationMatrix(self.node.point)
        mr = RotationMatrix(-3.1415/2)
        for i in range(len(self.ctrlPoints)):
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mr
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mt
            
        self.primitives.append(Circle(self.ctrlPoints[0].asList(), 5, eval(config("SupportColor")), 5))
        self.primitives.append(Circle(self.ctrlPoints[0].asList(), 3, (255, 255, 255), 5))
        self.primitives.append(Line(self.ctrlPoints[0].asList(), self.ctrlPoints[1].asList(), eval(config("SupportColor")), 5))
        self.primitives.append(Line(self.ctrlPoints[0].asList(), self.ctrlPoints[2].asList(), eval(config("SupportColor")), 5))

        for i in range(3, len(self.ctrlPoints), 2):
            self.primitives.append(Line(self.ctrlPoints[i].asList(), self.ctrlPoints[i+1].asList(), eval(config("SupportColor")), 5))
        
        return self.primitives