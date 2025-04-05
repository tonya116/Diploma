
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __add__(self, other):
        tmp = Vector(self.x, self.y, self.z)
        tmp.x += other.x
        tmp.y += other.y
        tmp.z += other.z
        return tmp
    
    def asList(self):
        return [self.x, self.y, self.z]