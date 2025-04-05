import json
import math
import os
from dearpygui import dearpygui as dpg
from Entities.force import Force
from Entities.node import Node
from Entities.element import Element
from Entities.fixed import Fixed

from Geometry.Vector import Vector
from Geometry.Point import Point


import configparser

# Создаём парсер
config = configparser.ConfigParser()

# Читаем файл
config.read(os.getcwd() + "/python/config.ini")

def setting(key):
    return config['DEFAULT'].get(key)

class Model:
    def __init__(self):

        self.x = 0
        self.y = 0

        self.x_rot = 0
        self.y_rot = 0
        self.z_rot = 0
        
        self.scale = 1
        
        self.data = ""
        self.nodes = []
        self.elements = []
        self.materials = {}
        self.forces = []
        self.supports = []

        self.name = None
        
        self.draw_node_id = dpg.generate_uuid()

        self.proj = dpg.create_orthographic_matrix(0, 1, 0, 1, 0, 1)

    def set_pos(self, point):
        self.x = point[0]
        self.y = point[1]

    def get_pos(self):
        return [self.x, self.y]

    def rotate_x(self, angle):
        self.x_rot += angle

    def rotate_y(self, angle):
        self.y_rot += angle

    def rotate_z(self, angle):
        self.z_rot += angle

    def load_model(self, filename:str):
        
        # TODO Надо бы переписать передачу имени файла

        self.name = filename.split("/")[-1][:-4]
        with open(filename, "r", encoding="utf-8-sig") as file:
            self.data = json.load(file)
        self.__parse_model()

    def __parse_model(self):

        for node in self.data.get("nodes"):
            self.nodes.append(Node(node.get("id"), Point(*node.get("coordinates"))))

        for element in self.data.get("elements"):
            self.elements.append(
                Element(
                    element.get("id"),
                    self.nodes[element.get("start_node")-1],
                    self.nodes[element.get("end_node")-1],
                    element.get("type"),
                    element.get("material"),
                )
            )

        self.loads = self.data.get("loads")
        for load in self.data.get("loads"):
            if load.get("type") == "force":
            
                self.forces.append(
                    Force(self.nodes[load.get("node")].point, Vector(*load.get("values")))
                )
                
        for support in self.data.get("supports"):
            
            self.supports.append(Fixed(self.nodes[support.get("node")-1], Vector(*support.get("direction"))))
            
        print(
            self.nodes,
            self.elements,
            self.materials,
            self.loads,
            sep="\n",
        )

    def update(self):
        self.model_matrix = (
            
            dpg.create_translation_matrix([self.x, self.y])
            * dpg.create_rotation_matrix(math.radians(self.x_rot), [1, 0, 0])
            * dpg.create_rotation_matrix(math.radians(self.y_rot), [0, 1, 0])
            * dpg.create_rotation_matrix(math.radians(self.z_rot), [0, 0, 1])
            * dpg.create_scale_matrix([self.scale, self.scale, self.scale]) 
        )
        dpg.apply_transform(
            self.draw_node_id, self.proj * self.model_matrix
        )

    def get_model_matrix(self):
        return self.model_matrix
    
    def set_scale(self, scale:float):
        self.scale = scale
        
    def get_scale(self):
        return self.scale