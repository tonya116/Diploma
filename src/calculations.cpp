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

extern "C" void reactions_calc(double &RA, double &RB, const double L) {
  double moment_sum = 0;
  double center;

  std::vector<std::vector<double>> point_loads = {{4, -30}};
  std::vector<std::vector<double>> distributed_loads = {{0, 2, -10}};
  std::vector<std::vector<double>> moments = {{2, 20}};

  for (auto &force : point_loads) {
    moment_sum += force[1] * (force[0] - 0);
  }
  for (auto &dl : distributed_loads) {
    double w = dl[2] * (dl[1] - dl[0]);
    double center = (dl[0] + dl[1]) / 2;
    moment_sum += w * (center - 0);
  }
  for (auto &moment : moments) {
    moment_sum += moment[1];
  }

  RB = -moment_sum / L;

  double total_vertical = 0;

  for (auto &force : point_loads) {
    total_vertical += force[1];
  }
  for (auto &dl : distributed_loads) {
    total_vertical += dl[2] * (dl[1] - dl[0]);
  }

  RA = -total_vertical - RB;
}

extern "C" void diagram_calc(double L, double *x, size_t size, double *V,
                             double *M) {
  double v, m;

  std::vector<std::vector<double>> point_loads = {{4, -30}};
  std::vector<std::vector<double>> distributed_loads = {{0, 2, -10}};
  std::vector<std::vector<double>> moments = {{2, 20}};

  double RA = 0, RB = 0;
  reactions_calc(RA, RB, L);

  for (int i = 0; i < size; i++) {
    v = RA;
    m = RA * x[i];
    for (auto &force : point_loads) {
      if (x[i] >= force[0]) {
        v += force[1];
        m += force[1] * (x[i] - force[0]);
      }
    }
    for (auto &dl : distributed_loads) {
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
    for (auto &moment : moments) {

      if (x[i] >= moment[0]) {
        m += -moment[1];
      }
    }

    V[i] = v;
    M[i] = m;
  }
}

// extern "C" void* create_matrix_from_array(double* data, int rows, int cols) {
//     Matrix* mat = new Matrix();
//     *mat = mat->fromFlatArray(data, rows, cols);
//     return static_cast<void*>(mat);
// }

// extern "C" void delete_matrix(void* matrix) {
//     delete static_cast<Matrix*>(matrix);
// }