from typing import List, Tuple

from Features.MathOperations import operators_co


def find_divisors(number: int) -> List[int]:
    """
    Находит все делители заданного числа.

    :param number: Целое число.
    :return: Список делителей.

    >>> find_divisors(28)
    [1, 2, 4, 7, 14, 28]
    """
    divisors = []
    for potential_divisor in range(1, int(number ** 0.5) + 1):
        if number % potential_divisor == 0:
            divisors.append(potential_divisor)
            paired_divisor = number // potential_divisor
            if potential_divisor != paired_divisor:
                divisors.append(paired_divisor)
    return sorted(divisors)


def find_friendly_numbers(max_limit: int) -> List[int]:
    """
    Находит все дружественные числа до заданного числа.

    :param max_limit: Максимальное число.
    :return: Список дружественных чисел.

    >>> find_friendly_numbers(300)
    [220, 284]
    """
    friendly_numbers = []
    for number in range(1, max_limit + 1):
        if number not in friendly_numbers:
            divisors_sum = sum(find_divisors(number)[:-1])
            if divisors_sum > max_limit or divisors_sum == number:
                continue
            counterpart_divisors_sum = sum(find_divisors(divisors_sum)[:-1])
            if counterpart_divisors_sum == number != divisors_sum:
                friendly_numbers.append(divisors_sum)
                friendly_numbers.append(number)
    return friendly_numbers


def check_divisors(comparison_operator: str, numbers: List[int], divisor_count: int) -> Tuple[
    List[int], List[int], List[Tuple[int, int]]]:
    """
    Проверяет количество делителей для каждого числа в списке.

    :param comparison_operator: Оператор сравнения ('<' или '>').
    :param numbers: Список чисел.
    :param divisor_count: Количество делителей.
    :return: Список чисел, количество их делителей и пары (число, количество делителей).

    >>> check_divisors('>', [10, 12, 15, 16], 4)
    ([12, 15, 16], [6, 4, 5], [(12, 6), (15, 4), (16, 5)])
    """
    result = []
    divisor_lengths = []
    for number in numbers:
        length = len(find_divisors(number))
        if operators_co[comparison_operator](length, divisor_count):
            result.append(number)
            divisor_lengths.append(length)
    return result, divisor_lengths, list(zip(result, divisor_lengths))
