import numpy as np


def stiffness_matrix(E, A, L):
    """Локальная матрица жёсткости элемента"""
    k = (E * A / L) * np.array([[1, -1], [-1, 1]])
    return k


def assemble_global_stiffness(elements, nodes, E, A):
    """Построение глобальной матрицы жёсткости"""
    size = len(nodes) * 2
    K = np.zeros((size, size))

    for element in elements:
        start, end = element
        L = np.linalg.norm(np.array(nodes[end]) - np.array(nodes[start]))
        k = stiffness_matrix(E, A, L)

        # Узлы элемента
        dof = [start * 2, start * 2 + 1, end * 2, end * 2 + 1]

        # Добавление в глобальную матрицу
        for i in range(2):
            for j in range(2):
                K[dof[i], dof[j]] += k[i, j]

    return K


def apply_boundary_conditions(K, F, fixed_dofs):
    """Учет граничных условий"""
    for dof in fixed_dofs:
        K[dof, :] = 0
        K[:, dof] = 0
        K[dof, dof] = 1
        F[dof] = 0
    return K, F


def solve_displacements(nodes, elements, E, A, forces, fixed_dofs):
    """Решение системы уравнений"""
    K = assemble_global_stiffness(elements, nodes, E, A)
    F = np.zeros(len(nodes) * 2)

    for dof, force in forces.items():
        F[dof] = force

    K, F = apply_boundary_conditions(K, F, fixed_dofs)
    u = np.linalg.solve(K, F)  # Решение системы K * u = F
    return u


# Входные данные
nodes = [(0, 0), (0, 5), (5, 5)]  # Координаты узлов
elements = [(0, 1), (1, 2)]  # Связи между узлами
E = 210e9  # Модуль упругости
A = 0.01  # Площадь сечения
forces = {1: -1000}  # Сила, приложенная в узле 1
fixed_dofs = [0, 3]  # Граничные условия: узлы 0 и 1 зафиксированы

u = solve_displacements(nodes, elements, E, A, forces, fixed_dofs)
print("Перемещения узлов:", u)
