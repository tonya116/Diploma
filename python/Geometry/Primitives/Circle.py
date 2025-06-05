from Geometry.Primitives.Entity import Entity
from Geometry.Vector import Vector

class Circle(Entity):
    def __init__(self, center, radius, color, thickness):
        super().__init__(center, [], color, thickness)
        
        self.radius = radius

    def translate(self, point:Vector):
        self.pos = point

    def __deepcopy__(self, _):
        return Circle(self.pos, self.radius, self.color ,self.thickness)