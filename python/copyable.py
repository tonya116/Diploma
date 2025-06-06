
import copy

class Copyable:    
    def __deepcopy__(self, memo):
        # Создаём новый экземпляр того же класса
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result  # Добавляем в memo для избежания циклических ссылок
        # Копируем все атрибуты
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
            
        return result