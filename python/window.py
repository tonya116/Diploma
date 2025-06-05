import ctypes
import json
import math
import os
from typing import Any

from dearpygui import dearpygui as dpg
from matplotlib import pyplot as plt
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
from calculations import Calculations
from Geometry.Matrix import Matrix
from tab import Tab
from data.data import Sortament


W = int(config("WIDTH"))
H = int(config("HEIGHT"))
DEFAULT = True

def mult(a1, a2, index):
    return a1[index] * a2[index]


E = 2e11  # модуль упругости (Па)
I = 0.00_000_255  # момент инерции (м^4)

sigma = 180e6

class Window:
    def __init__(self):
        
        self.current_model: Model = None
        self.calc: Calculations = Calculations()
        self.models: dict = {}
        self.tabs: dict = {}
        self.isDragging:bool = False
        self.sortament = Sortament()

        self.factor = 30

        # Настройка интерфейса
        dpg.create_context()
        dpg.create_viewport(title="C++ & Python Calculation", width=W, height=H)
        dpg.setup_dearpygui()

    def key_down_handler(self, sender, app_data, user_data):
        if not self.current_model:
            return

        if app_data == dpg.mvKey_Q:
            self.current_model.move(Vector(30, 0))
        if app_data == dpg.mvKey_E:
            self.current_model.move(Vector(-30, 0))

    def mouse_drag_handler(self, sender, app_data, user_data):
        if self.current_model:
            f = Vector(*dpg.get_mouse_pos()) 
            current_pos = self.current_model.get_pos()
            # self.current_model.set_pos(f + (f - current_pos))

    def mouse_double_click_handler(self, sender, app_data, user_data):
        if self.current_model and app_data == dpg.mvMouseButton_Left:
            mouse_pos = Vector(*dpg.get_drawing_mouse_pos()) - Vector(W//4, H//2)
            print(f"Mouse position: {mouse_pos}")

            dpg.draw_circle(mouse_pos.asList(), 5, color=(255, 255, 0), fill=(255, 255, 0), parent=self.current_model.draw_node_id)


    def mouse_wheel_handler(self, sender, app_data, user_data):
        if self.current_model:
            self.factor *= 1.5 ** app_data
            self.current_model.set_scale(self.factor)
  
    def select_open_file_cb(self, sender, app_data, user_data):
        self.current_model = Model()
        self.current_model.load_model(app_data.get("file_path_name"))
        self.create_tab(self.current_model)

    # Функция для проверки активного таба
    def tab_change_callback(self, sender, app_data, user_data):
        print(f"Active tab: {app_data}")
        print(self.models)
        self.current_model = self.tabs.get(app_data).model

    def build_diagram(self, type, model: Model, start_node, end_node, diagram):
        model.diagrams.append(Diagram(1001, type, start_node, end_node, diagram, model=model))

    def apply_force(self, sup):
        
        forces = []
        
        if isinstance(sup, Fixed):
            forces.append(Force(-10, sup.node, sup.direction.ort()))
            forces.append(Force(-10, sup.node, Vector(sup.direction.ort(), 0)))
            forces.append(Momentum(-10, sup.node, sup.direction.ort()))

        elif isinstance(sup, Pinned):
            forces.append(Force(-10, sup.node, sup.direction.ort()))
            forces.append(Force(-10, sup.node, Vector(sup.direction.ort(), 0)))
        
        elif isinstance(sup, Roller):
            forces.append(Force(-10, sup.node, sup.direction.ort()))

        return forces

    def make_determinate(self):
  
        sups = self.current_model.data.get("supports")
        
        applied_sups = []
        unit_forces = []

        fixed_n = 0
        roller_n = 0
        pinned_n = 0

        for sup in sups:
            if isinstance(sup, Fixed):
                fixed_n += 1
            elif isinstance(sup, Roller):
                roller_n += 1
            elif isinstance(sup, Pinned):
                pinned_n += 1
                    
        if fixed_n == 0 and pinned_n == 0:
            raise Exception("Конструкция является механизмом")

        elif fixed_n != 0:
            for sup in sups:
                if isinstance(sup, Fixed):
                    applied_sups.append(sup)
                    break
            
            for sup in sups:
                if sup not in applied_sups:
                    unit_forces.append(*self.apply_force(sup))
            
        elif pinned_n == 1:
            for sup in sups:
                if isinstance(sup, Pinned):
                    applied_sups.append(sup)
                    
                elif isinstance(sup, Roller):
                    applied_sups.append(sup)
                    break
                
            for sup in sups:
                if sup not in applied_sups:
                    unit_forces.append(*self.apply_force(sup))
        
        elif pinned_n > 1:
            f = 0
            for sup in sups:
                if isinstance(sup, Pinned):
                    applied_sups.append(sup)
                    f = 1
                if f:
                    applied_sups.append(Roller(node=sup.node, direction=sup.direction))
                    break
            for sup in sups:
                if sup not in applied_sups:
                    unit_forces.append(*self.apply_force(sup))
                
        return applied_sups, unit_forces
        
    def calculate_bending(self, M, model: Model, area):
        model.name = "bending_diagram"
        
        minW = abs(M).max()/sigma

        I = self.sortament.find_by_Wx(minW)
        if not I:
            raise Exception("Подходящая балка не найдена по сортаменту")

        # Нормализуем
        M = M / (E * I)
        # # Интегрируем
        theta = self.calc.integrate(M)
        v = self.calc.integrate(theta)

        # Нормализация прогиба по граничным условиям
        v -= v[0]                      # обнуляем левый конец
        v -= np.linspace(0, v[-1], len(v))  # убираем наклон (вторую постоянную)

        model.get_loads().clear()
        model.get_supports().clear()

        self.build_diagram(2, model, area[0], area[1], v)
        self.create_tab(model)
        
    def calculate(self):
        
        if self.current_model.dsi < 0:
            raise Exception("DSI < 0; Something went wrong")
        elif self.current_model.dsi == 0:
            print("DSI = 0; Система статически определимая")

        else:
            print("DSI > 0; Система статически неопределима. Переходим к О.С.")
        
        dsi = self.current_model.dsi
        
        eq_models = [self.current_model.copy() for _ in range(dsi)]
        for em in eq_models:
            em.get_loads().clear()

        sups, forces = self.make_determinate()
        
        for i, em in enumerate(eq_models):
            em.get_loads().append(forces[i])
        
        base_model = self.current_model.copy()
        base_model.update_data({"supports": sups})
        
        for em in eq_models:
            em.update_data({"supports": sups})

        area = [self.current_model.get_nodes()[0], self.current_model.get_nodes()[-1]]

        M1Vb, M1Mb = self.calc.calc(base_model, sups[0], sups[1])
        self.build_diagram(0, base_model, area[0], area[1], M1Vb)
        self.build_diagram(1, base_model, area[0], area[1], M1Mb)
        base_model.name += "_diagram"

        self.create_tab(base_model)
    
        M1Ves = []
        M1Mes = []
        for i, em in enumerate(eq_models):
            M1Ve, M1Me = self.calc.calc(em, sups[0], sups[1])
            M1Ves.append(M1Ve)
            M1Mes.append(M1Me)

        for i, em in enumerate(eq_models):
            em.name = f"X{i+1}"  
            self.build_diagram(0, em, area[0], area[1], M1Ves[i]) 
            self.build_diagram(1, em, area[0], area[1], M1Mes[i]) 
            em.name += "_diagram"

            self.create_tab(em)

        A, B = self.calc.Mores_integral(len(M1Mes[0]) if M1Mes else 0, M1Mes, M1Mb)
        X = self.calc.solve(A, B*-1)
        
        print("Матрица деформаций: \n", A)
        print("Матрица деформаций от внешних нагрузок: \n", B)

        print("Найденные реакции: \n", X)
        
        result_model = base_model.copy()
        for i, em in enumerate(eq_models):
            result_model.get_loads().append(Force(-100, em.data.get("loads")[0].node, Vector(0, X[i])))
            
        result_model.name = "result_diagram"
        
        res_A, res_B = self.calc.calc(result_model, sups[0], sups[1])
        
        self.build_diagram(0, result_model, area[0], area[1], res_A)
        self.build_diagram(1, result_model, area[0], area[1], res_B)

        self.create_tab(result_model)
        
        bending_model = result_model.copy()
        
        self.calculate_bending(res_B, bending_model, area)

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

    def create_tab(self, model:Model):
        tab = Tab(model, self.factor)
        self.tabs.update({tab.tab_id:tab})
        self.models.update({model.name: model})
        self._build_editable_tree("##dynamic_tree_root1", model.data)
        return tab.tab_id

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

            elif isinstance(value, (Fixed, Roller, Pinned)):
                with dpg.group(horizontal=True):
                    dpg.add_text(f"{value.__class__.__name__} #{value.id}:")
                    with dpg.group(horizontal=False):
                        dpg.add_text(f"Node:")

                        dpg.add_input_int(
                            default_value=value.node.id,
                            width=150,
                            callback=self._update_data
                        )
                        dpg.add_text(f"Direction:")
                        with dpg.group(horizontal=True):
                            for i, num in enumerate(value.direction.asList()):
                                dpg.add_input_float(
                                    default_value=num,
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
                            width=150,
                            callback=self._update_data
                        )
                        dpg.add_text(f"Direction:")
                        with dpg.group(horizontal=True):
                            for i, num in enumerate(value.direction.asList()):
                                dpg.add_input_float(
                                    default_value=num,
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
                            width=150,
                            callback=self._update_data
                        )
                        dpg.add_text(f"Direction:")
                        with dpg.group(horizontal=True):
                            for i, num in enumerate(value.direction.asList()):
                                dpg.add_input_float(
                                    default_value=num,
                                    width=150,
                                    callback=self._update_data
                                )
                                
                        dpg.add_text(f"Lenght:")
                        dpg.add_input_float(
                            default_value=value.lenght,
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
        with dpg.window(label="Build v0.0.12", tag="main_window", width=W, height=H):
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="Open", callback=self.create_file_dialog)
                    dpg.add_menu_item(label="Save", callback=self._save_to_file)
                    dpg.add_menu_item(label="Save As", callback=self._save_to_file)

                with dpg.menu(label="Calculate"):
                    dpg.add_menu_item(label="Run", callback=self.calculate)
                    
            with dpg.group(horizontal=True):

                # Левый блок — Канвас
                with dpg.child_window(width=W//2, height=H):
                    # Вкладки для переключения моделей
                    with dpg.tab_bar(tag="tab_bar", callback=self.tab_change_callback):
                        if DEFAULT: # исключительно в тестовых целях (открывает файл при запуске)
                            self.current_model = Model()
                            self.current_model.load_model(config("DEFAULT_MODEL"))
                            self.create_tab(self.current_model)
                        
                # Правый блок — Инспектор
                # Inspector()
                with dpg.child_window(width=W, height=H):
                    self._build_editable_tree("##dynamic_tree_root", self.current_model.data)
                    
                dpg.add_text("Inspector")
                dpg.add_text("Selected Node:", tag="node_id_text")
                dpg.add_input_int(label="X", tag="x_coord", callback=self.callback)
                dpg.add_input_int(label="Y", tag="y_coord", callback=self.callback)
        # Регистрируем шрифт
        with dpg.font_registry():
            # Первый параметр - размер, второй - путь к файлу шрифта
            default_font = dpg.add_font(config("FONT"), 16)

        # Устанавливаем шрифт по умолчанию для всех элементов
        dpg.bind_font(default_font)
        
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