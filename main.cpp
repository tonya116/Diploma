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
  Matrix* point_loads = new Matrix{{3, -28.75}, {7,  93.75}};
  Matrix* distributed_loads = new Matrix{{7, 10, 40}};
  Matrix* moments = new Matrix{{5, 60}};
  double L = 10;
  double dx = 0.01;
  size_t size = (int)(L / dx)+1;
  double x[size];
  double V[size];
  double M[size];

  for (int i = 0; i < size; i++) {
    x[i] = i*dx;
  }

  diagram_calc(L, x, size, V, M, point_loads, distributed_loads, moments);

  for (int i = 0; i < size; i++) {
    printf("%f, %f\n", V[i], M[i]);
  }

  Matrix* A = new Matrix{{4.9, 2.1}, {2.1, 9}};
  Matrix* B = new Matrix{{-8.4, -3.6}};

  auto C = lin_solve(A, B);
  C->logMatrix();
  return 0;
}
