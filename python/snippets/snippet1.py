import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(width=800, height=600, title="Выделение элементов")

selected_item = None
drawing_elements = []

def is_point_near_line(mouse_pos, p1, p2, threshold=5):
    # Проверяем, находится ли точка рядом с линией (упрощенная версия)
    x, y = mouse_pos
    x1, y1 = p1
    x2, y2 = p2
    distance = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / ((y2 - y1)**2 + (x2 - x1)**2)**0.5
    return distance < threshold

def mouse_click_callback(sender, app_data):
    global selected_item
    mouse_pos = dpg.get_mouse_pos(local=False)
    
    for elem in drawing_elements:
        elem_type = dpg.get_item_type(elem["id"])
        
        if elem_type == "mvAppItemType::mvDrawLine":
            p1 = dpg.get_item_configuration(elem["id"])["p1"]
            p2 = dpg.get_item_configuration(elem["id"])["p2"]
            if is_point_near_line(mouse_pos, p1, p2):
                if selected_item:
                    dpg.configure_item(selected_item, color=(255, 255, 255))
                selected_item = elem["id"]
                dpg.configure_item(selected_item, color=(255, 0, 0))
                break

def add_draw_elements():
    with dpg.window(label="Draw Area", width=600, height=500):
        with dpg.drawlist(width=550, height=450):
            line_id = dpg.draw_line((50, 50), (200, 200), color=(255, 255, 255), thickness=2)
            drawing_elements.append({"id": line_id, "type": "line"})
            
            # Можно добавить другие элементы (круги, прямоугольники)
            
        # Регистрируем обработчик клика на весь холст
        with dpg.item_handler_registry(tag="mouse_click_handler"):
            dpg.add_mouse_click_handler(callback=mouse_click_callback)
        dpg.bind_item_handler_registry(dpg.last_item(), "mouse_click_handler")

add_draw_elements()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()