#include "../include/matrix.h"
#include <cstddef>
#include <iostream>
#include <iomanip>
#include <vector>

Matrix::Matrix(std::initializer_list<std::initializer_list<double>> init) {
  _n = init.size();
  _m = init.begin()->size();
  for (const auto &row : init) {
    _matrix.emplace_back(row); // Копируем каждую строку в вектор
  }
}

Matrix::Matrix(double **data, size_t rows, size_t cols) {
  _n = rows;
  _m = cols;
  for (int i = 0; i < rows; ++i) {
    _matrix.emplace_back(std::vector<double>(cols));
    for (int j = 0; j < cols; ++j) {
      _matrix[i].emplace_back(data[i][j]); // Копируем каждую строку в вектор
    }
  }
}

Matrix::Matrix()
 :_n(0)
 ,_m(0)
 {
  _matrix.reserve(1);
  for (int i = 0; i < 1; ++i)
    _matrix.emplace_back(std::vector<double>(1, -1));
}

Matrix::Matrix(Matrix& other) {
  _n = other._n;
  _m = other._m;
  _det = other._det;
  _matrix = other._matrix;
}

Matrix::Matrix(int n, int m) : _n(n), _m(m) {

  _matrix.reserve(n);
  for (int i = 0; i < n; ++i)
    _matrix.emplace_back(std::vector<double>(m, 0));
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
  
  for(int i = 0; i < _n; i++){
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

  switch (_n) {
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
  for(int i = 0; i < _n; i++){
    for(int j = 0; j < _m; j++){
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
  auto tmp = Matrix(*this);
  tmp.inverse();
  return tmp;
}

Matrix Matrix::getTranspose(){
  auto tmp = Matrix(*this);
  tmp.transpose();
  return tmp;
}

Matrix Matrix::operator*(Matrix other) {

  if (_m != other._n) {
    std::runtime_error give_me_a_name("Cannot multply matrix with wrong dimentions");
    return Matrix();
  }

  Matrix resultMatrix(_n, other._m);
  double sum = 0;
  for (int i = 0; i < _n; i++) {
    for (int j = 0; j < other._m; j++) {
      sum = 0;
      for (int k = 0; k < _m; k++) {
        sum += _matrix[i][k] * other[k][j];
      }
      resultMatrix[i][j] = sum;
    }
  }
  return resultMatrix;
}


Matrix* Matrix::operator*(Matrix* other) {

  if (_m != other->_n) {
    std::runtime_error("Cannot multply matrix with wrong dimentions");
  }

  Matrix* resultMatrix = new Matrix(_n, other->_m);
  double sum = 0;
  for (int i = 0; i < _n; i++) {
    for (int j = 0; j < other->_m; j++) {
      sum = 0;
      for (int k = 0; k < _m; k++) {
        sum += _matrix[i][k] * other->_matrix[k][j];
      }
      resultMatrix->_matrix[i][j] = sum;
    }
  }
  return resultMatrix;
}

Matrix Matrix::operator*(double scalar) {
  Matrix resultMatrix(_n, _m);
  for (int i = 0; i < _n; i++) {
    for (int j = 0; j < _m; j++) {
      resultMatrix[i][j] = _matrix[i][j] * scalar;
    }
  }
  return resultMatrix;
}

void Matrix::operator*=(Matrix other) {
  
  *this = *this * other;
}


void Matrix::operator*=(double scalar) {
  Matrix resultMatrix(_n, _m);
  for (int i = 0; i < _n; i++) {
    for (int j = 0; j < _m; j++) {
      resultMatrix[i][j] = _matrix[i][j] * scalar;
    }
  }
  *this = resultMatrix;
}


Matrix Matrix::operator+(Matrix other) {

  if (!dimEqual(other)) {
    std::runtime_error("Cannot add matrix with wrong dimentions");
  }

  Matrix resultMatrix(other._n, _m);
  for (int i = 0; i < _n; i++) {
    for (int j = 0; j < _m; j++) {
      resultMatrix[i][j] = _matrix[i][j] + other[i][j];
    }
  }
  return resultMatrix;
}

std::vector<double> &Matrix::operator[](int index) { return _matrix[index]; }

void Matrix::operator+=(Matrix other) {
  *this = *this * other;
}

void Matrix::set(int row, int col, double value) { _matrix[row][col] = value; }
double Matrix::get(int row, int col) const { return _matrix[row][col]; }

int Matrix::getRows() const {
  return _n;
}
int Matrix::getCols() const {
  return _m;
}
