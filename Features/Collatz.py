def memoize(function):
    """
    Декоратор для мемоизации результата функции.

    :param function: Функция, результаты которой необходимо кэшировать.
    :return: Обёртка функции с кэшированием.

    >>> memoized_collatz = memoize(collatz)
    >>> memoized_collatz(5)
    (6, [5, 16, 8, 4, 2, 1])
    """
    memo_cache = {}

    def wrapped_function(num: int) -> tuple[int, list[int]]:
        if num in memo_cache:
            return memo_cache[num]
        result = function(num)
        memo_cache[num] = result
        return result

    wrapped_function.memo_cache = memo_cache
    return wrapped_function


@memoize
def collatz(starting_number: int) -> tuple[int, list[int]]:
    """
    Находит последовательность Коллатца для заданного числа.

    :param starting_number: Целое число.
    :return: Длина последовательности и сама последовательность.

    >>> collatz(5)
    (6, [5, 16, 8, 4, 2, 1])
    """
    sequence = [starting_number]
    length = 1  # Инициализация длины последовательности

    while starting_number != 1:
        starting_number = starting_number // 2 if starting_number % 2 == 0 else 3 * starting_number + 1
        sequence.append(starting_number)
        length += 1

    return length, sequence


def find_longest_collatz(max_limit: int) -> tuple[int, int]:
    """
    Находит самую длинную последовательность Коллатца для чисел до заданного числа.

    :param max_limit: Максимальное число, ограничение.
    :return: Длина самой длинной последовательности и начальное число этой последовательности.

    >>> find_longest_collatz(10)
    (7, 9)
    """
    max_length = 0
    starting_number_with_max_length = 0  # Переменная для хранения начального числа

    for number in range(2, max_limit):
        length, _ = collatz(number)  # Получаем длину и саму последовательность
        if length > max_length:
            max_length = length
            starting_number_with_max_length = number  # Обновляем начальное число

    return max_length, starting_number_with_max_length
