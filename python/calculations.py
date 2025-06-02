
import ctypes

from matplotlib import pyplot as plt
import numpy as np

from config import config
from Entities.diagrams import Diagram
from Entities.distributed_force import DistributedForce
from Entities.force import Force
from Entities.momentum import Momentum
from Geometry.Matrix import Matrix

from ctypes import POINTER, c_int, c_double, c_size_t, c_void_p


class Calculations:
    def __init__(self):
        
        # Загружаем библиотеку
        self.lib = ctypes.CDLL(config("DLL_PATH"))

        # Объявляем тип Matrix*
        class Matrix(ctypes.Structure):
            pass


        Matrix_p = ctypes.POINTER(Matrix)

        # Определяем типы аргументов и возвращаемого значения
        self.lib.diagram_calc.argtypes = [
            np.ctypeslib.ndpointer(dtype=np.float64),  # x
            c_double, # xA
            c_double, # xB
            c_size_t,  # size
            np.ctypeslib.ndpointer(dtype=np.float64),  # V
            np.ctypeslib.ndpointer(dtype=np.float64),  # M
            Matrix_p,  # pl
            Matrix_p,  # dl
            Matrix_p,  # moments
        ]

        self.lib.diagram_calc.restype = None
    
        # Определим возвращаемые и аргументные типы
        self.lib.Matrix_create.argtypes = [c_int, c_int]
        self.lib.Matrix_create.restype = Matrix_p

        self.lib.Matrix_create_from_data.argtypes = [POINTER(POINTER(c_double)), c_size_t, c_size_t]
        self.lib.Matrix_create_from_data.restype = Matrix_p

        self.lib.Matrix_destroy.argtypes = [c_void_p]
        self.lib.Matrix_destroy.restype = None

        self.lib.Mores_integral.argtypes = [np.ctypeslib.ndpointer(dtype=c_double), np.ctypeslib.ndpointer(dtype=c_double), c_size_t, c_double]
        self.lib.Mores_integral.restype = c_double

        self.lib.lin_solve.argtypes = [Matrix_p, Matrix_p]
        self.lib.lin_solve.restype = Matrix_p
        
        self.lib.Matrix_set.argtypes = [Matrix_p, c_int, c_int, c_double]
        self.lib.Matrix_set.restype = None

        self.lib.Matrix_get.argtypes = [Matrix_p, c_int, c_int]
        self.lib.Matrix_get.restype = c_double

        self.lib.integrate.argtypes = [
            np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS"),
            c_double,
            np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS"),
            c_size_t,
            c_int,
        ]

        self.lib.integrate.restype = None

    def create_matrix(self, py_data):
        # Преобразуем Python list of lists в C-совместимый формат
        rows = len(py_data)
        cols = len(py_data[0]) if rows > 0 else 0
        
        matrix_ptr = self.lib.Matrix_create(rows, cols)

        for i in range(rows):
            for j in range(cols):
                self.lib.Matrix_set(matrix_ptr, i, j, py_data[i][j])
        
        # Создаем матрицу
        return matrix_ptr

    def calc(self, model, sup1, sup2):
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

        point_loadsM = self.create_matrix(point_loads)
        distributed_loadsM = self.create_matrix(distributed_loads)
        momentsM = self.create_matrix(moments)

        # Подготавливаем массивы для результатов
        V = np.zeros(x.size, dtype=np.float64)
        M = np.zeros(x.size, dtype=np.float64)
        
        # Вызываем функцию
        self.lib.diagram_calc(x, sup1.node.point.x, sup2.node.point.x, x.size, V, M, point_loadsM, distributed_loadsM, momentsM)

        self.lib.Matrix_destroy(point_loadsM)
        self.lib.Matrix_destroy(distributed_loadsM)
        self.lib.Matrix_destroy(momentsM)

        return V, M

    def determinate_system(self):
        pass
    
    def undeterminate_system(self):
        pass
    
    def Mores_integral(self, size, M1Mes, M1Mb):

        A = [[self.lib.Mores_integral(ep1, ep2, size, float(config("DX"))) for ep2 in M1Mes] for ep1 in M1Mes]
        B = [[self.lib.Mores_integral(ep1, M1Mb, size, float(config("DX")))] for ep1 in M1Mes]
        
        return np.array(A), np.array(B)
        
    def solve(self, A, B):
                
        a_cpp = self.create_matrix(A)
        b_cpp = self.create_matrix(B)

        res = self.lib.lin_solve(a_cpp, b_cpp)
        
        X = []
        for i, _ in enumerate(B):
            X.append(self.lib.Matrix_get(res, i, 0))
                
        self.lib.Matrix_destroy(a_cpp)
        self.lib.Matrix_destroy(b_cpp)
        self.lib.Matrix_destroy(res)
        
        return X
    
    def integrate(self, y:np.array):

        result = np.zeros(y.size, dtype=np.float64)
        y = np.array(y)
        self.lib.integrate(y, float(config("DX")), result, len(y), 1)
        
        return result