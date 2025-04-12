
from Geometry.Primitives.Entity import Entity
from Geometry.Primitives.Line import Line
from config import config

class Element:
    def __init__(self, id, start_node, end_node, type, material):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.type = type
        self.material = material
        self.primitives = []

    def __str__(self):
        return f"Id: {self.id}, Start node: {self.start_node}, End node: {self.end_node}, Type: {self.type}, Material: {self.material}"

    def __repr__(self):
        print(self.__str__())
        
    def geometry(self):
        self.primitives.append(Line(self.start_node.point.asList(), self.end_node.point.asList(), color=eval(config("LineColor")), thickness=5))
        return self.primitives