#pragma once
#include <cstdio>
#include <cmath>
#include "../include/matrix.h"

extern "C" double integral(double (*func)(double), double a, double b, double step = 0.1);
extern "C" void reactions_calc(double& RA, double& RB, const double L);
extern "C" void diagram_calc(double L, double* x, size_t size, double* V, double* M);


// // Создает матрицу из плоского массива
// extern "C" void* create_matrix_from_array(double* data, int rows, int cols);
// // Удаляет матрицу
// extern "C" void delete_matrix(void* matrix);
