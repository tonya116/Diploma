

from Entities.node import Node
from Entities.object import Object
from Geometry.Primitives.Line import Line


class Diagram(Object):
    def __init__(self, id: int, start_node: Node, end_node: Node, diagram: list[float]):
        super().__init__(id)
        self.start_node = start_node
        self.end_node = end_node
        self.diagram = diagram

    def geometry(self):
        self.primitives.clear()
        for i, val in enumerate(self.diagram):
            if i == len(self.diagram) - 1:
                break
            self.primitives.append(
                Line([i / 10, -val, 0], [(i + 1) / 10, -self.diagram[i + 1], 0], (255, 255, 255), 1)
            )
        N = 50        
        # Не оптимально
        for i, val in enumerate(self.diagram):          
            if i % N == 0:
                self.primitives.append(
                    Line([i / 10, -val, 0], [i / 10, 0, 0], (255, 255, 255), 3)
                )
        return self.primitives
