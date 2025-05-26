
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

        n = 2
        self.ctrlPoints.append(Point(-n, 0))
        self.ctrlPoints.append(Point(n, 0))
        for i in range(-n//2, n+1):
            self.ctrlPoints.append(Point(i, 0))
            self.ctrlPoints.append(Point(i-1, 1))

    def geometry(self):
        self.primitives.clear()

        mt = TranslationMatrix(self.node.point)
        for i in range(len(self.ctrlPoints)):
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mt

        for i in range(0, len(self.ctrlPoints), 2):
            self.primitives.append(Line(self.ctrlPoints[i].asList(), self.ctrlPoints[i+1].asList(), eval(config("SupportColor")), 5))
        
        return self.primitives