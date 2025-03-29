import dearpygui.dearpygui as dpg
import numpy as np

dpg.create_context()

with dpg.window(label="Ortho Example", width=600, height=600):
    with dpg.drawlist(width=500, height=500, id="drawlist"):
        pass

def update_drawlist():
    
    l = dpg.create_orthographic_matrix(0, 500, 500, 0, 0.1, 100)
    l = dpg.create_perspective_matrix(3.1415 * 45.0 / 180.0, 1.0, 0.1, 100)

    dpg.apply_transform("drawlist", l)
    dpg.draw_line("drawlist", (50, 50), (450, 450), color=(255, 0, 0, 255), thickness=3)
    dpg.draw_circle("drawlist", (250, 250), 100, color=(0, 255, 0, 150), fill=(0, 255, 0, 50))

dpg.set_frame_callback(1, update_drawlist)  # Отложенный вызов после инициализации
dpg.create_viewport(title="Ortho Projection", width=800, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()