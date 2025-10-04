import tkinter as tk
from tkinter import ttk
from typing import Optional

from form import input_library_with_nums
from input_handler import check_input
from interface.Interface_logic import copy, cut, paste, ButtonVisual_PIL, BasicButton, CustomLogic, show_message
from interface.image_handler import (create_figureimage, Image, ImageTk,
                                     rgb_to_hex, darken_image, collage_extraction)
from tester import tester
from writer import *


class ConditionsWindow:
    """
    Класс ConditionsWindow управляет окном, в котором пользователь вводит условия для тестовой функции.
    Он отвечает за:
      - Инициализацию графических компонентов (окна, поля ввода, метки, кнопки);
      - Анимацию текста и ожидание ответа;
      - Обработку ввода пользователя и получение результата (с использованием кеша или тестера).
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Инициализирует окно условий.

        Args:
            root (tk.Tk): Корневое окно приложения.
        """
        self.root = root

        self._init_window()
        self._init_entry()
        self._init_label()
        self._init_buttons()
        self._init_wait_window()
        self.is_active: bool = False
        self.key: Optional[Any] = None
        self.conditions: List[Any] = []
        self.inputs: List[Any] = []
        self.reply_containter: List[Any] = []

    def _start_wait(self) -> None:
        """
        Запускает анимацию ожидания.
        """
        self.wait_anim_current_frame = 0
        self.wait_window.place(x=0, y=0)
        self.is_wait = True
        self._wait_anim()

    def _stop_wait(self) -> None:
        """
        Останавливает анимацию ожидания и скрывает окно ожидания.
        """
        self.wait_window.place_forget()
        self.is_wait = False

    def _wait_anim(self) -> None:
        """
        Анимирует окно ожидания: циклически меняет изображение из wait_collage.
        Вызывается с помощью метода after, создавая эффект анимации.
        """
        if len(self.reply_containter) > 0:
            return self._result_handler()
        if self.wait_anim_current_frame == len(self.wait_collage):
            self.wait_anim_current_frame = 0
        self.wait_window.itemconfig(
            self.wait_window_image,
            image=self.wait_collage[self.wait_anim_current_frame]
        )
        self.wait_anim_current_frame += 1
        self.canvas.after(20, self._wait_anim)

    def _cancel_condition(self) -> None:
        """
        Отменяет последнее введённое условие:
          - Очищает поле ввода;
          - Удаляет последний элемент из списка inputs;
          - Перезапускает анимацию текста.
        """
        self.entry.delete("1.0", tk.END)
        if len(self.inputs) == 0:
            return
        self.inputs.pop()
        self.animate_condition_text()

    def _check_condition(self) -> None:
        """
        Проверяет корректность введённого условия:
          - Извлекает и очищает введённый текст;
          - Преобразует ввод с помощью функции check_input;
          - Если ввод корректен, добавляет его в список inputs и либо вызывает получение результата,
            либо обновляет анимацию текста;
          - В случае ошибки выводит сообщение.
        """
        if len(self.inputs) < len(self.conditions[2]):
            user_input = self.entry.get("1.0", tk.END).strip()
            self.entry.delete("1.0", tk.END)

            formed_input = check_input(user_input, self.inputs, self.conditions[0])
            if formed_input[1] is True:
                self.inputs.append(formed_input[0])
                if len(self.inputs) == len(self.conditions[2]):
                    self._get_result()
                else:
                    self.animate_condition_text()
            else:
                show_message(formed_input[0])

    def _get_result(self) -> None:
        """
        Получает результат работы функции:
          - Сначала пытается получить кешированный ответ;
          - Если он найден, сразу выводит его;
          - Если нет, запускает тестер, начинает анимацию ожидания и вызывает обработку ответа.
        """
        cached_reply = cache(self.key, self.inputs)

        if cached_reply:
            self._give_result(cached_reply)
        else:
            tester(self.conditions[1], self.inputs, self.wait_window.label, self.reply_containter,
                   constants.get('Waiting_time'))
            self._start_wait()

    def _result_handler(self) -> None:
        """
        Обрабатывает полученный ответ:
          - Если ответ не None, сохраняет его в кеше и выводит;
          - Если результат отсутствует (None), удаляет последний ввод и выводит сообщение.
          После обработки анимация ожидания прекращается.
        """
        if self.reply_containter:
            self.reply_containter = self.reply_containter[- constants.get('Max_result_Len'):]
            write(self.key, self.inputs, self.reply_containter)
        self._give_result(self.reply_containter)
        self._stop_wait()

    def _give_result(self, reply: Any) -> None:
        """
        Выводит результат в текстовое поле и обновляет анимацию текста.

        Args:
            reply (Any): Результат, который необходимо отобразить.
        """
        self.entry.insert("1.0", reply)
        self.animate_condition_text(reply)

    def _back(self) -> None:
        """
        Возвращает пользователя в главное меню:
          - Очищает текстовое поле;
          - Сбрасывает флаг активности и положение анимации текста;
          - Показывает главное меню и скрывает текущее окно.
        """
        self.entry.delete("1.0", tk.END)
        self.is_active = False
        self.text_pos = 0
        self.main_menu_frame.place(x=0, y=0)
        self.frame.place_forget()

    def _init_label(self) -> None:
        """
        Инициализирует метку для отображения условий.
        Размещает метку по центру окна.
        """
        x, y = constants.get('Width_main') // 2, constants.get('Height_main') // 2
        self.label = tk.Label(self.canvas, text="TEST",
                              font=(constants.get('Base_font')[0], int(constants.get('Base_font')[1] * 1.5)))
        self.label.place(x=x, y=y, anchor="center")

    def _init_wait_window(self) -> None:
        """
        Создает окно ожидания с анимацией (набор изображений из wait_collage).
        На канвасе wait_window размещается изображение и дополнительная метка.
        """
        self.wait_window = tk.Canvas(self.canvas, width=constants.get('Width_main'),
                                     height=constants.get('Height_main'))
        self.wait_window.label = tk.Label(self.wait_window, text="")
        x, y, anchor = constants.get('Width_main') // 2, constants.get('Height_main') // 2, "center"
        self.wait_collage = collage_extraction(constants.get('Path_to_wait_collage'), ".png",
                                               constants.get('Height_main') // 15, constants.get('Height_main') // 15)
        self.wait_window_image = self.wait_window.create_image(x, y, anchor=anchor, image=self.wait_collage[0])
        self.wait_window.label.place(x=x, y=int(y * 1.3), anchor=anchor)

    def _init_buttons(self) -> None:
        """
        Инициализирует кнопки:
          - Кнопка "Назад" (слева вверху);
          - Кнопка "Отправить" (с определенными координатами);
          - Кнопка "Отмена" для отмены последнего ввода.
        Для кнопок используются изображения, измененные с помощью darken_image.
        """
        buttons_width, buttons_height = constants.get('Height_main') // 20, constants.get('Height_main') // 23
        base_image = Image.open(constants.get('Path_to_arrow')).resize((buttons_width, buttons_height))
        base_image_darker = darken_image(base_image, 0.8)

        inverse_image = Image.open(constants.get('Path_to_arrow_inverse')).resize(
            (int(buttons_width * 0.8), int(buttons_height * 0.8)))
        inverse_image_darker = darken_image(inverse_image, 0.8)

        base_image, base_image_darker, inverse_image, inverse_image_darker = map(ImageTk.PhotoImage, (
            base_image, base_image_darker, inverse_image, inverse_image_darker))

        back_button_visual = ButtonVisual_PIL(base_image, base_image_darker, base_image_darker)
        send_button_visual = ButtonVisual_PIL(inverse_image, inverse_image_darker, inverse_image_darker)
        back_button_logic = CustomLogic(self._back)
        send_button_logic = CustomLogic(self._check_condition)
        cancel_button_logic = CustomLogic(self._cancel_condition)

        # Координаты кнопки "Отправить" зависят от разрешения экрана
        if constants.get('Width_main') < 1280:
            send_button_x, send_button_y = int(constants.get('Width_main') // 1.57), int(
                constants.get('Height_main') // 1.3)
        else:
            send_button_x, send_button_y = int(constants.get('Width_main') // 1.532), int(
                constants.get('Height_main') // 1.295)

        BasicButton(self.canvas, constants.get('Height_main') // 100, constants.get('Height_main') // 100, base_image,
                    back_button_visual,
                    back_button_logic, anchor="nw")
        BasicButton(self.canvas, send_button_x, send_button_y, inverse_image, send_button_visual,
                    send_button_logic)
        BasicButton(self.canvas, int(constants.get('Width_main') // 3.25), send_button_y, base_image,
                    back_button_visual,
                    cancel_button_logic)

    def _init_entry(self) -> None:
        """
        Инициализирует текстовое поле для ввода условия.
        Создает фон для поля, рамку и настраивает прокрутку, а также привязывает обработчики для операций копирования, вырезания и вставки.
        """

        def _init_bg_entry() -> Tuple[int, int, int, int]:
            x, y = constants.get('Width_main') // 2, int(constants.get('Height_main') * 0.7)
            bg_width = int(constants.get('Width_main') * 0.34)
            bg_height = int(constants.get('Height_main') * 0.23)
            entry_bg = Image.new("RGBA", (bg_width, bg_height), constants.get('Base_back_ground'))
            entry_bg = create_figureimage("rounded_rectangle", entry_bg, constants.get('Round_radius'))
            entry_bg = ImageTk.PhotoImage(entry_bg)
            self.canvas.create_image(x, y, image=entry_bg)
            self.canvas.image = entry_bg  # Сохраняем ссылку, чтобы изображение не было удалено сборщиком мусора
            return bg_width, bg_height, x, y

        bg_width, bg_height, x, y = _init_bg_entry()
        bg_color = rgb_to_hex(*constants.get('Base_back_ground'))

        entry_frame = tk.Frame(self.canvas, width=int(constants.get('Width_main') * 0.32),
                               height=int(constants.get('Height_main') * 0.17))
        entry_frame.place(x=x - int(bg_width // 2.22), y=y - int(bg_height // 2.3), anchor="nw")

        dict_of_sizes = {1920: (37, 5), 1600: (38, 5), 1366: (35, 5), 1280: (40, 5), 800: (35, 7)}

        if constants.get('Width_main') in dict_of_sizes:
            width_symbols, height_symbols = dict_of_sizes[constants.get('Width_main')]
        else:
            width_symbols, height_symbols = 36, 5

        self.entry = tk.Text(entry_frame, wrap="word", bg=bg_color, bd=0, font=constants.get('Base_font'),
                             width=width_symbols, height=height_symbols)
        self.entry.pack(side="left", fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Vertical.TScrollbar", background="#c0c0c0",
                        troughcolor=bg_color, arrowcolor="#c0c0c0", borderwidth=0, highlightcolor="black")
        style.map("Custom.Vertical.TScrollbar",
                  background=[("active", "#adadad")],
                  arrowcolor=[("active", "#adadad")])

        scrollbar = ttk.Scrollbar(entry_frame, orient="vertical", command=self.entry.yview,
                                  style="Custom.Vertical.TScrollbar")
        scrollbar.pack(side="right", fill="y")

        self.entry.configure(yscrollcommand=scrollbar.set)
        self.entry.bind("<Control-c>", copy)
        self.entry.bind("<Control-x>", cut)
        self.entry.bind("<Control-v>", paste)

    def _init_window(self) -> None:
        """
        Инициализирует основной фрейм и canvas для отображения окна условий.
        """
        self.frame = tk.Frame(self.root, width=constants.get('Width_main'), height=constants.get('Height_main'))
        self.canvas = tk.Canvas(self.frame, width=constants.get('Width_main'), height=constants.get('Height_main'),
                                highlightthickness=0)
        self.canvas.place(x=0, y=0)

    def activate(self) -> None:
        """
        Активирует окно условий:
          - Скрывает главное меню;
          - Очищает предыдущие вводы;
          - Загружает условия для выбранного ключа;
          - Запускает анимацию текста.
        """
        self.is_active = True
        self.text_pos = 0
        self.main_menu_frame.place_forget()
        self.inputs.clear()
        self.frame.place(x=0, y=0, anchor="nw")
        self.conditions = input_library_with_nums[self.key]
        self.animate_condition_text()

    def animate_condition_text(self, reply: Optional[Any] = None) -> None:
        """
        Анимирует отображение текста условия по символам.
        Если передан параметр reply, используется форматирование строки с подстановкой результата и введенных значений.

        Args:
            reply (Optional[Any]): Результат для форматирования текста (если задан).
        """
        if reply and self.inputs:
            text = self.conditions[3].format(reply=reply, user_inputs=self.inputs)
        else:
            if len(self.inputs) >= len(self.conditions[2]):
                return
            text = self.conditions[2][len(self.inputs)]
        if self.text_pos > len(text) or not self.is_active:
            self.text_pos = 0
            if reply:
                self.reply_containter.clear()
            return
        self.label.configure(text=text[:self.text_pos])
        self.text_pos += 1
        self.frame.after(15, self.animate_condition_text, reply)
