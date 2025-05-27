from Geometry.Primitives.Entity import Entity
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Matrix import Matrix

class Text(Entity):
    def __init__(self, p1:Point, text:str, color, thickness):
        super().__init__(color=color, thickness=thickness)
        self.p1 = p1
        self.text = text
        
    def __str__(self):
        return f"Text: p1={self.p1}, text={self.text}"
    
    def __repr__(self):
        return self.__str__()
