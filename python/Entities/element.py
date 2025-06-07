
from Geometry.Primitives.Entity import Entity
from Geometry.Primitives.Line import Line
from Geometry.Point import Point
from .node import Node
from .object import Object

from config import config

class Element(Object):
    def __init__(self, id, start_node:Node, end_node:Node):
        super().__init__(id)
        self.start_node:Node = start_node
        self.end_node:Node = end_node
        
        self.make_ctrlPoints()
                
    def make_ctrlPoints(self):
        self.ctrlPoints = []
        self.ctrlPoints.append(Point())
        self.ctrlPoints.append(Point(1, 0))

    def __str__(self):
        return f"Id: {self.id}, Start node: {self.start_node}, End node: {self.end_node}"

    def __repr__(self):
        return self.__str__()

    def geometry(self):
        self.primitives.clear()

        # Трансляция
        self.ctrlPoints[0] = self.start_node.direction
        self.ctrlPoints[1] = self.end_node.direction
        
        self.primitives.append(Line(self.ctrlPoints[0].asList(), self.ctrlPoints[1].asList(), color=eval(config("LineColor")), thickness=5))
        return self.primitives

    def serialize(self):
        return {"id": self.id, "start_node": self.start_node.id, "end_node": self.end_node.id}