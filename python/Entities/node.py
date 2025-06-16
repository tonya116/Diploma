
from Geometry.Matrix import TranslationMatrix
from Geometry.Point import Point
from Geometry.Primitives.Circle import Circle
from config import config
from pydantic import BaseModel
from .object import Object


class NodeModel(BaseModel):
    id: int  # или str, в зависимости от типа вашего id
    coordinates: list[float]  # или создайте отдельную модель для Point

class Node(Object):
    def __init__(self, id: int, direction: Point):
        super().__init__(id)
        self.direction: Point = direction
        self.make_ctrlPoints()
        self.interest_points.append(Point())

    def make_ctrlPoints(self):
        self.ctrlPoints = []
        self.transformation = TranslationMatrix(self.direction)
        self.ctrlPoints.append(Point())
        self.ctrlPoints = self.apply_transformation(self.ctrlPoints)

    def __str__(self):
        return f"ID: {self.id}, Direction: {self.direction}"

    def __repr__(self):
        return self.__str__()

    def geometry(self):
        self.primitives.clear()

        self.primitives.append(Circle(self.ctrlPoints[0].asList(), 5, eval(config("NodeColor")), 5))

        return self.primitives

    def serialize(self):
        return {"id": self.id, "direction": self.direction.serialize()}