#pragma once
#include <cstdio>
#include <cmath>
#include "../include/matrix.h"

extern "C" double integral(double (*func)(double), double a, double b, double step = 0.1);
extern "C" void reactions_calc(double& RA, double& RB, const double L);
extern "C" void diagram_calc(double L, double* x, size_t size, double* V, double* M,Matrix* point_loads, Matrix* distributed_loads, Matrix* moments);


// Создает матрицу из плоского массива
extern "C" void* Matrix_create(int rows, int cols);
// Удаляет матрицу
extern "C" void Matrix_destroy(void* matrix);

extern "C" void Matrix_set(Matrix* mat, int row, int col, double value);

extern "C" double Matrix_get(Matrix* mat, int row, int col);