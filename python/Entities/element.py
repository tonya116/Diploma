
# Создаём парсер
import configparser
import os
from Geometry.Line import Line

config = configparser.ConfigParser()

# Читаем файл
config.read(os.getcwd() + "/python/config.ini")

def setting(key):
    return config['DEFAULT'].get(key)

class Element:
    def __init__(self, id, start_node, end_node, type, material):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.type = type
        self.material = material
        self.primitives = []

    def geometry(self):
        self.primitives.append(Line(self.start_node.point.asList(), self.end_node.point.asList(), color=eval(setting("LineColor")), thickness=5))
        return self.primitives