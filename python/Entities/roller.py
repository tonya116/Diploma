
from Geometry.Point import Point
from Geometry.Primitives.Circle import Circle
from Geometry.Primitives.Line import Line
from Geometry.Vector import Vector
from config import config
from Geometry.Matrix import *
from .node import Node
from .prop import Support


class Roller(Support):
    def __init__(self, id: int, node: Node, direction: Vector):
        super().__init__(id, node, direction)
        self.dof = 1
        self.make_ctrlPoints()

    def make_ctrlPoints(self):
        self.ctrlPoints = []
        self.rotation = RotationMatrix(self.direction.angle())
        self.transformation = TranslationMatrix(self.node.direction)
        self.scale = ScaleMatrix(0.5)

        self.ctrlPoints.append(Point())
        self.ctrlPoints.append(Point(0, 1))
        n = 2

        self.ctrlPoints.append(Point(-n, 1))
        self.ctrlPoints.append(Point(n, 1))
        for i in range(-n // 2, n + 1):
            self.ctrlPoints.append(Point(i, 1))
            self.ctrlPoints.append(Point(i - 1, 2))
        self.ctrlPoints = self.apply_transformation(self.ctrlPoints)

    def geometry(self):
        self.primitives.clear()

        self.primitives.append(
            Circle(self.ctrlPoints[0].asList(), 5, eval(config("SupportColor")), 5)
        )
        self.primitives.append(Circle(self.ctrlPoints[0].asList(), 3, (255, 255, 255), 5))
        self.primitives.append(
            Line(
                self.ctrlPoints[0].asList(),
                self.ctrlPoints[1].asList(),
                eval(config("SupportColor")),
                5,
        ))

        for i in range(2, len(self.ctrlPoints), 2):
            self.primitives.append(
                Line(
                    self.ctrlPoints[i].asList(),
                    self.ctrlPoints[i + 1].asList(),
                    eval(config("SupportColor")),
                    5,
            ))

        return self.primitives

    def serialize(self):
        return {
            "id": self.id,
            "node": self.node.id,
            "type": "roller",
            "direction": self.direction.serialize(),
        }