#pragma once
#include <cstdio>
#include <cmath>
#include <iostream>
#include "../include/matrix.h"

extern "C" double integral(double (*func)(double), double a, double b, double step = 0.1);

// // Структура для описания нагрузки
// struct Load {
//     double position; // Позиция приложения нагрузки (м)
//     double magnitude; // Величина нагрузки (Н)
//     bool is_distributed; // Истина, если нагрузка распределённая
//     double length; // Длина распределённой нагрузки (если применимо)
// };

// // Структура для описания балки
// struct Beam {
//     double length; // Длина балки (м)
//     double EI; // Жёсткость балки (Н*м^2)
//     std::vector<Load> loads; // Нагрузки
// };

// // Структура для описания реакций
// struct Reaction {
//     double left; // Реакция левой опоры (Н)
//     double right; // Реакция правой опоры (Н)
// };



// // Расчёт реакций опор
// Reaction calculateReactions(const Beam& beam);
// // Расчёт прогиба в точке x
// double calculateDeflection(const Beam& beam, const Reaction& reactions, double x);




// Узел системы
struct Node {
    double x, y; // Координаты узла
    int id;      // Идентификатор узла
};

// Сила
struct Force {
    int node_id;  // ID узла, к которому приложена сила
    double fx, fy; // Компоненты силы
};

// Момент силы
struct Moment {
    int node_id;   // ID узла, к которому приложен момент
    double value;  // Величина момента (в Н*м)
};

// Распределенная сила
struct DistributedForce {
    int element_id; // ID элемента, на который действует сила
    double q;       // Интенсивность нагрузки (Н/м)
    double start;   // Начальная координата действия нагрузки (относительно длины элемента)
    double end;     // Конечная координата действия нагрузки (относительно длины элемента)
};


// Элемент системы
struct Element {
    int start_node_id, end_node_id; // Узлы, соединенные элементом
    double stiffness;              // Жесткость элемента
};

// Структура для описания реакций
struct Reaction {
    double left; // Реакция левой опоры (Н)
    double right; // Реакция правой опоры (Н)
};

// Статически неопределимая система
class StaticSystem {
private:
    std::vector<Node> nodes;
    std::vector<Element> elements;
    std::vector<Force> forces;
    std::vector<Moment> moments;
    std::vector<DistributedForce> distributed_forces;

public:
    void addDistributedForce(int element_id, double q, double start, double end);
    // Добавить узел
    void addNode(double x, double y);

    // Добавить элемент
    void addElement(int start_node_id, int end_node_id, double stiffness);

    // Добавить силу
    void addForce(int node_id, double fx, double fy) ;

    // Добавить момент
    void addMoment(int node_id, double value) ;

    // Рассчитать систему
    void calculate() ;
};