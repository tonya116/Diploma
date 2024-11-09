import json
import math

# from dearpygui import dearpygui as dpg


class Model:
    def __init__(self):

        self.x_rot = 0
        self.y_rot = 0
        self.z_rot = 0
        self.data = ""

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
        print(self.data)
