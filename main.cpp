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


  // Matrix E(D);
  // E.logMatrix();

  // std::cout << E.dimEqual(B) << std::endl;

  // D.transpose();
  // D.logMatrix();

  // std::cout << C.getDeterminant() << " " << std::endl;


  // C.inverse();
  // C.logMatrix();
  Matrix A{{14.7, 12.3}, {12.3, 14.7}};
  Matrix B{{-731}, { -1025}};
  
  auto C = lin_solve(&A, &B);
  C->logMatrix();
  return 0;
}
