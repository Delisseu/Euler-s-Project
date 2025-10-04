import math
import operator
from collections import defaultdict
from functools import reduce
from itertools import cycle, islice
from typing import List, Union

from .my_utils import number_len, get_digits

# Словарь математических операторов
operators_ac = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}

# Словарь операторов сравнения
operators_co = {
    '==': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge
}


def count_paths_in_table(size: int) -> int:
    """
    Находит все пути в таблице (только вниз или вправо).

    :param size: Размер таблицы (размерная величина).
    :return: Количество всех возможных путей в таблице.
    """
    double_factorial = factorial = 1

    # Вычисляем (2n)!
    for x in range(1, size * 2 + 1):
        double_factorial *= x
        if x == size:
            factorial = double_factorial  # Сохраняем значение n!

    # Вычисляем количество маршрутов
    return double_factorial // (factorial * factorial)


def perform_action(operator_str: str, numbers: List[Union[int, float]]) -> Union[int, float]:
    """
    Выполняет математическую операцию над списком чисел.

    :param operator_str: Оператор в виде строки (например, '+', '-', '*', '/').
    :param numbers: Список чисел для выполнения операции.
    :return: Результат операции.
    """
    return reduce(lambda x, y: operators_ac[operator_str](x, y), numbers)


def generate_multiples(max_num: int, multiple: int) -> List[int]:
    """
    Возвращает список чисел, кратных заданному числу.

    :param max_num: Максимальное число, ограничение.
    :param multiple: Кратное число.
    :return: Список кратных чисел.
    """
    return list(range(multiple, max_num, multiple))


def square_of_sum(numbers: Union[int, List[int]]) -> int:
    """
    Возвращает квадрат суммы чисел.
    Если указано одно число, то находится квадрат суммы всех чисел меньше указанного.

    :param numbers: Список или целое число.
    :return: Квадрат суммы.
    """
    return (numbers * (numbers + 1) // 2) ** 2 if isinstance(numbers, int) else sum(numbers) ** 2


def sum_of_squares(numbers: Union[int, List[int]]) -> int:
    """
    Возвращает сумму квадратов чисел.
    Если указано одно число, то находится сумма квадратов всех чисел меньше указанного.

    :param numbers: Список или целое число.
    :return: Сумма квадратов.
    """
    return numbers * (numbers + 1) * (2 * numbers + 1) // 6 if isinstance(numbers, int) else sum(
        x ** 2 for x in numbers)


def filter_even_odd(numbers: List[int], type_str: str) -> List[int]:
    """
    Возвращает список четных или нечетных чисел.

    :param type_str: Тип ("2k" для четных или "2k+1" для нечетных).
    :param numbers: Список, содержащий числа.
    :return: Список четных или нечетных чисел.
    """
    parity = 1 if type_str == "!=" else 0
    return [num for num in numbers if num % 2 == parity]


def compare_numbers(num_list_1: Union[List[int], int], type_str: str, num_list_2: Union[List[int], int]) -> List[int]:
    """
    Сравнивает два списка чисел и возвращает соответствующие или несоответствующие числа.

    :param type_str: Тип сравнения ("Соответствующие" или "Не Соответствующие").
    :param num_list_1: Первый список или число.
    :param num_list_2: Второй список или число.
    :return: Список соответствующих или несоответствующих чисел.
    """
    set_1 = set(num_list_1 if isinstance(num_list_1, list) else [num_list_1])
    set_2 = set(num_list_2 if isinstance(num_list_2, list) else [num_list_2])
    if type_str == "!=":
        return list(filter(lambda x: x not in set_2, set_1))
    else:
        return list(filter(lambda x: x in set_2, set_1))


def calculate_own_degrees(max_exponent: int, digits: int) -> int:
    """
    Вычисляет сумму x^x для всех x от 1 до max_exponent (не включая).

    :param max_exponent: Максимальное число.
    :param digits: Количество цифр для ограничения результата.
    :return: Сумма x^x по модулю 10^digits.
    """
    total_sum = 0
    for base in range(1, max_exponent):
        current_value = pow(base, base, 10 ** digits)
        total_sum += current_value
    return total_sum % 10 ** digits


def e_approx(n: int) -> tuple[int, int]:
    """
    Вычисляет приближенную дробь для числа e с использованием разложения в непрерывную дробь.

    Параметры:
        n (int): Количество членов в разложении.

    Возвращает:
        tuple[int, int]: Числитель и знаменатель приближенной дроби для e.
    """
    e = islice(cycle([1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, 1]), n - 1)
    return period_approx(2, e)


def sqrts_odd_period(n: int) -> int:
    """
    Возвращает количество чисел от 2 до n-1, для которых
    период разложения квадратного корня в цепную дробь нечетный.

    :param n: Верхняя граница диапазона (не включается).
    :return: Количество чисел с нечетным периодом цепной дроби.
    """
    res = 0
    for num in range(2, n):
        period = len(sqrt_approx(num))
        if period % 2 != 0:
            res += 1
    return res


def sqrt_approx(num: int) -> tuple[int, list[int]]:
    """
    Вычисляет период разложения в цепную дробь для квадратного корня числа.

    :param num: Целое число, для которого вычисляется период.
    :return: Список коэффициентов цепной дроби (без начального члена).
    """
    a0 = math.isqrt(num)  # Целая часть корня
    if a0 * a0 == num:
        return a0, []  # Полный квадрат — нет периода

    m, d, a = 0, 1, a0
    seen = set()  # Храним состояния (m, d, a), чтобы отследить цикл
    period = []

    while (m, d, a) not in seen:
        seen.add((m, d, a))
        m = d * a - m
        d = (num - m * m) // d
        a = (a0 + m) // d
        period.append(a)

    return a0, period[:-1]


def diophantine_equation(d: int) -> tuple[int, int, int]:
    """
    Ищет максимальное значение x и соответствующее ему y среди решений уравнения Пелля:
        x^2 - D * y^2 = 1
    для всех значений 3 <= D <= d.

    Метод:
    - Использует разложение в цепную дробь для поиска фундаментального решения.
    - Если период нечётный, используем весь период.
    - Если период чётный, отбрасываем последний элемент периода.

    :param d: Верхняя граница диапазона значений D (целое число > 2).
    :return: Кортеж (max_x, max_y), где max_x — наибольшее найденное x, а max_y — соответствующее y.
    """
    max_x = max_y = max_d = 0
    for d_val in range(2, d + 1):
        a0, d_period = sqrt_approx(d_val)
        if not d_period:
            continue  # D — полный квадрат, решений нет

        # Корректировка периода в зависимости от чётности его длины
        if len(d_period) % 2 == 0:
            d_period.pop()

        x, y = period_approx(a0, d_period)
        if x > max_x:

            max_x, max_y, max_d = x, y, d_val

    return max_x, max_d, max_y


def period_approx(a0: int, period: (tuple[int], iter, list[int])) -> tuple[int, int]:
    """
        Строит подходящую дробь, соответствующую фундаментальному решению уравнения Пелля.

        :param a0: Целая часть квадратного корня (из sqrt_approx).
        :param period: Периодическая часть разложения (без последнего элемента, если период чётный).
        :return: Кортеж (x, y), где x и y — решение уравнения x^2 - D * y^2 = 1.
        """
    # Начальные значения для дробей
    q, p = 1, a0
    prev_q_2, prev_q = 0, 1
    prev_p_2, prev_p = 1, a0

    for a in period:
        p, q = a * prev_p + prev_p_2, a * prev_q + prev_q_2
        prev_p_2, prev_p = prev_p, p
        prev_q_2, prev_q = prev_q, q

    return p, q


def approximations_square_root(max_iters: int) -> list[tuple[int, int]]:
    """
    Генерирует последовательные приближения для представления квадратного корня из 2 в виде цепной дроби.

    Параметры:
        max_iters (int): Количество итераций для генерации последовательности приближений.

    Возвращаемое значение:
        list[tuple[int, int]]: Список кортежей, представляющих дробные приближения (числитель, знаменатель).
    """
    # Начальные значения числителя и знаменателя для последовательности приближений
    numerator = 3
    denominator = 2

    # Список для хранения приближений в виде пар (числитель, знаменатель)
    list_of_fractions = []

    for _ in range(max_iters):
        # Формула для вычисления нового приближения
        numerator += denominator * 2
        denominator = numerator - denominator

        # Проверяем, содержит ли числитель больше цифр, чем знаменатель
        if number_len(numerator) > number_len(denominator):
            list_of_fractions.append((numerator, denominator))

    return list_of_fractions


def cub_permutations(x: int = 5) -> list[int]:
    """
    Находит наименьшее кубическое число, у которого существует заданное количество перестановок с одинаковыми цифрами.

    Параметры:
        x (int): Количество кубов, которые являются перестановками друг друга.

    Возвращаемое значение:
        list[int]: Список кубов, представляющих перестановки друг друга.
    """
    # Начальное значение, с которого начинается поиск
    a = 2
    curr_cub = a ** 3  # Первый куб

    # Словарь для хранения перестановок (ключ — отсортированные цифры, значение — список кубов)
    hist_dict = defaultdict(list)

    while True:
        # Получаем отсортированные цифры текущего куба (используется как ключ в словаре)
        sorted_digits_cub = tuple(sorted(get_digits(curr_cub)))

        # Добавляем куб в соответствующую группу перестановок
        hist_dict[sorted_digits_cub].append(curr_cub)

        # Если найдена группа из `x` перестановок, возвращаем ее
        if len(hist_dict[sorted_digits_cub]) == x:
            return hist_dict[sorted_digits_cub]

        # Вычисляем следующий куб с помощью формулы для последовательности кубов (ускорение вычислений)
        curr_cub += 3 * (a * a) + 3 * a + 1
        a += 1
