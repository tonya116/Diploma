import ctypes
import math
import os
from dearpygui import dearpygui as dpg
from model import Model

W, H = 800, 600

models = []
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

    models[0].view *= dpg.create_fps_matrix([0, 0, 0], dy, dx)


def mouse_double_click_handler(sender, app_data, user_data):
    if models:
        if app_data == dpg.mvMouseButton_Left:
            for i in models[0].nodes:
                pass
                # if dpg.get_mouse_pos() == i[]


# Настройка интерфейса
dpg.create_context()
dpg.create_viewport(title="C++ & Python Calculation", width=W, height=H)
dpg.setup_dearpygui()


# Функция для отрисовки модели
def draw_model():
    for element in models[0].elements:
        # Находим начальный и конечный узлы элемента
        start_node = next(
            node for node in models[0].nodes if node["id"] == element["start_node"]
        )
        end_node = next(
            node for node in models[0].nodes if node["id"] == element["end_node"]
        )

        start_2d = start_node["coordinates"]
        end_2d = end_node["coordinates"]

        # Рисуем линию, представляющую элемент
        dpg.draw_line(p1=start_2d, p2=end_2d, color=(0, 150, 255), thickness=2)
        print(start_2d, end_2d)
    # Рисуем узлы
    for node in models[0].nodes:
        node_2d = node["coordinates"]
        dpg.draw_circle(node_2d, 5, color=(255, 0, 0), fill=(255, 0, 0))


def select_open_file_cb(sender, app_data, user_data):
    model = Model()
    models.append(model)
    model.load_model(app_data.get("file_path_name"))

    print(model.data)
    create_tab()


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


def create_tab():

    # Создаем уникальный идентификатор для вкладки и холста
    tab_id = dpg.generate_uuid()
    drawlist_id = dpg.generate_uuid()

    # Добавляем новую вкладку в tab_bar
    with dpg.tab(label=f"Tab {tab_id}", parent="tab_bar", tag=tab_id):
        # Добавляем область для рисования (drawlist) на этой вкладке
        with dpg.drawlist(width=W, height=H, tag=drawlist_id):
            with dpg.draw_layer(
                parent=drawlist_id,
                tag="main pass",
                depth_clipping=True,
                perspective_divide=True,
                cull_mode=dpg.mvCullMode_Back,
            ):
                with dpg.draw_node(parent="main pass", tag="cube"):

                    draw_model()

    dpg.set_clip_space("main pass", 0, 0, W, H, -1.0, 1.0)
    dpg.apply_transform(
        "cube", models[0].proj * models[0].view * models[0].model_matrix
    )


# Основное окно
with dpg.window(label="Build v0.0.1", tag="main_window", width=W, height=H):

    with dpg.viewport_menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Open", callback=create_file_dialog)

    with dpg.tab_bar(tag="tab_bar"):
        pass


with dpg.handler_registry():
    dpg.add_mouse_drag_handler(
        callback=mouse_drag_handler, button=dpg.mvMouseButton_Left
    )
    dpg.add_mouse_double_click_handler(callback=mouse_double_click_handler)

dpg.set_primary_window("main_window", True)
dpg.show_viewport()
dpg.start_dearpygui()

while dpg.is_dearpygui_running():
    if models:
        models[0].update()
    dpg.render_dearpygui_frame()

dpg.destroy_context()
