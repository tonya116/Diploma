import math
import dearpygui.dearpygui as dpg

# Размеры окна
WIDTH, HEIGHT = 700, 700

size = 2
# Пример координат для линий и узлов
lines = [
    ((-size, -size), (size, -size)),  # Линия от (100, 100) до (300, 100)
    ((size, -size), (size, size)),  # Линия от (300, 100) до (300, 300)
    ((size, size), (-size, size)),  # Линия от (300, 300) до (100, 300)
    ((-size, size), (-size, -size)),  # Линия от (100, 300) до (100, 100)
]

nodes = [
    (-size, -size),
    (size, -size),
    (size, size),
    (-size, size),
]

# Функция для создания линии
def draw_line(start, end, color=(0, 150, 255), thickness=2):
    print("lol")
    dpg.draw_line(p1=start, p2=end, color=color, thickness=thickness)

# Функция для создания узла (круга)
def draw_circle(center, radius=5, color=(255, 0, 0), fill=(255, 0, 0)):
    dpg.draw_circle(center=center, radius=radius, color=color, fill=fill)

# Создаём интерфейс
dpg.create_context()
dpg.create_viewport(title="Orthogonal Projection Example", width=WIDTH, height=HEIGHT)
dpg.setup_dearpygui()

# Создаём окно для рисования
with dpg.window(label="Orthogonal Projection", width=WIDTH, height=HEIGHT, tag="main_window"):
    with dpg.drawlist(width=WIDTH, height=HEIGHT):
        with dpg.draw_layer(tag="main pass", depth_clipping=True, perspective_divide=True, cull_mode=dpg.mvCullMode_Back):
            # Устанавливаем ортогональную проекцию
            with dpg.draw_node(tag="cube"):
                dpg.draw_circle((0, 0), 5, color = (255, 255, 255, 255))
                # Рисуем линии
                for start, end in lines:
     
                    draw_line(start, end)

                # Рисуем узлы
                for center in nodes:
                    draw_circle(center)
dpg.set_clip_space("main pass", top_left_x=0, top_left_y=0, width=WIDTH, height=HEIGHT, min_depth=-1, max_depth=1)

dpg.show_viewport()
dpg.set_primary_window("main_window", True)
# proj = dpg.create_perspective_matrix(math.pi*45.0/180.0, 1.0, 0.1, 100)
N = 40
a = -N
b = N
c = -N
d = N
e = -N*5
f = N*5
proj = dpg.create_orthographic_matrix(a, b, c, d, e, f)

dpg.apply_transform("cube", proj)
# while dpg.is_dearpygui_running():
#     dpg.render_dearpygui_frame()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
# # Запуск приложения
# dpg.show_viewport()
# dpg.start_dearpygui()
dpg.destroy_context()
