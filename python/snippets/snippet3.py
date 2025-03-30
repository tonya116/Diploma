import dearpygui.dearpygui as dpg


def mouse_drag_handler( sender, app_data, user_data):
    
    dx, dy = dpg.get_mouse_drag_delta()
    print(dx, dy)
        

def mouse_double_click_handler(self, sender, app_data, user_data):
    
    if app_data == dpg.mvMouseButton_Left:
        print(app_data, user_data)            


# Глобальные переменные для хранения модели
nodes = [
    {"id": 1, "x": 100, "y": 200},
    {"id": 2, "x": 300, "y": 200},
    {"id": 3, "x": 200, "y": 400},
]
edges = [(1, 2), (2, 3), (3, 1)]  # Связи между узлами
selected_node = None  # Выбранный узел


# Функция обновления инспектора
def update_inspector():
    dpg.set_value("node_id_text", f"ID: {selected_node['id']}")
    dpg.set_value("x_coord", selected_node["x"])
    dpg.set_value("y_coord", selected_node["y"])


# Функция изменения координат узла
def change_node_x(sender, app_data):
    if selected_node:
        selected_node["x"] = app_data
        draw_model()  # Перерисовываем


def change_node_y(sender, app_data):
    if selected_node:
        selected_node["y"] = app_data
        draw_model()


# Функция для обработки клика по узлу
def select_node(sender, app_data):
    global selected_node
    if app_data:
        click_x, click_y = app_data  # Координаты клика

        # Ищем ближайший узел
        for node in nodes:
            if abs(node["x"] - click_x) < 10 and abs(node["y"] - click_y) < 10:
                selected_node = node
                update_inspector()
                return


# Функция отрисовки модели
def draw_model():
    dpg.delete_item("canvas", children_only=True)  # Очищаем канвас

    # Рисуем связи (линии)
    for edge in edges:
        n1 = next(n for n in nodes if n["id"] == edge[0])
        n2 = next(n for n in nodes if n["id"] == edge[1])
        dpg.draw_line((n1["x"], n1["y"]), (n2["x"], n2["y"]), parent="canvas", color=(200, 200, 200), thickness=2)

    # Рисуем узлы (точки)
    for node in nodes:
        dpg.draw_circle((node["x"], node["y"]), 6, parent="canvas", color=(255, 0, 0), fill=(255, 0, 0))
        dpg.draw_text((node["x"] + 8, node["y"] - 8), str(node["id"]), parent="canvas", color=(255, 255, 255))


# Создание окна DearPyGui
dpg.create_context()

with dpg.window(label="Main Window", width=800, height=600):
    with dpg.group(horizontal=True):

        # Левый блок — Канвас
        with dpg.child_window(width=500, height=500):
            with dpg.drawlist(width=500, height=500, tag="canvas"):
                dpg.set_item_callback("canvas", select_node)

        # Правый блок — Инспектор
        with dpg.child_window(width=300, height=500):
            dpg.add_text("Inspector")
            dpg.add_text("Selected node:", tag="node_id_text")
            dpg.add_input_int(label="X", tag="x_coord", callback=change_node_x)
            dpg.add_input_int(label="Y", tag="y_coord", callback=change_node_y)

        with dpg.handler_registry():
            dpg.add_mouse_drag_handler(callback=mouse_drag_handler, button=dpg.mvMouseButton_Left)
            dpg.add_mouse_double_click_handler(callback=mouse_double_click_handler)

# Отрисовка модели
draw_model()

dpg.create_viewport(title="Model Editor", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
