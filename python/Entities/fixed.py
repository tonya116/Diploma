
from .prop import Support

import numpy as np
from .node import Node
from Geometry.Vector import Vector
from Geometry.Matrix import RotationMatrix, ScaleMatrix, TranslationMatrix
from Geometry.Point import Point
from Geometry.Primitives.Line import Line
from config import config

class Fixed(Support):
    def __init__(self, id, node:Node, direction: Vector):
        super().__init__(id, node, direction)
        self.dof = 3

        self.transformation = TranslationMatrix(self.node.point)
        self.rotation = RotationMatrix(self.direction.angle())
        self.scale = ScaleMatrix(0)
        n = 2
        self.ctrlPoints.append(Point(-n, 0))
        self.ctrlPoints.append(Point(n, 0))
        for i in range(-n//2, n+1):
            self.ctrlPoints.append(Point(i, 0))
            self.ctrlPoints.append(Point(i-1, 1))
        self.ctrlPoints = self.apply_transformation(self.ctrlPoints)

    def geometry(self):
        self.primitives.clear()

        for i in range(0, len(self.ctrlPoints), 2):
            self.primitives.append(Line(self.ctrlPoints[i].asList(), self.ctrlPoints[i+1].asList(), eval(config("SupportColor")), 5))
        
        return self.primitives
    
    def serialize(self):
        return {"id": self.id, "node": self.node.id, "type": "fixed", "direction": self.direction.serialize()}