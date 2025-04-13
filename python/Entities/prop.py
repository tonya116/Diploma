import numpy as np
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Entity import Entity
from config import config
from Entities.node import Node

class Support:
    def __init__(self, id:int, node:Node, direction: Vector):
        self.id = id
        self.node = node
        self.direction = direction

    def __str__(self):
        return f"Node: {self.node}, Direction: {self.direction}"

    def __repr__(self):
        print(self.__str__())