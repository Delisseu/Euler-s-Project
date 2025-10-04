import bisect
from .my_utils import *

def find_palindromes(max_num: int, min_num: int) -> list:
    """
    Находит все числа-палиндромы в заданном диапазоне.

    :param min_num: минимальное число.
    :param max_num: максимальное число.
    :return: список чисел-палиндромов.
    """
    list_palindromes = []
    mx_length = number_len(max_num)
    m_length = number_len(min_num)

    m_pal = int(min_num / 10 ** (m_length // 2)) if m_length % 2 == 0 else int(min_num / 10 ** (m_length // 2))
    mx_pal = int(max_num / 10 ** (mx_length // 2)) * 10 if mx_length % 2 == 0 else int(max_num / 10 ** (mx_length // 2))

    for half_palindrome in range(m_pal, mx_pal):
        half_palindrome_str = str(half_palindrome)

        # Проверка на нечетные палиндромы
        odd_palindrome = int(half_palindrome_str + half_palindrome_str[-2::-1])
        if odd_palindrome < max_num:
            list_palindromes.append(odd_palindrome)

        # Проверка на четные палиндромы
        even_palindrome = int(half_palindrome_str + half_palindrome_str[::-1])
        if even_palindrome < max_num:
            list_palindromes.append(even_palindrome)

    list_palindromes.sort()
    return list_palindromes[bisect.bisect_left(list_palindromes, min_num):]


def double_base_palindromes(max_num: int, min_num: int) -> list:
    """
    Вычисляет палиндромы, которые являются палиндромами как в десятичной, так и в двоичной системах счисления.

    :param max_num: Верхняя граница диапазона.
    :param min_num: Нижняя граница диапазона.
    :return: Список чисел-палиндромов в двух системах счисления.
    """
    palindromes_list = find_palindromes(max_num, min_num)
    double_base_palindromes_list = []

    for palindrome in palindromes_list:
        if bin(palindrome)[2:] == bin(palindrome)[2:][::-1]:
            double_base_palindromes_list.append(palindrome)

    return double_base_palindromes_list


def lychrel_numbers(max_num: int, iters: int = 50) -> list[tuple[int, int]]:
    """
    Определяет числа Личреля в заданном диапазоне.

    Число Личреля — это число, которое не становится палиндромом при реверсивном сложении в течение `iters` итераций.

    Параметры:
        max_num (int): Верхний предел диапазона чисел для проверки (начиная с 1).
        iters (int): Максимальное количество итераций реверсивного сложения (по умолчанию 50).

    Возвращаемое значение:
        list[tuple[int, int]]:
            - Список кортежей (число, количество итераций до палиндрома).
            - Если число не достигает палиндрома в `iters` итераций, оно не включается в список.
    """
    results = []  # Список чисел, которые стали палиндромами и количество шагов
    for number in range(1, max_num):
        new_number = number  # Текущее число, с которым выполняем операции
        for iteration in range(iters):
            new_number += int(str(new_number)[::-1])  # Реверсивное сложение
            if is_palindrome(new_number):  # Проверяем, является ли число палиндромом
                results.append((number, iteration + 1))  # Записываем число и количество итераций
                break  # Выходим из цикла, так как палиндром найден
    return results
