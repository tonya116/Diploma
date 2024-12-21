#include "matrix.h"
#include <iostream>

int main() {

  Matrix A = {
{1, 4, 3},
{2, 1, 5}, 
{3, 2, 1}
  };
  Matrix B = {
{5}, 
{4},
{2}
  };

  Matrix res = A.getInverse() * B;
  res.logMatrix();

  return 0;
}
