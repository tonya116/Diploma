import ctypes
from matplotlib import pyplot as plt
import numpy as np
import datetime


class Matrix:
    def __init__(self, lib, data):
        self.lib = lib
        rows = len(data)
        cols = len(data[0]) if rows > 0 else 0
        
        # Преобразуем в плоский массив
        flat_data = np.array(data, dtype=np.float64).flatten()
        
        # Создаем матрицу в C++
        self.obj = self.lib.create_matrix_from_array(
            flat_data.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            ctypes.c_int(rows),
            ctypes.c_int(cols)
        )
    
    def __del__(self):
        # Освобождаем память при удалении объекта
        self.lib.delete_matrix(self.obj)

# Загружаем библиотеку
lib = ctypes.CDLL('build/src/libcalculations.so')

# Определяем типы аргументов и возвращаемого значения
lib.diagram_calc.argtypes = [
    ctypes.c_double,                       # L
    np.ctypeslib.ndpointer(dtype=np.float64),  # x
    ctypes.c_size_t,                    # size
    np.ctypeslib.ndpointer(dtype=np.float64),  # V
    np.ctypeslib.ndpointer(dtype=np.float64)   # M
]
lib.diagram_calc.restype = None

 
# # Определяем типы функций
# lib.create_matrix_from_array.argtypes = [
#     ctypes.POINTER(ctypes.c_double),
#     ctypes.c_int,
#     ctypes.c_int
# ]
# lib.create_matrix_from_array.restype = ctypes.c_void_p

# lib.delete_matrix.argtypes = [ctypes.c_void_p]
# lib.delete_matrix.restype = None


def call_diagram_calc(L, x):
    
    # Подготавливаем массивы для результатов
    V = np.zeros(x.size, dtype=np.float64)
    M = np.zeros(x.size, dtype=np.float64)
    # Вызываем функцию
    lib.diagram_calc(L, x, x.size, V, M)
    
    return V, M



L = 6  # длина балки, м
dx = 0.000_001

x = np.arange(0, L + dx, dx)


# --- Нагрузки ---
point_loads = [[4, -30]]  # (позиция, сила в кН)
distributed_loads = [[0, 2, -10]]   # (от, до, q кН/м)
moments = [[2, 20]]                # (позиция, момент в кН·м), отриц — по часовой

start = datetime.datetime.now()

V, M = call_diagram_calc(L, x)

# --- Графики ---
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(x, V, label='V(x) — поперечная сила', color='blue')
plt.axhline(0, color='black', linewidth=0.5)
plt.ylabel('V, кН')
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(x, M, label='M(x) — изгибающий момент', color='red')
plt.axhline(0, color='black', linewidth=0.5)
plt.xlabel('x, м')
plt.ylabel('M, кН·м')
plt.grid(True)
plt.legend()

plt.tight_layout()
end = datetime.datetime.now()
print("c++", end-start)

plt.show()
