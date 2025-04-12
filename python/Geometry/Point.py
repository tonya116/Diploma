from Geometry.Vector import Vector
class Point:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
        
    def __add__(self, other):
        tmp = Point(self.x, self.y, self.z)
        tmp.x += other.x
        tmp.y += other.y
        tmp.z += other.z
        return tmp
    
    def __sub__(self, other):
        tmp = Vector(self.x, self.y, self.z)
        tmp.x -= other.x
        tmp.y -= other.y
        tmp.z -= other.z
        return tmp    
    
    def __str__(self):
        return f"Point: x={self.x}, y={self.y}, z={self.z}"
    
    def __repr__(self):
        print(self.__str__())
    
    def asList(self):
        return [self.x, self.y, self.z]