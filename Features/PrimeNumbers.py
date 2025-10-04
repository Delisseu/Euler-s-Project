import itertools
import multiprocessing
import random
from collections import Counter
from typing import Tuple

import gmpy2
import numpy as np
from bitarray import bitarray
from .my_utils import *


def truncatable_primes(n: int) -> Tuple[int, List[int]]:
    """
    Находит усеченные простые числа до заданного значения.

    :param n: Верхняя граница для поиска.
    :return: Сумма усеченных простых чисел и отсортированный список усеченных простых чисел.
    """
    if n > 739397:
        n = 739397
    primes = frozenset(prime_num(n)[4:])
    result = set()
    for prime in primes:
        for left in range(1, len(str(prime))):
            if not is_prime(int(str(prime)[:-left])) or not is_prime(int(str(prime)[left:])):
                break
        else:
            result.add(prime)
    return sum(result), sorted(result)


def is_prime(n: int) -> bool:
    """
    Проверяет, является ли число простым.

    :param n: Проверяемое число.
    :return: True, если число простое, иначе False.
    """
    if n <= 1:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    if n < 1000000:
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(5):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def prime_num(max_num: int) -> List[int]:
    """
    Находит все простые числа до заданного числа.

    :param max_num: Целое число.
    :return: Список простых чисел.
    """
    prime = bitarray(max_num + 1)
    prime.setall(True)
    primes = [2]
    sqrt = int(max_num ** 0.5) + 1
    for p in range(3, sqrt, 2):
        if prime[p]:
            primes.append(p)
            prime[p * p::p * 2] = False
    if sqrt % 2 == 0:
        sqrt += 1
    primes.extend([x for x in range(sqrt, max_num, 2) if prime[x]])
    return primes


def prime_divisor(num: int) -> List[int]:
    """
    Находит все простые делители заданного числа.

    :param num: Целое число.
    :return: Список простых делителей.
    """
    div_list = set()
    count = 2
    while count * count <= num:
        if num % count == 0:
            div_list.add(count)
            num //= count
        else:
            count += 1 if count == 2 else 2
    if num > 1:
        div_list.add(num)
    return sorted(div_list)


def quadratic_primes(max_b: int, max_a: int) -> Tuple[int, int]:
    """
    Находит максимальное количество простых чисел, получаемых по формуле n^2 + an + b.

    :param max_b: Верхняя граница для b.
    :param max_a: Верхняя граница для a.
    :return: Максимальное количество простых чисел и произведение a и b.
    """
    list_b = prime_num(max_b)
    max_n, result = 0, 0
    for b in list_b:
        for a in range(-max_a, max_a + 1):
            n = 0
            while True:
                current = n * n + a * n + b
                if is_prime(current):
                    n += 1
                else:
                    if max_n < n:
                        max_n = n
                        result = a * b
                    break
    return max_n, result


def circular_primes(max_num: int) -> List[int]:
    """
    Находит циклические простые числа до заданного значения.

    :param max_num: Верхняя граница диапазона.
    :return: Список циклических простых чисел.
    """
    primes = prime_num(max_num)
    final_result = set()
    for prime in primes:
        if all(d not in str(prime) for d in "2468"):
            result = {prime}
            str_prime = str(prime)
            for num in range(1, len(str_prime)):
                numb = int(str_prime[num:] + str_prime[:num])
                if is_prime(numb):
                    result.add(numb)
                else:
                    break
            final_result.update(result)
    return sorted(final_result)


def different_prime_factors(count: int, len_subsequence: int) -> int:
    """
    Находит первое число с заданным количеством уникальных простых делителей
    и проверяет наличие последовательности заданной длины.

    :param count: Требуемое количество уникальных простых делителей.
    :param len_subsequence: Длина последовательности.
    :return: Первое число с заданным количеством уникальных простых делителей.
    """

    def prime_divisor(num: int) -> int:
        prime_factors_count = 0
        if num % 2 == 0:
            prime_factors_count += 1
            while num % 2 == 0:
                num //= 2
            if prime_factors_count > count:
                return False

        for x in range(3, int(num ** 0.5) + 1, 2):
            if num % x == 0:
                prime_factors_count += 1
                while num % x == 0:
                    num //= x
                if prime_factors_count > count:
                    return False

        if num > 2:
            prime_factors_count += 1

        return prime_factors_count == count

    num = 1
    while True:
        if prime_divisor(num):
            if all(prime_divisor(num + x) for x in range(len_subsequence)):
                return num
        num += 1


def sum_consecutive_prime_numbers(max_num: int) -> Tuple[int, int]:
    """
    Находит максимальное простое число, которое можно выразить
    как сумму последовательных простых чисел.

    :param max_num: Верхняя граница для суммы.
    :return: Максимальное простое число и количество слагаемых.
    """
    primes = prime_num(max_num)
    primes_find = set(primes)
    end = result = 2
    start = max_counts = max_prime_c = 0

    while end < len(primes):
        if result > max_num:
            result -= primes[start]
            start += 1
            continue

        if result in primes_find:
            long = end - start
            if long > max_counts:
                max_counts = long
                max_prime_c = result

        result += primes[end]
        end += 1

    return max_prime_c, max_counts


def combining_pair_prime(n: int) -> tuple[int, list[int]]:
    """
    Находит минимальную сумму чисел в последовательности простых чисел, которые могут быть объединены, чтобы сформировать "комбинированную пару".
    Функция использует числа из ряда простых чисел и проверяет, можно ли объединить числа в пары так, чтобы их объединение не было простым числом.
    Когда последовательность достигает заданной длины (n), она возвращает минимальную сумму чисел.

    Параметры:
        n (int): Количество чисел, которые должны быть в последовательности.

    Возвращаемое значение:
        tuple: Кортеж из минимальной суммы и индексов простых чисел, составляющих эту последовательность.
    """

    # Вспомогательная функция для проверки, является ли число простым
    # или оно уже вычислено и находится в множестве простых чисел
    def is_prime_in_set_or_computable(x, max_primes, prime_set):
        # Если число больше максимального предела, проверяем его на простоту
        return is_prime(x) if x >= max_primes else x in prime_set

    # Устанавливаем максимальное значение для поиска простых чисел
    max_prime_value = 20000

    # Получаем список всех простых чисел до max_prime_value
    prime_numbers_list = prime_num(max_prime_value)

    # Преобразуем список простых чисел в множество для быстрой проверки
    prime_set = set(prime_numbers_list)

    # Начальные индексы и список для хранения подходящих простых чисел
    prime_indices = [0]
    valid_prime_sequence = [0]
    valid_prime_sequence.pop()

    # Устанавливаем максимальный индекс для перебора простых чисел
    max_index = len(prime_numbers_list)

    # Переменная для хранения минимальной суммы
    min_sum = 0

    # Основной цикл поиска подходящей последовательности простых чисел
    while True:
        # Флаг, указывающий, была ли найдена последовательность
        sequence_found = False

        # Перебор простых чисел с текущего индекса
        for current_prime in prime_numbers_list[prime_indices[-1]:max_index]:
            # Обновляем текущий индекс
            prime_indices[-1] += 1

            # Проверяем каждую пару чисел в последовательности
            for num in valid_prime_sequence:
                for pair in ((num, current_prime), (current_prime, num)):
                    # Проверяем, является ли объединенная пара чисел простым числом
                    if not is_prime_in_set_or_computable(num_concatenate(*pair), max_prime_value, prime_set):
                        break
                else:
                    # Если все проверки прошли успешно, продолжаем
                    continue
                break
            else:
                # Если последовательность проходит все проверки, добавляем новое простое число
                valid_prime_sequence.append(current_prime)

                # Если последовательность достигла заданной длины, вычисляем сумму
                if len(valid_prime_sequence) == n:
                    sequence_sum = sum(valid_prime_sequence)
                    min_sum = min(min_sum, sequence_sum) if min_sum else sequence_sum

                    # Убираем последние два элемента для продолжения поиска
                    valid_prime_sequence = valid_prime_sequence[:-2]
                    prime_indices.pop()
                    sequence_found = True
                break
        else:
            # Если последовательность не была найдена, возвращаем минимальную сумму и индексы
            if not valid_prime_sequence:
                return min_sum, prime_indices
            valid_prime_sequence.pop()
            prime_indices.pop()
            sequence_found = True

        # Если минимальная сумма найдена, продолжаем обработку
        if min_sum:
            # Вычисляем остаток суммы и корректируем, если она четная
            current_sum = min_sum - sum(valid_prime_sequence)
            current_sum = current_sum if current_sum % 2 != 0 else current_sum + 1

            # Ищем минимальное подходящее число для продолжения последовательности
            while not is_prime_in_set_or_computable(current_sum, max_prime_value, prime_set):
                current_sum -= 2
                # Если число стало меньше последнего в последовательности, обнуляем его
                if current_sum < valid_prime_sequence[-1] if valid_prime_sequence else 0:
                    current_sum = 3
                    break

            # Ищем индекс следующего простого числа, подходящего для последовательности
            max_index = binary_search(prime_numbers_list, current_sum) + 1 if prime_numbers_list[
                                                                                  -1] > current_sum else len(
                prime_numbers_list)

            # Если подходящих чисел больше нет, завершаем работу
            if not prime_numbers_list[prime_indices[-1]:max_index]:
                if not valid_prime_sequence:
                    return min_sum, prime_indices
                valid_prime_sequence.pop()
                sequence_found = True

        # Если последовательность не была найдена, повторяем попытку с текущими индексами
        if not sequence_found:
            prime_indices.append(prime_indices[-1])


def spiral_primes(lower: int) -> int:
    """
    Вычисляет уровень спирали чисел, на котором доля простых чисел на диагоналях
    становится меньше заданного значения.

    Параметры:
        lower: Пороговое значение для доли простых чисел. Доля простых чисел на диагоналях
                       должна быть меньше этого значения, чтобы остановить поиск.
    Возвращаемое значение:
        int: Уровень спирали, на котором доля простых чисел становится меньше заданного порога.
    """
    # Преобразуем пороговое значение в десятичную дробь
    lower /= 100

    # Переменные для подсчета простых чисел на диагоналях и общего числа диагональных чисел
    diag_primes = 0
    diag_numbers = 0

    # Начальный уровень спирали
    level = 1

    # Максимальное значение для поиска простых чисел
    max_first_prime = 10000000
    # Множество простых чисел для быстрых проверок
    first_primes = set(prime_num(max_first_prime))

    # Начинаем цикл поиска, пока доля простых чисел не станет меньше порога
    while True:
        # Шаг на каждом уровне спирали (по 2 на каждом шаге)
        step = level * 2

        # Число на левой нижней диагонали для текущего уровня
        left_down = (step + 1) ** 2 - step
        diag_numbers += 4  # Увеличиваем количество диагональных чисел на текущем уровне

        # Проверяем 3 диагональных числа для простоты
        for _ in range(3):
            # Проверяем, является ли число простым (если оно меньше максимального, то проверяем в множестве)
            if left_down in first_primes if left_down < max_first_prime else is_prime(left_down):
                diag_primes += 1  # Увеличиваем счетчик простых чисел на диагонали
            left_down -= step  # Переходим к следующему числу на диагонали

        level += 1  # Переходим на следующий уровень спирали

        # Если доля простых чисел на диагоналях меньше порога, завершаем цикл
        if diag_primes / diag_numbers < lower:
            break

    # Возвращаем уровень, на котором условие выполнено
    return level


def replacing_prime(need_length: int) -> list[int]:
    """
    Ищет группу простых чисел, получающихся заменой цифр в простом числе.

    Параметры:
        need_length (int): Требуемое количество простых чисел в группе.

    Возвращаемое значение:
        list[int]: Список найденных простых чисел.
    """
    max_prime = 1_000_000  # Начальное ограничение для поиска простых чисел
    primes = prime_num(max_prime)  # Генерация простых чисел до max_prime
    primes_check = set(primes)  # Для быстрого поиска простых чисел
    result = []
    x = 0  # Индекс текущего простого числа

    while True:
        # Если индекс выходит за пределы списка, расширяем диапазон поиска
        if x == (primes_len := len(primes)):
            max_prime *= 2
            primes = prime_num(max_prime)[primes_len:]
            primes_check = set(primes)
            x = 0

        curr_prime = primes[x]
        prime_digits = get_digits(curr_prime)

        # Пропускаем числа, содержащие только большие цифры
        if all(digit > 10 - need_length for digit in prime_digits):
            x += 1
            continue

        result.append(curr_prime)
        prime_len = int(math.log10(curr_prime)) + 1  # Количество цифр в числе
        counter = Counter(prime_digits)  # Подсчет повторяющихся цифр

        # Ищем наиболее часто встречающиеся цифры и заменяем их
        for rep_digit, count in counter.most_common():
            if count == 1:
                break
            if rep_digit > 10 - need_length:
                continue

            positions = [i for i, digit in enumerate(prime_digits) if digit == rep_digit]

            for comb_len in range(2, len(positions) + 1):
                for curr_comb in itertools.combinations(positions, comb_len):
                    temp_num = curr_prime
                    for _ in range(1, 10 - rep_digit):
                        for pos in curr_comb:
                            temp_num += 10 ** (prime_len - pos - 1)
                        if temp_num in primes_check:
                            result.append(temp_num)

                    if len(result) == need_length:
                        return result

                    result = result[:1]  # Оставляем только первое число

        # Замена отдельных цифр и проверка на простоту
        for pos in range(prime_len):
            num_on_pos = get_digit_by_position(curr_prime, pos)
            if num_on_pos > 10 - need_length:
                continue

            # Четные замены запрещены в первой позиции
            possible_replacements = range(2, 10 - num_on_pos, 2) if pos == 0 else range(1, 10 - num_on_pos)

            for num in possible_replacements:
                new_num = curr_prime + (num * 10 ** (prime_len - pos - 1))
                if new_num in primes_check:
                    result.append(new_num)

            if len(result) == need_length:
                return result

            result = result[:1]  # Сбрасываем список результатов

        result.clear()  # Полный сброс результатов, если не удалось найти группу
        x += 1


def lucas_lehmer_test(p: int, m_p: gmpy2.mpz) -> bool:
    """
    Выполняет тест Люка-Лемера для проверки простоты числа Мерсенна.
    :param p: Показатель степени числа Мерсенна.
    :param m_p: Число Мерсенна 2^p - 1.
    :return: True, если число Мерсенна простое, иначе False.
    """
    s = gmpy2.mpz(4)
    const_2 = gmpy2.mpz(2)
    M_p = m_p - gmpy2.mpz(1)  # M_p = 2^p - 1

    # Итеративное вычисление последовательности S_i
    for _ in range(p - const_2):
        s = (s * s - const_2) % M_p

    # Если s == 0, то число Мерсенна является простым
    return s == 0


def proc_center(primes: List[int]) -> List[int]:
    """
    Проверяет список простых чисел на соответствие числам Мерсенна.
    :param primes: Список простых чисел.
    :return: Список показателей степеней p, для которых 2^p - 1 является простым.
    """
    res = []
    m_p = gmpy2.mpz(1)
    previous = gmpy2.mpz(0)

    for p in primes:
        p = gmpy2.mpz(p)
        m_p <<= p - previous  # Обновляем m_p = 2^p - 1

        if lucas_lehmer_test(p, m_p):
            res.append(int(p))
        previous = p
    return res


def mersenne_primes(maxi: int, procs: int = 2) -> np.ndarray:
    """
    Основная функция, выполняющая параллельную проверку простых чисел Мерсенна.
    :param maxi: Верхняя граница диапазона простых чисел.
    :param procs: Количество процессов для параллельного вычисления.
    :return: Массив показателей степеней p, для которых 2^p - 1 простые.
    """
    primes = prime_num(maxi)  # Получаем список простых чисел
    partitions = logarithmic_partition(0, len(primes), procs)  # Разбиение списка

    with multiprocessing.Pool(procs) as executor:
        active = executor.map(proc_center,
                              [primes[mini: partitions[i + 1]] for i, mini in enumerate(partitions[:-1])])

    return np.concatenate(active)