import numpy as np
from calculations import Calculations
from data.data import Sortament
from model import Model
from Entities.force import Force
from Entities.diagrams import Diagram
from Entities.fixed import Fixed
from Entities.momentum import Momentum
from Entities.pinned import Pinned
from Entities.roller import Roller
from Geometry.Vector import Vector
from config import config
from Entities.node import Node
from Geometry.Point import Point
from tab import Tab
from window import Window

from dearpygui import dearpygui as dpg

DEFAULT = True

sigma = 180e6
E = 2e11  # модуль упругости (Па)

class Application:
    def __init__(self):
        self.callbacks = {
            "calculate": self.calculate,
            "create_tab": self.create_tab,
            "mouse_wheel_handler": self.mouse_wheel_handler,
            "tab_change_callback": self.tab_change_callback,
            "key_down_handler": self.key_down_handler,
            "get_active_tab": self.get_active_tab,
            "update_E": self.update_E,
            "save_file": self.save_file,
            "_update_data" : self._update_data,
        }
        self.tabs: dict = {}
        self.w = Window(self.callbacks)
        self.calc: Calculations = Calculations()
        self.sortament = Sortament()
        self.active_tab: Tab = None
        if DEFAULT: # исключительно в тестовых целях (открывает файл при запуске)
            model = Model()
            model.load_model(config("DEFAULT_MODEL"))
            self.create_tab(model)
            self.w._build_editable_tree("tree", self.active_tab.model.data)

    def run(self):
        
        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            if self.active_tab:
                self.active_tab.update_model()
            dpg.render_dearpygui_frame()
        dpg.destroy_context()
                
    def calculate(self):
        dsi = self.active_tab.model.dsi
        if dsi < 0:
            raise Exception("DSI < 0; Конструкция является механизмом")
        elif dsi == 0:
            print("DSI = 0; Система статически определима")
        else:
            print("DSI > 0; Система статически неопределима. Переходим к О.С.")
        
        eq_models = [self.active_tab.model.copy() for _ in range(dsi)]
        for em in eq_models:
            em.get_loads().clear()

        sups, forces = self.make_determinate()
        
        for i, em in enumerate(eq_models):
            em.get_loads().append(forces[i])
        
        base_model = self.active_tab.model.copy()
        base_model.name += "_diagram"
        base_model.update_data({"supports": sups})
        
        for em in eq_models:
            em.update_data({"supports": sups})

        area = [self.active_tab.model.get_nodes()[0], self.active_tab.model.get_nodes()[-1]]

        M1Vb, M1Mb = self.calc.calc(base_model, sups[0], sups[1])
        self.build_diagram(0, base_model, area[0], area[1], M1Vb)
        self.build_diagram(1, base_model, area[0], area[1], M1Mb)

        self.create_tab(base_model)
    
        M1Ves = []
        M1Mes = []
        
        for i, em in enumerate(eq_models):
            M1Ve, M1Me = self.calc.calc(em, sups[0], sups[1])
            M1Ves.append(M1Ve)
            M1Mes.append(M1Me)

        for i, em in enumerate(eq_models):
            em.name = f"X{i+1}_diagram"
            self.build_diagram(0, em, area[0], area[1], M1Ves[i])
            self.build_diagram(1, em, area[0], area[1], M1Mes[i])

            self.create_tab(em)

        A, B = self.calc.Mores_integral(len(M1Mes[0]) if M1Mes else 0, M1Mes, M1Mb)
        X = self.calc.solve(A, B*-1)
        
        print("Матрица деформаций: \n", A)
        print("Матрица деформаций от внешних нагрузок: \n", B)
        print("Найденные реакции: \n", X)
        
        self.w.add_find_loads(X)
        
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
        

    def build_diagram(self, type, model: Model, start_node, end_node, diagram):
        model.diagrams.append(Diagram(1001, type, start_node, end_node, diagram))

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
  
        sups = self.active_tab.model.data.get("supports")
        
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
        
    def create_tab(self, model:Model):
        tab = Tab(model)
        self.active_tab = tab
        self.tabs.update({tab.tab_id:tab})

    def mouse_wheel_handler(self, sender, app_data, user_data):
        if self.active_tab:
            self.active_tab.factor *= 1.5 ** app_data
            
    # Функция для проверки активного таба
    def tab_change_callback(self, sender, app_data, user_data):
        self.active_tab = self.tabs.get(app_data)
        self.w._build_editable_tree("tree", self.active_tab.model.data)

    def key_down_handler(self, sender, app_data, user_data):
            if not self.active_tab:
                return
            dx = Vector()
            # match app_data:
            #     case dpg.mvKey_Q:
            #         dx = Vector(30, 0)
            #     case dpg.mvKey_E:
            #         dx = Vector(-30, 0)
            #     case dpg.mvKey_W:
            #         dx = Vector(0, 30)
            #     case dpg.mvKey_S:
            #         dx = Vector(-30, 0)
            self.active_tab.model.move(dx)
            
    def get_active_tab(self):
        return self.active_tab
    
    def update_E(self, sender, app_data, user_data):
        E = app_data
        
    def save_file(self):
        self.active_tab.model.save_to_file()
        
    def _update_data(self, sender, app_data):
        """Обновление данных при изменении значений"""
        print(sender)
        print(app_data)
        path = sender
        try:
            # Находим нужный элемент в структуре данных
            keys = path.split('.')
            current = self.active_tab.model.data
            
            for key in keys[:-1]:
                if '[' in key:
                    # Обработка индексов массивов
                    base = key.split('[')[0]
                    idx = int(key.split('[')[1].rstrip(']'))
                    current = current[base][idx]
                else:
                    current = current.__getattribute__(key)
            
            # Устанавливаем новое значение
            last_key = keys[-1]
            if '[' in last_key:
                base = last_key.split('[')[0]
                idx = int(last_key.split('[')[1].rstrip(']'))
                # current[base][idx] = app_data

            else:
                if isinstance(current.__getattribute__(last_key), Node):
                    for node in self.active_tab.model.get_nodes():
                        if node.id == app_data:
                            current.__setattr__(last_key, node)
                            break

                elif isinstance(current.__getattribute__(last_key), (int|  float)):
                    current.__setattr__(last_key, app_data)

            for k, v in self.active_tab.model.data.items():
                for i in v:
                    i.make_ctrlPoints()
            
            self.active_tab.update_model()
            self.active_tab.draw_model()
        except Exception as e:
            print(f"Error updating {path}: {e}")
       