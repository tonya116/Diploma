
import numpy as np
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Arrow import Arrow
from Geometry.Matrix import TranslationMatrix
from config import config
from Entities.node import Node
from .load import Load

class Force(Load):
    def __init__(self, id: int, node:Node, direction: Vector):
        super().__init__(id, node, direction)
 
        self.ctrlPoints.append(Point())
        self.ctrlPoints.append(Point(1, 0, 0))

    def __str__(self):
        return f"Node: {self.node}, Direction: {self.direction}, Force: {self.force}"

    def __repr__(self):
        print(f"Node: {self.node}, Direction: {self.direction}, Force: {self.force}")
        
    def geometry(self):
        self.primitives.clear()

        mt = TranslationMatrix(self.node.point)
        for i in range(len(self.ctrlPoints)):
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mt
                    
        self.primitives.append(Arrow(self.ctrlPoints[0], self.ctrlPoints[1], eval(config("ForceColor")), 5))

        return self.primitives