﻿import json
import math
import os
from dearpygui import dearpygui as dpg
from Entities.force import Force
from Entities.distributed_force import DistributedForce

from Entities.node import Node
from Entities.element import Element
from Entities.fixed import Fixed
from Entities.pinned import Pinned
from Entities.roller import Roller

from Entities.momentum import Momentum

from Geometry.Vector import Vector
from Geometry.Point import Point

class Model:
    def __init__(self):

        self.x = 0
        self.y = 0

        self.x_rot = 0
        self.y_rot = 0
        self.z_rot = 0
        
        self.scale = 1
        
        self.data = {}
       
        self.name = None
        
        self.draw_node_id = dpg.generate_uuid()

        self.proj = dpg.create_orthographic_matrix(0, 1, 0, 1, 0, 1)

    def move(self, delta: Vector):
        self.x += delta.x
        self.y += delta.y

    def set_pos(self, point:Vector):
        self.x = point.x
        self.y = point.y

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
            data = json.load(file)
        self.__parse_model(data)
        
        dsd = -3
        
        for sup in self.data.get("supports"):
            if isinstance(sup, Fixed):
                dsd += 3
            elif isinstance(sup, Pinned):
                dsd += 2
            elif isinstance(sup, Roller):
                dsd += 1
        
        print(f"Степень статической неопределимости: {dsd}")
        
    def __parse_model(self, data:dict):
        print(data)
        nodes = []
        elements = []
        loads = []
        supports = []
        for node in data.get("nodes"):
            nodes.append(Node(node.get("id"), Point(*node.get("coordinates"))))
        self.data.update({"nodes": nodes})

        for element in data.get("elements"):
            elements.append(
                Element(
                    element.get("id"),
                    self.data.get("nodes")[element.get("start_node") - 1],
                    self.data.get("nodes")[element.get("end_node") - 1],
                    element.get("type"),
                    element.get("material"),
            ))
        self.data.update({"elements": elements})

        for load in data.get("loads"):
            if load.get("type") == "force":
                loads.append(Force(load.get("id"), nodes[load.get("node")-1], Vector(*load.get("direction"))))
            elif load.get("type") == "distributed_force":
                loads.append(DistributedForce(load.get("id"), nodes[load.get("node")-1], Vector(*load.get("direction")), load.get("lenght")))
            elif load.get("type") == "momentum":
                loads.append(Momentum(load.get("id"), nodes[load.get("node")-1], Vector(*load.get("momentum"))))
        self.data.update({"loads": loads})

        for support in data.get("supports"):
            if support.get("type") == "fixed":
                supports.append(Fixed(support.get("id"), nodes[support.get("node")-1], Vector(*support.get("direction"))))
            elif support.get("type") == "pinned":
                supports.append(Pinned(support.get("id"), nodes[support.get("node")-1], Vector(*support.get("direction"))))
            elif support.get("type") == "roller":
                supports.append(Roller(support.get("id"), nodes[support.get("node")-1], Vector(*support.get("direction"))))
                
        self.data.update({"supports": supports})

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