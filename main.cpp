#include "matrix.h"
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
  
  std::cout << A.getDeterminant() << std::endl;

  (A.getInverse()).logMatrix();


  return 0;
}
