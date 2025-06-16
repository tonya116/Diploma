

from Entities.node import Node
from Entities.object import Object
from Geometry.Point import Point
from Geometry.Primitives.Line import Line
from Geometry.Primitives.Text import Text
from config import config


class Diagram(Object):
    def __init__(self, id: int, type: str, start_node: Node, end_node: Node, diagram: list[float]):
        super().__init__(id)
        self.type = type
        self.start_node = start_node
        self.end_node = end_node
        self.diagram = list(diagram)
        self.factor = 10

        match (self.type):
            case 0:
                self.color = eval(config("QDiagramColor"))
            case 1:
                self.color = eval(config("MDiagramColor"))
            case _:
                self.color = eval(config("BDiagramColor"))

        if self.type == 2:
            self.factor = 1e-14
        self.interest_points.append(
            Point(
                self.diagram.index(max(self.diagram)) * float(config("DX")),
                -max(self.diagram) / self.factor,
        ))
        self.interest_points.append(
            Point(
                self.diagram.index(min(self.diagram)) * float(config("DX")),
                -min(self.diagram) / self.factor,
        ))
        self.interest_points.append(Point(0, self.diagram[0] / self.factor))
        self.interest_points.append(
            Point((len(diagram) - 1) * float(config("DX")), self.diagram[-1] / self.factor)
        )

    def geometry(self):
        self.primitives.clear()
        dx = float(config("DX"))

        for point in self.interest_points:
            self.primitives.append(
                Text(
                    (point).asList(),
                    f"{-point.y*(10 if self.type != 2 else 1):.3}",
                    eval(config("TextColor")),
                    3,
            ))
        for i, val in enumerate(self.diagram):
            if i == len(self.diagram) - 1:
                break
            self.primitives.append(
                Line(
                    [i * dx, -val / self.factor],
                    [(i + 1) * dx, -self.diagram[i + 1] / self.factor],
                    self.color,
                    2,
            ))
        n = 50

        if self.type != 2:
            for i in range(0, len(self.diagram), n):
                if i % n == 0:
                    self.primitives.append(
                        Line([i * dx, -self.diagram[i] / self.factor], [i * dx, 0], self.color, 1)
                    )

        return self.primitives
