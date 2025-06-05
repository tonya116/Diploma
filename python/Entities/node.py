
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Circle import Circle
from config import config
from Geometry.Matrix import TranslationMatrix
from .object import Object
from pydantic import BaseModel
from typing import Dict, Any


class NodeModel(BaseModel):
    id: int  # или str, в зависимости от типа вашего id
    coordinates: list[float]  # или создайте отдельную модель для Point

class Node(Object):
    def __init__(self, id, point:Point):
        super().__init__(id)
        self.point:Point = point
        self.ctrlPoints.append(Point())
        self.interest_points.append(Point())
        
        self.transformation = TranslationMatrix(self.point)

    def __str__(self):
        return f"ID: {self.id}, Point: {self.point}"
    
    def __repr__(self):
        return self.__str__()
    
    def __dict__(self):
        return {"id": self.id, "coordinates": self.point.__dict__()}
    
    def geometry(self):
        self.primitives.clear()
        self.ctrlPoints = self.apply_transformation(self.ctrlPoints)
        
        self.primitives.append(Circle(self.ctrlPoints[0].asList(), 5, eval(config("NodeColor")), 5))

        return self.primitives
    
    def to_pydantic(self) -> 'NodeModel':
        return NodeModel(**self.__dict__())
    
    @classmethod
    def from_pydantic(cls, node_model: 'NodeModel'):
        # Предполагая, что Point может быть создан из словаря coordinates
        point = Point(*node_model.coordinates)
        return cls(node_model.id, point)

    def __deepcopy__(self, _):
        return Node(self.id, self.point)