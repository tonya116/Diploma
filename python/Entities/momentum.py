
import numpy as np
from Geometry.Point import Point
from Geometry.Primitives.QBezier import QBezier
from Geometry.Vector import Vector
from Geometry.Matrix import TranslationMatrix
from .node import Node

from config import config

class Momentum:
    def __init__(self, id:int, node:Node, direction: Vector):
        self.id = id
        self.node: Node = node
        self.direction = direction
        self.force = np.linalg.norm(self.direction.asList())
        self.primitives = []
        self.ctrlPoints:list[Point] = [Point(0, -2, 0), Point(4, 0, 0), Point(0, 2, 0)]

    def __str__(self):
        return f"Node: {self.node}, Direction: {self.direction}, Momentum: {self.force}"

    def __repr__(self):
        print(self.__str__())

    def geometry(self):

        mt = TranslationMatrix(self.node.point)
        for i in range(len(self.ctrlPoints)):
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mt
                    
        self.primitives.append(QBezier(self.ctrlPoints[0].asList(), self.ctrlPoints[1].asList(), self.ctrlPoints[2].asList(), 2, eval(config("ForceColor")), 5))

        return self.primitives