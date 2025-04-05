import configparser
import os

import numpy as np
from Geometry.Point import Point
from Geometry.QBezier import QBezier
from Geometry.Vector import Vector

# Создаём парсер
config = configparser.ConfigParser()

# Читаем файл
config.read(os.getcwd() + "/python/config.ini")

def setting(key):
    return config['DEFAULT'].get(key)


class Momentum:
    def __init__(self, element, offset: float, direction: Vector):
        self.element = element
        self.offset = offset
        self.direction = direction
        self.force = np.linalg.norm(self.direction.asList())
        self.primitives = []

    def __str__(self):
        return f"Element: {self.element}, Direction: {self.direction}, Momentum: {self.force}"

    def __repr__(self):
        print(f"Element: {self.element}, Direction: {self.direction}, Momentum: {self.force}")

    def geometry(self):
        radius = 2
        t = self.element.end_node.point - self.element.start_node.point
        ort = Vector()
        if self.force > 0:
            ort = t / t.norm()

        self.primitives.append(
            QBezier(
                (self.element.start_node.point + ort * self.offset + Point(0, -radius, 0)).asList(),
                (self.element.start_node.point + ort * self.offset + Point(radius, 0, 0)).asList(),
                (self.element.start_node.point + ort * self.offset + Point(0, radius, 0)).asList(),
                2,
                eval(setting("ForceColor")),
                5,
        ))

        return self.primitives