import json
import os
import sys
from multiprocessing import Pipe


def resource_path(relative_path: str) -> str:
    """Возвращает путь к ресурсу (для dev и exe)."""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Constants:
    _instance = None  # Это будет хранить единственный экземпляр класса

    def __new__(cls, *args, **kwargs):
        # Если экземпляр еще не существует, создаем новый
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Инициализация значений констант
            cls._instance._data = {
                'Width_main': 1920,
                'Height_main': 1080,
                'Base_back_ground': (220, 220, 220),
                'Base_white_color': (240, 240, 240),
                'Base_button_color': (35, 35, 35),
                'Waiting_time': 60,
                'Max_result_Len': 1500,
                'Maximum_cache_size': 100,
                'Setting_file_name': resource_path(r"settings.json"),
                'Cache_file_name': resource_path(r"total.json"),
                'Path_to_setting_collage': resource_path(r"..\interface\images\setting_collage"),
                'Path_to_cache_button': resource_path(r"..\interface\images\cache.png"),
                'Path_to_wait_collage': resource_path(r"..\interface\images\wait_collage"),
                'Path_to_arrow': resource_path(r"..\interface\images\arrow.png"),
                'Path_to_arrow_inverse': resource_path(r"..\interface\images\arrow_inverse.png"),
                'Base_font': ("Inter Light", (1920 + 1080 // 10) // 125),
                'Round_radius': 1080 // 22,
                'Active_Pipe': Pipe()
            }
        return cls._instance

    def load_settings(self, file_name=None):
        """Загружает настройки из JSON-файла."""
        if file_name is None:
            file_name = self._data['Setting_file_name']

        if os.path.isfile(file_name):
            try:
                with open(file_name, "r") as file:
                    data = json.load(file)
                    if isinstance(data.get("Window_size"), (list, tuple)) and len(data["Window_size"]) == 2:
                        self._data['Width_main'], self._data['Height_main'] = data["Window_size"]
                    if isinstance(data.get("Waiting_time"), int):
                        self._data['Waiting_time'] = data["Waiting_time"]
                    if isinstance(data.get("Maximum_cache_size"), int):
                        self._data['Maximum_cache_size'] = data["Maximum_cache_size"]
            except json.JSONDecodeError:
                pass

        # После загрузки настроек пересчитываем вычисляемые параметры
        self._data['Base_font'] = ("Inter Light", (self._data['Width_main'] + self._data['Height_main'] // 10) // 125)
        self._data['Round_radius'] = self._data['Height_main'] // 22

    def get(self, key):
        """Возвращает значение по ключу"""
        return self._data.get(key)

    def set(self, key, value):
        self._data[key] = value


# Получаем единственный экземпляр класса
constants = Constants()

# Загружаем настройки из файла (если файл существует)
constants.load_settings()
