#include "../include/calculations.h"
#include "matrix.h"
#include <cmath>
#include <cstdio>
#include <iostream>

double integral( double (*func)(double), double a, double b, double step){
  double res = 0;
  for(double i = a; i < b; i+= step){
    std::cout << res << std::endl;
    res += func(i) * step;
  }
  return res;
}

// // Расчёт реакций опор
// Reaction calculateReactions(const Beam& beam) {
//     double total_force = 0.0;
//     double total_moment = 0.0;

//     for (const auto& load : beam.loads) {
//         if (load.is_distributed) {
//             // Считаем эквивалентную силу и её точку приложения
//             double equivalent_force = load.magnitude * load.length;
//             double equivalent_position = load.position + load.length / 2.0;

//             total_force += equivalent_force;
//             total_moment += equivalent_force * equivalent_position;
//         } else {
//             total_force += load.magnitude;
//             total_moment += load.magnitude * load.position;
//         }
//     }

//     double right_reaction = total_moment / beam.length;
//     double left_reaction = total_force - right_reaction;

//     return {left_reaction, right_reaction};
// }

// // Расчёт прогиба в точке x
// double calculateDeflection(const Beam& beam, const Reaction& reactions, double x) {
//     double v = 0.0;

//     for (const auto& load : beam.loads) {
//         if (x < load.position) {
//             continue; // Прогиб из-за нагрузки ещё не влияет
//         }

//         if (load.is_distributed) {
//             double start = load.position;
//             double end = load.position + load.length;

//             if (x <= end) {
//                 // Прогиб из-за распределённой нагрузки в пределах её действия
//                 double q = load.magnitude; // Интенсивность распределённой нагрузки
//                 double a = x - start;
//                 v += (q * a * a * a) / (6 * beam.EI);
//             } else {
//                 // Прогиб из-за полной распределённой нагрузки
//                 double q = load.magnitude;
//                 double L = load.length;
//                 double a = x - start;
//                 v += (q * L * L * L) / (6 * beam.EI);
//             }
//         } else {
//             // Прогиб из-за точечной нагрузки
//             double a = load.position;
//             v += (load.magnitude * std::pow(x - a, 3)) / (6 * beam.EI);
//         }
//     }

//     // Прогиб от реакций
//     v -= (reactions.left * std::pow(x, 3)) / (6 * beam.EI);
//     v += (reactions.right * std::pow(beam.length - x, 3)) / (6 * beam.EI);

//     return v;
// }

void StaticSystem::addDistributedForce(int element_id, double q, double start, double end) {
        distributed_forces.push_back({element_id, q, start, end});
    }

// Добавить узел
void StaticSystem::addNode(double x, double y) {
    nodes.push_back({x, y, static_cast<int>(nodes.size())});
}

// Добавить элемент
void StaticSystem::addElement(int start_node_id, int end_node_id, double stiffness) {
    elements.push_back({start_node_id, end_node_id, stiffness});
}

// Добавить силу
void StaticSystem::addForce(int node_id, double fx, double fy) {
    forces.push_back({node_id, fx, fy});
}

// Добавить момент
void StaticSystem::addMoment(int node_id, double value) {
    moments.push_back({node_id, value});
}

// Рассчитать систему
void StaticSystem::calculate() {
  int n = nodes.size();
  int eq_count = 3 * n;// Уравнения: 2 силы (x, y) + 1 момент на каждый узел
  Matrix stiffness_matrix(eq_count, eq_count);
  std::vector<double> load_vector(eq_count, 0.0);

  // Заполнение вектора нагрузок от сосредоточенных сил
  for (const auto& force : forces) {
      int index_x = 3 * force.node_id;
      int index_y = 3 * force.node_id + 1;
      load_vector[index_x] += force.fx;
      load_vector[index_y] += force.fy;
  }

  // Учет распределенных сил
  for (const auto& df : distributed_forces) {
      const Element& element = elements[df.element_id];
      const Node& start_node = nodes[element.start_node_id];
      const Node& end_node = nodes[element.end_node_id];

      // Длина элемента
      double L = std::sqrt(std::pow(end_node.x - start_node.x, 2) +
                            std::pow(end_node.y - start_node.y, 2));

      // Эквивалентные силы
      double F1 = df.q * L / 2.0;
      double F2 = df.q * L / 2.0;

      // Эквивалентные моменты
      double M1 = df.q * L * L / 12.0;
      double M2 = -df.q * L * L / 12.0;

      // Добавление в вектор нагрузок
      load_vector[3 * element.start_node_id + 1] += F1;
      load_vector[3 * element.end_node_id + 1] += F2;

      load_vector[3 * element.start_node_id + 2] += M1;
      load_vector[3 * element.end_node_id + 2] += M2;
  }



  // Заполнение вектора нагрузок
  for (const auto& force : forces) {
      int index_x = 3 * force.node_id;       // Сила по x
      int index_y = 3 * force.node_id + 1;   // Сила по y
      load_vector[index_x] += force.fx;
      load_vector[index_y] += force.fy;
  }

  for (const auto& moment : moments) {
      int index_moment = 3 * moment.node_id + 2; // Момент
      load_vector[index_moment] += moment.value;
  }

  // Заполнение матрицы жесткости
  for (const auto& element : elements) {
      int start_index = 3 * element.start_node_id;
      int end_index = 3 * element.end_node_id;

      // Пример упрощенной жесткости (диагональный элемент)
      stiffness_matrix[start_index][start_index] += element.stiffness;
      stiffness_matrix[end_index][end_index] += element.stiffness;
  }

  // for (const auto& element : elements) {

  //   double total_force = 0.0;
  //   double total_moment = 0.0;

  //   for (const auto& load : load_vector) {

  //     int index_x = 3 * load.node_id;       // Сила по x
  //     int index_y = 3 * load.node_id + 1;   // Сила по y


  //     total_force += 3 * load_vector[index_y];
  //     total_moment += load_vector[index_y+1];

  //   }

  //   double right_reaction = total_moment / beam.length;
  //   double left_reaction = total_force - right_reaction;

  // }


  // Решение системы уравнений
  // (упрощено для примера)
  std::vector<double> displacements(eq_count, 0.0);

  for (int i = 0; i < eq_count; ++i) {
      if (stiffness_matrix[i][i] != 0) {
          displacements[i] = load_vector[i] / stiffness_matrix[i][i];
      }
  }

  // Вывод результатов
  for (int i = 0; i < n; ++i) {
      std::cout << "Node " << i << ":\n";
      std::cout << "  Displacement X: " << displacements[3 * i] << "\n";
      std::cout << "  Displacement Y: " << displacements[3 * i + 1] << "\n";
      std::cout << "  Rotation (Moment): " << displacements[3 * i + 2] << "\n";
  }
}
