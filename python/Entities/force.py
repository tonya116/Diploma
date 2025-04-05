import numpy as np

class Force:
    def __init__(self, point, direction):
        self.point = point
        self.direction = direction
        self.force = np.linalg.norm(self.direction)


    def __str__(self):
        return f"Point: {self.point}, Direction: {self.direction}, Force: {self.force}"

    def __repr__(self):
        print(f"Point: {self.point}, Direction: {self.direction}, Force: {self.force}")