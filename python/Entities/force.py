
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Arrow import Arrow
from Geometry.Matrix import RotationMatrix, ScaleMatrix, TranslationMatrix
from config import config
from Entities.node import Node
from .load import Load

class Force(Load):
    def __init__(self, id: int, node:Node, direction: Vector):
        super().__init__(id, node, direction)
        self.make_ctrlPoints()

    def make_ctrlPoints(self):
        self.ctrlPoints = []
        self.ctrlPoints.append(Point())
        self.ctrlPoints.append(Point(self.direction.ort().x, -self.direction.ort().y))

        self.rotation = RotationMatrix(self.direction.angle())
        self.transformation = TranslationMatrix(self.node.direction)
        self.scale = ScaleMatrix()
        
        self.ctrlPoints = self.apply_transformation(self.ctrlPoints)

    def __str__(self):
        return f"Force: {self.node}, Direction: {self.direction}, Force: {self.force}"

    def geometry(self):
        self.primitives.clear()

        self.primitives.append(Arrow(self.ctrlPoints[0].asList(), self.ctrlPoints[1].asList(), eval(config("ForceColor")), 5))

        return self.primitives
    
    def serialize(self):
        return {"id": self.id, "node": self.node.id, "type": "force", "direction": self.direction.serialize()}