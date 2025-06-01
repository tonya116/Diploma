import datetime
import numpy as np
import matplotlib.pyplot as plt

dx = 0.001

L = 10  # длина балки, м
# --- Нагрузки ---
point_loads = [(3, -28.75), (7, 93.75)]  # (позиция, сила в кН)
distributed_loads = [(7, 10, 40)]   # (от, до, q кН/м)
moments = [(5, 60)]                # (позиция, момент в кН·м), отриц — по часовой

# L = 4  # длина балки, м

# point_loads = [(4, 1)]  # (позиция, сила в кН)
# distributed_loads = []   # (от, до, q кН/м)
# moments = []  

# L = 3  # длина балки, м
# point_loads = [(1, 10)]  # (позиция, сила в кН)
# distributed_loads = [(1, 2, 10)]   # (от, до, q кН/м)
# moments = [(2, -10)]    


pos_RA = 0
pos_RB = 10

x = np.arange(0, L + dx, dx)
start = datetime.datetime.now()

def Reactions():
        # --- Опоры ---
    # Предполагаем простую балку: опоры на x=0 (A) и x=L (B)
    RA = 0  # реакция на A
    RB = 0  # реакция на B

    # --- Расчет RB (по моменту относительно точки A) ---
    moment_sum = 0
    total_vertical = 0
    
    for pos, P in point_loads:
        total_vertical += P
        moment_sum += P * pos

    for x1, x2, q in distributed_loads:
        w = q * (x2 - x1)
        center = (x1 + x2) / 2
        total_vertical += w
        moment_sum += w * center

    # Момент от сосредоточенных моментов (знаковая сумма)
    for pos, M0 in moments:
        moment_sum += M0

    RB = moment_sum / pos_RB
    # --- RA из равновесия по вертикали ---
    RA = -total_vertical + RB
    
    print(RA, RB)
    return RA, RB

RA, RB = Reactions()

# point_loads.append((pos_RA, RA))
# point_loads.append((pos_RB, RB))

# --- Эпюры ---
V = np.zeros_like(x)
M = np.zeros_like(x)

# for ui in u:
for i, xi in enumerate(x):
    
    V[i] = RA
    M[i] = RA * xi
    
    for pos, P in point_loads:
        if xi >= pos:
            V[i] += P
            M[i] += P * (xi - pos)

    for x1, x2, q in distributed_loads:
        if xi >= x1:
            if xi <= x2:
                V[i] += q * (xi - x1)
                M[i] += q * (xi - x1)**2 / 2
            else:
                V[i] += q * (x2 - x1)
                M[i] += q * (x2 - x1) * (xi - (x1 + x2)/2)

    for pos, M0 in moments:
        if xi >= pos:
            M[i] += M0  # прибавляем сосредоточенный момент



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
