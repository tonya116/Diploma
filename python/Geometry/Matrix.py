from typing import Union
from Geometry.Vector import Vector
from math import atan2, sin, cos
class Matrix:
    def __init__(self, data):
        """
        Инициализация матрицы.
        :param data: двумерный список (например, [[1, 2], [3, 4]]).
        """
        if not all(len(row) == len(data[0]) for row in data):
            raise ValueError("Все строки матрицы должны иметь одинаковую длину")
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    def __str__(self):
        """Строковое представление матрицы."""
        return '\n'.join([' '.join(map(str, row)) for row in self.data])

    def __add__(self, other):
        """Сложение матриц."""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Матрицы должны быть одного размера")
        result = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __sub__(self, other):
        """Вычитание матриц."""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Матрицы должны быть одного размера")
        result = [
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __mul__(self, other):
        """Умножение матриц (или на скаляр)."""
        if isinstance(other, (int, float)):
            # Умножение на скаляр
            result = [
                [self.data[i][j] * other for j in range(self.cols)]
                for i in range(self.rows)
            ]
            return Matrix(result)
        else:
            # Умножение матриц
            if self.cols != other.rows:
                raise ValueError("Количество столбцов первой матрицы должно равно количеству строк второй")
            result = [
                [
                    sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                    for j in range(other.cols)
                ]
                for i in range(self.rows)
            ]
            return Matrix(result)

    def __matmul__(self, other):
        return self.__mul__(other)

    def transpose(self):
        """Транспонирование матрицы."""
        result = [
            [self.data[j][i] for j in range(self.rows)]
            for i in range(self.cols)
        ]
        return Matrix(result)

    def determinant(self):
        """Вычисление определителя матрицы (рекурсивно)."""
        if self.rows != self.cols:
            raise ValueError("Матрица должна быть квадратной")
        n = self.rows
        
        # Базовый случай: матрица 1x1
        if n == 1:
            return self.data[0][0]
        
        # Базовый случай: матрица 2x2
        if n == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        
        det = 0
        for col in range(n):
            # Минор матрицы без первой строки и col-того столбца
            minor = [
                [self.data[i][j] for j in range(n) if j != col]
                for i in range(1, n)
            ]
            minor_matrix = Matrix(minor)
            # Рекурсивный расчёт определителя минора
            det += (-1) ** col * self.data[0][col] * minor_matrix.determinant()
        return det

    def is_square(self):
        """Проверка, является ли матрица квадратной."""
        return self.rows == self.cols

    
    def inverse(self):
        """Вычисляет обратную матрицу."""
        if not self.is_square():
            raise ValueError("Обратная матрица существует только для квадратных матриц")
        
        det = self.determinant()
        if det == 0:
            raise ValueError("Матрица вырождена (определитель равен 0), обратной не существует")
        
        n = self.rows
        
        # Для матриц 2x2 используем упрощенную формулу
        if n == 2:
            a, b = self.data[0][0], self.data[0][1]
            c, d = self.data[1][0], self.data[1][1]
            inv_det = 1.0 / det
            return Matrix([
                [d * inv_det, -b * inv_det],
                [-c * inv_det, a * inv_det]
            ])
        
        # Для матриц большего размера используем метод алгебраических дополнений
        # Создаем матрицу алгебраических дополнений (союзную матрицу)
        cofactor_matrix = [
            [0 for _ in range(n)] 
            for _ in range(n)
        ]
        
        for i in range(n):
            for j in range(n):
                # Получаем минор для элемента (i,j)
                minor = [
                    [self.data[row][col] for col in range(n) if col != j]
                    for row in range(n) if row != i
                ]
                minor_matrix = Matrix(minor)
                
                # Алгебраическое дополнение
                cofactor = (-1) ** (i + j) * minor_matrix.determinant()
                cofactor_matrix[j][i] = cofactor  # Транспонируем сразу
        
        # Умножаем союзную матрицу на 1/det
        inv_det = 1.0 / det
        inverse_matrix = [
            [cofactor_matrix[i][j] * inv_det for j in range(n)]
            for i in range(n)
        ]
        
        return Matrix(inverse_matrix)
    
    
class TranslationMatrix(Matrix):
    def __init__(self, dirVec: Vector = Vector()):
        self.data = [[1, 0, dirVec.x], [0, 1, dirVec.y], [0, 0, 1]]
        super().__init__(self.data)


class RotationMatrix(Matrix):
    def __init__(self, angle: float = 0, direction: Union[Vector, float] = 1.0):
        """
        Создает 2D матрицу поворота
        
        Параметры:
        - angle: угол поворота в радианах
        - direction: 
          * число 1.0 для поворота против часовой стрелки, -1.0 для обратного направления
          * либо Vector, задающий ось (для совместимости с 3D, но в 2D будет проигнорирован)
        """
        # Для 2D достаточно только угла, направление вращения определяется знаком угла
        cos_theta = cos(angle)
        sin_theta = sin(angle)
        
        # Стандартная 2D матрица поворота
        self.data = [
            [cos_theta, -sin_theta, 0],
            [sin_theta,  cos_theta, 0],
            [0,          0,         1]
        ]
        
        super().__init__(self.data)

    @property
    def rotation_angle(self):
        """Возвращает угол поворота в радианах"""
        return atan2(self.data[1][0], self.data[0][0])


class ScaleMatrix(Matrix):
    def __init__(self, scale: float = 1):
        self.data = [[scale, 0, 0], [0, scale, 0], [0, 0, 1]]
        super().__init__(self.data)
