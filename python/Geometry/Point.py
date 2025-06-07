from Geometry.Vector import Vector
from Geometry.Matrix import Matrix
class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def __add__(self, other: Vector):
        tmp = Point(self.x, self.y)
        tmp.x += other.x
        tmp.y += other.y
        return tmp
    
    def __sub__(self, other):
        tmp = Vector(self.x, self.y)
        tmp.x -= other.x
        tmp.y -= other.y
        return tmp    
    def __matmul__(self, matrix):
        """Умножение 2D точки на матрицу (оператор @)."""
        if not isinstance(matrix, Matrix):
            raise TypeError("Ожидается объект класса Matrix")
        
        # Преобразуем точку в однородные координаты [x, y, 1] для 2D
        homogeneous_point = [self.x, self.y, 1]
        
        # Умножаем матрицу на вектор-столбец
        result = [0] * matrix.cols
        for i in range(matrix.rows):
            for j in range(min(matrix.cols, 3)):  # Обрабатываем только первые 3 элемента
                result[i] += homogeneous_point[j] * matrix.data[i][j]
        
        # Обработка разных размеров матриц
        if matrix.rows == 2 and matrix.cols == 2:
            # Матрица 2x2 (линейное преобразование без трансляции)
            return Point(result[0], result[1])
        elif matrix.rows == 3 and matrix.cols == 3:
            # Матрица 3x3 (аффинное преобразование с трансляцией)
            w = result[2] if result[2] != 0 else 1  # Избегаем деления на 0
            return Point(result[0]/w, result[1]/w)
        else:
            raise ValueError("Матрица должна быть размером 2x2 или 3x3 для 2D преобразований")
            
    def __str__(self):
        return f"Point: x={self.x}, y={self.y}"
    
    def __repr__(self):
        return self.__str__()
    
    def __mul__(self, scalar):
        tmp = Point(self.x, self.y)
        tmp.x *= scalar
        tmp.y *= scalar
        return tmp
    
    def asList(self):
        return [self.x, self.y]
    
    def serialize(self):
        return self.asList()