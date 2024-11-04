import ctypes
import math
import os
from dearpygui import dearpygui as dpg
import json
from model import Model

def print_me(sender):
    print(f"Menu Item: {sender}")


W, H = 800, 600

model = Model()

rotation_x, rotation_y = 0, 0  # Углы вращения в радианах

model_data = {}


# Обработчик для движения мыши
is_dragging = False
last_mouse_pos = (0, 0)


def mouse_drag_handler(sender, app_data, user_data):
    global is_dragging, rotation_x, rotation_y, last_mouse_pos, view

    if app_data == dpg.mvMouseButton_Left:
        is_dragging = not is_dragging  # Начало или конец перетаскивания
        last_mouse_pos = dpg.get_mouse_pos()

    current_pos = dpg.get_mouse_pos()
    # Изменение углов на основе смещения мыши
    dx, dy = current_pos[0] - last_mouse_pos[0], current_pos[1] - last_mouse_pos[1]
    dx *= 0.01
    dy *= 0.01

    last_mouse_pos = current_pos

    print(dx, dy)

    view *= dpg.create_fps_matrix([0, 0, 0], dy, dx)

    print(view)
    # dpg.apply_transform("cube", proj * view * model_matrix)


# Настройка интерфейса
dpg.create_context()
dpg.create_viewport(title="C++ & Python Calculation", width=W, height=H)
dpg.setup_dearpygui()


view = dpg.create_fps_matrix([0, 0, 50], 0.0, 0.0)
proj = dpg.create_perspective_matrix(math.pi * 45.0 / 180.0, 1.0, 0.1, 100)
model_matrix = (
    dpg.create_rotation_matrix(math.radians(model.x_rot), [1, 0, 0])
    * dpg.create_rotation_matrix(math.radians(model.y_rot), [0, 1, 0])
    * dpg.create_rotation_matrix(math.radians(model.z_rot), [0, 0, 1])
)


def load_model(filename):
    with open(filename, "r", encoding="utf-8-sig") as file:
        data = json.load(file)
    return data


# Функция для отрисовки модели
def draw_model():
    for element in model_data["elements"]:
        # Находим начальный и конечный узлы элемента
        start_node = next(
            node for node in model_data["nodes"] if node["id"] == element["start_node"]
        )
        end_node = next(
            node for node in model_data["nodes"] if node["id"] == element["end_node"]
        )

        start_2d = start_node["coordinates"]
        end_2d = end_node["coordinates"]

        # Рисуем линию, представляющую элемент
        dpg.draw_line(p1=start_2d, p2=end_2d, color=(0, 150, 255), thickness=2)

    # Рисуем узлы
    for node in model_data["nodes"]:
        node_2d = node["coordinates"]
        dpg.draw_circle(node_2d, 5, color=(255, 0, 0), fill=(255, 0, 0))


def select_open_file_cb(sender, app_data, user_data):
    global model_data
    print(app_data)
    model_data = load_model(app_data.get("file_path_name"))
    print(model_data)
    dpg.show_item("tab_bar")


model_data = load_model("models/model.mdl")


# Путь к скомпилированной C++ библиотеке
lib_path = os.path.join(os.path.dirname(__file__), "../build/src/libcalculations.so")
calculations = ctypes.CDLL(lib_path)

# Указываем типы для C++ функции
calculations.add.argtypes = [ctypes.c_double, ctypes.c_double]
calculations.add.restype = ctypes.c_double


def callback(sender, app_data, user_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)
    print("User Data: ", user_data)


with dpg.file_dialog(
    directory_selector=False,
    show=False,
    callback=select_open_file_cb,
    id="file_dialog_id",
    width=700,
    height=400,
):
    dpg.add_file_extension(".mdl", color=(255, 0, 255, 255), custom_text="[model]")


# Основное окно
with dpg.window(label="Build v0.0.1", tag="main_window", width=W, height=H):

    with dpg.viewport_menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Save", callback=print_me)
            dpg.add_menu_item(label="Save As", callback=print_me)
            dpg.add_menu_item(
                label="Open", callback=lambda: dpg.show_item("file_dialog_id")
            )
            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Setting 1", callback=print_me, check=True)
                dpg.add_menu_item(label="Setting 2", callback=print_me)

        dpg.add_menu_item(label="Help", callback=print_me)

    with dpg.tab_bar(label="tab", tag="tab_bar", show=False):
        with dpg.tab(label="Tab 1"):
            with dpg.drawlist(width=W, height=H, tag="canvas"):
                with dpg.draw_layer(
                    tag="main pass",
                    depth_clipping=True,
                    perspective_divide=True,
                    cull_mode=dpg.mvCullMode_Back,
                ):
                    with dpg.draw_node(tag="cube"):
                        draw_model()


dpg.set_clip_space("main pass", 0, 0, W, H, -1.0, 1.0)
dpg.apply_transform("cube", proj * view * model_matrix)


with dpg.handler_registry():
    dpg.add_mouse_drag_handler(
        callback=mouse_drag_handler, button=dpg.mvMouseButton_Left
    )

# dpg.start_dearpygui()
dpg.set_primary_window("main_window", True)
dpg.show_viewport()

while dpg.is_dearpygui_running():

    model_matrix = (
        dpg.create_rotation_matrix(math.radians(model.x_rot), [1, 0, 0])
        * dpg.create_rotation_matrix(math.radians(model.y_rot), [0, 1, 0])
        * dpg.create_rotation_matrix(math.radians(model.z_rot), [0, 0, 1])
    )

    dpg.apply_transform("cube", proj * view * model_matrix)

    dpg.render_dearpygui_frame()

dpg.destroy_context()
