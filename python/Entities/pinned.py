
import math
from Geometry.Matrix import *
from .prop import Support

import numpy as np
from .node import Node
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Line import Line
from Geometry.Primitives.Circle import Circle
from config import config

class Pinned(Support):
    def __init__(self, id:int, node:Node, direction: Vector):
        super().__init__(id, node, direction)
                
        self.transformation = TranslationMatrix(self.node.point)
        self.rotation = RotationMatrix(self.direction.angle())
        self.scale = ScaleMatrix(0.5)
        
        self.dof = 2
        
        self.ctrlPoints.append(Point(0, 0))
        self.ctrlPoints.append(Point(-1, 1))
        self.ctrlPoints.append(Point(1, 1))
        n = 2
        self.ctrlPoints.append(Point(-n, 1))
        self.ctrlPoints.append(Point(n, 1))
        for i in range(-n//2, n+1):
            self.ctrlPoints.append(Point(i, 1))
            self.ctrlPoints.append(Point(i-1, 2))
        self.ctrlPoints = self.apply_transformation(self.ctrlPoints)
            
    def geometry(self):
        self.primitives.clear()

        
        self.primitives.append(Circle(self.ctrlPoints[0].asList(), 5, eval(config("SupportColor")), 5))
        self.primitives.append(Circle(self.ctrlPoints[0].asList(), 3, (255, 255, 255), 5))
        self.primitives.append(Line(self.ctrlPoints[0].asList(), self.ctrlPoints[1].asList(), eval(config("SupportColor")), 5))
        self.primitives.append(Line(self.ctrlPoints[0].asList(), self.ctrlPoints[2].asList(), eval(config("SupportColor")), 5))

        for i in range(3, len(self.ctrlPoints), 2):
            self.primitives.append(Line(self.ctrlPoints[i].asList(), self.ctrlPoints[i+1].asList(), eval(config("SupportColor")), 5))
        
        return self.primitives
    
    def serialize(self):
        return {"id": self.id, "node": self.node.id, "type": "pinned", "direction": self.direction.serialize()}