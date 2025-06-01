#pragma once
#include <cstdio>
#include "../include/matrix.h"

extern "C" double integral(double (*func)(double), double a, double b, double step = 0.1);
extern "C" void reactions_calc(double &RA, double xa, double &RB, double xb, Matrix* point_loads, Matrix* distributed_loads, Matrix* moments);
extern "C" void diagram_calc(double* x, double xa, double xb, size_t size, double* V, double* M,Matrix* point_loads, Matrix* distributed_loads, Matrix* moments);


// Создает матрицу из плоского массива
extern "C" void* Matrix_create(int rows, int cols);

extern "C" Matrix* Matrix_create_from_data(double** data, size_t rows, size_t cols);
// Удаляет матрицу
extern "C" void Matrix_destroy(void* matrix);

extern "C" void Matrix_set(Matrix* mat, int row, int col, double value);

extern "C" double Matrix_get(Matrix* mat, int row, int col);

extern "C" double Mores_integral(double *A, double *B, size_t size, double dx);

extern "C" Matrix* lin_solve(Matrix* A, Matrix* B);