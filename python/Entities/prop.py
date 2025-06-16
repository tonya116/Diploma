from Entities.node import Node
from Geometry.Vector import Vector
from .object import Object


class Support(Object):
    def __init__(self, id: int, node: Node, direction: Vector):
        super().__init__(id)
        self.node = node
        self.direction = direction

    def __str__(self):
        return f"Node: {self.node}, Direction: {self.direction}"

    def __repr__(self):
        return self.__str__()
