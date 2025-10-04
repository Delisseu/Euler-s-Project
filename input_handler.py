from form import Check_methods, Type_methods

"""
Модуль для обработки ввода пользователя.
"""


def get_user_input(prompt: str) -> str:
    """
    Получает ввод пользователя на основе запроса.

    :param prompt: Запрос ввода.
    :return: Ввод пользователя в нужном формате.
    """
    if prompt == 'Введите многострочный ввод (Введите "END" для завершения ввода):':
        user_input = []
        while True:
            line = input()
            if line == 'END':
                break
            user_input.append(line)
        return "\n".join(user_input)
    else:
        user_input = input(f'\n{prompt}\n')
        return user_input


def check_input(user_input: str, user_inputs: list, method: str) -> tuple:
    """
    Проверяет корректность введенных данных.

    :param user_input: Ввод пользователя.
    :param user_inputs: Список предыдущих вводов.
    :param method: Метод проверки вводимых данных.
    :return: Кортеж с результатом проверки и булевым значением.
    """

    if len(str(user_inputs)) > 4300:
        return "Входные данные должны быть не более 4300 символов в длинну!", False

    length = len(user_inputs)
    # Какой по счету элемент мы проверяем
    # Получаем список условий для текущего метода проверки
    type_method, condition, error_message = Check_methods[method][length]

    t_method_condition, t_error_message = Type_methods[type_method]
    # Проверяем тип данных
    try:
        user_input = t_method_condition(user_input)
        if user_input is False:
            raise ValueError
    except ValueError:
        return t_error_message, False

    # Проверка других условий
    if not condition(user_input, user_inputs):
        return error_message, False

    return user_input, True  # Ввод корректен
