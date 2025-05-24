import datetime
import numpy as np
import matplotlib.pyplot as plt

L = 6  # длина балки, м
dx = 0.000_001

x = np.arange(0, L + dx, dx)

# --- Нагрузки ---
point_loads = [(4, -30)]  # (позиция, сила в кН)
distributed_loads = [(0, 2, -10)]   # (от, до, q кН/м)
moments = [(2, 20)]                # (позиция, момент в кН·м), отриц — по часовой

# --- Опоры ---
# Предполагаем простую балку: опоры на x=0 (A) и x=L (B)
RA = 0  # реакция на A
RB = 0  # реакция на B

# --- Расчет RB (по моменту относительно точки A) ---
moment_sum = 0

start = datetime.datetime.now()


# Момент от точечных сил
for pos, P in point_loads:
    moment_sum += P * (pos - 0)

# Момент от РРН (вес * плечо до центра)
for x1, x2, q in distributed_loads:
    w = q * (x2 - x1)
    center = (x1 + x2) / 2
    moment_sum += w * (center - 0)

# Момент от сосредоточенных моментов (знаковая сумма)
for pos, M0 in moments:
    moment_sum += M0

RB = -moment_sum / L

# --- RA из равновесия по вертикали ---
total_vertical = sum(P for _, P in point_loads) + sum(q*(x2-x1) for x1, x2, q in distributed_loads)
RA = - total_vertical - RB

# --- Эпюры ---
V = np.zeros_like(x)
M = np.zeros_like(x)

# for ui in u:
for i, xi in enumerate(x):
        v = RA
        m = RA * xi

        for pos, P in point_loads:
            if xi >= pos:
                v += P
                m += P * (xi - pos)

        for x1, x2, q in distributed_loads:
            if xi >= x1:
                if xi <= x2:
                    v += q * (xi - x1)
                    m += q * (xi - x1)**2 / 2
                else:
                    v += q * (x2 - x1)
                    m += q * (x2 - x1) * (xi - (x1 + x2)/2)

        for pos, M0 in moments:
            if xi >= pos:
                m += -M0  # прибавляем сосредоточенный момент

        V[i] = v
        M[i] = m

# --- Графики ---
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(x, V, label='V(x) — поперечная сила', color='blue')
plt.axhline(0, color='black', linewidth=0.5)
plt.ylabel('V, кН')
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

end = datetime.datetime.now()
print("python", end-start)
plt.show()
