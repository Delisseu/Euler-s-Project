import bisect
import math

from .my_utils import get_digits

from .MathOperations import perform_action
from .PrimeNumbers import prime_num


def count_ways_to_make_change(coins: list, target_sum: int) -> int:
    """
    Считает количество способов сделать сумму с помощью заданных монет.

    :param coins: список доступных монет.
    :param target_sum: целевая сумма.
    :return: количество способов.
    """
    dp = [0] * (target_sum + 1)
    dp[0] = 1

    for coin in coins:
        for i in range(coin, target_sum + 1):
            dp[i] += dp[i - coin]

    return dp[target_sum]


def sum_fifth_powers_digits(power: int) -> list:
    """
    Находит числа, равные сумме своих цифр в пятой степени.

    :param power: степень.
    :return: список подходящих чисел.
    """
    if power == 1:
        return []
    minim = 2 ** power
    char_num = 0
    result = []

    while True:
        char_num += 1
        maxim = 9 ** power * char_num
        if maxim < 10 ** char_num:
            break

    for num in range(minim, maxim):
        if num == sum(int(digit) ** power for digit in str(num)):
            result.append(num)

    return result


def distinct_powers_count(max_num: int, min_num: int) -> tuple:
    """
    Считает количество различных степеней чисел в заданном диапазоне.

    :param max_num: максимальное число.
    :param min_num: минимальное число.
    :return: множество различных степеней и их количество.
    """
    result = set()
    for num in range(min_num, max_num + 1):
        for power in range(min_num, max_num + 1):
            result.add(num ** power)
    return sorted(result), len(result)


def fraction(maximum: int) -> tuple:
    """
    Находит знаменатель с самой длинной периодической частью в дроби 1/denominator.

    :param maximum: максимальный знаменатель.
    :return: лучший знаменатель и длина периодической части.
    """
    numerator = 1
    max_length = 0
    best_denominator = 0

    for denominator in range(2, maximum):
        remainders = {}
        remainder = numerator
        position = 0

        while remainder != 0 and remainder not in remainders:
            remainders[remainder] = position
            remainder = (remainder * 10) % denominator
            position += 1

        if remainder != 0 and remainder in remainders:
            cycle_length = position - remainders[remainder]
            if cycle_length > max_length:
                max_length = cycle_length
                best_denominator = denominator

    return best_denominator, max_length


def dictionary_permutations(nums: list, desired: int) -> str:
    """
    Возвращает нужную перестановку из списка чисел.

    :param nums: список чисел.
    :param desired: индекс желаемой перестановки.
    :return: строка нужной перестановки.
    """
    nums = list(set(nums))
    ready = []

    if math.factorial(len(nums)) > desired:
        while nums:
            diapason = math.factorial(len(nums) - 1)
            index = desired // diapason
            ready.append(nums[index])
            desired -= index * diapason
            del nums[index]
        return ''.join(map(str, ready))

    return None


def name_score(names: list) -> int:
    """
    Считает сумму очков имен на основе их позиции в алфавитном порядке.

    :param names: список имен.
    :return: сумма очков имен.
    """
    names.sort()
    total_score = 0
    for index, name in enumerate(names):
        name_score = sum(ord(char) - ord('A') + 1 for char in name)
        total_score += name_score * (index + 1)

    return total_score


def sum_digit_factorial(fact: int) -> int:
    """
    Считает сумму цифр факториала числа.

    :param fact: целое число для расчета факториала.
    :return: сумма цифр факториала.
    """
    return sum(int(digit) for digit in str(math.factorial(fact)))


def counting_sundays(max_year: int, min_year: int, day: int) -> int:
    """
    Считает количество воскресений, выпадающих на первое число месяца.

    :param max_year: конечный год.
    :param min_year: начальный год.
    :param day: день недели от 1 до 7.
    :return: количество воскресений.
    """
    sunday_count = 0
    while min_year < max_year:
        feb = 28
        if (min_year % 4 == 0 and min_year % 100 != 0) or (min_year % 400 == 0):
            feb = 29

        for month in range(1, 13):
            if month in (4, 6, 9, 11):
                days = 30
            elif month == 2:
                days = feb
            else:
                days = 31

            day += days
            if day % 7 == 0:
                sunday_count += 1

        min_year += 1

    return sunday_count


def sum_of_digits_of_degree(num: int, degree: int) -> int:
    """
    Считает сумму цифр степени числа.

    :param num: целое число.
    :param degree: степень.
    :return: сумма цифр.

    """
    return sum(map(int, str(num ** degree)))


def least_multiple(max_num: int) -> tuple:
    """
    Находит наименьшее общее кратное для чисел до max_num.

    :param max_num: целое число.
    :return: наименьшее общее кратное и список простых множителей.
    """
    multiples = []
    primes = prime_num(max_num)

    for prime in primes:
        prime_power = prime
        while prime_power <= max_num:
            multiples.append(prime_power)
            prime_power *= prime

    return perform_action("*", tuple(multiples)), sorted(multiples)


def multiplication_check(chars: int, num_list: list) -> tuple:
    """
    Проверяет числа на возможность их представления в виде произведения двух чисел.

    :param chars: количество знаков.
    :param num_list: список чисел.
    :return: список чисел и строка с результатами.

    """
    max_num = int(10 ** chars - 1)
    min_num = (max_num // 10 + 1)
    sort_list = num_list[bisect.bisect_left(num_list, min_num ** 2): bisect.bisect_left(num_list, max_num ** 2)]
    valid_products = []
    multiplication_results = []

    for sort_num in sort_list:
        for first in range(max(min_num, sort_num // max_num), int(sort_num ** 0.5) + 1):
            if sort_num % first == 0:
                second = sort_num // first
                if max_num > second > min_num:
                    multiplication_results.append(f"{sort_num} = {first} * {second}\n")
                    valid_products.append(sort_num)
                    break

    return valid_products, ''.join(multiplication_results)


def list_set(num_list: list) -> set:
    """
    Удаляет дубликаты из списка.

    :param num_list: список чисел.
    :return: множество без дубликатов.
    """
    return set(num_list)


def list_sort(num_list: list) -> list:
    """
    Сортирует список.

    :param num_list: список чисел.
    :return: отсортированный список.
    """
    return sorted(num_list)


def list_filter(num_list: list, max_num: int, min_num: int) -> list:
    """
    Фильтрует список, обрезая по максимальному и минимальному значению.

    :param num_list: список чисел.
    :param max_num: максимальное значение.
    :param min_num: минимальное значение.
    :return: отфильтрованный список.
    """
    num_list.sort()
    return num_list[bisect.bisect_left(num_list, min_num):bisect.bisect_left(num_list, max_num)]


def max_sum_digits(max_num: int, max_degree: int) -> tuple[int, tuple[int, int, int]]:
    """
    Находит число и его степень, при которых сумма цифр результата максимальна.

    Параметры:
        max_num (int): Верхняя граница для основания числа.
        max_degree (int): Верхняя граница степени.

    Возвращаемое значение:
        tuple[int, tuple[int, int, int]]:
            - Максимальная сумма цифр среди всех возможных степеней.
            - Кортеж (основание числа, степень).
    """
    res = [0, (0, 0, 0)]
    for num in range(1, max_num):
        cur_num = num
        for degree in range(2, max_degree):
            cur_num *= num
            res = max(res, [sum(get_digits(cur_num)), (num, degree)], key=lambda x: x[0])
    return res


def combinatorial_samples(max_n: int, min_num: int, ) -> int:
    """
    Вычисляет количество сочетаний C(n, r), превышающих `min_num`,
    для 1 ≤ n ≤ max_n.

    Параметры:
        min_num (int): Минимальный порог для значений сочетаний C(n, r).
        max_n (int): Максимальное значение n для вычисления сочетаний.

    Возвращаемое значение:
        int: Количество сочетаний, превышающих `min_num`.
    """
    res = 0  # Счетчик подходящих сочетаний
    n_f = 1  # Факториал n (инициализируется для n = 1)

    for n in range(1, max_n + 1):
        base_r = n // 2  # Базовое значение r (центр биномиального треугольника)
        r = base_r

        # Вычисляем C(n, r) = n! / (r! * (n-r)!)
        n_f *= n
        r_f = math.factorial(r)
        n_r_f = math.factorial(n - r)

        # Проверяем, превышает ли C(n, r) заданный порог
        while n_f / (r_f * n_r_f) > min_num:
            n_r_f *= n - r + 1  # Пересчитываем факториал (n-r)!
            r_f //= r  # Пересчитываем r!
            r -= 1  # Уменьшаем r

        if base_r != r:
            res += (base_r - r) * 2  # Учитываем симметрию биномиального коэффициента
            if n % 2 == 0:
                res -= 1  # Корректируем для четных n

    return res


def multiples_rearranged_digits(maxi: int) -> list[int]:
    """
    Находит `maxi` чисел, у которых множители 2x, 3x, 4x, 5x и 6x содержат те же цифры.

    Параметры:
        maxi (int, по умолчанию 1): Количество чисел, которые нужно найти.

    Возвращаемое значение:
        list[int]: Список найденных чисел.
    """
    results = []  # Список чисел, удовлетворяющих условию
    num = 0  # Текущее проверяемое число
    factors = range(6, 1, -1)  # Факторы умножения (от 6 до 2)

    while len(results) < maxi:
        num += 1  # Проверяем следующее число
        orig_digits = set(get_digits(num))  # Цифры исходного числа

        for factor in factors:
            multiplied_digits = get_digits(num * factor)  # Цифры умноженного числа
            if any(digit not in orig_digits for digit in multiplied_digits):
                break  # Если хотя бы одна цифра отличается — число не подходит
        else:
            results.append(num)  # Если прошли все проверки, добавляем число в список

    return results
