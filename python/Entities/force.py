import numpy as np
from Geometry.Vector import Vector
from Geometry.Point import Point


class Force:
    def __init__(self, point: Point, direction: Vector):
        self.point = point
        self.direction = direction
        self.force = np.linalg.norm(self.direction.asList())


    def __str__(self):
        return f"Point: {self.point}, Direction: {self.direction}, Force: {self.force}"

    def __repr__(self):
        print(f"Point: {self.point}, Direction: {self.direction}, Force: {self.force}")