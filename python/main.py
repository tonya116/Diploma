import ctypes
import math
import os
from dearpygui import dearpygui as dpg
from model import Model

W, H = 800, 600

model = Model()
model.load_model("models/model.mdl")
model.parse_model()
rotation_x, rotation_y = 0, 0  # Углы вращения в радианах

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

    view *= dpg.create_fps_matrix([0, 0, 0], dy, dx)


def mouse_double_click_handler(sender, app_data, user_data):

    if app_data == dpg.mvMouseButton_Left:
        for i in model.nodes:
            pass
            # if dpg.get_mouse_pos() == i[]


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


# Функция для отрисовки модели
def draw_model():
    for element in model.elements:
        # Находим начальный и конечный узлы элемента
        start_node = next(
            node for node in model.nodes if node["id"] == element["start_node"]
        )
        end_node = next(
            node for node in model.nodes if node["id"] == element["end_node"]
        )

        start_2d = start_node["coordinates"]
        end_2d = end_node["coordinates"]

        # Рисуем линию, представляющую элемент
        dpg.draw_line(p1=start_2d, p2=end_2d, color=(0, 150, 255), thickness=2)
        print(start_2d, end_2d)
    # Рисуем узлы
    for node in model.nodes:
        node_2d = node["coordinates"]
        dpg.draw_circle(node_2d, 5, color=(255, 0, 0), fill=(255, 0, 0))


def select_open_file_cb(sender, app_data, user_data):
    print(app_data)
    model.data = model.load_model(app_data.get("file_path_name"))
    print(model.data)
    dpg.show_item("tab_bar")


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


def create_file_dialog():
    with dpg.file_dialog(
        directory_selector=False,
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
            dpg.add_menu_item(label="Open", callback=create_file_dialog)

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
    # dpg.add_child_window(
    #     parent="main_window",
    #     tag="testwindow",
    #     no_move=True,
    #     modal=True,
    #     no_focus_on_appearing=True,
    #     pos=[W - 250, 0],
    #     width=250,
    #     height=H,
    # )


dpg.set_clip_space("main pass", 0, 0, W, H, -1.0, 1.0)
dpg.apply_transform("cube", proj * view * model_matrix)


with dpg.handler_registry():
    dpg.add_mouse_drag_handler(
        callback=mouse_drag_handler, button=dpg.mvMouseButton_Left
    )
    dpg.add_mouse_double_click_handler(callback=mouse_double_click_handler)

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
