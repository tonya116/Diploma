import numpy as np

class Vector:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
        
    def __add__(self, other):
        tmp = Vector(self.x, self.y, self.z)
        tmp.x += other.x
        tmp.y += other.y
        tmp.z += other.z
        return tmp
    
    def __mul__(self, scalar):
        tmp = Vector(self.x, self.y, self.z)
        tmp.x *= scalar
        tmp.y *= scalar
        tmp.z *= scalar
        return tmp
    
    def __truediv__(self, scalar):
        tmp = Vector(self.x, self.y, self.z)
        tmp.x /= scalar
        tmp.y /= scalar
        tmp.z /= scalar
        return tmp
    
    def __gt__(self, scalar):
        return self.norm() > scalar
    
    def __str__(self):
        return f"Vector: x={self.x}, y={self.y}, z={self.z}"
    
    def __repr__(self):
        print(self.__str__())
    
    def cross(self, other):
        """Векторное произведение (кросс-произведение) с другим вектором."""
        new_x = self.y * other.z - self.z * other.y
        new_y = self.z * other.x - self.x * other.z
        new_z = self.x * other.y - self.y * other.x
        return Vector(new_x, new_y, new_z)
        
    def norm(self) -> float:
        return np.linalg.norm(self.asList())
    
    def asList(self):
        return [self.x, self.y, self.z]