from Geometry.Primitives.Entity import Entity
from Geometry.Vector import Vector

class QBezier(Entity):
    def __init__(self, p1, p2, p3, radius, color, thickness):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.radius = radius
        self.color = color
        self.thickness = thickness


    def translate(self, dir:Vector):
        offset1 = self.p1 - self.p2
        offset2 = self.p2 - self.p3
        self.p1 = dir
        self.p2 = self.p1 + offset1
        self.p3 = self.p2 + offset2