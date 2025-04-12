
import configparser
import os
from Geometry.Vector import Vector
from Geometry.Point import Point

class Entity:
    def __init__(self, pos:Point = Point(), rot = [], color = (255, 255, 255), thickness:int = 1):
        self.pos = pos
        self.rot = rot
        self.color = color
        self.thickness = thickness

    