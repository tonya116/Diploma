from ast import Load
import json
import math
import os
from copy import deepcopy

from dearpygui import dearpygui as dpg
from pydantic import BaseModel
from Entities.force import Force
from Entities.distributed_force import DistributedForce
from config import config
from Entities.node import Node, NodeModel
from Entities.element import Element
from Entities.fixed import Fixed
from Entities.pinned import Pinned
from Entities.roller import Roller
from Entities.prop import Support
from Entities.momentum import Momentum

from Geometry.Vector import Vector
from Geometry.Point import Point
from Entities.diagrams import Diagram


class Model:
    def __init__(self):

        self.pos = Point()
        self.scale = 1
        
        self.data = {}
        self.dsi = -3
       
        self.name = None
        self.filename = None
        self.draw_node_id = dpg.generate_uuid()
        self.diagrams: list[Diagram] = [] 
        
    def move(self, delta: Vector):
        self.pos += delta

    def set_pos(self, point:Vector):
        self.pos = Point(*point.asList())

    def get_pos(self):
        return self.pos

    def load_model(self, filename:str):
        self.filename = filename
        # TODO Надо бы переписать передачу имени файла
        self.name = filename.split("/")[-1][:-4]        
        # Создаем экземпляр Node
        point = Point(x=10, y=20)  # предположим, что Point принимает x и y
        node = Node(id=1, point=point)
        
        # Преобразуем в Pydantic-модель и затем в JSON
        
        with open(filename, "r", encoding="utf-8-sig") as file:
            data = json.load(file)
        self.__parse_model(data)
                
        for sup in self.get_supports():
            self.dsi += sup.dof
                
    def __parse_model(self, data:dict):
        
        nodes = []
        elements = []
        loads = []
        supports = []
        for node in data.get("nodes"):
            nodes.append(Node(node.get("id"), Point(*node.get("coordinates"))))
        self.update_data({"nodes": nodes})

        for element in data.get("elements"):
            elements.append(
                Element(
                    element.get("id"),
                    self.data.get("nodes")[element.get("start_node") - 1],
                    self.data.get("nodes")[element.get("end_node") - 1],
            ))
        self.update_data({"elements": elements})

        for load in data.get("loads"):
            if load.get("type") == "force":
                loads.append(Force(load.get("id"), nodes[load.get("node")-1], Vector(*load.get("direction"))))
            elif load.get("type") == "distributed_force":
                loads.append(DistributedForce(load.get("id"), nodes[load.get("node")-1], Vector(*load.get("direction")), load.get("lenght")))
            elif load.get("type") == "momentum":
                loads.append(Momentum(load.get("id"), nodes[load.get("node")-1], Vector(*load.get("momentum"))))
        self.update_data({"loads": loads})

        for support in data.get("supports"):
            if support.get("type") == "fixed":
                supports.append(Fixed(support.get("id"), nodes[support.get("node")-1], Vector(*support.get("direction"))))
            elif support.get("type") == "pinned":
                supports.append(Pinned(support.get("id"), nodes[support.get("node")-1], Vector(*support.get("direction"))))
            elif support.get("type") == "roller":
                supports.append(Roller(support.get("id"), nodes[support.get("node")-1], Vector(*support.get("direction"))))
                
        self.update_data({"supports": supports})
        
    def get_nodes(self) -> list[Node]:
        return self.data.get("nodes")
    def get_supports(self) -> list[Support]:
        return self.data.get("supports")
    def get_elements(self) -> list[Element]:
        return self.data.get("elements")
    def get_loads(self) -> list[Load]:
        return self.data.get("loads")
        
    def update_data(self, data):
        self.data.update(data)   
                              
    def save_to_file(self, filename:str):
        print(filename)
        if not filename:
            with open(self.filename, "w") as f:
                json.dump(self.data, f, default=__dict__, indent=5)
            print(f"Write model to {self.filename}")

        else:
            with open(filename, "w") as f:
                json.dump(self.data, f, indent=4)
            print(f"Write model to {filename}")
        
    def update(self):
        self.model_matrix = (
            
            dpg.create_translation_matrix(self.pos.asList())
            * dpg.create_scale_matrix([self.scale, self.scale, self.scale]) 
        )
        dpg.apply_transform(
            self.draw_node_id, self.model_matrix
        )

    def get_model_matrix(self):
        return self.model_matrix
    
    def set_scale(self, scale:float):
        self.scale = scale
        
    def get_scale(self):
        return self.scale
    
    def copy(self):
        tmp = Model()
        tmp.pos = self.pos
        tmp.filename = self.filename
        tmp.data = deepcopy(self.data)
        tmp.name = self.name
        tmp.dsi = self.dsi
        return tmp
    