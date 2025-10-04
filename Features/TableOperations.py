from . import MathOperations
from typing import List, Tuple


def table(tab: str) -> Tuple[List[int], int]:
    """
    Читает многострочный ввод и возвращает длину первой строки и список чисел.

    :param tab: Многострочный ввод.
    :return: Кортеж, содержащий список чисел и длину первой строки.

    >>> table("1 2 3\n4 5 6")
    ([1, 2, 3, 4, 5, 6], 3)
    """
    lines = tab.splitlines()
    length = len(lines[0].split()) if lines else 0
    numbers = [int(num) for num in tab.split()]
    return numbers, length


def triangle(triangle_input: str) -> int:
    """
    Находит в треугольнике наибольшее возможное число, перемещаясь вниз по смежным числам.

    :param triangle_input: Строка, представляющая треугольник.
    :return: Наибольшее возможное число в треугольнике.

    >>> triangle("3\n7 4\n2 4 6\n8 5 9 3")
    23
    """
    triangle_list = [list(map(int, line.split())) for line in triangle_input.strip().split("\n")]
    triangle_list.reverse()  # Реверсируем для удобства
    for i in range(1, len(triangle_list)):
        for j in range(len(triangle_list[i])):
            # Обновляем элемент, добавляя максимальное значение из двух возможных
            triangle_list[i][j] += max(triangle_list[i - 1][j], triangle_list[i - 1][j + 1])
    return triangle_list[-1][0]


def sel_num_sum_1(table_input: str, selection: int, operation: str) -> int:
    """
    Извлекает первые n цифр из каждого числа в списке и проводит операции с ними.

    :param table_input: Список чисел в виде таблицы.
    :param selection: Количество цифр для извлечения.
    :param operation: Оператор для математической операции.
    :return: Результат операции.

    >>> sel_num_sum_1("12345\n67890", 3, '+')
    21
    """
    numbers = table(table_input)[0]
    selected_numbers = [int(str(num)[:selection]) for num in numbers]
    result = MathOperations.action(operation, selected_numbers)
    return result


def sel_num_sum_2(table_input: str, selection: int, operation: str) -> int:
    """
    Обрабатывает все числа в списке и возвращает первые n цифр результата.

    :param table_input: Список чисел в виде таблицы.
    :param selection: Количество цифр для извлечения из результата.
    :param operation: Оператор для математической операции.
    :return: Первые n цифр результата.

    >>> sel_num_sum_2("12345\n67890", 3, '+')
    21
    """
    numbers = table(table_input)[0]
    result = MathOperations.action(operation, numbers)
    return int(str(result)[:selection])
