#include "../include/calculations.h"
// #include "../include/matrix.h"
#include <cmath>
#include <cstdio>

void print_info(double arr[], size_t size) {
  for (size_t i = 0; i < size; ++i)
    printf("%f\n", arr[i]);
}


std::vector<double> &Matrix::operator[](int index) { return _matrix[index]; }
