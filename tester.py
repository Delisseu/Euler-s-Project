from multiprocessing import Pipe, Process
from tkinter import Label
from typing import Union, List, Optional

import numpy

from interface.Interface_logic import show_message, constants


class TimeoutError(Exception):
    """
    Исключение, вызываемое при превышении времени выполнения функции.
    """
    message = "Функция выполнялась дольше, чем ожидалось. Остановка процесса."

    def __init__(self, msg=message):
        self.msg = str(msg)

    def __str__(self) -> str:
        return self.msg


def reply(child_conn: Pipe) -> None:
    """
    Выполняет функцию с переданными аргументами и помещает результат в очередь.

    :param child_conn: Pipe для получения и отправки результата выполнения.
    """
    while True:
        func, args = child_conn.recv()
        try:
            child_conn.send(func(*args))
        except (OverflowError, MemoryError) as error:
            child_conn.send(error)


def time_counter(seconds: int, parent_conn: Pipe, label: Label, reply_container: List[Optional[Union[str, int, float]]],
                 process, current_time: float = 0.0) -> None:
    """
    Счетчик времени, который обновляет метку каждую 0.1 секунды и завершает процесс по окончании отсчета.

    :param seconds: Общее количество секунд для отсчета.
    :param parent_conn: Канал для связи между процессами.
    :param label: Виджет метки (Label) для обновления времени.
    :param reply_container: Контейнер для хранения результата выполнения.
    :param process: Запущенный процесс, который будет завершен после отсчета.
    :param current_time: Текущее значение отсчета времени (по умолчанию 0.0).
    :return: None
    """
    label.configure(text=f"{current_time} secs -> {seconds}")
    if current_time >= seconds:
        return reply_handler(reply_container, process, TimeoutError())

    if parent_conn.poll():
        return reply_handler(reply_container, process, parent_conn.recv())

    current_time = round(current_time + 0.1, 1)
    label.after(100,
                lambda: time_counter(seconds, parent_conn, label, reply_container, process, current_time))


def reply_handler(container: List[Optional[Union[str, int, float]]], process,
                  result: Optional[Union[Exception, tuple, set, list, str, int, float]]) -> None:
    """
    Обработчик завершения процесса и записи результата в контейнер.

    :param container: Контейнер для хранения результата выполнения.
    :param process: Запущенный процесс, который необходимо завершить.
    :param result: Опциональный результат выполнения, переданный через канал.
    :return: None
    """
    if isinstance(result, Exception):
        show_message(result)
        container.append(None)
        if isinstance(result, TimeoutError):
            try:
                process.terminate()
            except BrokenPipeError:
                pass
            finally:
                create_process()
    elif isinstance(result, (tuple, set, list)):
        container.extend(result if result else ["None"])
    elif isinstance(result, numpy.ndarray):
        container.extend(result.tolist())
    else:
        container.append(result)


def create_process():
    _, child_conn = constants.get('Active_Pipe')
    process = Process(target=reply, args=(child_conn,))
    process.start()
    constants.set('Active_Process', process)


def tester(func, args: tuple, label, reply_containter, time_limit: int = 10) -> any:
    """
    Тестирует выполнение функции с ограничением времени.

    :param func: Функция для тестирования.
    :param args: Аргументы для функции.
    :return: Результат выполнения функции или вызывает исключение.
    """
    parent_conn, child_conn = constants.get('Active_Pipe')
    process = constants.get('Active_Process')
    parent_conn.send((func, args))
    time_counter(time_limit, parent_conn, label, reply_containter, process)
