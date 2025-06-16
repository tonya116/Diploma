from typing import Any

from dearpygui import dearpygui as dpg
from model import Model

from config import config
from Entities.node import Node
from Entities.element import Element
from Entities.fixed import Fixed
from Entities.pinned import Pinned
from Entities.roller import Roller
from Entities.force import Force
from Entities.prop import Support
from Entities.load import Load

from Entities.distributed_force import DistributedForce
from Entities.momentum import Momentum

W = int(config("WIDTH"))
H = int(config("HEIGHT"))

TITLE = "HyprBeam"

class Window:
    def __init__(self, callbacks):
        self.callbacks: dict = callbacks
        # Настройка интерфейса
        dpg.create_context()
        dpg.create_viewport(title=TITLE, width=W, height=H)
        dpg.setup_dearpygui()

        with dpg.font_registry():

            with dpg.font(config("FONT"), 18) as default_font:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        dpg.bind_font(default_font)

        self.setup()

    def select_open_file_cb(self, sender, app_data, user_data):
        model = Model(False)
        model.load_model(app_data.get("file_path_name"))
        self.callbacks.get("create_tab")(model)
        

    def callback(self, sender, app_data, user_data):
        print("Sender: ", sender)
        print("App Data: ", app_data)
        print("User Data: ", user_data)

    def _create_file_dialog(self, sender, app_data, user_data):
        with dpg.file_dialog(
            directory_selector=False,
            callback=user_data,
            id="file_dialog_id",
            width=700,
            height=400,
        ):
            dpg.add_file_extension(".mdl", color=(255, 0, 255), custom_text="[model]")

    def _build_editable_tree(self, parent: str, data: Any, path: str = ""):
        name_map = {"nodes": "Узлы", "supports": "Опоры", "loads": "Нагрузки", "elements": "Балки"}
        
        """Рекурсивное построение дерева с элементами редактирования"""
        if isinstance(data, dict):
            if dpg.does_item_exist(parent):
                dpg.delete_item(parent, children_only=True)
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                if isinstance(value, (dict, list)):
                    with dpg.tree_node(label=name_map[key], parent=parent) as tree_node:
                        self._build_editable_tree(tree_node, value, new_path)
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

    def __add_node_field(self, value, path, text = "Узел:"):
        dpg.add_text(text)
        dpg.add_input_int(
            label="#Узла",
            default_value=value.node.id,
            width=int(config("FieldWidth")),
            tag=f"{path}.node",
            callback=self.callbacks.get("_update_data")
        )

    def __add_direction_field(self, value: Node| Load| Support, path, x = "м", y = "м"):
        dpg.add_text(f"Направление:")
        with dpg.group(horizontal=True):
                dpg.add_input_float(
                    label=x,
                    default_value=value.direction.x,
                    width=int(config("FieldWidth")),
                    tag=f"{path}.direction.x",
                    callback=self.callbacks.get("_update_data")
                )
                dpg.add_input_float(
                    label=y,
                    default_value=value.direction.y,
                    width=int(config("FieldWidth")),
                    tag=f"{path}.direction.y",
                    callback=self.callbacks.get("_update_data")
                )

    def _add_editable_field(self, parent: str, value: Any, path: str):
        name_map = {"Node": "Узел", "Fixed": "Заделка", "Roller": "Шарнирно-подвижная", "Pinned": "Шарнирно-неподвижная", "element": "Балка", "Momentum": "Момент", "DistributedForce": "Распределенная нагрузка", "Force": "Сосредоточенная сила"}

        """Добавление поля с возможностью редактирования"""
        with dpg.group(horizontal=True, parent=parent):
            if isinstance(value, Node):
                with dpg.group(horizontal=True):
                    dpg.add_text(f"{name_map[value.__class__.__name__]} #{value.id}:")
                    self.__add_direction_field(value, path)

            elif isinstance(value, Element):
                with dpg.group(horizontal=True):
                    dpg.add_text(f"Балка #{value.id}:")
                    with dpg.group(horizontal=False):
                        dpg.add_text(f"Начальный узел:")

                        dpg.add_input_int(
                            label="#Узла",
                            default_value=value.start_node.id,
                            tag=f"{path}.start_node",
                            width=int(config("FieldWidth")),
                            callback=self.callbacks.get("_update_data")
                        )
                        dpg.add_text(f"Конечный узел:")

                        dpg.add_input_int(
                            label="#Узла",
                            default_value=value.end_node.id,
                            tag=f"{path}.end_node",
                            width=int(config("FieldWidth")),
                            callback=self.callbacks.get("_update_data")
                        )

            elif isinstance(value, (Fixed, Roller, Pinned)):
                with dpg.group(horizontal=True):
                    dpg.add_text(f"{name_map[value.__class__.__name__]} #{value.id}:")
                    with dpg.group(horizontal=False):
                        self.__add_node_field(value, path)
                        self.__add_direction_field(value, path)
                        
            elif isinstance(value, (Force, Momentum)):
                with dpg.group(horizontal=True):
                    dpg.add_text(f"{name_map[value.__class__.__name__]} #{value.id}:")
                    with dpg.group(horizontal=False):
                        self.__add_node_field(value, path)
                        self.__add_direction_field(value, path, "кН*м(x)", "кН*м(y)")

            elif isinstance(value, DistributedForce):
                with dpg.group(horizontal=True):
                    dpg.add_text(f"{name_map[value.__class__.__name__]} #{value.id}:")
                    with dpg.group(horizontal=False):
                        self.__add_node_field(value, path)
                        self.__add_direction_field(value, path, "кН/м(x)", "кН/м(y)")

                        dpg.add_text(f"Протяженность:")
                        dpg.add_input_float(
                            label="м",
                            default_value=value.lenght,
                            width=int(config("FieldWidth")),
                            tag=f"{path}.lenght",
                            callback=self.callbacks.get("_update_data")
                        )
    
    def add_find_loads(self, values):
        dpg.add_text(f"Найденные реакции", parent="inspector")   

        for i, x in enumerate(values):
            dpg.add_text(f"X{i+1}: {x:.5} кH", parent="inspector")   
       
    def setup(self):
        # Основное окно
        with dpg.window(label="Build v0.0.13", tag="main_window", width=W, height=H, no_scroll_with_mouse=True):
            with dpg.menu_bar():
                with dpg.menu(label="Файл"):
                    dpg.add_menu_item(label="Открыть", callback=self._create_file_dialog, user_data=self.select_open_file_cb)
                    dpg.add_menu_item(label="Сохранить", callback=self.callbacks.get("save_file"))
                    dpg.add_menu_item(label="Сохранить как", callback=self._create_file_dialog, user_data=self.callbacks.get("save_as_file"))

                with dpg.menu(label="Расчет"):
                    dpg.add_menu_item(label="Запуск", callback=self.callbacks.get("calculate"))
                    
            with dpg.group(horizontal=True):

                # Левый блок — Канвас
                with dpg.child_window(width=W//4*3-190, height=H, no_scroll_with_mouse=True):
                    # Вкладки для переключения моделей
                    with dpg.tab_bar(tag="tab_bar", callback=self.callbacks.get("tab_change_callback")):
                        pass          
                                  
                # Правый блок — Инспектор
                with dpg.child_window(width=W//4+150, height=H, tag="inspector"):
                    dpg.add_text("Инспектор")
                    
                    dpg.add_text(f"Модуль продольной упругости:")
                    dpg.add_input_text(label="(Па)", default_value=2e11, tag="E", width=200, callback=self.callbacks.get("update_E"))
                    
                    dpg.add_text(f"Допускаемое нормальное напряжение:")
                    dpg.add_input_int(default_value=180e6, tag="sigma", width=200, callback=self.callback)
                    with dpg.group(tag="tree") as tree:
                        pass
                    
        
        with dpg.handler_registry():
            dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Middle, callback=self.callbacks.get("tab_change_callback"))
            dpg.add_mouse_wheel_handler(callback=self.callbacks.get("mouse_wheel_handler"))

        dpg.set_primary_window("main_window", True)
        