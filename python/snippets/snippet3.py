import numpy as np
import matplotlib.pyplot as plt

# Параметры балки
L = 10      # длина балки, м
q = 5       # равномерная нагрузка, кН/м
Q = q * L   # суммарная нагрузка

# Реакции опор
RA = q * L / 2
RB = q * L / 2

# Координаты вдоль балки
x = np.linspace(0, L, 500)

# Поперечная сила
V = RA - q * x

# Изгибающий момент
M = RA * x - (q * x**2) / 2

# Построение графиков
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(x, V, label='Поперечная сила V(x)', color='blue')
plt.axhline(0, color='black', linewidth=0.5)
plt.title('Эпюра поперечных сил (равномерная нагрузка)')
plt.ylabel('V, кН')
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(x, M, label='Изгибающий момент M(x)', color='red')
plt.axhline(0, color='black', linewidth=0.5)
plt.title('Эпюра изгибающих моментов (равномерная нагрузка)')
plt.xlabel('x, м')
plt.ylabel('M, кН·м')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
