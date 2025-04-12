﻿
from Geometry.Primitives.Entity import Entity
from Geometry.Primitives.Line import Line
from Geometry.Point import Point
from .node import Node

from config import config

class Element:
    def __init__(self, id, start_node, end_node, type, material):
        self.id = id
        self.start_node:Node = start_node
        self.end_node:Node = end_node
        self.type = type
        self.material = material
        self.primitives = []
        self.ctrlPoints = [Point(), Point(1, 0, 0)]

    def __str__(self):
        return f"Id: {self.id}, Start node: {self.start_node}, End node: {self.end_node}, Type: {self.type}, Material: {self.material}"

    def __repr__(self):
        print(self.__str__())
        
    def geometry(self):
        # Трансляция
        self.ctrlPoints[0] = self.start_node.point
        self.ctrlPoints[1] = self.end_node.point
        
        self.primitives.append(Line(self.ctrlPoints[0].asList(), self.ctrlPoints[1].asList(), color=eval(config("LineColor")), thickness=5))
        return self.primitives