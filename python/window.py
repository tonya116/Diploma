import ctypes
import math
import os
from typing import Any

from dearpygui import dearpygui as dpg
import numpy as np
from model import Model
from Geometry.Primitives.Circle import Circle
from Geometry.Primitives.Line import Line
from Geometry.Primitives.Arrow import Arrow
from Geometry.Primitives.QBezier import QBezier
from config import config
from Geometry.Vector import Vector
from Entities.node import Node
from Entities.element import Element
from Entities.fixed import Fixed
from Entities.pinned import Pinned
from Entities.roller import Roller
from Entities.force import Force
from Entities.distributed_force import DistributedForce
from Entities.momentum import Momentum
from Entities.diagrams import Diagram

W = int(config("WIDTH"))
H = int(config("HEIGHT"))
DEFAULT = True

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

            # self.current_model.set_pos(Vector(dx/2 - W//2, dy/2 - H//2, 0))

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
                        
                        # dpg.draw_line(p1=[screen_x + 500, screen_y + 500], p2=p, color=eval(config("LineColor")), thickness=2)

                # Получаем экранные координаты (w=1, поэтому деление не нужно)
                screen_x = transformed[0] + W//8
                screen_y = transformed[1] + H//4
                print(f"Point {i} (id={node.id}): model={node.point}, screen=({screen_x}, {screen_y})")
                
            #     # Вычисляем расстояние до курсора
            #     distance = ((screen_x - mouse_pos[0])**2 + (screen_y - mouse_pos[1])**2)**0.5
                
            #     if distance < threshold and distance < min_distance:
            #         min_distance = distance
            #         closest_node = node
            
            # if closest_node:
            #     return closest_node.id
            # else:
            #     return None
        
    def mouse_wheel_handler(self, sender, app_data, user_data):
        if self.current_model:
            self.current_model.set_scale(self.current_model.get_scale() * (1.5**app_data))

    def draw_diagrams(self, diagrams):
                # Добавляем новую вкладку в tab_bar
        with dpg.tab(label=self.current_model.name, parent="tab_bar"):
            # Добавляем область для рисования (drawlist) на этой вкладке
            with dpg.drawlist(width=W, height=H, tag=self.drawlist_id):
                with dpg.draw_layer( parent=self.drawlist_id, tag=self.draw_layer_id):
                    with dpg.draw_node(parent=self.draw_layer_id, tag=self.current_model.draw_node_id) as f:
                        for prim in diagrams:
                            if isinstance(prim, Circle):
                                dpg.draw_circle(center=prim.pos, radius=prim.radius, color=prim.color, thickness=prim.thickness)
                            elif isinstance(prim, Line):
                                dpg.draw_line(prim.p1, prim.p2, color=prim.color, thickness=prim.thickness)

    # Функция для отрисовки модели
    def draw_model(self):
        
        if not self.current_model:
            return
        
        self.current_model.update()
        
        for key, val in self.current_model.data.items():
            for object in val:
                for prim in object.geometry():
                    if isinstance(prim, Arrow):
                        dpg.draw_arrow(prim.p1, prim.p2, color=prim.color, thickness=prim.thickness, size = 1)
                    elif isinstance(prim, Circle):
                        dpg.draw_circle(center=prim.pos, radius=prim.radius, color=prim.color, thickness=prim.thickness)
                    elif isinstance(prim, Line):
                        dpg.draw_line(prim.p1, prim.p2, color=prim.color, thickness=prim.thickness)
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

        L = 6  # длина балки, м
        dx = 0.01

        x = np.arange(0, L + dx, dx)
        
        # --- Нагрузки ---
        point_loads = [[4, -30]]  # (позиция, сила в кН)
        distributed_loads = [[0, 2, -10]]   # (от, до, q кН/м)
        moments = [[2, 20]]                # (позиция, момент в кН·м), отриц — по часовой

        # Загружаем библиотеку
        lib = ctypes.CDLL('build/src/libcalculations.so')

        # Определяем типы аргументов и возвращаемого значения
        lib.diagram_calc.argtypes = [
            ctypes.c_double,                       # L
            np.ctypeslib.ndpointer(dtype=np.float64),  # x
            ctypes.c_size_t,                    # size
            np.ctypeslib.ndpointer(dtype=np.float64),  # V
            np.ctypeslib.ndpointer(dtype=np.float64)   # M
        ]
        lib.diagram_calc.restype = None
        
        # Подготавливаем массивы для результатов
        V = np.zeros(x.size, dtype=np.float64)
        M = np.zeros(x.size, dtype=np.float64)
        # Вызываем функцию
        lib.diagram_calc(L, x, x.size, V, M)
                
        diag = Diagram(-1, self.current_model.data.get("nodes")[0], self.current_model.data.get("nodes")[1], V)
        diag2 = Diagram(0, self.current_model.data.get("nodes")[0], self.current_model.data.get("nodes")[1], M)

        self.draw_diagrams(diag.geometry() + diag2.geometry())

        s = sum(V) * dx
        print(s)
            

        
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
            dpg.add_file_extension(".mdl", color=(255, 0, 255), custom_text="[model]")

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
                    with dpg.draw_node(parent=self.draw_layer_id, tag=self.current_model.draw_node_id) as f:
                        self.current_model.set_pos(Vector(W//8, H//4, 0))
                        self.draw_model()
                        
        dpg.delete_item("file_dialog_id")

    def _build_editable_tree(self, parent: str, data: Any, path: str = ""):
        """Рекурсивное построение дерева с элементами редактирования"""
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                if isinstance(value, (dict, list)):
                    with dpg.tree_node(label=key, parent=parent):
                        self._build_editable_tree(parent, value, new_path)
                else:
                    self._add_editable_field(parent, key, value, new_path)

        elif isinstance(data, list):
            for idx, item in enumerate(data):
                new_path = f"{path}[{idx}]"
                if isinstance(item, (dict, list)):
                    with dpg.tree_node(label=f"Item {item.index}", parent=parent):
                        self._build_editable_tree(parent, item, new_path)
                else:
                    self._add_editable_field(parent, item, new_path)

    def _add_editable_field(self, parent: str, value: Any, path: str):
        """Добавление поля с возможностью редактирования"""
        with dpg.group(horizontal=True, parent=parent):
            if isinstance(value, Node):
                with dpg.group(horizontal=True):
                    dpg.add_text(f"{value.__class__.__name__} #{value.id}:")

                    for i, num in enumerate(value.point.asList()):
                        dpg.add_input_float(
                            default_value=num,
                            tag=f"{path}[{i}]",
                            width=100,
                            callback=self._update_data
                        )
                        
            elif isinstance(value, Element):
                with dpg.group(horizontal=True):
                    dpg.add_text(f"{value.__class__.__name__} #{value.id}:")
                    with dpg.group(horizontal=False):
                        dpg.add_text(f"Start Node:")

                        dpg.add_input_int(
                            default_value=value.start_node.id,
                            # tag=f"Element.{value.id}.start_node.id",
                            width=150,
                            callback=self._update_data
                        )
                        dpg.add_text(f"End Node:")

                        dpg.add_input_int(
                            default_value=value.end_node.id,
                            tag=f"{path}",
                            width=150,
                            callback=self._update_data
                        )
                        dpg.add_text(f"Material:")

                        dpg.add_input_text(
                            default_value=str(value.material),
                            # tag=path,
                            width=200,
                            callback=self._update_data
                        )
                        
            elif isinstance(value, (Fixed, Roller, Pinned)):
                with dpg.group(horizontal=True):
                    dpg.add_text(f"{value.__class__.__name__} #{value.id}:")
                    with dpg.group(horizontal=False):
                        dpg.add_text(f"Node:")

                        dpg.add_input_int(
                            default_value=value.node.id,
                            # tag=f"{path}",
                            width=150,
                            callback=self._update_data
                        )
                        dpg.add_text(f"Direction:")
                        with dpg.group(horizontal=True):
                            for i, num in enumerate(value.direction.asList()):
                                dpg.add_input_float(
                                    default_value=num,
                                    # tag=f"{path}[{i}]",
                                    width=150,
                                    callback=self._update_data
                                )
            elif isinstance(value, (Force, Momentum)):
                with dpg.group(horizontal=True):
                    dpg.add_text(f"{value.__class__.__name__} #{value.id}:")
                    with dpg.group(horizontal=False):
                        dpg.add_text(f"Node:")

                        dpg.add_input_int(
                            default_value=value.node.id,
                            # tag=f"{path}",
                            width=150,
                            callback=self._update_data
                        )
                        dpg.add_text(f"Direction:")
                        with dpg.group(horizontal=True):
                            for i, num in enumerate(value.direction.asList()):
                                dpg.add_input_float(
                                    default_value=num,
                                    # tag=f"{path}[{i}]",
                                    width=150,
                                    callback=self._update_data
                                )
            elif isinstance(value, DistributedForce):
                with dpg.group(horizontal=True):
                    dpg.add_text(f"{value.__class__.__name__} #{value.id}:")
                    with dpg.group(horizontal=False):
                        dpg.add_text(f"Node:")

                        dpg.add_input_int(
                            default_value=value.node.id,
                            # tag=f"{path}",
                            width=150,
                            callback=self._update_data
                        )
                        dpg.add_text(f"Direction:")
                        with dpg.group(horizontal=True):
                            for i, num in enumerate(value.direction.asList()):
                                dpg.add_input_float(
                                    default_value=num,
                                    # tag=f"{path}[{i}]",
                                    width=150,
                                    callback=self._update_data
                                )
                                
                        dpg.add_text(f"Lenght:")
                        dpg.add_input_float(
                            default_value=value.lenght,
                            # tag=f"{path}",
                            width=150,
                            callback=self._update_data
                        )
    
    def _update_data(self, sender, app_data):
        """Обновление данных при изменении значений"""
        print(sender)
        print(app_data)
        path = sender
        try:
            # Находим нужный элемент в структуре данных
            keys = path.split('.')
            current = self.current_model.data
            
            for key in keys[:-1]:
                if '[' in key:
                    # Обработка индексов массивов
                    base = key.split('[')[0]
                    idx = int(key.split('[')[1].rstrip(']'))
                    current = current[base][idx]
                else:
                    current = current[key]
            
            # Устанавливаем новое значение
            last_key = keys[-1]
            if '[' in last_key:
                base = last_key.split('[')[0]
                idx = int(last_key.split('[')[1].rstrip(']'))
                current[base][idx] = app_data
            else:
                current[last_key] = app_data

        except Exception as e:
            print(f"Error updating {path}: {e}")
       
    def _save_to_file(self, sender, app_data, user_data:str = ""):
        """Сохранение данных в файл"""
        self.current_model.save_to_file(user_data)
       
    def setup(self):
        # Основное окно
        with dpg.window(label="Build v0.0.6", tag="main_window", width=W, height=H):
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="Open", callback=self.create_file_dialog)
                    dpg.add_menu_item(label="Save", callback=self._save_to_file, user_data="")
                    dpg.add_menu_item(label="Save As", callback=self._save_to_file)

                with dpg.menu(label="Calculate"):
                    dpg.add_menu_item(label="Run", callback=self.calculate)
                    
            with dpg.group(horizontal=True):

                # Левый блок — Канвас
                with dpg.child_window(width=W//2, height=H):
                    # Вкладки для переключения моделей
                    with dpg.tab_bar(tag="tab_bar", callback=self.tab_change_callback):
                        if DEFAULT: # исключительно в тестовых целях
                            self.current_model = Model()
                            self.current_model.load_model("/home/denour/Develop/Diplom/models/model3.mdl")
                            self.models.update({self.current_model.name: self.current_model})
                            self.create_tab(self.current_model.name)
                        
                # Правый блок — Инспектор
                # Inspector()
                with dpg.child_window(width=W//1, height=H):
                    self._build_editable_tree("##dynamic_tree_root", self.current_model.data)
                    
                dpg.add_text("Inspector")
                dpg.add_text("Selected Node:", tag="node_id_text")
                dpg.add_input_int(label="X", tag="x_coord", callback=self.callback)
                dpg.add_input_int(label="Y", tag="y_coord", callback=self.callback)
        # Регистрируем шрифт
        with dpg.font_registry():
            # Первый параметр - размер, второй - путь к файлу шрифта
            default_font = dpg.add_font("/home/denour/Develop/cpp/fps/assets/font/arial.ttf", 16)

        # Устанавливаем шрифт по умолчанию для всех элементов
        dpg.bind_font(default_font)
        
        with dpg.handler_registry():
            # dpg.add_mouse_double_click_handler(callback=self.mouse_double_click_handler)

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