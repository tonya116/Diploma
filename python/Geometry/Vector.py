import math
import numpy as np

class Vector:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        tmp = Vector(self.x, self.y)
        tmp.x += other.x
        tmp.y += other.y
        return tmp
    
    def __sub__(self, other):
        tmp = Vector(self.x, self.y)
        tmp.x -= other.x
        tmp.y -= other.y
        return tmp
    
    def __mul__(self, scalar):
        tmp = Vector(self.x, self.y)
        tmp.x *= scalar
        tmp.y *= scalar
        return tmp
    
    def __truediv__(self, scalar):
        tmp = Vector(self.x, self.y)
        tmp.x /= scalar
        tmp.y /= scalar
        return tmp
    
    def __gt__(self, scalar):
        return self.norm() > scalar
    
    def __str__(self):
        return f"Vector: x={self.x}, y={self.y}"
    
    def __repr__(self):
        return self.__str__()
    
    def cross(self, other):
        raise Exception("Not impl")
        """Векторное произведение (кросс-произведение) с другим вектором."""
        new_x = self.y * other.z - self.z * other.y
        new_y = self.z * other.x - self.x * other.z
        new_z = self.x * other.y - self.y * other.x
        return Vector(new_x, new_y, new_z)
        
    def norm(self) -> float:
        return np.linalg.norm(self.asList())
    
    def asList(self):
        return [self.x, self.y]
    
    def __complex__(self):
        return complex(self.x, self.y)
    
    def angle(self):
        t = self.__complex__()
        return math.atan(t.imag/(t.real if t.real != 0 else 1e-14)) - 3.1415/2
        
    def ort(self):
        return Vector(self.x / self.norm(), self.y / self.norm())
    
    def serialize(self):
        return self.asList()