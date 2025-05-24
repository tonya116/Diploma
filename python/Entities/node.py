
from Geometry.Vector import Vector
from Geometry.Point import Point
from Geometry.Primitives.Circle import Circle
from config import config
from Geometry.Matrix import TranslationMatrix
from .object import Object
from pydantic import BaseModel
from typing import Dict, Any


class NodeModel(BaseModel):
    id: int  # или str, в зависимости от типа вашего id
    coordinates: list[float]  # или создайте отдельную модель для Point

class Node(Object):
    def __init__(self, id, point:Point):
        super().__init__(id)
        self.point:Point = point
        self.ctrlPoints.append(Point())

    def __str__(self):
        return f"ID: {self.id}, Point: {self.point}"
    
    def __repr__(self):
        return self.__dict__()
    
    def __dict__(self):
        return {"id": self.id, "coordinates": self.point.__dict__()}
    
    def geometry(self):
        self.primitives.clear()

        mt = TranslationMatrix(self.point)
        for i in range(len(self.ctrlPoints)):
            self.ctrlPoints[i] = self.ctrlPoints[i] @ mt
        self.primitives.append(Circle(self.ctrlPoints[0].asList(), 5, eval(config("NodeColor")), 5))

        return self.primitives
    
    def to_pydantic(self) -> 'NodeModel':
        return NodeModel(**self.__dict__())
    
    @classmethod
    def from_pydantic(cls, node_model: 'NodeModel'):
        # Предполагая, что Point может быть создан из словаря coordinates
        point = Point(*node_model.coordinates)
        return cls(node_model.id, point)
    
    
if __name__ == "__main__":
    # Создаем экземпляр Node
    point = Point(x=10, y=20)  # предположим, что Point принимает x и y
    node = Node(id=1, point=point)
    
    # Преобразуем в Pydantic-модель и затем в JSON
    node_model = node.to_pydantic()
    
    print(node_model.__str__())
    
    json_str = node_model.model_dump_json(indent=2)
    print(json_str)
    
    # Сохраняем в файл
    with open("test.txt", "w") as f:
        f.write(json_str)
    
    # Загружаем из файла и создаем Node
    with open("test.txt", "r") as f:
        loaded_model = NodeModel.model_validate_json(f.read())
    loaded_node = Node.from_pydantic(loaded_model)
    print(loaded_node)