import numpy as np
import matplotlib.pyplot as plt

# Дано
F = 10  # кН
L = 4   # м
a = 1   # м от левой опоры

# 1. Реакции
R_A = F * (L - a) / L
R_B = F * a / L

# 2. Уравнения усилий
def Q(x):
    return np.where(x < a, R_A, R_A - F)

def M(x):
    return np.where(x < a, R_A * x, R_A * x - F * (x - a))

# 3. Построение эпюр
x = np.linspace(0, L, 100)
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(x, Q(x))
plt.title("Эпюра Q (кН)")

plt.subplot(1, 2, 2)
plt.plot(x, M(x))
plt.title("Эпюра M (кН·м)")

plt.tight_layout()
plt.show()