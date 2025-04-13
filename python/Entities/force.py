
import numpy as np
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Arrow import Arrow
from Geometry.Matrix import TranslationMatrix
from config import config
from Entities.node import Node
from .object import Object

class Force(Object):
    def __init__(self, id: int, node:Node, direction: Vector):
        super().__init__(id)
        self.node = node
        self.direction = direction
        self.force:float = np.linalg.norm(self.direction.asList())
        self.primitives = []
        self.ctrlPoints:list[Point] = [Point(), Point(1, 0, 0)]

    def __str__(self):
        return f"Node: {self.node}, Direction: {self.direction}, Force: {self.force}"

    def __repr__(self):
        print(f"Node: {self.node}, Direction: {self.direction}, Force: {self.force}")
        
    def geometry(self):
        mt = TranslationMatrix(self.node.point)
        for i in range(len(self.ctrlPoints)):
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mt
                    
        self.primitives.append(Arrow(self.ctrlPoints[0], self.ctrlPoints[1], eval(config("ForceColor")), 5))

        return self.primitives