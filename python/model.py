import json
import math
from dearpygui import dearpygui as dpg
from force import Force
from node import Node
from element import Element

class Model:
    def __init__(self):

        self.x_rot = 0
        self.y_rot = 0
        self.z_rot = 0
        
        self.scale = 1
        
        self.data = ""
        self.nodes = []
        self.elements = []
        self.materials = {}
        self.forces = []
        self.boundary_conditions = []

        self.name = None
        
        self.draw_node_id = dpg.generate_uuid()

        self.model_matrix = (
            
            dpg.create_translation_matrix([1900//2, 900//2])
            * dpg.create_rotation_matrix(math.radians(self.x_rot), [1, 0, 0])
            * dpg.create_rotation_matrix(math.radians(self.y_rot), [0, 1, 0])
            * dpg.create_rotation_matrix(math.radians(self.z_rot), [0, 0, 1])
            * dpg.create_scale_matrix([self.scale, self.scale, self.scale]) 
        )

    def rotate_x(self, angle):
        self.x_rot += angle

    def rotate_y(self, angle):
        self.y_rot += angle

    def rotate_z(self, angle):
        self.z_rot += angle

    def load_model(self, filename:str):
        self.name = filename.split("/")[-1][:-4]
        with open(filename, "r", encoding="utf-8-sig") as file:
            self.data = json.load(file)
        self.__parse_model()

    def __parse_model(self):
        # TODO Надо бы переписать передачу имени файла

        for node in self.data.get("nodes"):
            self.nodes.append(Node(node.get("id"), node.get("coordinates")))

        for element in self.data.get("elements"):
            self.elements.append(
                Element(
                    element.get("id"),
                    element.get("start_node"),
                    element.get("end_node"),
                    element.get("type"),
                    element.get("material"),
                )
            )

        self.loads = self.data.get("loads")
        for load in self.data.get("loads"):
            if load.get("type") == "force":
                self.forces.append(
                    Force(self.nodes[load.get("node")].point, load.get("values"))
                )
        self.boundary_conditions = self.data.get("boundary_conditions")

        print(
            self.nodes,
            self.elements,
            self.materials,
            self.loads,
            self.boundary_conditions,
            sep="\n",
        )

    def update(self):
        self.model_matrix = (
            
            dpg.create_translation_matrix([1900//2, 900//2])
            * dpg.create_rotation_matrix(math.radians(self.x_rot), [1, 0, 0])
            * dpg.create_rotation_matrix(math.radians(self.y_rot), [0, 1, 0])
            * dpg.create_rotation_matrix(math.radians(self.z_rot), [0, 0, 1])
            * dpg.create_scale_matrix([self.scale, self.scale, self.scale]) 
        )
        dpg.apply_transform(
            self.draw_node_id,  self.model_matrix
        )


    def get_model_matrix(self):
        return self.model_matrix
    
    def set_scale(self, scale:float):
        self.scale = scale
        
    def get_scale(self):
        return self.scale