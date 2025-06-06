

from Geometry.Point import Point
from Geometry.Primitives.Entity import Entity
from Geometry.Matrix import RotationMatrix, ScaleMatrix, TranslationMatrix
from copyable import Copyable

class Object(Copyable):
    m_id = -1
    def __init__(self, id: int = -1):
        self.id = id
        self.m_id += 1
        self.primitives:list[Entity] = []
        self.ctrlPoints:list[Point] = []
        self.interest_points:list[Point] = []
        
        self.transformation = TranslationMatrix()
        self.rotation = RotationMatrix()
        self.scale = ScaleMatrix()
        
    def apply_transformation(self, list):       
        return [list[i] @ self.scale @ self.rotation @ self.transformation for i in range(len(list))]
    