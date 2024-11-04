import xml.etree.ElementTree as ET
from dearpygui import dearpygui as dpg


# Функция обратного вызова для кнопки
def on_button_click(sender, app_data, user_data):
    print("Button clicked!")


# Функция для обработки XML и создания интерфейса
def build_interface_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for window in root.findall("window"):
        window_label = window.get("label", "Window")
        window_width = int(window.get("width", 400))
        window_height = int(window.get("height", 300))

        with dpg.window(label=window_label, width=window_width, height=window_height):
            for element in window:
                if element.tag == "text":
                    label = element.get("label", "")
                    dpg.add_text(label)
                elif element.tag == "button":
                    label = element.get("label", "Button")
                    callback_name = element.get("callback", None)
                    callback = globals().get(callback_name) if callback_name else None
                    dpg.add_button(label=label, callback=callback)
                elif element.tag == "input_text":
                    label = element.get("label", "Input")
                    default_value = element.get("default_value", "")
                    dpg.add_input_text(label=label, default_value=default_value)


# Создание интерфейса с XML
dpg.create_context()
build_interface_from_xml("python/interface/interface.xml")

# Настройка окна и запуск
dpg.create_viewport(title="XML-Based Interface", width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
