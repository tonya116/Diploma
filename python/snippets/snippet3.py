import dearpygui.dearpygui as dpg

# Словарь моделей, где каждый ключ — это ID вкладки, а значение — список узлов и связей
models = {
    "Model 1": {
        "nodes": [{"id": 1, "x": 100, "y": 200}, {"id": 2, "x": 300, "y": 200}, {"id": 3, "x": 200, "y": 400}],
        "edges": [(1, 2), (2, 3), (3, 1)]
    },
    "Model 2": {
        "nodes": [{"id": 1, "x": 150, "y": 250}, {"id": 2, "x": 350, "y": 250}],
        "edges": [(1, 2)]
    }
}
selected_model = "Model 1"  # Текущая активная модель
selected_node = None  # Выбранный узел


# Функция обновления инспектора
def update_inspector():
    if selected_node:
        dpg.set_value("node_id_text", f"ID: {selected_node['id']}")
        dpg.set_value("x_coord", selected_node["x"])
        dpg.set_value("y_coord", selected_node["y"])
    else:
        dpg.set_value("node_id_text", "ID: None")


# Функция изменения координат узла
def change_node_x(sender, app_data):
    if selected_node:
        selected_node["x"] = app_data
        draw_model()


def change_node_y(sender, app_data):
    if selected_node:
        selected_node["y"] = app_data
        draw_model()


# Функция для обработки клика по узлу
def select_node(sender, app_data):
    global selected_node
    click_x, click_y = app_data

    # Проверяем, какая модель активна
    nodes = models[selected_model]["nodes"]

    for node in nodes:
        if abs(node["x"] - click_x) < 10 and abs(node["y"] - click_y) < 10:
            selected_node = node
            update_inspector()
            return


# Функция отрисовки модели
def draw_model():
    dpg.delete_item("canvas", children_only=True)  # Очищаем канвас

    nodes = models[selected_model]["nodes"]
    edges = models[selected_model]["edges"]

    # Рисуем связи (линии)
    for edge in edges:
        n1 = next(n for n in nodes if n["id"] == edge[0])
        n2 = next(n for n in nodes if n["id"] == edge[1])
        dpg.draw_line((n1["x"], n1["y"]), (n2["x"], n2["y"]), parent="canvas", color=(200, 200, 200), thickness=2)

    # Рисуем узлы (точки)
    for node in nodes:
        dpg.draw_circle((node["x"], node["y"]), 6, parent="canvas", color=(255, 0, 0), fill=(255, 0, 0))
        dpg.draw_text((node["x"] + 8, node["y"] - 8), str(node["id"]), parent="canvas", color=(255, 255, 255))


# Функция переключения модели
def switch_model(sender, app_data):
    global selected_model, selected_node
    selected_model = app_data
    selected_node = None  # Сбрасываем выбранный узел
    update_inspector()
    draw_model()


# Создание окна DearPyGui
dpg.create_context()

with dpg.window(label="Main Window", width=800, height=600):
    with dpg.group(horizontal=True):

        # Левый блок — Канвас
        with dpg.child_window(width=500, height=500):
            dpg.add_text("Модель")
            
            # Вкладки для переключения моделей
            with dpg.tab_bar(tag="tab_bar", callback=switch_model):
                for model_name in models.keys():
                    dpg.add_tab(label=model_name, tag=model_name)

            with dpg.drawlist(width=500, height=500, tag="canvas"):
                dpg.set_item_callback("canvas", select_node)

        # Правый блок — Инспектор
        with dpg.child_window(width=300, height=500):
            dpg.add_text("Инспектор")
            dpg.add_text("Выбранный узел:", tag="node_id_text")
            dpg.add_input_int(label="X", tag="x_coord", callback=change_node_x)
            dpg.add_input_int(label="Y", tag="y_coord", callback=change_node_y)

# Отрисовка начальной модели
draw_model()

dpg.create_viewport(title="Model Editor", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
