

from Entities.node import Node
from Entities.object import Object
from Geometry.Primitives.Line import Line
from Geometry.Primitives.Text import Text
from Geometry.Point import Point

from config import config

class Diagram(Object):
    def __init__(self, id: int, start_node: Node, end_node: Node, color, diagram: list[float]):
        super().__init__(id)
        self.start_node = start_node
        self.end_node = end_node
        self.diagram = diagram
        self.color = color

    def geometry(self):
        self.primitives.clear()
        dx = float(config("DX"))
        
        factor = 10
        
        for i, val in enumerate(self.diagram):
            if i == 0:
                self.primitives.append(Text(Point(i*dx, -val/factor).asList(), str(val), eval(config("TextColor")), 3))

            if i == len(self.diagram) // 2:
                self.primitives.append(Text(Point(i*dx, -val/factor).asList(), str(val), eval(config("TextColor")), 3))

            if i == len(self.diagram) - 1:
                self.primitives.append(Text(Point(i*dx, -val/factor).asList(), str(val), eval(config("TextColor")), 3))
                break
            self.primitives.append(
                Line([i * dx, -val/factor], [(i + 1) * dx, -self.diagram[i + 1]/factor], self.color, 1)
            )
        N = 0.5/dx
        # Не оптимально
        for i, val in enumerate(self.diagram):          
            if i % N == 0:
                self.primitives.append(
                    Line([i * dx, -val/factor], [i * dx, 0], self.color, 3)
                )
        return self.primitives
