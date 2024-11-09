import json
import math

# from dearpygui import dearpygui as dpg


class Model:
    def __init__(self):

        self.x_rot = 0
        self.y_rot = 0
        self.z_rot = 0
        self.data = ""
        self.nodes = []
        self.elements = []
        self.materials = {}
        self.loads = []
        self.boundary_conditions = []

    def rotate_x(self, angle):
        self.x_rot += angle

    def rotate_y(self, angle):
        self.y_rot += angle

    def rotate_z(self, angle):
        self.z_rot += angle

    def load_model(self, filename):
        with open(filename, "r", encoding="utf-8-sig") as file:
            self.data = json.load(file)

    def parse_model(self):
        self.nodes = self.data.get("nodes")
        self.elements = self.data.get("elements")
        self.materials = self.data.get("materials")
        self.loads = self.data.get("loads")
        self.boundary_conditions = self.data.get("boundary_conditions")

        print(
            self.nodes,
            self.elements,
            self.materials,
            self.loads,
            self.boundary_conditions,
            sep="\n",
        )
