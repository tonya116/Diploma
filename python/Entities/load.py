
import numpy as np
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Arrow import Arrow
from Geometry.Matrix import TranslationMatrix
from config import config
from Entities.node import Node
from .object import Object

class Load(Object):
    def __init__(self, id: int, node:Node, direction: Vector):
        super().__init__(id)
        self.node = node
        self.direction = direction
        self.force = self.direction.norm()

    def __str__(self):
        return f"Node: {self.node}, Direction: {self.direction}, Force: {self.force}"

    def __repr__(self):
        print(f"Node: {self.node}, Direction: {self.direction}, Force: {self.force}")
       