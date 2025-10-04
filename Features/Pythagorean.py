from typing import List, Tuple


def pythagorean_triple_1(num: int) -> List[Tuple[int, int, int]]:
    """
    Находит все Пифагоровы тройки (a, b, c) для заданного периметра.

    :param num: Целое число, периметр тройки.
    :return: Список Пифагоровых троек (a, b, c).

    >>> pythagorean_triple_1(12)
    [(3, 4, 5)]
    """
    result = []
    for a in range(1, num // 3):
        num_a = num - a
        a2 = a ** 2
        for b in range(a + 1, num_a // 2):
            c = num_a - b
            if c ** 2 == a2 + b ** 2:
                result.append((a, b, c))
                break
    return result


def pythagorean_triple_2(num: int) -> List[Tuple[int, int]]:
    """
    Находит все Пифагоровы тройки (a, b) для заданного c.

    :param num: Целое число, значение c.
    :return: Список пар (a, b) для Пифагоровых тройек.

    >>> pythagorean_triple_2(25)
    [(7, 24)]
    """
    num_list = []
    maxi = num
    num = int(num ** 0.5)
    for a in range(1, num // 2):
        a2 = a ** 2
        for b in range(a, num + 1):
            if a2 + b ** 2 == maxi:
                num_list.append((a, b))
                break
    return num_list


def whole_right_triangles(maxim: int) -> Tuple[List[Tuple[int, int, int]], int, int]:
    """
    Находит значение p, дающее максимальное количество Пифагоровых троек
    для всех p ≤ maxim, а также возвращает количество найденных троек.

    :param maxim: Целое число, максимальное значение периметра p для поиска.
    :return: Кортеж, содержащий:
        - список найденных Пифагоровых троек для максимального p,
        - количество найденных троек,
        - значение p, дающее максимальное количество троек.

    >>> whole_right_triangles(12)
    ([(3, 4, 5)], 1, 12)
    """
    result = max(map(pythagorean_triple_1, range(1, maxim + 1)), key=len)
    length = len(result)
    p = sum(result[0]) if result else 0
    return result, length, p
