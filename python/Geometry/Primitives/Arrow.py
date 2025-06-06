from Geometry.Primitives.Line import Line
from Geometry.Vector import Vector

class Arrow(Line):
    def __init__(self, p1, p2, color, thickness):
        super().__init__(p1, p2, color=color, thickness=thickness)
