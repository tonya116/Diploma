
from .prop import Support

import numpy as np
from .node import Node
from Geometry.Vector import Vector
from Geometry.Matrix import TranslationMatrix
from Geometry.Point import Point
from Geometry.Primitives.Line import Line
from config import config

class Fixed(Support):
    def __init__(self, id, node:Node, direction: Vector):
        super().__init__(id, node, direction)
        self.dof = 3

        self.primitives = []
        self.ctrlPoints:list[Point] = []
        self.ctrlPoints.append(Point(-2, 0, 0))
        self.ctrlPoints.append(Point(2, 0, 0))
        for i in range(-1, 3):
            self.ctrlPoints.append(Point(i, 0, 0))
            self.ctrlPoints.append(Point(i-1, 1, 0))

    def geometry(self):
        mt = TranslationMatrix(self.node.point)
        for i in range(len(self.ctrlPoints)):
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mt

        for i in range(0, len(self.ctrlPoints), 2):
            self.primitives.append(Line(self.ctrlPoints[i].asList(), self.ctrlPoints[i+1].asList(), eval(config("SupportColor")), 5))
        
        return self.primitives