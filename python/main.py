import ctypes
import os
from dearpygui import dearpygui as dpg
import json

def load_model(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Пример использования
model_data = load_model("model.json")

# Путь к скомпилированной C++ библиотеке
lib_path = os.path.join(os.path.dirname(__file__), "../build/src/libcalculations.so")
calculations = ctypes.CDLL(lib_path)

# Указываем типы для C++ функции
calculations.add.argtypes = [ctypes.c_double, ctypes.c_double]
calculations.add.restype = ctypes.c_double


# Callback-функция для кнопки
def on_calculate(sender, app_data, user_data):
    try:
        # Получаем числа из интерфейса
        a = float(dpg.get_value("input_a"))
        b = float(dpg.get_value("input_b"))

        # Вызываем C++ функцию и выводим результат
        result = calculations.add(a, b)
        dpg.set_value("result_text", f"Result: {result}")
    except ValueError:
        dpg.set_value("result_text", "Enter correct values!")


# Настройка интерфейса
dpg.create_context()

# Основное окно
with dpg.window(label="Build v0.0.1", tag="main_window", width=800, height=600):
    dpg.add_text("Enter two numbers for sum:")

    # Поля ввода
    dpg.add_input_text(label="Number A", tag="input_a", width=200)
    dpg.add_input_text(label="Number B", tag="input_b", width=200)

    # Кнопка для выполнения операции
    dpg.add_button(label="Calculate", callback=on_calculate)

    # Поле для вывода результата
    dpg.add_text("", tag="result_text")

dpg.create_viewport(title="C++ & Python Calculation", width=600, height=400)
dpg.setup_dearpygui()
dpg.set_primary_window("main_window", True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
