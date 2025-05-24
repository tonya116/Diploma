

from Geometry.Point import Point
from Geometry.Primitives.Entity import Entity


class Object:
    def __init__(self, id: int = -1):
        self.id = id
        self.primitives:list[Entity] = []
        self.ctrlPoints:list[Point] = []
        
    def __dict__(self):
        return {"id": self.id}