import numpy as np
import matplotlib.pyplot as plt

class Beam:
    def __init__(self, length, num_points=1000):
        """
        Инициализация балки.
        :param length: Длина балки (м).
        :param num_points: Количество точек для расчёта.
        """
        self.length = length
        self.num_points = num_points
        self.x = np.linspace(0, length, num_points)
        self.forces = []       # Список сосредоточенных сил: (position, value)
        self.moments = []      # Список моментов: (position, value)
        self.distributed = []  # Список распределённых нагрузок: (start, end, value)

    def add_force(self, position, value):
        """Добавить сосредоточенную силу (кН)."""
        self.forces.append((position, value))

    def add_moment(self, position, value):
        """Добавить внешний момент (кН·м)."""
        self.moments.append((position, value))

    def add_distributed_load(self, start, end, value):
        """Добавить равномерно распределённую нагрузку (кН/м)."""
        self.distributed.append((start, end, value))

    def calculate_reactions(self):
        """Рассчитать реакции опор (для консольной балки)."""
        R = 0
        M = 0
        
        # Сумма сил и моментов от сосредоточенных нагрузок
        for pos, val in self.forces:
            R += val
            M += val * pos
        
        # Сумма моментов от распределённых нагрузок
        for start, end, val in self.distributed:
            length = end - start
            R += val * length
            M += val * length * (start + length/2)
        
        # Сумма внешних моментов
        for pos, val in self.moments:
            M += val
        
        return R, M

    def calculate_internal_forces(self):
        """Рассчитать поперечные силы Q и изгибающие моменты M."""
        Q = np.zeros_like(self.x)
        M = np.zeros_like(self.x)
        
        # Реакции (для консоли: R_A и M_A в заделке)
        R_A, M_A = self.calculate_reactions()
        
        # Учёт реакций
        Q += R_A
        M += M_A - R_A * self.x
        
        # Сосредоточенные силы
        for pos, val in self.forces:
            mask = self.x >= pos
            Q[mask] -= val
            M[mask] += val * (self.x[mask] - pos)
        
        # Распределённые нагрузки
        for start, end, val in self.distributed:
            mask = (self.x >= start) & (self.x <= end)
            Q[mask] -= val * (self.x[mask] - start)
            M[mask] += 0.5 * val * (self.x[mask] - start)**2
            
            mask = self.x > end
            Q[mask] -= val * (end - start)
            M[mask] += val * (end - start) * (self.x[mask] - (start + end)/2)
        
        # Внешние моменты
        for pos, val in self.moments:
            mask = self.x >= pos
            M[mask] -= val
        
        return Q, M

    def plot_diagrams(self):
        """Построить эпюры Q и M."""
        Q, M = self.calculate_internal_forces()
        
        plt.figure(figsize=(12, 6))
        
        # Эпюра Q
        plt.subplot(1, 2, 1)
        plt.plot(self.x, Q, 'r-', linewidth=2)
        plt.fill_between(self.x, Q, alpha=0.3, color='red')
        plt.title("Эпюра поперечных сил Q (кН)")
        plt.xlabel("Длина балки (м)")
        plt.grid(True)
        
        # Эпюра M
        plt.subplot(1, 2, 2)
        plt.plot(self.x, M, 'b-', linewidth=2)
        plt.fill_between(self.x, M, alpha=0.3, color='blue')
        plt.title("Эпюра изгибающих моментов M (кН·м)")
        plt.xlabel("Длина балки (м)")
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()

# Пример использования
if __name__ == "__main__":
    beam = Beam(length=6, num_points=1000)
    
    # Добавляем нагрузки
    beam.add_force(position=2, value=10)          # Сосредоточенная сила 10 кН на 2 м
    beam.add_distributed_load(start=3, end=5, value=4)  # Распределённая нагрузка 4 кН/м от 3 до 5 м
    beam.add_moment(position=4, value=8)          # Момент 8 кН·м на 4 м
    
    # Расчёт и построение эпюр
    beam.plot_diagrams()