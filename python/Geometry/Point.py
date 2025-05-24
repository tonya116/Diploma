from Geometry.Vector import Vector
from Geometry.Matrix import Matrix
class Point:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
        
    def __dict__(self):
        return [self.x, self.y, self.z]
    def __add__(self, other):
        tmp = Point(self.x, self.y, self.z)
        tmp.x += other.x
        tmp.y += other.y
        tmp.z += other.z
        return tmp
    
    def __sub__(self, other):
        tmp = Vector(self.x, self.y, self.z)
        tmp.x -= other.x
        tmp.y -= other.y
        tmp.z -= other.z
        return tmp    
    
    def __matmul__(self, matrix):
        """Умножение точки на матрицу (используется оператор @)."""
        if not isinstance(matrix, Matrix):
            raise TypeError("Ожидается объект класса Matrix")
        
        # Преобразуем точку в однородные координаты [x, y, z, 1]
        homogeneous_point = [self.x, self.y, self.z, 1]
        
        # Умножаем матрицу на вектор-столбец (транспонируем точку)
        result = [0] * matrix.cols
        for i in range(matrix.rows):
            for j in range(matrix.cols):
                result[i] += homogeneous_point[j] * matrix.data[i][j]
        
        # Если матрица 3x3 (без трансляции), отбрасываем последний элемент
        if matrix.rows == 3 and matrix.cols == 3:
            return Point(result[0], result[1], result[2])
        # Для матрицы 4x4 (с трансляцией) нормализуем однородные координаты
        elif matrix.rows == 4 and matrix.cols == 4:
            w = result[3]
            return Point(result[0]/w, result[1]/w, result[2]/w)
        else:
            raise ValueError("Матрица должна быть размером 3x3 или 4x4")
        
        
    def __str__(self):
        return f"Point: x={self.x}, y={self.y}, z={self.z}"
    
    def __repr__(self):
        print(self.__str__())
    
    def asList(self):
        return [self.x, self.y, self.z]