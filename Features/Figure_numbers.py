import functools
import math


@functools.cache
def is_octagonal(number):
    if number <= 0:
        return None, False

    # Решаем уравнение для n
    discriminant = 1 + 3 * number
    sqrt_d = math.sqrt(discriminant)

    # Вычисляем n
    n = (1 + sqrt_d) / 3
    return int(n), n.is_integer() and sqrt_d.is_integer()


@functools.cache
def nearest_octagonal_positive(number):
    curr, flag = is_octagonal(number)
    if not flag:
        curr += 1
        number = curr * (3 * curr - 2)
    return int(number), curr * 6 + 1


@functools.cache
def next_octagonal(number, step=None):
    if not step:
        curr, _ = is_octagonal(number)
        step = curr * 6 + 1
    return number + step, step + 6


@functools.cache
def is_triangular(number):
    # Решаем уравнение n^2 + n - 2x = 0
    if number <= 0:
        return None, False
    discriminant = 1 + 8 * number

    sqrt_d = math.sqrt(discriminant)
    n = (-1 + sqrt_d) / 2
    return int(n), n.is_integer() and sqrt_d.is_integer()


@functools.cache
def nearest_triangle_positive(number):
    curr, flag = is_triangular(number)
    if not flag:
        curr += 1
        number = curr * (curr + 1) / 2
    return int(number), curr + 1


@functools.cache
def next_triangle(number, step=None):
    if not step:
        curr, _ = is_triangular(number)
        step = curr + 1
    return number + step, step + 1


@functools.cache
def is_square(number):
    # Решаем уравнение n^2 + n - 2x = 0
    if number <= 0:
        return None, False

    sqrt_n = math.sqrt(number)
    return int(sqrt_n), sqrt_n.is_integer()


@functools.cache
def nearest_square_positive(number):
    curr, flag = is_square(number)
    if not flag:
        curr += 1
        number = curr ** 2
    return int(number), curr * 2 + 1


@functools.cache
def next_square(number, step=None):
    if not step:
        curr, _ = is_square(number)
        step = curr * 2 + 1
    return number + step, step + 2


@functools.cache
def is_pentagonal(number):
    if number <= 0:
        return None, False
    discriminant = 1 + 24 * number

    sqrt_d = math.sqrt(discriminant)
    n = (1 + sqrt_d) / 6
    return int(n), n.is_integer() and sqrt_d.is_integer()


@functools.cache
def nearest_pentagonal_positive(number):
    curr, flag = is_pentagonal(number)
    if not flag:
        curr += 1
        number = curr * (3 * curr - 1) / 2
    return int(number), curr * 3 + 1


@functools.cache
def next_pentagonal(number, step=None):
    if not step:
        curr, _ = is_pentagonal(number)
        step = curr * 3 + 1
    return number + step, step + 3


@functools.cache
def is_hexagonal(number):
    if number <= 0:
        return None, False
    discriminant = 1 + 8 * number

    sqrt_d = math.sqrt(discriminant)
    n = (1 + sqrt_d) / 4
    return int(n), n.is_integer() and sqrt_d.is_integer()


@functools.cache
def nearest_hexagonal_positive(number):
    curr, flag = is_pentagonal(number)
    if not flag:
        curr += 1
        number = curr * (2 * curr - 1)
    return int(number), curr * 4 + 1


@functools.cache
def next_hexagonal(number, step=None):
    if not step:
        curr, _ = is_pentagonal(number)
        step = curr * 4 + 1
    return number + step, step + 4


@functools.cache
def is_heptagonal(number):
    if number <= 0:
        return None, False
    discriminant = 9 + 40 * number

    sqrt_d = math.sqrt(discriminant)
    n = (3 + sqrt_d) / 10
    return int(n), n.is_integer() and sqrt_d.is_integer()


@functools.cache
def nearest_heptagonal_positive(number):
    curr, flag = is_pentagonal(number)
    if not flag:
        curr += 1
        number = curr * (5 * curr - 3) / 2
    return int(number), curr * 5 + 1


@functools.cache
def next_heptagonal(number, step=None):
    if not step:
        curr, _ = is_pentagonal(number)
        step = curr * 5 + 1
    return number + step, step + 5
