#include "matrix.h"
#include "calculations.h"
#include <cmath>
#include <iostream>

double f(double x){
  double y = 3.14;
  return y;
}

int main() {

  Matrix A(3, 3);
  A.setIdentityMatrix();

  A.logMatrix();

  Matrix B = {{0, 1, 2}, 
              {3, 4, 5},
              {6, 7, 8}};

  Matrix C = B*B;
  C.logMatrix();

  // StaticSystem system;

  // // Добавление узлов
  // system.addNode(0, 0);
  // system.addNode(2, 0);
  // system.addNode(4, 0);
  // system.addNode(6, 0);

  // // Добавление элемента2
  // system.addElement(0, 3, 1000);

  // system.addForce(2, 0, -30);
  // // Добавление распределенной силы (интенсивность 10 Н/м на всем элементе)
  // system.addDistributedForce(0, -10, 0, 1);
  // system.addMoment(1, 20);

  // // Рассчитать систему
  // system.calculate();

  return 0;
}
