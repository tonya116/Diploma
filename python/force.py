﻿import numpy as np


class Force:
    def __init__(self, point, direction):
        self.point = point
        self.direction = direction
        self.force = np.linalg.norm(self.direction)
