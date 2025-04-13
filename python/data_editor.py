import dearpygui.dearpygui as dpg
from typing import Dict, Any
import json

class DataEditor:
    def __init__(self):
        self.data = None
        self.original_data = None

    def load_data(self, data: Dict[str, Any]):
        """Загрузка данных для редактирования"""
        self.data = data
        self.original_data = json.loads(json.dumps(data))  # Deep copy

    def show_editor(self):
        """Отображение редактора"""
        dpg.create_context()
        dpg.create_viewport(title="Structural Data Editor", width=1200, height=800)

        with dpg.window(label="Editor", width=1180, height=760):
            with dpg.tab_bar():
                with dpg.tab(label="Data"):
                    self._build_editable_tree("root", self.data)
                with dpg.tab(label="Actions"):
                    dpg.add_button(label="Save to File", callback=self._save_to_file)
                    dpg.add_button(label="Reset Changes", callback=self._reset_changes)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def _build_editable_tree(self, parent: str, data: Any, path: str = ""):
        """Рекурсивное построение дерева с элементами редактирования"""
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                if isinstance(value, (dict, list)):
                    with dpg.tree_node(label=key, parent=parent):
                        self._build_editable_tree(parent, value, new_path)
                else:
                    self._add_editable_field(parent, key, value, new_path)

        elif isinstance(data, list):
            for idx, item in enumerate(data):
                new_path = f"{path}[{idx}]"
                if isinstance(item, (dict, list)):
                    with dpg.tree_node(label=f"Item {idx}", parent=parent):
                        self._build_editable_tree(parent, item, new_path)
                else:
                    self._add_editable_field(parent, str(idx), item, new_path)

    def _add_editable_field(self, parent: str, label: str, value: Any, path: str):
        """Добавление поля с возможностью редактирования"""
        with dpg.group(horizontal=True, parent=parent):
            dpg.add_text(f"{label}:")

            # Специальные обработчики для разных типов данных
            if isinstance(value, bool):
                dpg.add_checkbox(default_value=value, tag=path, callback=self._update_data)
            elif isinstance(value, (int, float)):
                dpg.add_input_float(
                    default_value=value,
                    tag=path,
                    width=100,
                    callback=self._update_data
                )
            elif isinstance(value, list) and all(isinstance(x, (int, float)) for x in value):
                # Обработка векторов (координат, направлений)
                with dpg.group(horizontal=True):
                    for i, num in enumerate(value):
                        dpg.add_input_float(
                            default_value=num,
                            tag=f"{path}[{i}]",
                            width=70,
                            callback=self._update_data
                        )
            else:
                dpg.add_input_text(
                    default_value=str(value),
                    tag=path,
                    width=200,
                    callback=self._update_data
                )

    def _update_data(self, sender, app_data):
        """Обновление данных при изменении значений"""
        path = dpg.get_item_label(sender)
        try:
            # Находим нужный элемент в структуре данных
            keys = path.split('.')
            current = self.data
            
            for key in keys[:-1]:
                if '[' in key:
                    # Обработка индексов массивов
                    base = key.split('[')[0]
                    idx = int(key.split('[')[1].rstrip(']'))
                    current = current[base][idx]
                else:
                    current = current[key]
            
            # Устанавливаем новое значение
            last_key = keys[-1]
            if '[' in last_key:
                base = last_key.split('[')[0]
                idx = int(last_key.split('[')[1].rstrip(']'))
                current[base][idx] = app_data
            else:
                current[last_key] = app_data

        except Exception as e:
            print(f"Error updating {path}: {e}")

    def _save_to_file(self):
        """Сохранение данных в файл"""
        with open("modified_structure.json", "w") as f:
            json.dump(self.data, f, indent=4)
        print("Data saved to modified_structure.json")

    def _reset_changes(self):
        """Сброс изменений к исходным данным"""
        self.data = json.loads(json.dumps(self.original_data))
        print("All changes have been reset")

# Пример использования
if __name__ == "__main__":
    # Ваши данные
    data = {
        "nodes": [
            {"id": 1, "coordinates": [0, 0, 0]},
            {"id": 2, "coordinates": [10, 0, 0]}
        ],
        "elements": [
            {"id": 1, "start_node": 1, "end_node": 2, "type": "beam"}
        ],
        "materials": {
            "steel": {"modulus": 210e9, "density": 7800}
        }
    }

    editor = DataEditor()
    editor.load_data(data)
    editor.show_editor()