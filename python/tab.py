
from Geometry.Primitives.Arrow import Arrow
from Geometry.Primitives.Circle import Circle
from Geometry.Primitives.Line import Line
from Geometry.Primitives.QBezier import QBezier
from config import config
from dearpygui import dearpygui as dpg
from model import Model

W = int(config("WIDTH"))
H = int(config("HEIGHT"))

def draw(primitive, node_id):
    if isinstance(primitive, Arrow):
        dpg.draw_arrow(
            primitive.p1,
            primitive.p2,
            color=primitive.color,
            thickness=primitive.thickness,
            parent=node_id,
        )
    elif isinstance(primitive, Circle):
        dpg.draw_circle(
            center=primitive.pos,
            radius=primitive.radius,
            color=primitive.color,
            thickness=primitive.thickness,
            parent=node_id,
        )
    elif isinstance(primitive, Line):
        dpg.draw_line(
            primitive.p1,
            primitive.p2,
            color=primitive.color,
            thickness=primitive.thickness,
            parent=node_id,
        )
    elif isinstance(primitive, QBezier):
        dpg.draw_bezier_quadratic(
            primitive.p1,
            primitive.p2,
            primitive.p3,
            color=primitive.color,
            thickness=primitive.thickness,
            parent=node_id,
        )


class Tab:
    def __init__(self, model: Model):

        self.model = model

        self.model = model
        self.drawlist_id = None
        self.draw_layer_id = None

        # Создаем вкладку и все дочерние элементы
        with dpg.tab(label=self.model.name, parent="tab_bar") as self.tab_id:
            with dpg.drawlist(width=W, height=H, parent=self.tab_id) as self.drawlist_id:
                with dpg.draw_layer(parent=self.drawlist_id) as self.draw_layer_id:
                    with dpg.draw_node(parent=self.draw_layer_id) as self.model.draw_node_id:
                        self.draw_model()

    def draw_model(self):
        # Очищаем предыдущие элементы
        self.clear_model()

        if not self.model:
            return

        self.model.update()

        for key, val in self.model.data.items():
            for obj in val:
                for prim in obj.geometry():
                    draw(prim, self.model.draw_node_id)

    def clear_model(self):
        """Удаляет все графические элементы модели"""
        if dpg.does_item_exist(self.model.draw_node_id):
            dpg.delete_item(self.model.draw_node_id, children_only=True)
