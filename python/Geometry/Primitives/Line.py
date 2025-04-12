from Geometry.Primitives.Entity import Entity
from Geometry.Vector import Vector

class Line(Entity):
    def __init__(self, p1, p2, color, thickness):
        super().__init__(color=color, thickness=thickness)
        self.p1 = p1
        self.p2 = p2

    def translate(self, dir:Vector):
        print("Arrow translate", dir, self.p1, self.p2)
        offset = self.p1 - self.p2
        self.p1 = dir
        self.p2 = self.p1 + offset