
import numpy as np
from Geometry.Point import Point
from Geometry.Primitives.QBezier import QBezier
from Geometry.Vector import Vector
from Geometry.Matrix import RotationMatrix, TranslationMatrix
from Geometry.Primitives.Line import Line
from Geometry.Primitives.Arrow import Arrow
from .node import Node

from config import config
from .load import Load

class Momentum(Load):
    def __init__(self, id:int, node:Node, direction: Vector):
        super().__init__(id, node, direction)

        self.ctrlPoints.append(Point(0, -1 * direction.ort().y ))
        self.ctrlPoints.append(Point(0, 1 *  direction.ort().y ))
        self.ctrlPoints.append(Point(1, -1 * direction.ort().y ))
        self.ctrlPoints.append(Point(-1, 1 * direction.ort().y ))

    def __str__(self):
        return f"Momentum: {self.node}, Direction: {self.direction}, Momentum: {self.force}"

    def geometry(self):
        self.primitives.clear()

        mr = RotationMatrix(self.direction.angle())
        mt = TranslationMatrix(self.node.point)

        for i in range(len(self.ctrlPoints)):
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mr
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mt
        
        
        self.primitives.append(Line(self.ctrlPoints[0].asList(), self.ctrlPoints[1].asList(), eval(config("ForceColor")), 2))
        self.primitives.append(Arrow(self.ctrlPoints[3].asList(), self.ctrlPoints[1].asList(), eval(config("ForceColor")), 2))
        self.primitives.append(Arrow(self.ctrlPoints[2].asList(), self.ctrlPoints[0].asList(), eval(config("ForceColor")), 2))

        return self.primitives