import ctypes
import math
import os

from dearpygui import dearpygui as dpg
from model import Model
import configparser
import numpy as np
from Geometry.Circle import Circle
from Geometry.Line import Line
from Geometry.Arrow import Arrow
from Geometry.QBezier import QBezier

def invert_matrix(mat):
    """Инвертирование 4x4 матрицы, представленной как flat list"""
    # Для ортогональной матрицы можно использовать упрощенный метод
    # (транспонирование вращения и инвертирование перемещения)
    
    # Разбираем матрицу на компоненты
    print(type(mat))
    # for i in mat:
    #     print(i)
        
    # m = []
    # for i in mat:
    #     t = []
    #     for j in i:
    #         t.append(j)
    #     m.append(t)
        
        
        
    # m = [mat[i*4:(i+1)*4] for i in range(4)]
    
    # Вычисляем обратную матрицу вращения (транспонирование)
    inv_rot = [
        [m[0][0], m[1][0], m[2][0], 0],
        [m[0][1], m[1][1], m[2][1], 0],
        [m[0][2], m[1][2], m[2][2], 0],
        [0, 0, 0, 1]
    ]
    
    # Вычисляем обратное перемещение
    inv_trans = [
        [1, 0, 0, -m[3][0]],
        [0, 1, 0, -m[3][1]],
        [0, 0, 1, -m[3][2]],
        [0, 0, 0, 1]
    ]
    
    # Комбинируем (умножаем матрицы)
    result = [0]*16
    for i in range(4):
        for j in range(4):
            for k in range(4):
                result[i*4+j] += inv_rot[i][k] * inv_trans[k][j]
    
    return result

# Создаём парсер
config = configparser.ConfigParser()

# Читаем файл
config.read(os.getcwd() + "/python/config.ini")

def setting(key):
    return config['DEFAULT'].get(key)

W = int(setting("WIDTH"))
H = int(setting("HEIGHT"))

class Window:
    def __init__(self):
        
        self.current_model: Model = None
        self.models: dict = {}
        self.isDragging = False
        
        # Настройка интерфейса
        dpg.create_context()
        dpg.create_viewport(title="C++ & Python Calculation", width=W, height=H)
        dpg.setup_dearpygui()

    def key_down_handler(self, sender, app_data, user_data):
        if not self.current_model:
            return
        
        if app_data == dpg.mvKey_LShift:
            self.current_model.rotate_x(1)
        if app_data == dpg.mvKey_ModCtrl:
            self.current_model.rotate_x(-1)

        if app_data == dpg.mvKey_W:
            self.current_model.rotate_y(1)
        if app_data == dpg.mvKey_S:
            self.current_model.rotate_y(-1)

        if app_data == dpg.mvKey_A:
            self.current_model.rotate_z(1)
        if app_data == dpg.mvKey_D:
            self.current_model.rotate_z(-1)            


        if app_data == dpg.mvKey_Q:
            self.current_model.x = self.current_model.x - 30
        if app_data == dpg.mvKey_E:
            self.current_model.x = self.current_model.x + 30

    def mouse_drag_handler(self, sender, app_data, user_data):
        
        if self.current_model:
            
            dx, dy = dpg.get_mouse_drag_delta()
            self.current_model.rotate_x(dx/100)
            self.current_model.rotate_y(dy/100)

    def mouse_double_click_handler(self, sender, app_data, user_data):
        if self.current_model and app_data == dpg.mvMouseButton_Left:
            mouse_pos = dpg.get_drawing_mouse_pos()
            # mouse_pos[0] -= self.current_model.get_pos()[0]
            # mouse_pos[1] -= self.current_model.get_pos()[1]

            # Рисуем круг в месте клика для визуальной обратной связи
            with dpg.draw_layer(parent=self.drawlist_id, tag=self.draw_layer_id):
                with dpg.draw_node(parent=self.draw_layer_id):
                    dpg.draw_circle(mouse_pos, 5, color=(255, 255, 0), fill=(255, 255, 0))
            # print(type(self.current_model.get_model_matrix()))

            # Получаем матрицу преобразования (модель * проекция)
            # model_matrix = self.current_model.get_model_matrix()
            
            # print(model_matrix)
            model_matrix = (
            # dpg.create_lookat_matrix([1, 0, 0], [1, 0, 0.1], [0, 1, 0])
            dpg.create_translation_matrix([self.current_model.x+100000, self.current_model.y])
            * dpg.create_rotation_matrix(math.radians(self.current_model.x_rot), [1, 0, 0])
            * dpg.create_rotation_matrix(math.radians(self.current_model.y_rot), [0, 1, 0])
            * dpg.create_rotation_matrix(math.radians(self.current_model.z_rot), [0, 0, 1])
            * dpg.create_scale_matrix([self.current_model.scale, self.current_model.scale, self.current_model.scale]) 
        
        )
            transform = model_matrix#  * dpg.create_rotation_matrix(3.1415/2, [0, 1, 0])
            print(f"Mouse position: {mouse_pos}")
            
            closest_node = None
            min_distance = float('inf')
            threshold = 10  # Пороговое расстояние для попадания
            
            for i, node in enumerate(self.current_model.nodes):
                
                # Преобразуем точку модели в однородные координаты
                point = dpg.mvVec4(*node.point, 1.0)
                
                # Применяем преобразование (ортогональное, без перспективы)
                transformed = point * transform
                screen_x = transformed[0]
                screen_y = transformed[1]
                
                # Рисуем круг для визуальной обратной связи
                with dpg.draw_layer(parent=self.drawlist_id, tag=self.draw_layer_id):
                    with dpg.draw_node(parent=self.draw_layer_id):
                        dpg.draw_circle([screen_x + W//8, screen_y + H//4], 5, color=(0, 255, 0), fill=(0, 255, 0))
                        
                        # p = [0, 0]
                        # if i + 1 < len(self.current_model.nodes) :
                        #     n = self.current_model.nodes[i+1]
                        #     y = dpg.mvVec4(*n.point, 1.0)
                        #     q = y * transform
                        #     p[0] = q[0] + W//8
                        #     p[1] = q[1] + H//4
                        
                        # dpg.draw_line(p1=[screen_x + 500, screen_y + 500], p2=p, color=eval(setting("LineColor")), thickness=2)

# Получаем экранные координаты (w=1, поэтому деление не нужно)
                screen_x = transformed[0] + W//8
                screen_y = transformed[1] + H//4
                

                print(f"Point {i} (id={node.id}): model={node.point}, screen=({screen_x}, {screen_y})")
                
                # Вычисляем расстояние до курсора
                distance = ((screen_x - mouse_pos[0])**2 + (screen_y - mouse_pos[1])**2)**0.5
                
                if distance < threshold and distance < min_distance:
                    min_distance = distance
                    closest_node = node
            
            if closest_node:
                return closest_node.id
            else:
                return None
        
    def mouse_wheel_handler(self, sender, app_data, user_data):
        if self.current_model:
            self.current_model.set_scale(self.current_model.get_scale() * (1.5**app_data))

    # Функция для отрисовки модели
    def draw_model(self):
        
        if not self.current_model:
            return
        
        self.current_model.update()
        drawables = [self.current_model.elements, self.current_model.nodes, self.current_model.supports, self.current_model.forces, self.current_model.distributed_forces]
        
        for drawable in drawables:
            for object in drawable:
                for prim in object.geometry():
                    if isinstance(prim, Circle):
                        dpg.draw_circle(prim.center, radius=prim.radius, color=prim.color, thickness=prim.thickness)
                    elif isinstance(prim, Line):
                        dpg.draw_line(prim.p1, prim.p2, color=prim.color, thickness=prim.thickness)
                    elif isinstance(prim, Arrow):
                        dpg.draw_arrow(prim.p1, prim.p2, color=prim.color, thickness=prim.thickness, size = 1)
                    elif isinstance(prim, QBezier):
                        dpg.draw_bezier_quadratic(prim.p1, prim.p2, prim.p3, color=prim.color, thickness=prim.thickness)
                        
                
    def select_open_file_cb(self, sender, app_data, user_data):
        self.current_model = Model()
        self.current_model.load_model(app_data.get("file_path_name"))
        self.models.update({self.current_model.name: self.current_model})
        self.create_tab(self.current_model.name)

    # Функция для проверки активного таба
    def tab_change_callback(self, sender, app_data, user_data):
        self.current_model = self.models[app_data]
        print(f"Active tab: {app_data}")

    def calculate(self):

        # Путь к скомпилированной C++ библиотеке
        lib_path = os.path.join(os.path.dirname(__file__), "../build/src/libcalculations.so")
        calculations = ctypes.CDLL(lib_path)

        calculations.createMatrix.argtypes = [ctypes.c_int, ctypes.c_int]
        calculations.createMatrix.restype = ctypes.c_void_p

        calculations.destroyMatrix.argtypes = [ctypes.c_void_p]

        calculations.getDeterminant.argtypes = [ctypes.c_void_p]

        mat = calculations.createMatrix(5, 5)
        print(mat)
        # Создаем массив данных

    def callback(self, sender, app_data, user_data):
        print("Sender: ", sender)
        print("App Data: ", app_data)
        print("User Data: ", user_data)

    def create_file_dialog(self):
        with dpg.file_dialog(
            directory_selector=False,
            callback=self.select_open_file_cb,
            id="file_dialog_id",
            width=700,
            height=400,
        ):
            dpg.add_file_extension(".mdl", color=(255, 0, 255, 255), custom_text="[model]")

    def create_tab(self, model_name):

        # Создаем уникальный идентификатор для вкладки и холста
        tab_id = dpg.generate_uuid()
        self.drawlist_id = dpg.generate_uuid()
        self.draw_layer_id = dpg.generate_uuid()
        # Добавляем новую вкладку в tab_bar
        with dpg.tab(label=model_name, parent="tab_bar", tag=tab_id):
            # Добавляем область для рисования (drawlist) на этой вкладке
            with dpg.drawlist(width=W, height=H, tag=self.drawlist_id):
                with dpg.draw_layer( parent=self.drawlist_id, tag=self.draw_layer_id):
                    with dpg.draw_node(parent=self.draw_layer_id, tag=self.current_model.draw_node_id):
                        self.current_model.set_pos([W//8, H//4])
                        self.draw_model()
                        
        dpg.delete_item("file_dialog_id")

    def setup(self):
        # Основное окно
        with dpg.window(label="Build v0.0.4", tag="main_window", width=W, height=H):
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="Open", callback=self.create_file_dialog)

                with dpg.menu(label="Calculate"):
                    dpg.add_menu_item(label="Run", callback=self.calculate)
                    
            with dpg.group(horizontal=True):

                # Левый блок — Канвас
                with dpg.child_window(width=W//1, height=H):
                    # Вкладки для переключения моделей
                    with dpg.tab_bar(tag="tab_bar", callback=self.tab_change_callback):
                        pass

                # Правый блок — Инспектор
                with dpg.child_window(width=W//2, height=H):
                    dpg.add_text("Inspector")
                    dpg.add_text("Selected Node:", tag="node_id_text")
                    dpg.add_input_int(label="X", tag="x_coord", callback=self.callback)
                    dpg.add_input_int(label="Y", tag="y_coord", callback=self.callback)

        with dpg.handler_registry():
            dpg.add_mouse_double_click_handler(callback=self.mouse_double_click_handler)

            dpg.add_mouse_drag_handler(callback=self.mouse_drag_handler, button=dpg.mvMouseButton_Left)
            dpg.add_mouse_wheel_handler(callback=self.mouse_wheel_handler)
            # dpg.add_key_down_handler(callback=self.key_down_handler)
            dpg.add_key_press_handler(callback=self.key_down_handler)
        dpg.set_primary_window("main_window", True)


    def run(self):
        
        self.setup()
        
        dpg.show_viewport()
        
        while dpg.is_dearpygui_running():
            if self.current_model:
                self.current_model.update()

            dpg.render_dearpygui_frame()

        dpg.destroy_context()