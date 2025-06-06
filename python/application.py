import numpy as np
from calculations import Calculations
from data.data import Sortament
from model import Model
from Entities.force import Force
from Entities.diagrams import Diagram
from Entities.fixed import Fixed
from Entities.momentum import Momentum
from Entities.pinned import Pinned
from Entities.roller import Roller
from Geometry.Vector import Vector
from window import Window

sigma = 180e6
E = 2e11  # модуль упругости (Па)

class Application:
    def __init__(self):
        self.current_model: Model = None
        self.calc: Calculations = Calculations()
        self.sortament = Sortament()
        self.w = Window(self)
        self.models: dict = {}
        self.w.run()
        
    def calculate(self):
        
        if self.current_model.dsi < 0:
            raise Exception("DSI < 0; Something went wrong")
        elif self.current_model.dsi == 0:
            print("DSI = 0; Система статически определимая")

        else:
            print("DSI > 0; Система статически неопределима. Переходим к О.С.")
        
        dsi = self.current_model.dsi
        
        eq_models = [self.current_model.copy() for _ in range(dsi)]
        for em in eq_models:
            em.get_loads().clear()

        sups, forces = self.make_determinate()
        
        for i, em in enumerate(eq_models):
            em.get_loads().append(forces[i])
        
        base_model = self.current_model.copy()
        base_model.name += "_diagram"
        base_model.update_data({"supports": sups})
        
        for em in eq_models:
            em.update_data({"supports": sups})

        area = [self.current_model.get_nodes()[0], self.current_model.get_nodes()[-1]]

        M1Vb, M1Mb = self.calc.calc(base_model, sups[0], sups[1])
        self.build_diagram(0, base_model, area[0], area[1], M1Vb)
        self.build_diagram(1, base_model, area[0], area[1], M1Mb)

        self.w.create_tab(base_model)
    
        M1Ves = []
        M1Mes = []
        
        for i, em in enumerate(eq_models):
            M1Ve, M1Me = self.calc.calc(em, sups[0], sups[1])
            M1Ves.append(M1Ve)
            M1Mes.append(M1Me)

        for i, em in enumerate(eq_models):
            em.name = f"X{i+1}_diagram"  
            self.build_diagram(0, em, area[0], area[1], M1Ves[i]) 
            self.build_diagram(1, em, area[0], area[1], M1Mes[i]) 

            self.w.create_tab(em)

        A, B = self.calc.Mores_integral(len(M1Mes[0]) if M1Mes else 0, M1Mes, M1Mb)
        X = self.calc.solve(A, B*-1)
        
        print("Матрица деформаций: \n", A)
        print("Матрица деформаций от внешних нагрузок: \n", B)
        print("Найденные реакции: \n", X)
        
        self.w.add_find_loads(X)
        
        result_model = base_model.copy()
        for i, em in enumerate(eq_models):
            result_model.get_loads().append(Force(-100, em.data.get("loads")[0].node, Vector(0, X[i])))
            
        result_model.name = "result_diagram"
        
        res_A, res_B = self.calc.calc(result_model, sups[0], sups[1])
        
        self.build_diagram(0, result_model, area[0], area[1], res_A)
        self.build_diagram(1, result_model, area[0], area[1], res_B)

        self.w.create_tab(result_model)
        
        bending_model = result_model.copy()
        
        self.calculate_bending(res_B, bending_model, area)
        

    def build_diagram(self, type, model: Model, start_node, end_node, diagram):
        model.diagrams.append(Diagram(1001, type, start_node, end_node, diagram, model))

    def apply_force(self, sup):
        
        forces = []
        
        if isinstance(sup, Fixed):
            forces.append(Force(-10, sup.node, sup.direction.ort()))
            forces.append(Force(-10, sup.node, Vector(sup.direction.ort(), 0)))
            forces.append(Momentum(-10, sup.node, sup.direction.ort()))

        elif isinstance(sup, Pinned):
            forces.append(Force(-10, sup.node, sup.direction.ort()))
            forces.append(Force(-10, sup.node, Vector(sup.direction.ort(), 0)))
        
        elif isinstance(sup, Roller):
            forces.append(Force(-10, sup.node, sup.direction.ort()))

        return forces

    def make_determinate(self):
  
        sups = self.current_model.data.get("supports")
        
        applied_sups = []
        unit_forces = []

        fixed_n = 0
        roller_n = 0
        pinned_n = 0

        for sup in sups:
            if isinstance(sup, Fixed):
                fixed_n += 1
            elif isinstance(sup, Roller):
                roller_n += 1
            elif isinstance(sup, Pinned):
                pinned_n += 1
                    
        if fixed_n == 0 and pinned_n == 0:
            raise Exception("Конструкция является механизмом")

        elif fixed_n != 0:
            for sup in sups:
                if isinstance(sup, Fixed):
                    applied_sups.append(sup)
                    break
            
            for sup in sups:
                if sup not in applied_sups:
                    unit_forces.append(*self.apply_force(sup))
            
        elif pinned_n == 1:
            for sup in sups:
                if isinstance(sup, Pinned):
                    applied_sups.append(sup)
                    
                elif isinstance(sup, Roller):
                    applied_sups.append(sup)
                    break
                
            for sup in sups:
                if sup not in applied_sups:
                    unit_forces.append(*self.apply_force(sup))
        
        elif pinned_n > 1:
            f = 0
            for sup in sups:
                if isinstance(sup, Pinned):
                    applied_sups.append(sup)
                    f = 1
                if f:
                    applied_sups.append(Roller(node=sup.node, direction=sup.direction))
                    break
            for sup in sups:
                if sup not in applied_sups:
                    unit_forces.append(*self.apply_force(sup))
                
        return applied_sups, unit_forces
        
    def calculate_bending(self, M, model: Model, area):
        model.name = "bending_diagram"
        
        minW = abs(M).max()/sigma

        I = self.sortament.find_by_Wx(minW)
        if not I:
            raise Exception("Подходящая балка не найдена по сортаменту")

        # Нормализуем
        M = M / (E * I)
        # # Интегрируем
        theta = self.calc.integrate(M)
        v = self.calc.integrate(theta)

        # Нормализация прогиба по граничным условиям
        v -= v[0]                      # обнуляем левый конец
        v -= np.linspace(0, v[-1], len(v))  # убираем наклон (вторую постоянную)

        model.get_loads().clear()
        model.get_supports().clear()

        self.build_diagram(2, model, area[0], area[1], v)
        self.w.create_tab(model)
    
    def add_model(self, model: Model):
        self.models.update({model.name: model})