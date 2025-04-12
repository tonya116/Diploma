
from .prop import Support

import numpy as np
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Line import Line
from config import config

class Fixed(Support):
    def __init__(self, node:int, direction: Vector):
        super().__init__(node, direction)
        self.primitives = []

    def geometry(self):
        
        self.primitives.append(Line((self.node.point-self.direction *5 ).asList(), (self.node.point+self.direction * 5).asList(), eval(config("SupportColor")), 5))
        for i in range(-4, 5):
            self.primitives.append(Line((self.node.point + self.direction * i).asList(), (self.node.point+self.direction*(i-1) + Point(0, 1, 0)).asList(), eval(config("SupportColor")), 5))

        return self.primitives