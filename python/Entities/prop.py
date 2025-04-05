import numpy as np
from Geometry.Vector import Vector
from Geometry.Point import Point

class Support:
    def __init__(self, node:int, direction: Vector):
        self.node = node
        self.direction = direction

    def __str__(self):
        return f"Node: {self.node}, Direction: {self.direction}"

    def __repr__(self):
        print(f"Node: {self.node}, Direction: {self.direction}")