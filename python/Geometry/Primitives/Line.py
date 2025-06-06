from Geometry.Primitives.Entity import Entity
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Matrix import Matrix

class Line(Entity):
    def __init__(self, p1:Point, p2:Point, color, thickness):
        super().__init__(color=color, thickness=thickness)
        self.p1 = p1
        self.p2 = p2
        self.r = [Point(), Point(1, 0)]
        
    def __str__(self):
        return f"Line: p1={self.p1}, p2={self.p2}"
    
    def __repr__(self):
        return self.__str__()
