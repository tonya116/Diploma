import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve, integrate, Piecewise

class BeamSolver:
    def __init__(self, L):
        self.L = L  # Длина балки
        self.loads = []  # Список нагрузок
        self.supports = []  # Список опор
        self.x = symbols('x')  # Координата по длине балки

    def add_support(self, pos, type_fix='hinge'):
        """Добавить опору: 'hinge' (шарнир) или 'fixed' (заделка)."""
        self.supports.append({'pos': pos, 'type': type_fix})

    def add_point_load(self, pos, P):
        """Сосредоточенная сила P (вниз = отрицательная)."""
        self.loads.append({'type': 'point', 'pos': pos, 'value': P})

    def add_distributed_load(self, q, x_start=0, x_end=None):
        """Распределённая нагрузка q (по умолчанию на всю балку)."""
        if x_end is None:
            x_end = self.L
        self.loads.append({'type': 'distributed', 'start': x_start, 'end': x_end, 'value': q})

    def solve_reactions(self):
        """Найти реакции опор."""
        R = symbols('R0:%d' % len(self.supports))
        sum_M = 0
        sum_Fy = 0

        # Сумма моментов и сил от нагрузок
        for load in self.loads:
            if load['type'] == 'point':
                sum_M += load['value'] * (load['pos'] - self.supports[0]['pos'])
                sum_Fy += load['value']
            elif load['type'] == 'distributed':
                q, a, b = load['value'], load['start'], load['end']
                sum_M += q * ( (b**2 - a**2)/2 - self.supports[0]['pos']*(b - a) )
                sum_Fy += q * (b - a)

        # Уравнения равновесия
        eq1 = Eq(R[0] + R[1] + sum_Fy, 0)
        eq2 = Eq(R[1] * (self.supports[1]['pos'] - self.supports[0]['pos']) + sum_M, 0)
        reactions = solve((eq1, eq2), R)
        self.reactions = reactions
        return reactions

    def compute_internal_forces(self):
        """Вычислить Q(x) и M(x)."""
        Q = 0
        M = 0

        # Влияние реакций
        for i, sup in enumerate(self.supports):
            r = self.reactions[symbols('R%d' % i)]
            Q += r * Piecewise((1, self.x >= sup['pos']), (0, True))
            M += r * Piecewise((self.x - sup['pos'], self.x >= sup['pos']), (0, True))

        # Влияние нагрузок
        for load in self.loads:
            if load['type'] == 'point':
                P, a = load['value'], load['pos']
                Q += P * Piecewise((1, self.x >= a), (0, True))
                M += P * Piecewise((self.x - a, self.x >= a), (0, True))
            elif load['type'] == 'distributed':
                q, a, b = load['value'], load['start'], load['end']
                Q += q * Piecewise((self.x - a, (self.x >= a) & (self.x <= b)), (b - a, self.x > b), (0, True))
                M += q * Piecewise(((self.x - a)**2/2, (self.x >= a) & (self.x <= b)), 
                                  ((b - a)*(self.x - (a + b)/2), self.x > b), (0, True))

        self.Q = Q
        self.M = M
        return Q, M

    def plot_diagrams(self):
        """Построить эпюры."""
        x_vals = np.linspace(0, self.L, 500)
        Q_vals = [self.Q.subs(self.x, x) for x in x_vals]
        M_vals = [self.M.subs(self.x, x) for x in x_vals]

        plt.figure(figsize=(12, 4))
        plt.subplot(1, 2, 1)
        plt.plot(x_vals, Q_vals, 'r-', linewidth=2)
        plt.title("Эпюра поперечных сил (Q)")
        plt.xlabel("Длина балки (м)")
        plt.ylabel("Q (Н)")
        plt.grid()

        plt.subplot(1, 2, 2)
        plt.plot(x_vals, M_vals, 'b-', linewidth=2)
        plt.title("Эпюра изгибающих моментов (M)")
        plt.xlabel("Длина балки (м)")
        plt.ylabel("M (Н·м)")
        plt.grid()

        plt.tight_layout()
        plt.show()

# Пример использования
if __name__ == "__main__":
    beam = BeamSolver(L=10)  # Балка длиной 10 м
    beam.add_support(pos=0, type_fix='hinge')  # Шарнир в начале
    beam.add_support(pos=8, type_fix='hinge')  # Шарнир на 8 м
    beam.add_point_load(pos=5, P=-5000)  # Сила 5 кН вниз посередине
    beam.add_distributed_load(q=-1000, x_start=2, x_end=6)  # Распределённая нагрузка 1 кН/м

    reactions = beam.solve_reactions()
    print("Реакции опор:", reactions)
    Q, M = beam.compute_internal_forces()
    beam.plot_diagrams()