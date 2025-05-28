
import ctypes

from matplotlib import pyplot as plt
import numpy as np

from config import config
from Entities.diagrams import Diagram
from Entities.distributed_force import DistributedForce
from Entities.force import Force
from Entities.momentum import Momentum


class Calculations:
    def __init__(self):
        
        # Загружаем библиотеку
        self.lib = ctypes.CDLL(config("DLL_PATH"))

        # Объявляем тип Matrix*
        class Matrix(ctypes.Structure):
            pass

        Matrix_p = ctypes.POINTER(Matrix)
        # Создаем матрицы параметров

        # Определяем типы аргументов и возвращаемого значения
        self.lib.diagram_calc.argtypes = [
            ctypes.c_double,  # L
            np.ctypeslib.ndpointer(dtype=np.float64),  # x
            ctypes.c_size_t,  # size
            np.ctypeslib.ndpointer(dtype=np.float64),  # V
            np.ctypeslib.ndpointer(dtype=np.float64),  # M
            Matrix_p,  # pl
            Matrix_p,  # dl
            Matrix_p,  # moments
        ]

        self.lib.diagram_calc.restype = None
    
        # Определим возвращаемые и аргументные типы
        self.lib.Matrix_create.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.Matrix_create.restype = Matrix_p

        self.lib.Matrix_destroy.argtypes = [ctypes.c_void_p]
        self.lib.Matrix_destroy.restype = None

        self.lib.Matrix_set.argtypes = [Matrix_p, ctypes.c_int, ctypes.c_int, ctypes.c_double]
        self.lib.Matrix_get.argtypes = [Matrix_p, ctypes.c_int, ctypes.c_int]
        self.lib.Matrix_get.restype = ctypes.c_double

    def calc(self, model):
        nodes = model.data.get("nodes")
        
        start_node = nodes[0]
        end_node = nodes[-1]
        lenght = (end_node.point - start_node.point).norm()  # длина балки, м
        x = np.arange(0, lenght + float(config("DX")), float(config("DX")))
        # --- Нагрузки ---
        point_loads = [] # (позиция, сила в кН)
        distributed_loads = [] # (от, до, q кН/м)
        moments = [] # (позиция, момент в кН·м), отриц — по часовой

        for load in model.data.get("loads"):
            if isinstance(load, DistributedForce):
                distributed_loads.append([load.node.point.x - load.lenght/2, load.node.point.x + load.lenght/2, load.direction.y])
            if isinstance(load, Force):
                point_loads.append([load.node.point.x, load.direction.y])
            if isinstance(load, Momentum):
                moments.append([load.node.point.x, load.direction.y])

        point_loadsM = self.lib.Matrix_create(len(point_loads), len(point_loads[0])) if point_loads else self.lib.Matrix_create(0, 0)
        distributed_loadsM = self.lib.Matrix_create(len(distributed_loads), len(distributed_loads[0])) if distributed_loads else self.lib.Matrix_create(0, 0)
        momentsM = self.lib.Matrix_create(len(moments), len(moments[0])) if moments else self.lib.Matrix_create(0, 0)

        for i, t in enumerate(point_loads):
            for j, load in enumerate(t):
                self.lib.Matrix_set(point_loadsM, i, j, load)

        for i, t in enumerate(distributed_loads):
            for j, load in enumerate(t):
                self.lib.Matrix_set(distributed_loadsM, i, j, load)
                
        for i, t in enumerate(moments):
            for j, load in enumerate(t):
                self.lib.Matrix_set(momentsM, i, j, load)                            
        
        # Подготавливаем массивы для результатов
        V = np.zeros(x.size, dtype=np.float64)
        M = np.zeros(x.size, dtype=np.float64)
        
        # Вызываем функцию
        self.lib.diagram_calc(lenght, x, x.size, V, M, point_loadsM, distributed_loadsM, momentsM)  
      
        self.lib.Matrix_destroy(point_loadsM)
        self.lib.Matrix_destroy(distributed_loadsM)
        self.lib.Matrix_destroy(momentsM)

        return V, M

    def determinate_system(self):
        pass
    
    def undeterminate_system(self):
        pass