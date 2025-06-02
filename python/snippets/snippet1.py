import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

# Параметры
E = 2e11  # модуль упругости (Па)
I = 0.00_000_255  # момент инерции (м^4)
L = 10  # длина балки (м)
dx = 0.0001
x = np.linspace(0, L, 100001)

s = []

with open("lol", "r") as f:
    s = f.readlines()

M = np.array(list(map(lambda x: float(x), s)))

# Нормализуем
M /= (E * I)

# Интегрируем
theta = integrate.cumulative_trapezoid(M, x, initial=0)
v = integrate.cumulative_trapezoid(theta, x, initial=0)

# Нормализация прогиба по граничным условиям
v -= v[0]                      # обнуляем левый конец
v -= np.linspace(0, v[-1], len(v))  # убираем наклон (вторую постоянную)

# --- Графики ---
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(x, theta, label='V(x) — поперечная сила', color='blue')
plt.axhline(0, color='black', linewidth=0.5)
plt.ylabel('V, кН')
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(x, v, label='M(x) — изгибающий момент', color='red')
plt.axhline(0, color='black', linewidth=0.5)
plt.xlabel('x, м')
plt.ylabel('M, кН·м')
plt.grid(True)
plt.legend()

plt.tight_layout()


plt.show()
