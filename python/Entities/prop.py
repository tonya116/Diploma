import numpy as np
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Entity import Entity
from config import config
from Entities.node import Node
from .object import Object

class Support(Object):
    def __init__(self, id:int, node:Node, direction: Vector):
        super().__init__(id)
        self.node = node
        self.direction = direction

    def __str__(self):
        return f"Node: {self.node}, Direction: {self.direction}"

    def __repr__(self):
        return self.__str__()
         
    def __dict__(self):
        return {"node": self.node.id, "direction": self.direction.__dict__}
    
    def __deepcopy__(self, _):
        return Support(self.id, self.node, self.direction)