
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Arrow import Arrow
from Geometry.Matrix import RotationMatrix, TranslationMatrix
from config import config
from Entities.node import Node
from .load import Load

class Force(Load):
    def __init__(self, id: int, node:Node, direction: Vector):
        super().__init__(id, node, direction)
 
        self.ctrlPoints.append(Point())
        self.ctrlPoints.append(Point(direction.ort().x, -direction.ort().y))

    def __str__(self):
        return f"Force: {self.node}, Direction: {self.direction}, Force: {self.force}"

    def geometry(self):
        self.primitives.clear()

        mt = TranslationMatrix(self.node.point)
        mr = RotationMatrix(self.direction.angle())

        for i in range(len(self.ctrlPoints)):
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mr
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mt
                    
        self.primitives.append(Arrow(self.ctrlPoints[0].asList(), self.ctrlPoints[1].asList(), eval(config("ForceColor")), 5))

        return self.primitives