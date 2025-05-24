#include "matrix.h"
#include "calculations.h"
#include <cmath>
#include <iostream>

double f(double x){
  double y = 3.14;
  return y;
}

int main() {


  double d11 = 5.33/5;
  double D1p = -15/5;
  std::cout << -D1p / d11;
  Matrix A = {{5.33/5}};

  Matrix B = {{-15/5}};
  A.getInverse().logMatrix();
  Matrix C = A.getInverse() * (B * -1);
  C.logMatrix();

  return 0;
}
