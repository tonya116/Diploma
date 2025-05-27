#include "../include/calculations.h"
#include "matrix.h"
#include <cmath>
#include <cstddef>
#include <cstdio>
#include <iostream>
#include <vector>

double integral(double (*func)(double), double a, double b, double step) {
  double res = 0;
  for (double i = a; i < b; i += step) {
    std::cout << res << std::endl;
    res += func(i) * step;
  }
  return res;
}

extern "C" void reactions_calc(double &RA, double &RB, const double L, Matrix* point_loads, Matrix* distributed_loads, Matrix* moments) {
  double moment_sum = 0;
  double center;


  for (auto &force : point_loads->_matrix) {
    moment_sum += force[1] * (force[0] - 0);
  }
  for (auto &dl : distributed_loads->_matrix) {
    double w = dl[2] * (dl[1] - dl[0]);
    double center = (dl[0] + dl[1]) / 2;
    moment_sum += w * (center - 0);
  }
  for (auto &moment : moments->_matrix) {
    moment_sum += moment[1];
  }

  RB = -moment_sum / L; 

  double total_vertical = 0;

  for (auto &force : point_loads->_matrix) {
    total_vertical += force[1];
  }
  for (auto &dl : distributed_loads->_matrix) {
    total_vertical += dl[2] * (dl[1] - dl[0]);
  }

  RA = -total_vertical - RB;
}

extern "C" void diagram_calc(double L, double *x, size_t size, double *V,
                             double *M, Matrix* point_loads, Matrix* distributed_loads, Matrix* moments) {
  double v, m;

  for (int i = 0; i < size; i++) {
    v = 0;
    m = 0;
    for (auto &force : point_loads->_matrix) {
      if (x[i] >= force[0]) {
        v += force[1];
        m += force[1] * (x[i] - force[0]);
      }
    }
    for (auto &dl : distributed_loads->_matrix) {
      if (x[i] >= dl[0]) {
        if (x[i] <= dl[1]) {
          v += dl[2] * (x[i] - dl[0]);
          m += dl[2] * powf(x[i] - dl[0], 2) / 2;
        } else {
          v += dl[2] * (dl[1] - dl[0]);
          m += dl[2] * (dl[1] - dl[0]) * (x[i] - (dl[0] + dl[1]) / 2);
        }
      }
    }
    for (auto &moment : moments->_matrix) {

      if (x[i] >= moment[0]) {
        m += -moment[1];
      }
    }

    V[i] = v;
    M[i] = m;
  }
}

extern "C" void* Matrix_create(int rows, int cols) {
    Matrix* mat = new Matrix(rows, cols);
    return static_cast<void*>(mat);
}

extern "C" void Matrix_destroy(void* matrix) {
    delete static_cast<Matrix*>(matrix);
}

extern "C" void Matrix_set(Matrix* mat, int row, int col, double value) {
  mat->set(row, col, value);
}

extern "C" double Matrix_get(Matrix* mat, int row, int col) {
  return mat->get(row, col);
}