import math

# from dearpygui import dearpygui as dpg


class Model:
    def __init__(self):

        self.x_rot = 0
        self.y_rot = 0
        self.z_rot = 0

        # self.view = dpg.create_fps_matrix([0, 0, 50], 0.0, 0.0)
        # self.proj = dpg.create_perspective_matrix(math.pi * 45.0 / 180.0, 1.0, 0.1, 100)
        # self.model_matrix = (
        #     dpg.create_rotation_matrix(math.radians(self.x_rot), [1, 0, 0])
        #     * dpg.create_rotation_matrix(math.radians(self.y_rot), [0, 1, 0])
        #     * dpg.create_rotation_matrix(math.radians(self.z_rot), [0, 0, 1])
        # )

    def rotate_x(self, angle):
        self.x_rot += angle

    def rotate_y(self, angle):
        self.y_rot += angle

    def rotate_z(self, angle):
        self.z_rot += angle

    def update(self):
        self.model_matrix = (
            dpg.create_rotation_matrix(math.radians(self.x_rot), [1, 0, 0])
            * dpg.create_rotation_matrix(math.radians(self.y_rot), [0, 1, 0])
            * dpg.create_rotation_matrix(math.radians(self.z_rot), [0, 0, 1])
        )
        dpg.apply_transform("cube", self.proj * self.view * self.model)
