from Geometry.Point import Point
from Geometry.Primitives.Arrow import Arrow
from Geometry.Primitives.Circle import Circle
from Geometry.Primitives.Line import Line
from Geometry.Primitives.QBezier import QBezier
from Geometry.Primitives.Text import Text
from Geometry.Vector import Vector
from config import config
from dearpygui import dearpygui as dpg
from model import Model

W = int(config("WIDTH"))
H = int(config("HEIGHT"))

class Tab:
    far = 1000
    def __init__(self, model: Model):
        self.factor = 50
        self.model = model
        self.grid = []
        self.drawlist_id = None
        self.draw_layer_id = None
        self.model.set_scale(self.factor)
        s = self.model.get_nodes()[0]
        e = self.model.get_nodes()[-1]
        d = e.direction - s.direction

        self.order = ["supports", "elements", "nodes", "loads"]

        self.model.set_pos(Vector(W // 4 - d.norm() / 2 * self.factor, H // 2))
        # Создаем вкладку и все дочерние элементы
        with dpg.tab(label=self.model.name, parent="tab_bar", closable=True) as self.tab_id:
            with dpg.drawlist(width=W, height=H, parent=self.tab_id) as self.drawlist_id:
                with dpg.draw_layer(parent=self.drawlist_id) as self.draw_layer_id:
                    with dpg.draw_node(parent=self.draw_layer_id) as self.draw_node_id:
                        self.draw_model()

    @staticmethod
    def f(s, a, u):
        print(s, a, u)

    def update_model(self):
        self.model.set_scale(self.factor)

        self.model.update()

        dpg.apply_transform(self.draw_node_id, self.model.model_matrix)

    def draw_model(self):

        if not self.model:
            return

        # Очищаем предыдущие элементы
        self.clear_model()
        self.model.set_scale(self.factor)
        self.update_model()

        for _, val in self.model.data.items():
            for obj in val:
                self.draw_grid(obj.apply_transformation(obj.interest_points))

        for obj in self.model.diagrams:
            self.draw_grid(obj.apply_transformation(obj.interest_points))

        for element in self.order:
            for obj in self.model.data.get(element):
                for prim in obj.geometry():
                    self.draw(prim)

        for obj in self.model.diagrams:
            for prim in obj.geometry():
                self.draw(prim)

    def clear_model(self):
        """Удаляет все графические элементы модели"""
        if dpg.does_item_exist(self.draw_node_id):
            dpg.delete_item(self.draw_node_id, children_only=True)

    def draw_grid(self, interest_points: list[Point]):

        for point in interest_points:
            self.grid.append(
                Line(
                    Point(point.x, self.far).asList(),
                    Point(point.x, -self.far).asList(),
                    eval(config("GridColor")),
                    1,
            ))
            self.grid.append(
                Line(
                    Point(self.far, point.y).asList(),
                    Point(-self.far, point.y).asList(),
                    eval(config("GridColor")),
                    1,
            ))

        for prim in set(self.grid):
            self.draw(prim)

    def draw(self, primitive):
        if isinstance(primitive, Arrow):
            dpg.draw_arrow(
                primitive.p1,
                primitive.p2,
                color=primitive.color,
                thickness=primitive.thickness,
                parent=self.draw_node_id,
                size=0.5,
            )
        elif isinstance(primitive, Circle):
            dpg.draw_circle(
                center=primitive.pos,
                radius=primitive.radius,
                color=primitive.color,
                thickness=primitive.thickness,
                parent=self.draw_node_id,
            )
        elif isinstance(primitive, Line):
            dpg.draw_line(
                primitive.p1,
                primitive.p2,
                color=primitive.color,
                thickness=primitive.thickness,
                parent=self.draw_node_id,
            )
        elif isinstance(primitive, QBezier):
            dpg.draw_bezier_quadratic(
                primitive.p1,
                primitive.p2,
                primitive.p3,
                color=primitive.color,
                thickness=primitive.thickness,
                parent=self.draw_node_id,
            )
        elif isinstance(primitive, Text):
            dpg.draw_text(
                pos=primitive.p1,
                text=primitive.text,
                color=primitive.color,
                size=30,
                parent=self.draw_node_id,
            )