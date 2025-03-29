#include "../include/matrix.h"
#include <iostream>
#include <iomanip>

Matrix::Matrix(std::initializer_list<std::initializer_list<double>> init) {
  _m = init.size();
  _n = init.begin()->size();
  for (const auto &row : init) {
    _matrix.emplace_back(row); // Копируем каждую строку в вектор
  }
}

Matrix::Matrix(int n, int m) : _n(n), _m(m) {

  _matrix.reserve(m);
  for (int i = 0; i < m; ++i)
    _matrix.emplace_back(std::vector<double>(n, 0));
}

void Matrix::setIdentityMatrix() {

  for (int i = 0; i < _n; i++) {
    for (int j = 0; j < _m; j++) {
      _matrix[i][j] = i == j;
    }
  }
}

void Matrix::logMatrix() {

    int cellWidth = 10; // Ширина одной ячейки

    // Функция для создания границы
    auto printBorder = [&]() {
        std::cout << "+";
        for (size_t i = 0; i < _n; ++i) {
            std::cout << std::string(cellWidth, '-') << "+";
        }
        std::cout << std::endl;
    };

    // Вывод верхней границы
    printBorder();

    // Вывод строк матрицы
    for (const auto& row : _matrix) {
        std::cout << "|";
        for (double item : row) {
            std::cout << std::setw(cellWidth) << item << "|";
        }
        std::cout << std::endl;

        // Вывод границы после каждой строки
        printBorder();
    }

}

bool Matrix::dimEqual(Matrix other){
  return (other._m == _m && other._n == _n);
}

void Matrix::transpose(){
  
  for(int i = 0; i < _m; i++){
    for(int j = 0; j < i; j++){
      std::swap(_matrix[i][j], _matrix[j][i]);
    }
  }
}

Matrix Matrix::minor(int r, int c) {
  Matrix temp(_n - 1, _m - 1 );
  int a = 0;
  int b = 0;
  for (int i = 0; i < _m; i++) {
    if (i != r) {
      b = 0;
      for (int j = 0; j < _n; j++) {
        if (j != c) {
          temp[a][b] = _matrix[i][j];
          b++;
        }
      }
      a++;
    }
  }
  temp.logMatrix();
  return temp;

}

void Matrix::determinant(){
  if (!std::isnan(_det)){
    return;
  }
  if(_m != _n){
    std::runtime_error("Cannot calculate det for non square matrix");
  }

  switch (_m) {
    case 0:
      _det = 0.;
      break;
    case 1:
      _det = _matrix[0][0];
      break;
    case 2:
      _det = _matrix[0][0] * _matrix[1][1] - _matrix[1][0] * _matrix[0][1];
      break;
    default:
      double det = 0;
      for(int i = 0; i < _m; i++){
        det += _matrix[0][i] * std::pow(-1, i) * minor(0, i).getDeterminant();
      }
      _det = det;
  }
}

void Matrix::inverse(){

  Matrix minors(_n, _m);
  for(int i = 0; i < _m; i++){
    for(int j = 0; j < _n; j++){
      minors[i][j] = pow(-1, i+j) * minor(i, j).getDeterminant();
    }
  }

  Matrix temp = minors.getTranspose() * (1/getDeterminant());
  for(int i = 0; i < _m; i++){
    for(int j = 0; j < _n; j++){
      _matrix[i][j] = temp[i][j];
    }
  }

  _det = std::nan("1");
}

double Matrix::getDeterminant(){
  determinant();
  return _det;
}

Matrix Matrix::getInverse(){
  inverse();
  return *this;
}

Matrix Matrix::getTranspose(){
  transpose();
  return *this;
}

Matrix Matrix::operator*(Matrix other) {

  if (_m != other._n) {
    std::runtime_error("Cannot multply matrix with wrong dimentions");
  }

  Matrix resultMatrix(other._n, _m);
  double sum = 0;
  for (int i = 0; i < _m; i++) {
    for (int j = 0; j < other._n; j++) {
      sum = 0;
      for (int k = 0; k < _n; k++) {
        sum += _matrix[i][k] * other[k][j];
      }
      resultMatrix[i][j] = sum;
    }
  }
  return resultMatrix;
}


Matrix Matrix::operator*(double scalar) {
  Matrix resultMatrix(_n, _m);
  for (int i = 0; i < _m; i++) {
    for (int j = 0; j < _n; j++) {
      resultMatrix[i][j] = _matrix[i][j] * scalar;
    }
  }
  return resultMatrix;
}

void Matrix::operator*=(Matrix other) {

  if (_m != other._n) {
    std::runtime_error("Cannot multply matrix with wrong dimentions");
  }

  Matrix resultMatrix(other._n, _m);
  double sum = 0;
  for (int i = 0; i < _m; i++) {
    for (int j = 0; j < other._n; j++) {
      sum = 0;
      for (int k = 0; k < _n; k++) {
        sum += _matrix[i][k] * other[k][j];
      }
      resultMatrix[i][j] = sum;
    }
  }
  *this = resultMatrix;
}


void Matrix::operator*=(double scalar) {
  Matrix resultMatrix(_n, _m);
  for (int i = 0; i < _m; i++) {
    for (int j = 0; j < _n; j++) {
      resultMatrix[i][j] = _matrix[i][j] * scalar;
    }
  }
  *this = resultMatrix;
}


Matrix Matrix::operator+(Matrix other) {

  if (!dimEqual(other)) {
    std::runtime_error("Cannot multply matrix with wrong dimentions");
  }

  Matrix resultMatrix(other._n, _m);
  for (int i = 0; i < _m; i++) {
    for (int j = 0; j < other._n; j++) {
      resultMatrix[i][j] = _matrix[i][j] + other[i][j];
    }
  }
  return resultMatrix;
}

std::vector<double> &Matrix::operator[](int index) { return _matrix[index]; }

Matrix &Matrix::operator+=(Matrix other) {
  for (int i = 0; i < _m; i++) {
    for (int j = 0; j < other._n; j++) {
      _matrix[i][j] += other[i][j];
    }
  }
  return *this;
}
