
import ctypes

import numpy as np

from config import config
from Entities.diagrams import Diagram
from Entities.distributed_force import DistributedForce
from Entities.force import Force
from Entities.momentum import Momentum


class Calculations:
    def __init__(self):
        
        # Загружаем библиотеку
        self.lib = ctypes.CDLL('build/src/libcalculations.so')

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
        end_node = nodes[1]
        L = (end_node.point - start_node.point).norm()  # длина балки, м

        x = np.arange(0, L + float(config("DX")), float(config("DX")))
        # --- Нагрузки ---
        point_loads = []  # (позиция, сила в кН)
        distributed_loads = []   # (от, до, q кН/м)
        moments = []                # (позиция, момент в кН·м), отриц — по часовой
        
        for load in model.data.get("loads"):
            if load.node in [start_node, end_node]:
                if isinstance(load, DistributedForce):
                    distributed_loads.append([load.node.point.x- load.lenght/2, load.node.point.x + load.lenght/2, load.force])
                if isinstance(load, Force):
                    point_loads.append([load.node.point.x, load.force])
                if isinstance(load, Momentum):
                    moments.append([load.node.point.x, load.force])
        
        
        point_loadsM = self.lib.Matrix_create(0, 0)

        distributed_loadsM = self.lib.Matrix_create(0, 0)
        momentsM = self.lib.Matrix_create(0, 0)
        
        if point_loads:
            point_loadsM = self.lib.Matrix_create(len(point_loads), len(point_loads[0]))
        if distributed_loads:
            distributed_loadsM = self.lib.Matrix_create(len(distributed_loads), len(distributed_loads[0]))
        if moments:
                
            momentsM = self.lib.Matrix_create(len(moments), len(moments[0]))

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
        self.lib.diagram_calc(L, x, x.size, V, M, point_loadsM, distributed_loadsM, momentsM)
        
        M1V = sum(V) * float(config("DX"))
        M1M = sum(M) * float(config("DX"))
        print(M1M, M1V)    

        diag = Diagram(-1, start_node, end_node, V)
        diag2 = Diagram(0, start_node, end_node, M)

        model.diagrams.append(diag.geometry())
        model.diagrams.append(diag2.geometry())
        
        self.lib.Matrix_destroy(point_loadsM)
        self.lib.Matrix_destroy(distributed_loadsM)
        self.lib.Matrix_destroy(momentsM)

    def center_of_mass_1d(values, dx=0.01):
        total_mass = 0.0
        cx = 0.0
        for i, v in enumerate(values):
            x = i * dx
            cx += x * v
            total_mass += v
        return cx / total_mass if total_mass else None
