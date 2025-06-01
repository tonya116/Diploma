from matplotlib import pyplot as plt
import numpy as np


L = 4  # длина балки, м

point_loads = []  # (позиция, сила в кН)
distributed_loads = [(0, 2, 4)]   # (от, до, q кН/м)

pos_RA = 0
pos_RB = 4
dx = 0.01

x = np.arange(0, L + dx, dx)

moment = 0

Q = np.zeros(x.size)
M = np.zeros(x.size)
for i, xi in enumerate(x):

    for pos, P in point_loads:
        if xi > pos:
            Q[i] += P
            
    for s, e, q in distributed_loads:
        if xi > s and xi < e:
            Q[i] += q * (xi - s)


    for pos, P in point_loads:
        if xi > pos:
            M[i] += P * pos

    for x1, x2, q in distributed_loads:
        if xi >= x1:
            if xi <= x2:
                Q[i] += q * (xi - x1)
                M[i] += q * (xi - x1)**2 / 2
            else:
                Q[i] += q * (x2 - x1)
                M[i] += q * (x2 - x1) * (xi - (x1 + x2)/2)



plt.subplot(2, 1, 1)
plt.plot(x, Q, label='Q(x)', color='blue')
plt.axhline(0, color='black', linewidth=0.5)
plt.xlabel('x, м')
plt.ylabel('M, кН·м')
plt.grid(True)
plt.legend()


plt.subplot(2, 1, 2)
plt.plot(x, M, label='M(x) — изгибающий момент', color='red')
plt.axhline(0, color='black', linewidth=0.5)
plt.xlabel('x, м')
plt.ylabel('M, кН·м')
plt.grid(True)
plt.legend()


plt.tight_layout()

plt.show()
