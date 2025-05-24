import numpy as np
import matplotlib.pyplot as plt

# Параметры балки
L = 4  # длина балки, м
P = 10  # сила, кН
a = 3  # расстояние до силы от левой опоры

# Реакции опор (по уравнениям равновесия)
RA = P * (L - a) / L  # реакция в A
RB = P * a / L        # реакция в B

# Координаты по длине балки
x = np.linspace(0, L, 500)

# Поперечная сила V(x)
V = np.piecewise(x, [x < a, x >= a], [lambda x: RA, lambda x: RA - P])

# Изгибающий момент M(x)
M = np.piecewise(x, [x < a, x >= a],
                 [lambda x: RA * x,
                  lambda x: RA * x - P * (x - a)])

# Построение графиков
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(x, V, label='Поперечная сила V(x)', color='blue')
plt.axhline(0, color='black', linewidth=0.5)
plt.title('Эпюра поперечных сил')
plt.ylabel('V, кН')
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(x, M, label='Изгибающий момент M(x)', color='red')
plt.axhline(0, color='black', linewidth=0.5)
plt.title('Эпюра изгибающих моментов')
plt.xlabel('x, м')
plt.ylabel('M, кН·м')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
