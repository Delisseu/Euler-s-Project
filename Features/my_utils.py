import math
import time
from functools import reduce
from typing import List, Callable, Optional


def massive_concatenate(massive: List[int]) -> int:
    """
    Соединяет список чисел в одно число путём последовательной конкатенации.

    :param massive: Список целых чисел
    :return: Число, полученное после объединения всех чисел из списка
    """
    return reduce(num_concatenate, massive)


def time_it(func: Callable) -> Callable:
    """
    Декоратор для измерения времени выполнения функции.

    :param func: Функция, время выполнения которой требуется измерить
    :return: Обёрнутая функция, возвращающая кортеж (результат работы функции, затраченное время)
    """

    def inside(*args):
        start = time.time()
        return func(*args), time.time() - start

    return inside


def num_concatenate(first: int, second: int) -> int:
    """
    Объединяет два числа в одно путём конкатенации их цифр.

    :param first: Первое число
    :param second: Второе число
    :return: Объединённое число
    """
    return first * 10 ** number_len(second) + second


def binary_search(mass: List[int], num: int) -> Optional[int]:
    """
    Выполняет бинарный поиск числа в отсортированном списке.

    :param mass: Отсортированный список чисел
    :param num: Число, которое нужно найти
    :return: Индекс числа в списке или None, если число не найдено
    """
    start = 0
    end = len(mass)
    while start < end:
        middle_ind = (start + end) // 2
        if num == mass[middle_ind]:
            return middle_ind
        elif num > mass[middle_ind]:
            start = middle_ind + 1
        else:
            end = middle_ind
    return None


def get_digits(n: int) -> List[int]:
    """
    Разбивает число на список его цифр.

    :param n: Исходное число
    :return: Список цифр числа в правильном порядке
    """
    digits = []
    while n > 0:
        digits.append(n % 10)
        n //= 10
    return digits[::-1]


def is_palindrome(number: int) -> bool:
    """
    Проверяет, является ли число палиндромом.

    :param number: Число для проверки
    :return: True, если число палиндром, иначе False
    """
    number = get_digits(number)
    return number == number[::-1]


def get_digit_by_position(n: int, position: int) -> int:
    """
    Получает цифру числа по заданной позиции (слева направо, начиная с 0).

    :param n: Исходное число
    :param position: Позиция цифры (начиная с 0 слева)
    :return: Цифра на указанной позиции
    """
    num_digits = number_len(n)
    return (n // 10 ** (num_digits - position - 1)) % 10


def number_len(num: int) -> int:
    """
    Вычисляет количество цифр в числе.

    :param num: Число
    :return: Количество цифр в числе
    """
    if num == 0:
        return 1  # У нуля 1 цифра
    return math.floor(math.log10(abs(num))) + 1


def mod_exp(base: int, exp: int, mod: int) -> int:
    """
    Быстрое возведение в степень по модулю (алгоритм бинарного возведения в степень).

    :param base: Основание степени
    :param exp: Показатель степени
    :param mod: Модуль
    :return: Результат (base^exp) % mod
    """
    result = 1
    base %= mod

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod

    return result


def reverse_number(n: int) -> int:
    """
    Переворачивает число (123 -> 321).

    :param n: Исходное число
    :return: Число, записанное в обратном порядке
    """
    reversed_num = 0
    while n > 0:
        reversed_num = reversed_num * 10 + n % 10
        n //= 10
    return reversed_num


def logarithmic_partition(start: int, end: int, n: int) -> List[int]:
    """
    Разделяет диапазон на n частей по логарифмическому распределению.
    :param start: Начало диапазона.
    :param end: Конец диапазона.
    :param n: Количество частей.
    :return: Список границ разбиения.
    """
    partition_points = []

    for i in range(n + 1):
        # Расчёт границы разбиения по логарифмическому распределению
        point = int(start + (end - start) * (math.log(i + 1) / math.log(n + 1)))
        partition_points.append(point)

    return partition_points
