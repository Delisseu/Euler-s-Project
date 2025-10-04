import json
import os
from typing import Union, List, Tuple, Any

import pandas as pd

from constants import constants

Keys = ["Task", "Input", "Output"]
File_name = 'total.json'


def check_structure(structure):
    for key, value in structure.items():
        if key not in Keys or not isinstance(value, list):
            raise ValueError


def write(task_name: str, inputs: Union[str, List[Any], Tuple[Any, ...]],
          output: Union[str, List[Any], Tuple[Any, ...]]) -> None:
    """
    Сохраняет задачу, входные данные и вывод в файл.

    Если выходные данные слишком большие, они сокращаются до 500 символов или 100 элементов.

    Args:
        task_name (str): Имя задачи.
        inputs (Union[str, List[Any], Tuple[Any, ...]]): Входные данные для задачи.
        output (Union[str, List[Any], Tuple[Any, ...]]): Выходные данные задачи.
    """
    data = {
        Keys[0]: [task_name],
        Keys[1]: [inputs],
        Keys[2]: [output]
    }

    def save(data):
        for x in range(2, 6):
            try:
                with open(constants.get('Cache_file_name'), 'w') as file:
                    json.dump(data, file)
                    break
            except TypeError:
                break
            except IOError:
                continue

    if not os.path.isfile(constants.get('Cache_file_name')):
        save(data)
    else:
        try:
            with open(constants.get('Cache_file_name'), 'r') as file:
                file_data = json.load(file)
                check_structure(file_data)
            file_data[Keys[0]].extend(data[Keys[0]])
            file_data[Keys[1]].extend(data[Keys[1]])
            file_data[Keys[2]].extend(data[Keys[2]])
            if len(file_data[Keys[0]]) > 100:
                file_data[Keys[0]] = file_data[Keys[0]][:100]
                file_data[Keys[1]] = file_data[Keys[1]][:100]
                file_data[Keys[2]] = file_data[Keys[2]][:100]
            data = file_data
        except ValueError:
            remove_cache_file()
        finally:
            save(data)


def cache(task_name: str, inputs: Union[str, List[Any], Tuple[Any, ...]]) -> Union[bool, Any]:
    """
    Проверяет, существует ли кэш для данных задачи в файле.

    Args:
        task_name (str): Имя задачи.
        inputs (Union[str, List[Any], Tuple[Any, ...]]): Входные данные для задачи.

    Returns:
        Union[bool, Any]: Возвращает результат задачи, если он есть, или False.

    """
    df = get_results()
    if isinstance(df, pd.DataFrame):
        cached_data = df[(df['Task'] == task_name) & (df['Input'].apply(lambda x: x == inputs))]
        if cached_data.empty:
            return False
        return cached_data['Output'].values[0]
    return False


def get_results() -> Union[pd.DataFrame, None]:
    """
    Возвращает содержимое если файл существует.

    Returns:
        Union[pd.DataFrame, None]: Данные из файла, если файл есть, или None.

    """
    if os.path.isfile(constants.get('Cache_file_name')):
        with open(constants.get('Cache_file_name'), 'r') as file:
            try:
                data_file = json.load(file)
                check_structure(data_file)
                return pd.DataFrame(data_file)
            except (json.JSONDecodeError, ValueError):
                return None
    return None


def remove_cache_file() -> None:
    """
    Удаляет файл, если он существует.
    """
    if os.path.isfile(constants.get('Cache_file_name')):
        for x in range(2, 6):
            try:
                os.remove(constants.get('Cache_file_name'))
                break
            except PermissionError:
                continue


def write_setting(data) -> None:
    with open(constants.get('Setting_file_name'), "w") as file:
        json.dump(data, file)
