from typing import Any

from dearpygui import dearpygui as dpg
from model import Model

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

from tab import Tab

W = int(config("WIDTH"))
H = int(config("HEIGHT"))

DEFAULT = True

TITLE = "HyprBeam"

class Window:
    def __init__(self, callbacks):
        self.callbacks: dict = callbacks
        # Настройка интерфейса
        dpg.create_context()
        dpg.create_viewport(title=TITLE, width=W, height=H)
        dpg.setup_dearpygui()

        # Регистрируем шрифт
        with dpg.font_registry():
            # Первый параметр - размер, второй - путь к файлу шрифта
            default_font = dpg.add_font(config("FONT"), int(config("FONT_SIZE")), tag="rus_font")
            # Устанавливаем шрифт по умолчанию для всех элементов
            dpg.bind_font(default_font)

    def mouse_drag_handler(self, sender, app_data, user_data):
        if self.app.active_tab:
            f = Vector(*dpg.get_mouse_pos()) 
            current_pos = self.active_tab.model.get_pos()
            # self.app.current_model.set_pos(f + (f - current_pos))

    def mouse_double_click_handler(self, sender, app_data, user_data):
        if self.app.active_tab and app_data == dpg.mvMouseButton_Left:
            mouse_pos = Vector(*dpg.get_drawing_mouse_pos()) - Vector(W//4, H//2)
            print(f"Mouse position: {mouse_pos}")
            dpg.draw_circle(mouse_pos.asList(), 5, color=(255, 255, 0), fill=(255, 255, 0), parent=self.app.active_tab.model.draw_node_id)

    def select_open_file_cb(self, sender, app_data, user_data):
        model = Model()
        model.load_model(app_data.get("file_path_name"))
        self.callbacks.get("create_tab")(model)
        

    def callback(self, sender, app_data, user_data):
        print("Sender: ", sender)
        print("App Data: ", app_data)
        print("User Data: ", user_data)

    def _create_file_dialog(self):
        with dpg.file_dialog(
            directory_selector=False,
            callback=self.select_open_file_cb,
            id="file_dialog_id",
            width=700,
            height=400,
        ):
            dpg.add_file_extension(".mdl", color=(255, 0, 255), custom_text="[model]")


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
            current = self.app.current_model.data
            
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
        self.app.current_model.save_to_file(user_data)
       
    def add_find_loads(self, values):
        dpg.add_text(f"Found reactions", parent="inspector")   

        for i, x in enumerate(values):
            dpg.add_text(f"X{i+1}: {x:.5} KH", parent="inspector")   
       
    def setup(self):
        # Основное окно
        with dpg.window(label="Build v0.0.13", tag="main_window", width=W, height=H):
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="Open", callback=self._create_file_dialog)
                    dpg.add_menu_item(label="Save", callback=self._save_to_file)
                    dpg.add_menu_item(label="Save As", callback=self._save_to_file)

                with dpg.menu(label="Calculate"):
                    dpg.add_menu_item(label="Run", callback=self.callbacks.get("calculate"))
                    
            with dpg.group(horizontal=True):
                if DEFAULT: # исключительно в тестовых целях (открывает файл при запуске)
                    model = Model()
                    model.load_model(config("DEFAULT_MODEL"))
                # Левый блок — Канвас
                with dpg.child_window(width=W//2, height=H):
                    # Вкладки для переключения моделей
                    with dpg.tab_bar(tag="tab_bar", callback=self.callbacks.get("tab_change_callback")):
                        if DEFAULT: # исключительно в тестовых целях (открывает файл при запуске)
                            self.callbacks.get("create_tab")(model)
                        
                # Правый блок — Инспектор
                # Inspector()
                with dpg.child_window(width=W//2, height=H, tag="inspector"):
                    dpg.add_text("Inspector")
                    dpg.add_text(f"E - модуль упругости (Па)")

                    dpg.add_input_int(tag="E", width=100, callback=self.callback)
                    dpg.add_text(f"SIGMA")

                    dpg.add_input_int(tag="sigma", width=100, callback=self.callback)
                    self._build_editable_tree("##dynamic_tree_root", model.data)
        
        with dpg.handler_registry():
            dpg.add_mouse_double_click_handler(callback=self.mouse_double_click_handler)
            dpg.add_mouse_drag_handler(callback=self.mouse_drag_handler, button=dpg.mvMouseButton_Left)
            dpg.add_mouse_wheel_handler(callback=self.callbacks.get("mouse_wheel_handler"))
            dpg.add_key_down_handler(callback=self.callbacks.get("key_down_handler"))
            dpg.add_key_press_handler(callback=self.callbacks.get("key_down_handler"))
        dpg.set_primary_window("main_window", True)

    def run(self):
        self.setup()
        dpg.show_viewport()
        
        while dpg.is_dearpygui_running():
            # if self.active_tab:
            #     self.active_tab.model.update()

            dpg.render_dearpygui_frame()
        dpg.destroy_context()