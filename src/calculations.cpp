#include "../include/calculations.h"
#include "matrix.h"
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

extern "C" void reactions_calc(double &RA, double xa, double &RB, double xb, Matrix* point_loads, Matrix* distributed_loads, Matrix* moments) {
  double moment_sum = 0;
  double total_vertical = 0;
  double L = xb - xa;

  for (auto &force : point_loads->_matrix) {
    total_vertical += force[1];
    moment_sum += force[1] * (force[0] - xa);
    
  }
  for (auto &dl : distributed_loads->_matrix) {

    double w = dl[2] * (dl[1] - dl[0]);
    double x = (dl[0] + dl[1]) / 2;
    total_vertical += w;
    moment_sum += w * (x - xa);
    
  }
  for (auto &moment : moments->_matrix) {
    moment_sum += moment[1];
  }

  RB = moment_sum / L; 
  RA = total_vertical - RB;
}

extern "C" void diagram_calc(double *x, double xa, double xb, size_t size, double *V,
                             double *M, Matrix* point_loads, Matrix* distributed_loads, Matrix* moments) {
  double v, m;
  double RA = 0, RB = 0;

  reactions_calc(RA, xa, RB, xb, point_loads, distributed_loads, moments);

  for (int i = 0; i < size; i++) {
    v = 0;
    m = 0;
    if (x[i] >= xa) {
      v += RA;
      m += RA * (x[i] - xa);
    }
    if (x[i] >= xb) {
      v += RB;
      m += RB * (x[i] - xb);
    }
    for (auto &force : point_loads->_matrix) {
      double l = force[0];
      double f = force[1];
      if (x[i] >= l) {
        v -= f;
        m -= f * (x[i] - l);
      }
    }
    for (auto &dl : distributed_loads->_matrix) {
      double start = dl[0];
      double end = dl[1];
      double force = dl[2];
      if (x[i] >= start) {
        double x1 = start;
        double x2 = std::min(x[i], end);
        double l = x2 - x1;
        v -= force * l;
        m -= force * l * (x[i] - (x1 + x2) / 2);

        }
      }
    for (auto &moment : moments->_matrix) {
      double l = moment[0];
      double mom = moment[1];
      if (x[i] >= l) {
        m += mom;
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

extern "C" double Mores_integral(double *A, double *B, size_t size, double dx) {

  double s = 0;
  for (int x = 0; x < size; x++) {
    s += A[x] * B[x];
  }
  return s * dx;
}

extern "C" Matrix* lin_solve(Matrix* A, Matrix* B) {
    
  auto r = A->getInverse() * *B;

  Matrix* res = new Matrix(r);
  return res;
}

extern "C" Matrix* Matrix_create_from_data(double** data, size_t rows, size_t cols) {
  Matrix* matrix = new Matrix(data, rows, cols);
  return matrix;
}

extern "C" void integrate(const double* y, double dx, double* result, size_t size, int initial_zero) {
    if (size < 2) return;

    if (initial_zero)
        result[0] = 0.0;

    for (size_t i = 1; i < size; ++i) {
        double trap = 0.5 * (y[i] + y[i - 1]) * dx;
        result[i] = result[i - 1] + trap;
    }
}
