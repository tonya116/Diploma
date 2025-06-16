#pragma once

#include <cmath>
#include <vector>

class Matrix {
public:
  int _n; // Rows
  int _m; // Cols
  double _det = std::nan("1");
  std::vector<std::vector<double>> _matrix;

public:
  // Конструкторы
  Matrix();
  Matrix(int n, int m);
  Matrix(std::initializer_list<std::initializer_list<double>> init);
  Matrix(double **data, size_t rows, size_t cols);
  Matrix(Matrix &other);

  // Добавляем метод для создания матрицы из C-массива
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
  int getRows() const;
  int getCols() const;

  void set(int row, int col, double value);
  double get(int row, int col) const;

  Matrix operator*(Matrix other);
  Matrix *operator*(Matrix *other);
  void operator*=(Matrix other);

  Matrix operator*(double scalar);
  void operator*=(double other);

  Matrix operator+(Matrix other);

  std::vector<double> &operator[](int index);
  void operator+=(Matrix other);
};