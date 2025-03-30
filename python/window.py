import ctypes
import os

from dearpygui import dearpygui as dpg
from model import Model
import configparser

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

    def mouse_drag_handler(self, sender, app_data, user_data):
        
        if self.current_model:
            
            dx, dy = dpg.get_mouse_drag_delta()
            self.current_model.rotate_x(dx/100)
            self.current_model.rotate_y(dy/100)

    def mouse_double_click_handler(self, sender, app_data, user_data):
        if self.current_model:
            if app_data == dpg.mvMouseButton_Left:
                for i, node in enumerate(self.current_model.nodes):
                    mouse_pos = dpg.get_drawing_mouse_pos()
                    print(f"mouse: ", mouse_pos)
                    t = dpg.mvVec4(*node.point, 1)
                    print("node: ", t)
                    t *= self.current_model.get_model_matrix()
                    
                    if ((t[0] - mouse_pos[0])**2 + (t[1] - mouse_pos[1])**2)**0.5 < 5:
                        print(node.id)
                    

    def mouse_wheel_handler(self, sender, app_data, user_data):
        
        if self.current_model:
            self.current_model.set_scale(self.current_model.get_scale() * (1.5**app_data))

    # Функция для отрисовки модели
    def draw_model(self):
        
        if not self.current_model:
            return
        
        self.current_model.update()
        
        for element in self.current_model.elements:
            start_node = next(node for node in self.current_model.nodes if node.id == element.start_node)
            end_node = next(node for node in self.current_model.nodes if node.id == element.end_node)

            dpg.draw_line(p1=start_node.point, p2=end_node.point, color=eval(setting("LineColor")), thickness=2)

        for node in self.current_model.nodes:
            dpg.draw_circle(node.point, 5, color=eval(setting("NodeColor")), fill=eval(setting("NodeColor")))

    def select_open_file_cb(self, sender, app_data, user_data):
        self.current_model = Model()
        self.current_model.load_model(app_data.get("file_path_name"))
        self.models.update({self.current_model.name: self.current_model})
        print(self.current_model.data)
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
        drawlist_id = dpg.generate_uuid()
        draw_layer_id = dpg.generate_uuid()
        # Добавляем новую вкладку в tab_bar
        with dpg.tab(label=model_name, parent="tab_bar", tag=tab_id):
            # Добавляем область для рисования (drawlist) на этой вкладке
            with dpg.drawlist(width=W, height=H, tag=drawlist_id):
                with dpg.draw_layer( parent=drawlist_id, tag=draw_layer_id):
                    
                    with dpg.draw_node(parent=draw_layer_id, tag=self.current_model.draw_node_id):
                        self.current_model.set_scale(0.5)
                        self.draw_model()
                        
        dpg.delete_item("file_dialog_id")

    def run(self):
        # Основное окно
        with dpg.window(label="Build v0.0.3", tag="main_window", width=W, height=H):
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="Open", callback=self.create_file_dialog)

                with dpg.menu(label="Calculate"):
                    dpg.add_menu_item(label="Run", callback=self.calculate)
                    
            with dpg.group(horizontal=True):


                # Левый блок — Канвас
                with dpg.child_window(width=W, height=H) as d:
                    # Вкладки для переключения моделей
                    with dpg.tab_bar(tag="tab_bar", callback=self.tab_change_callback) as f:
                        pass
                        

                # Правый блок — Инспектор
                with dpg.child_window(width=300, height=H):
                    dpg.add_text("Inspector")
                    dpg.add_text("Selected Node:", tag="node_id_text")
                    dpg.add_input_int(label="X", tag="x_coord", callback=self.callback)
                    dpg.add_input_int(label="Y", tag="y_coord", callback=self.callback)

        with dpg.handler_registry():
            dpg.add_mouse_double_click_handler(callback=self.mouse_double_click_handler)

            dpg.add_mouse_drag_handler(callback=self.mouse_drag_handler, button=dpg.mvMouseButton_Left)
            dpg.add_mouse_wheel_handler(callback=self.mouse_wheel_handler)

        dpg.set_primary_window("main_window", True)
        dpg.show_viewport()

        while dpg.is_dearpygui_running():
            if self.current_model:
                self.current_model.update()

            dpg.render_dearpygui_frame()

        dpg.destroy_context()
        
