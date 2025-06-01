#include "matrix.h"
#include "calculations.h"
#include <cmath>
#include <cstddef>
#include <iostream>

double f(double x){
  double y = 3.14;
  return y;
}

int main() {  
  Matrix* point_loads = new Matrix{{3, -10}, {4,  2.81}};
  Matrix* distributed_loads = new Matrix{{0, 2, -10}};
  Matrix* moments = new Matrix(0, 0);
  double L = 4;
  double dx = 0.01;
  size_t size = (int)(L / dx)+1;
  double x[size];
  double V[size];
  double M[size];

  for (int i = 0; i < size; i++) {
    x[i] = i*dx;
  }

  diagram_calc(x, 0, 4, size, V, M, point_loads, distributed_loads, moments);

  for (int i = 0; i < size; i++) {
    printf("%f, %f\n", V[i], M[i]);
  }

  return 0;
}
