#pragma once 

#include <vector>
#include <cmath>

class Matrix {
public:
  int _n, _m;
  double _det = std::nan("1");
  std::vector<std::vector<double>> _matrix;

public:
  Matrix() {}
  Matrix(int n, int m);
  Matrix(std::initializer_list<std::initializer_list<double>> init);

  // Добавляем метод для создания матрицы из C-массива
  // static Matrix fromFlatArray(double *data, int rows, int cols);
  void logMatrix();
  bool dimEqual(Matrix other);
  void transpose();
  void determinant();
  void inverse();
  Matrix minor(int r, int c);

  double getDeterminant();
  Matrix getTranspose();
  Matrix getInverse();

  void setIdentityMatrix();

  Matrix operator*(Matrix other);
  void operator*=(Matrix other);

  Matrix operator*(double scalar);
  void operator*=(double other);

  Matrix operator+(Matrix other);

  std::vector<double> &operator[](int index);
  Matrix &operator+=(Matrix other);
};