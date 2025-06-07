import json
from typing import Dict, List, Any, Set
from dataclasses import is_dataclass, asdict
from inspect import getmembers, ismethod

class Serializable:
    """
    Базовый класс для сериализуемых объектов.
    Переопределите __serialize_fields__ для указания полей.
    """
    __serialize_fields__: Set[str] = set()
    __exclude_fields__: Set[str] = {'_cache', '_dirty'}  # Пример полей для исключения
    
    def serialize(self) -> Dict[str, Any]:
        """Сериализует объект в словарь"""
        result = {}
        
        # Обработка dataclass
        if is_dataclass(self):
            result = asdict(self)
        else:
            # Получаем все атрибуты, исключая методы и приватные поля
            members = getmembers(self, lambda x: not ismethod(x))
            for name, value in members:
                if not name.startswith('_') or name in self.__serialize_fields__:
                    if name not in self.__exclude_fields__:
                        result[name] = value
        
        # Фильтрация полей по __serialize_fields__ если они заданы
        if self.__serialize_fields__:
            result = {k: v for k, v in result.items() 
                     if k in self.__serialize_fields__}
        
        # Рекурсивная сериализация вложенных объектов
        for key, value in result.items():
            if isinstance(value, Serializable):
                result[key] = value.serialize()
            elif isinstance(value, (list, tuple)):
                result[key] = [v.serialize() if isinstance(v, Serializable) else v 
                             for v in value]
            elif isinstance(value, dict):
                result[key] = {k: v.serialize() if isinstance(v, Serializable) else v 
                             for k, v in value.items()}
        
        return result
