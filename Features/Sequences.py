import itertools

from .my_utils import *

from .Figure_numbers import *


def spiral_diagonals_sum(maximum: int) -> int:
    """
    Вычисляет сумму диагоналей спирали, построенной из натуральных чисел.

    :param maximum: Максимальный размер спирали (должен быть нечётным).
    :return: Сумма диагоналей спирали.

    """
    diagonal_sum = 0
    for size in range(3, maximum + 1, 2):
        diagonal_sum += sum([size ** 2, size ** 2 - (size - 1), size ** 2 - (size - 1) * 2, size ** 2 - (size - 1) * 3])
    return diagonal_sum


def triangular_numbers(max_num: int) -> List[int]:
    """
    Находит треугольные числа до заданного числа.

    :param max_num: Целое число, верхняя граница для треугольных чисел.
    :return: Список треугольных чисел.

    """
    current_number = 0
    triangular_nums = [0]
    while triangular_nums[-1] < max_num:
        current_number += 1
        triangular_nums.append(triangular_nums[-1] + current_number)
    return triangular_nums[1:-1]


def fibonacci(max_num: int) -> List[int]:
    """
    Находит числа Фибоначчи до заданного числа.

    :param max_num: Целое число, верхняя граница для чисел Фибоначчи.
    :return: Список чисел Фибоначчи.
    """
    fib_sequence = [0, 1]
    while fib_sequence[-1] <= max_num:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    if fib_sequence[-1] >= max_num:
        fib_sequence.pop()
    return fib_sequence


def count_triangular_words(words: List[str]) -> int:
    """
    Считает количество треугольных слов в заданном списке.

    :param words: Список слов.
    :return: Количество треугольных слов.

    """

    # Мемоизация треугольных чисел
    def memoize_triangular_numbers(func):
        def wrapper(maxi):
            return func(maxi)

        wrapper.triangular_nums = [1]  # Начальное треугольное число
        wrapper.n = 2  # Начинаем с n=2
        return wrapper

    @memoize_triangular_numbers
    def triangular_numbers(maxi):
        while triangular_numbers.triangular_nums[-1] < maxi:
            next_num = triangular_numbers.n * (triangular_numbers.n + 1) // 2
            triangular_numbers.triangular_nums.append(next_num)
            triangular_numbers.n += 1
        return triangular_numbers.triangular_nums

    def word_value(word: str) -> int:
        """Возвращает числовое значение слова."""
        return sum(ord(c) - ord('A') + 1 for c in word)

    def is_triangular_word(word: str) -> bool:
        """Проверяет, является ли значение слова треугольным."""
        word_val = word_value(word)
        if word_val > triangular_numbers.triangular_nums[-1]:
            triangular_numbers(word_val)
        return word_val in triangular_numbers.triangular_nums

    triangular_word_count = sum(1 for word in words if is_triangular_word(word))
    return triangular_word_count


def triangular_pentagonal_hexagonal(max_id: int) -> List[int]:
    """
    Находит шестиугольные числа, которые также являются пентагональными.

    :param max_id: Максимальное количество найденных чисел.
    :return: Список шестиугольных чисел, которые являются пентагональными.
    """
    if max_id > 66:
        max_id = 66

    def hexagonal_number(n: int) -> int:
        """Возвращает n-е шестиугольное число."""
        return n * (2 * n - 1)

    def estimate_growth_rate(hexagonal_numbers_list: List[int]) -> float:
        """Оценивает скорость роста шестиугольных чисел."""
        return hexagonal_numbers_list[-1] / hexagonal_numbers_list[-2] if len(hexagonal_numbers_list) > 1 else 1.0

    step_increment = 9
    hexagonal_numbers = []
    current_hexagonal = 6

    while len(hexagonal_numbers) < max_id:
        if is_pentagonal(current_hexagonal):
            hexagonal_numbers.append(current_hexagonal)

            if len(hexagonal_numbers) > 1:
                growth_rate = estimate_growth_rate(hexagonal_numbers) - 1
                suspect = current_hexagonal * growth_rate
                n = int((1 + (1 + 8 * suspect) ** 0.5) / 4)
                previous_hexagonal = hexagonal_number(n - 1)
                current_hexagonal = hexagonal_number(n)
                step_increment = current_hexagonal - previous_hexagonal + 4
                continue

        current_hexagonal, step_increment = next_hexagonal(current_hexagonal, step_increment)

    return hexagonal_numbers


def cyclic_figur_nums(n: int) -> list[int] | None:
    """
    Находит набор циклических многоугольных чисел заданной длины.

    Параметры:
        n (int): Количество используемых многоугольных чисел.

    Возвращаемое значение:
        list[int]| None:
            - Список найденных циклических чисел.
            - Если n нечетное, возвращает None.
    """
    # Проверка на четность, так как алгоритм требует парного разбиения числа
    if n % 2 != 0:
        return None

    # Определение функций для поиска многоугольных чисел
    funcs = [
        (nearest_triangle_positive, next_triangle),
        (nearest_square_positive, next_square),
        (nearest_pentagonal_positive, next_pentagonal),
        (nearest_hexagonal_positive, next_hexagonal),
        (nearest_heptagonal_positive, next_heptagonal),
        (nearest_octagonal_positive, next_octagonal),
    ]

    half_len = n // 2  # Половина длины числа
    end = 10 ** n  # Верхний предел поиска
    start = end / 10  # Нижний предел поиска

    # Перебираем все возможные комбинации функций
    for funcs_comb in itertools.permutations(funcs):
        curr_num, step = funcs[0][0](start)  # Начальное число
        parameters = [(curr_num, end, step)]  # Список текущих параметров поиска

        while True:
            not_zero = False
            curr_num, curr_max, step = parameters[-1]  # Текущие параметры

            # Если число превысило предел, откатываемся на предыдущий шаг
            if curr_num >= curr_max:
                parameters.pop()
                if not parameters:
                    break  # Завершаем поиск, если нет возможных значений
                curr_num, curr_max, step = parameters[-1]
                curr_nearest_func, curr_next_func = funcs_comb[len(parameters) - 1]
                curr_num, step = curr_next_func(curr_num, step)
                parameters[-1] = (curr_num, curr_max, step)
                continue

            # Следующая функция для проверки
            next_nearest_func = funcs_comb[len(parameters)][0]
            curr_digits = get_digits(curr_num)  # Получаем цифры текущего числа

            # Проверяем, содержит ли число ненулевые значения в нужной половине
            if 0 not in curr_digits[half_len:-1]:
                # Если последний элемент, проверяем замыкание цикла
                if len(parameters) == len(funcs) - 1:
                    curr_new = massive_concatenate(curr_digits[half_len:] + get_digits(parameters[0][0])[:half_len])
                    if next_nearest_func(curr_new)[0] == curr_new:
                        return [x[0] for x in parameters] + [curr_new]
                    else:
                        curr_nearest_func, curr_next_func = funcs_comb[len(parameters) - 1]
                        curr_num, step = curr_next_func(curr_num, step)
                        parameters[-1] = (curr_num, curr_max, step)
                        continue

                # Формируем новое число для следующего шага
                sus_new = massive_concatenate(curr_digits[half_len:] + [0] * half_len)
                curr_new, new_step = next_nearest_func(sus_new)
                new_max = sus_new + 10 ** half_len
                not_zero = True

            # Если не удалось найти подходящее число, откатываемся назад
            if not not_zero or curr_new >= new_max:
                curr_nearest_func, curr_next_func = funcs_comb[len(parameters) - 1]
                curr_num, step = curr_next_func(curr_num, step)
                parameters[-1] = (curr_num, curr_max, step)
                continue

            # Добавляем новое число в параметры
            parameters.append((curr_new, new_max, new_step))
