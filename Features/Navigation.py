from . import TableOperations
from . import MathOperations


def most_navigate(table_list: list, selection_length: int) -> int:
    """
    Проверяет таблицу и находит максимальное число с выбранной длиной в любом направлении.

    :param selection_length: длина числа для поиска.
    :param table_list: список чисел в виде таблицы.
    :return: максимальное число.

    >>> most_navigate([[1, 2], [3, 4]], 2)
    8
    """
    num_list, length = TableOperations.table(table_list)
    max_horizontal = max_vertical = max_diagonal_1 = max_diagonal_2 = 0

    for index in range(selection_length, len(num_list)):
        max_index = min(len(num_list), index + (length * (selection_length - 1)) + 1)
        start_index = index - selection_length

        max_horizontal = max(max_horizontal, horizon("*", num_list, start_index, index))
        max_vertical = max(max_vertical, vertical("*", num_list, start_index, max_index, length))
        max_diagonal_1 = max(max_diagonal_1, diagonal_1("*", num_list, start_index, max_index, length))
        max_diagonal_2 = max(max_diagonal_2, diagonal_2("*", num_list, start_index, max_index, length))

    return max(max_horizontal, max_vertical, max_diagonal_1, max_diagonal_2)


def horizon(operator: str, num_list: list, start: int, end: int) -> float:
    """
    Выполняет горизонтальную операцию над числами.

    :param operator: оператор для операции.
    :param num_list: список чисел.
    :param start: начальная позиция.
    :param end: конечная позиция.
    :return: результат операции.

    >>> horizon("*", [1, 2, 3, 4], 0, 2)
    2
    """
    return MathOperations.perform_action(operator, num_list[start:end])


def vertical(operator: str, num_list: list, start: int, end: int, step: int) -> float:
    """
    Выполняет вертикальную операцию над числами.

    :param operator: оператор для операции.
    :param num_list: список чисел.
    :param start: начальная позиция.
    :param end: конечная позиция.
    :param step: длина шага.
    :return: результат операции.

    >>> vertical("*", [1, 2, 3, 4], 0, 4, 2)
    3
    """
    return MathOperations.perform_action(operator, num_list[start:end:step])


def diagonal_1(operator: str, num_list: list, start: int, end: int, step: int) -> float:
    """
    Выполняет диагональную операцию (слева направо) над числами.

    :param operator: оператор для операции.
    :param num_list: список чисел.
    :param start: начальная позиция.
    :param end: конечная позиция.
    :param step: длина шага.
    :return: результат операции.

    >>> diagonal_1("*", [1, 2, 3, 4], 0, 4, 2)
    2
    """
    return MathOperations.perform_action(operator, num_list[start:end:step - 1])


def diagonal_2(operator: str, num_list: list, start: int, end: int, step: int) -> float:
    """
    Выполняет диагональную операцию (справа налево) над числами.

    :param operator: оператор для операции.
    :param num_list: список чисел.
    :param start: начальная позиция.
    :param end: конечная позиция.
    :param step: длина шага.
    :return: результат операции.

    >>> diagonal_2("*", [1, 2, 3, 4], 0, 4, 2)
    4
    """
    return MathOperations.perform_action(operator, num_list[start:end:step + 1])
