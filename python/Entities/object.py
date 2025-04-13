

from Geometry.Point import Point


class Object:
    def __init__(self, id: int = -1):
        self.id = id
        self.primitives = []
        self.ctrlPoints:list[Point] = []