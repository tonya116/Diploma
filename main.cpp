#include "include/calculations.h"
#include <iostream>

int main() {

  Matrix A = {
{1, 4, 3},
{2, 1, 5}, 
{3, 2, 1}
  };
  Matrix B = {
{5, 2, 1}, 
{4, 3, 2},
{2, 1, 5}
  };

  A.logMatrix();
  
  // std::cout << A.getDeterminant() << std::endl;


  // B.inverse();
  // B.logMatrix();
  // A.logMatrix();
  // B.logMatrix();
  // Matrix res = A * B;
  // res.logMatrix();

  // (A + B).logMatrix();

  return 0;
}
