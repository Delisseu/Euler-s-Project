import tkinter as tk
from tkinter import messagebox
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from constants import \
    constants  # Предполагается, что здесь определены такие константы, как Base_font, Round_radius, Waiting_time, Maximum_cache_size, Width_main и Height_main
from interface.animated_canvas_panel import PanelButtonAnim
from interface.image_handler import slider_background, rgb_to_hex, Image, ImageTk, create_figureimage
from writer import write_setting


class ButtonVisual:
    """
    Базовый класс для визуального отображения кнопок.
    Определяет базовую логику смены состояний кнопки (наведение, нажатие, отпускание).
    """

    def __init__(
            self,
            base_status: Any,
            active_button_status: Optional[Any] = None,
            push_button_status: Optional[Any] = None,
            offset: Tuple[int, int] = (0, 0)
    ) -> None:
        """
        Инициализация визуального представления кнопки.

        Args:
            base_status (Any): Изображение или цвет в исходном состоянии.
            active_button_status (Optional[Any]): Изображение/цвет при наведении. Если не задан, используется base_status.
            push_button_status (Optional[Any]): Изображение/цвет при нажатии. Если не задан, используется base_status.
            offset (Tuple[int, int]): Смещение фигуры при нажатии.
        """
        self.base_status = base_status
        self.active_button_status = active_button_status or self.base_status
        self.push_button_status = push_button_status or self.base_status
        self.offset = offset
        self.is_available = True
        self.is_pushed = False
        self.is_active = False
        # Словарь связывает события с соответствующими методами обработки
        self.func_dict: Dict[str, Callable[[tk.Canvas, int, int], None]] = {
            "<Enter>": self.on_hover,
            "<Leave>": self.on_leave,
            "<Button-1>": self.push_logic,
            "<ButtonRelease-1>": self.unpush_logic
        }

    def handler(self, canvas: tk.Canvas, figure: int, label: int, event: str) -> None:
        """
        Вызывает обработчик события из словаря func_dict.

        Args:
            canvas (tk.Canvas): Канвас, на котором находится кнопка.
            figure (int): ID фигуры (изображения) на канвасе.
            label (int): ID текста (метки) на канвасе.
            event (str): Строка, обозначающая событие (например, "<Enter>").
        """
        self.func_dict[event](canvas, figure, label)

    def changer(self, canvas: tk.Canvas, figure: int, label: int, new_status: Any) -> None:
        """
        Заглушка для смены состояния. Должна быть переопределена в подклассах.

        Args:
            canvas (tk.Canvas): Канвас, на котором находится элемент.
            figure (int): ID фигуры.
            label (int): ID текста.
            new_status (Any): Новое состояние (например, изображение или цвет).
        """
        pass

    def on_hover(self, canvas: tk.Canvas, figure: int, label: int) -> None:
        """
        Обработчик наведения мыши. Изменяет состояние кнопки на активное, если кнопка не нажата.
        """
        self.is_active = True
        if not self.is_pushed:
            self.changer(canvas, figure, label, self.active_button_status)

    def push_logic(self, canvas: tk.Canvas, figure: int, label: int) -> None:
        """
        Обработчик начала нажатия на кнопку.
        Изменяет состояние кнопки на нажатое и смещает её согласно offset.
        """
        if not self.is_pushed:
            self.is_pushed = True
            self.changer(canvas, figure, label, self.push_button_status)
            canvas.move(figure, *self.offset)
            canvas.move(label, *self.offset)

    def unpush_logic(self, canvas: tk.Canvas, figure: int, label: int) -> None:
        """
        Обработчик отпускания кнопки.
        В зависимости от состояния, возвращает кнопку в активное или исходное состояние,
        а также сбрасывает смещение.
        """
        if self.is_active:
            self.changer(canvas, figure, label, self.active_button_status)
        else:
            self.changer(canvas, figure, label, self.base_status)
        x, y = self.offset
        canvas.move(figure, -x, -y)
        canvas.move(label, -x, -y)
        self.is_pushed = False

    def on_leave(self, canvas: tk.Canvas, figure: int, label: int) -> None:
        """
        Обработчик ухода курсора с кнопки.
        Возвращает кнопку в исходное состояние, если она не нажата.
        """
        self.is_active = False
        if not self.is_pushed:
            self.changer(canvas, figure, label, self.base_status)


class ButtonVisual_PIL(ButtonVisual):
    """
    Класс визуального отображения кнопки с использованием PIL-изображений.
    Переопределяет метод changer для смены изображения.
    """

    def changer(self, canvas: tk.Canvas, figure: int, label: int, fill: Any) -> None:
        """
        Меняет изображение элемента на новое.

        Args:
            canvas (tk.Canvas): Канвас с элементом.
            figure (int): ID фигуры.
            label (int): ID текста (не изменяется).
            fill (Any): Новое изображение (PhotoImage).
        """
        canvas.itemconfig(figure, image=fill)


class ButtonVisual_Canvas(ButtonVisual):
    """
    Класс визуального отображения кнопки для стандартного Canvas,
    где меняется цвет заливки.
    """

    def changer(self, canvas: tk.Canvas, figure: int, label: int, fill: Any) -> None:
        """
        Меняет цвет заливки фигуры.

        Args:
            canvas (tk.Canvas): Канвас с элементом.
            figure (int): ID фигуры.
            label (int): ID текста (не изменяется).
            fill (Any): Новый цвет в формате строки.
        """
        canvas.itemconfig(figure, fill=fill)


class Animated_mixin(ButtonVisual):
    """
    Миксин для добавления анимации к кнопке.
    При определённых действиях запускается последовательность кадров из collage.
    """

    def __init__(
            self,
            collage: List[Any],
            time: float,
            base_status: Any,
            active_button_status: Optional[Any] = None,
            push_button_status: Optional[Any] = None,
            offset: Tuple[int, int] = (0, 0)
    ) -> None:
        """
        Инициализация анимированного визуального представления кнопки.

        Args:
            collage (List[Any]): Список кадров (например, PhotoImage) для анимации.
            time (float): Время анимации (используется для расчёта количества кадров).
            base_status (Any): Изображение в исходном состоянии.
            active_button_status (Optional[Any]): Изображение при наведении.
            push_button_status (Optional[Any]): Изображение при нажатии.
            offset (Tuple[int, int]): Смещение при нажатии.
        """
        super().__init__(base_status, active_button_status, push_button_status, offset)
        self.collage = collage
        frames = time * 60  # Количество кадров основывается на времени и FPS (60)
        self.max_frames = int(frames - (frames % len(collage)))
        self.current_frame = 0
        self.total_quantity = 0

    def push_logic(self, canvas: tk.Canvas, figure: int, label: int) -> None:
        """
        При нажатии фиксируем состояние нажатия без изменения изображения.
        """
        if not self.is_pushed:
            self.is_pushed = True

    def unpush_logic(self, canvas: tk.Canvas, figure: int, label: int) -> None:
        """
        При отпускании запускает полную анимацию, если кнопка доступна.
        """
        if self.is_available:
            self.is_pushed = False
            self.current_frame = 0
            self.is_available = False
            self.animate_logic(canvas, figure, label)

    def on_leave(self, canvas: tk.Canvas, figure: int, label: int) -> None:
        """
        При уходе курсора запускает анимацию в обратном направлении, если кнопка доступна.
        """
        if self.is_available:
            self.is_active = False
            self.partial_animate(canvas, figure, label, forward=False)

    def on_hover(self, canvas: tk.Canvas, figure: int, label: int) -> None:
        """
        При наведении запускает анимацию в прямом направлении, если кнопка доступна.
        """
        if self.is_available:
            self.is_active = True
            self.partial_animate(canvas, figure, label)

    def partial_animate(
            self, canvas: tk.Canvas, figure: int, label: int, forward: bool = True, delay: int = 15
    ) -> None:
        """
        Запускает частичную анимацию (при наведении или уходе курсора).
        Анимация продолжается до достижения конца (или начала) списка кадров.

        Args:
            canvas (tk.Canvas): Канвас с элементом.
            figure (int): ID фигуры.
            label (int): ID текста.
            forward (bool): Направление анимации. True – вперёд, False – назад.
            delay (int): Задержка между кадрами в миллисекундах.
        """
        if not self.is_pushed:
            if forward:
                if self.current_frame >= len(self.collage) or not self.is_active:
                    return
                self.changer(canvas, figure, label, self.collage[self.current_frame])
                self.current_frame += 1
            else:
                if self.current_frame <= 0:
                    return
                self.current_frame -= 1
                self.changer(canvas, figure, label, self.collage[self.current_frame])
            canvas.after(delay, lambda: self.partial_animate(canvas, figure, label, forward, delay))

    def animate_logic(self, canvas: tk.Canvas, figure: int, label: int) -> None:
        """
        Запускает полную анимацию кнопки до достижения максимального количества кадров.
        По завершении происходит задержка и сброс анимации.

        Args:
            canvas (tk.Canvas): Канвас с элементом.
            figure (int): ID фигуры.
            label (int): ID текста.
        """
        if self.current_frame >= len(self.collage):
            self.current_frame = 0
        if self.total_quantity == self.max_frames:
            canvas.after(100, self.reset)
            return
        self.changer(canvas, figure, label, self.collage[self.current_frame])
        self.current_frame += 1
        self.total_quantity += 1
        delay = int(1 + (35 - 1) * (self.total_quantity / self.max_frames))
        canvas.after(delay, lambda: self.animate_logic(canvas, figure, label))

    def reset(self) -> None:
        """
        Сбрасывает анимацию, обнуляет счетчики и переворачивает порядок кадров,
        делая кнопку доступной для следующей анимации.
        """
        self.current_frame = 0
        self.total_quantity = 0
        self.collage.reverse()
        self.is_available = True


class Animated_PIL_Button_Visual(Animated_mixin, ButtonVisual_PIL):
    """
    Комбинированный класс анимированной кнопки с использованием PIL-изображений.
    Наследует логику анимации и смены изображений.
    """


class ButtonLogic:
    """
    Базовый класс для описания логики работы кнопок.
    """

    def control_func(self, *args: Any, **kwargs: Any) -> None:
        """
        Заглушка для основной логики обработки событий кнопки.
        """
        pass


class SettingsChanger(ButtonLogic):
    """
    Класс для изменения настроек приложения.
    Поддерживает изменение времени ожидания, размера кеша, разрешения окна и сохранение настроек.
    """
    waiting_time_values: Dict[int, int] = {0: 10, 1: 20, 2: 30, 3: 60, 4: 120, 5: 600}
    cache_size_values: Dict[int, int] = {0: 1, 1: 5, 2: 10, 3: 50, 4: 100}
    current_waiting_time: int = constants.get('Waiting_time')
    current_cache_size: int = constants.get('Maximum_cache_size')
    current_window_size: Tuple[int, int] = (constants.get('Width_main'), constants.get('Height_main'))

    def __init__(self, selected_func: str) -> None:
        """
        Инициализирует SettingsChanger, выбирая необходимую функцию по ключу.

        Args:
            selected_func (str): Ключ, определяющий, какая функция должна быть вызвана.
                                 Возможные значения: "Waiting_time", "Cache", "Save".
        """
        funcs: Dict[str, Callable[[Any], None]] = {
            "Waiting_time": self.waiting_time,
            "Cache": self.cache,
            "Save": self.save
        }
        self.selected_func = funcs[selected_func]

    def control_func(self, key: Union[int, bool] = False) -> None:
        """
        Вызывает выбранную функцию изменения настройки.

        Args:
            key (Union[int, bool]): Значение для изменения настройки или False, если изменение не требуется.
        """
        self.selected_func(key)

    def waiting_time(self, key: Union[int, bool]) -> None:
        """
        Изменяет время ожидания функции, если передан корректный ключ.

        Args:
            key (Union[int, bool]): Ключ для выбора времени ожидания.
        """
        if key is not False:
            SettingsChanger.current_waiting_time = self.waiting_time_values[key]

    def cache(self, key: Union[int, bool]) -> None:
        """
        Изменяет размер кеша, если передан корректный ключ.

        Args:
            key (Union[int, bool]): Ключ для выбора размера кеша.
        """
        if key is not False:
            SettingsChanger.current_cache_size = self.cache_size_values[key]

    @staticmethod
    def get_key_from_value(dicti: Dict[int, int], need_value: int) -> int:
        """
        Возвращает ключ, соответствующий заданному значению в словаре.

        Args:
            dicti (Dict[int, int]): Словарь значений.
            need_value (int): Искомое значение.

        Returns:
            int: Найденный ключ или 0, если значение не найдено.
        """
        for key, value in dicti.items():
            if need_value == value:
                return key
        return 0

    @staticmethod
    def change_resolution(width: int, height: int) -> None:
        """
        Изменяет разрешение окна приложения.

        Args:
            width (int): Новая ширина.
            height (int): Новая высота.
        """
        SettingsChanger.current_window_size = (width, height)

    def save(self, *args: Any) -> None:
        """
        Сохраняет настройки и выводит сообщение о необходимости перезапуска приложения.
        """
        if SettingsChanger.current_window_size != (constants.get('Width_main'), constants.get('Height_main')):
            show_message("Для изменения разрешения необходимо перезапустить приложение.")
        data = {
            "Waiting_time": SettingsChanger.current_waiting_time,
            "Maximum_cache_size": SettingsChanger.current_cache_size,
            "Window_size": SettingsChanger.current_window_size
        }
        write_setting(data)
        constants.load_settings()


def show_message(text: (str, Exception), title: str = "Внимание!") -> None:
    """
    Выводит информационное окно с заданным сообщением.

    Args:
        text (str): Текст сообщения.
        title (str): Заголовок окна.
    """
    tk.messagebox.showinfo(title, text)


class Logic_Frame(ButtonLogic):
    """
    Класс для управления логикой открытия/закрытия боковой панели.
    """

    def __init__(self, side_frame: Any, selected_func: str, extra_func: Optional[Callable[[], None]] = None) -> None:
        """
        Инициализация логики для боковой панели.

        Args:
            side_frame (Any): Объект боковой панели (должен иметь метод toggle_panel).
            selected_func (str): Тип логики. Возможные значения: "Open/Close", "Close", "Open".
            extra_func (Optional[Callable[[], None]]): Дополнительная функция, вызываемая после основной логики.
        """
        self.side_frame = side_frame
        funcs: Dict[str, Callable[[], None]] = {
            "Open/Close": self.open_close_logic,
            "Close": self.close_frame_anim,
            "Open": self.open_frame_anim
        }
        self.selected_func = funcs[selected_func]
        self.extra_func = extra_func

    def control_func(self) -> None:
        """
        Вызывает выбранную логику для боковой панели и дополнительную функцию (если задана).
        """
        self.selected_func()
        if self.extra_func:
            self.extra_func()

    def open_close_logic(self) -> None:
        """
        Переключает состояние панели (открыта/закрыта).
        """
        self.side_frame.toggle_panel()

    def close_frame_anim(self) -> None:
        """
        Закрывает панель с анимацией.
        """
        self.side_frame.toggle_panel()

    def open_frame_anim(self) -> None:
        """
        Открывает панель с анимацией.
        """
        self.side_frame.toggle_panel()


class Logic_FrameAndText(Logic_Frame):
    """
    Расширяет Logic_Frame, добавляя возможность изменения текста на панели.
    """

    def __init__(
            self,
            side_frame: Any,
            selected_func: str,
            side_label: int,
            text: str,
            current_canvas: Optional[tk.Canvas] = None,
            extra_func: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Инициализация логики с дополнительной сменой текста.

        Args:
            side_frame (Any): Объект боковой панели.
            selected_func (str): Тип логики ("Open/Close", "Close", "Open").
            side_label (int): ID текстового элемента на панели.
            text (str): Текст, который должен быть установлен.
            current_canvas (Optional[tk.Canvas]): Канвас, содержащий текст. Если не задан, берется из side_frame.panel.
            extra_func (Optional[Callable[[], None]]): Дополнительная функция.
        """
        super().__init__(side_frame, selected_func, extra_func)
        self.current_canvas = current_canvas if current_canvas else self.side_frame.panel
        self.side_label = side_label
        self.text = text

    def open_close_logic(self) -> None:
        """
        Если текст на панели совпадает с ожидаемым, закрывает панель,
        иначе открывает её и меняет текст.
        """
        if self.current_canvas.itemcget(self.side_label, "text") == self.text:
            self.close_frame_anim()
        else:
            self.open_frame_anim()

    def close_frame_anim(self) -> None:
        self.side_frame.toggle_panel()

    def open_frame_anim(self) -> None:
        if self.current_canvas.itemcget(self.side_label, "text") == self.text:
            self.close_frame_anim()
        else:
            self.current_canvas.itemconfig(self.side_label, text=self.text)
            if not self.side_frame.panel_open:
                self.side_frame.toggle_panel()


class CustomLogic(ButtonLogic):
    """
    Класс для обёртки произвольной функции в виде логики кнопки.
    """

    def __init__(self, function: Callable[..., None]) -> None:
        """
        Args:
            function (Callable[..., None]): Функция, которая будет вызвана при срабатывании логики.
        """
        self.selected_func = function

    def control_func(self, *args: Any, **kwargs: Any) -> None:
        """
        Вызывает выбранную функцию с переданными аргументами.
        """
        self.selected_func(*args, **kwargs)


class BasicButton:
    """
    Класс для создания базовой кнопки на Canvas.
    Создаёт изображение и текст, а также привязывает обработчики событий.
    """

    def __init__(
            self,
            canvas: tk.Canvas,
            x: int,
            y: int,
            figure: Any,
            visual: ButtonVisual,
            button_logic: ButtonLogic,
            label: str = "",
            anchor: str = "n",
            text_color: str = "White",
            font: Tuple[str, int] = constants.get('Base_font')
    ) -> None:
        """
        Инициализация кнопки.

        Args:
            canvas (tk.Canvas): Канвас для размещения кнопки.
            x (int): X-координата центра кнопки.
            y (int): Y-координата центра кнопки.
            figure (Any): Изображение для кнопки.
            visual (ButtonVisual): Объект, отвечающий за визуальное поведение кнопки.
            button_logic (ButtonLogic): Объект, содержащий логику кнопки.
            label (str): Текст кнопки.
            anchor (str): Точка привязки.
            text_color (str): Цвет текста.
            font (Tuple[str, int]): Шрифт и размер текста.
        """
        self.canvas = canvas
        # Создаём изображение кнопки и текст на канвасе
        self.figure = self.canvas.create_image(x, y, image=figure, anchor=anchor)
        self.visual = visual
        self.button_logic = button_logic
        self.label = self.canvas.create_text(x, y, text=label, fill=text_color, font=font, anchor=anchor)

        # Привязка событий для обработки наведения, нажатия и отпускания
        for event, func in zip(
                ("<Enter>", "<Leave>", "<Button-1>", "<ButtonRelease-1>"),
                (self.on_hover, self.on_leave, self.base_push_logic, self.unpush_logic)
        ):
            self.canvas.tag_bind(self.figure, event, func)
            self.canvas.tag_bind(self.label, event, func)

    def on_hover(self, event: tk.Event) -> None:
        """
        Обработчик наведения курсора.
        """
        self.visual.handler(self.canvas, self.figure, self.label, "<Enter>")

    def base_push_logic(self, event: tk.Event) -> None:
        """
        Обработчик начала нажатия кнопки.
        """
        self.visual.handler(self.canvas, self.figure, self.label, "<Button-1>")

    def unpush_logic(self, event: tk.Event) -> None:
        """
        Обработчик отпускания кнопки.
        При этом вызывается логика кнопки, если она доступна.
        """
        if self.visual.is_available:
            self.button_logic.control_func()
        self.visual.handler(self.canvas, self.figure, self.label, "<ButtonRelease-1>")

    def on_leave(self, event: tk.Event) -> None:
        """
        Обработчик ухода курсора с кнопки.
        """
        self.visual.handler(self.canvas, self.figure, self.label, "<Leave>")


class Button_Panel(BasicButton):
    """
    Класс для создания кнопки, которая управляет боковой панелью.
    Помимо стандартного отображения, включает в себя логику создания и анимации боковой панели.
    """

    def __init__(
            self,
            canvas: tk.Canvas,
            x: int,
            y: int,
            panel_size: Tuple[int, int],
            back_color: Tuple[int, int, int],
            panel_color: Tuple[int, int, int],
            figure: Any,
            visual: ButtonVisual,
            label: str = "",
            text_color: str = "White",
            panel_figure: str = "rounded_rectangle",
            font: Tuple[str, int] = constants.get('Base_font'),
            panel_mode: str = "v"
    ) -> None:
        """
        Инициализирует кнопку для боковой панели.

        Args:
            canvas (tk.Canvas): Канвас для размещения кнопки.
            x (int): X-координата размещения.
            y (int): Y-координата размещения.
            panel_size (Tuple[int, int]): Размеры панели (ширина, высота).
            back_color (Tuple[int, int, int]): Цвет фона в формате RGB.
            panel_color (Tuple[int, int, int]): Цвет панели в формате RGB.
            figure (Any): Изображение кнопки.
            visual (ButtonVisual): Визуальное поведение кнопки.
            label (str): Текст кнопки.
            text_color (str): Цвет текста.
            panel_figure (str): Фигура для отрисовки панели (например, "rounded_rectangle").
            font (Tuple[str, int]): Шрифт для текста.
            panel_mode (str): Режим панели. Возможные значения: 'h', 'h+', 'v', 'v+'.
        """
        hex_back_color = rgb_to_hex(*back_color)

        # Инициализация вспомогательного канваса для боковой панели
        canvas_for_side_panel = self._canvas_for_side_panel_init(canvas, hex_back_color, x, y, figure, panel_size,
                                                                 panel_mode)
        # Создание боковой панели с заданным фоном и фигурой
        side_panel = self._create_side_panel(canvas_for_side_panel, hex_back_color, panel_size, panel_color,
                                             panel_figure, x, y, panel_mode, figure)
        # Создание анимированной боковой панели
        self.side_panel = self._create_animated_side_panel(side_panel, canvas_for_side_panel, panel_size, panel_mode)
        logic = Logic_Frame(self.side_panel, "Open/Close")
        super().__init__(canvas, x, y, figure, visual, logic, label)

    def _canvas_for_side_panel_init(
            self,
            canvas: tk.Canvas,
            hex_back_color: str,
            x: int,
            y: int,
            figure: Any,
            panel_size: Tuple[int, int],
            panel_mode: str
    ) -> tk.Canvas:
        """
        Инициализирует вспомогательный канвас для боковой панели в зависимости от режима.

        Args:
            canvas (tk.Canvas): Родительский канвас.
            hex_back_color (str): Фоновый цвет в HEX.
            x (int): X-координата размещения.
            y (int): Y-координата размещения.
            figure (Any): Изображение кнопки.
            panel_size (Tuple[int, int]): Размеры панели.
            panel_mode (str): Режим панели ('h', 'h+', 'v', 'v+').

        Returns:
            tk.Canvas: Созданный канвас для боковой панели.
        """
        width, height = panel_size
        if panel_mode == "h":
            y += figure.height() // 2
            x += figure.width() // 2
            width = 0
            anchor = "w"
        elif panel_mode == "h+":
            y += figure.height() // 2
            x -= figure.width() // 2
            width = 0
            anchor = "e"
        elif panel_mode == "v":
            y += figure.height()
            height = 0
            anchor = "n"
        elif panel_mode == "v+":
            height -= figure.height()
            height = 0
            anchor = "s"
        else:
            raise ValueError(f"Panel mode only can be ['h', 'h+', 'v', 'v+'], not {panel_mode}")

        canvas_for_side_panel = tk.Canvas(canvas, width=width, height=height, background=hex_back_color,
                                          highlightthickness=0)
        canvas_for_side_panel.place(x=x, y=y, anchor=anchor)
        return canvas_for_side_panel

    def _create_side_panel(
            self,
            canvas: tk.Canvas,
            hex_back_color: str,
            panel_size: Tuple[int, int],
            panel_color: Tuple[int, int, int],
            panel_figure: str,
            x: int,
            y: int,
            panel_mode: str,
            figure: Any
    ) -> tk.Canvas:
        """
        Создаёт боковую панель с заданными размерами и фоном.

        Args:
            canvas (tk.Canvas): Канвас, на котором создается панель.
            hex_back_color (str): Цвет фона в HEX.
            panel_size (Tuple[int, int]): Размеры панели.
            panel_color (Tuple[int, int, int]): Цвет панели в формате RGB.
            panel_figure (str): Фигура для отрисовки (например, "rounded_rectangle").
            x (int): X-координата размещения.
            y (int): Y-координата размещения.
            panel_mode (str): Режим панели.
            figure (Any): Изображение, используемое для отрисовки.

        Returns:
            tk.Canvas: Созданный канвас боковой панели.
        """
        side_panel = tk.Canvas(canvas, width=panel_size[0], height=panel_size[1],
                               bg=hex_back_color, highlightthickness=0)
        panel_image = Image.new("RGBA", (panel_size[0], panel_size[1]), panel_color)
        side_panel.panel_image = ImageTk.PhotoImage(
            create_figureimage(panel_figure, panel_image, radius=constants.get('Round_radius') // 2)
        )
        side_panel.create_image(0, 0, image=side_panel.panel_image, anchor="nw")
        return side_panel

    def _create_animated_side_panel(
            self,
            side_panel: tk.Canvas,
            canvas_for_side_panel: tk.Canvas,
            panel_size: Tuple[int, int],
            panel_mode: str,
    ) -> PanelButtonAnim:
        """
        Оборачивает боковую панель в объект, обеспечивающий анимацию при открытии/закрытии.

        Args:
            side_panel (tk.Canvas): Канвас боковой панели.
            canvas_for_side_panel (tk.Canvas): Вспомогательный канвас для панели.
            panel_size (Tuple[int, int]): Размеры панели.
            panel_mode (str): Режим панели.

        Returns:
            PanelButtonAnim: Объект, управляющий анимацией боковой панели.
        """
        return PanelButtonAnim(
            side_panel,
            canvas_for_side_panel,
            panel_size[0],
            panel_size[1],
            panel_mode,
            panel_size[0],
            panel_size[1]
        )


class Slider(BasicButton):
    """
    Класс для создания слайдера на Canvas.
    Слайдер состоит из заднего фона, меток (если заданы) и движущегося элемента.
    """

    def __init__(
            self,
            canvas: tk.Canvas,
            back_ground: Any,
            color: Tuple[int, int, int],
            x: int,
            y: int,
            figure: Any,
            num_slides: int,
            visual: ButtonVisual,
            button_logic: ButtonLogic,
            labels: Optional[List[str]] = None,
            anchor: str = "center",
            orientation: str = "h",
            base_value: int = 0
    ) -> None:
        """
        Инициализирует слайдер.

        Args:
            canvas (tk.Canvas): Канвас, на котором размещается слайдер.
            back_ground (Any): Изображение или объект, задающий фон слайдера.
            color (Tuple[int, int, int]): Цвет, используемый для генерации заднего фона слайдера.
            x (int): X-координата размещения.
            y (int): Y-координата размещения.
            figure (Any): Изображение для движущегося элемента слайдера.
            num_slides (int): Количество позиций слайдера.
            visual (ButtonVisual): Визуальное поведение слайдера.
            button_logic (ButtonLogic): Логика слайдера.
            labels (Optional[List[str]]): Метки для позиций слайдера.
            anchor (str): Точка привязки.
            orientation (str): Ориентация слайдера ("h" для горизонтального, "v" для вертикального).
            base_value (int): Начальное значение слайдера.
        """
        # Извлекаем размеры заднего фона слайдера
        self.width, self.height = back_ground.size
        hex_color = rgb_to_hex(*color)
        self.orientation = orientation

        # Инициализация переменных для расчёта позиций и значений слайдера
        self._init_side_variables(num_slides, labels, figure, back_ground, base_value)

        # Если заданы метки, создаём их
        self._init_labels(canvas, num_slides, labels, x, y, hex_color, anchor)

        # Инициализация канваса слайдера и привязка логики перетаскивания
        self._init_slider(canvas, color, hex_color, back_ground, anchor, x, y, figure, visual, button_logic)

        self.update_slider_position()

    def _init_slider(
            self,
            canvas: tk.Canvas,
            color: Tuple[int, int, int],
            hex_color: str,
            back_ground: Any,
            anchor: str,
            x: int,
            y: int,
            figure: Any,
            visual: ButtonVisual,
            button_logic: ButtonLogic
    ) -> None:
        """
        Инициализирует канвас для слайдера, создаёт задний фон и накладываемое изображение,
        а затем вызывает базовый конструктор BasicButton.

        Args:
            canvas (tk.Canvas): Родительский канвас.
            color (Tuple[int, int, int]): Цвет для генерации заднего фона.
            hex_color (str): HEX-значение цвета.
            back_ground (Any): Объект заднего фона.
            anchor (str): Точка привязки.
            x (int): X-координата.
            y (int): Y-координата.
            figure (Any): Изображение для слайдера.
            visual (ButtonVisual): Визуальное поведение.
            button_logic (ButtonLogic): Логика слайдера.
        """
        slider_canvas = tk.Canvas(canvas, width=self.width, height=self.height, background=hex_color,
                                  highlightthicknes=0)
        slider_canvas.back_ground, slider_canvas.overlap_figure = slider_background(color, back_ground)
        self.back_ground = slider_canvas.create_image(self.width // 2, self.height // 2,
                                                      image=slider_canvas.back_ground, anchor="center")
        slider_canvas.create_image(0, 0, image=slider_canvas.overlap_figure, anchor="nw")
        super().__init__(slider_canvas, self.width // 2, self.height // 2, figure, visual, button_logic,
                         anchor="center")
        # Размещаем канвас слайдера в указанной позиции
        self.canvas.place(x=x, y=y, anchor=anchor)
        # Привязка обработчика перетаскивания к движению мыши
        self.canvas.tag_bind(self.figure, "<B1-Motion>", self.on_drag)

    def _init_side_variables(
            self,
            num_slides: int,
            labels: Optional[List[str]],
            figure: Any,
            back_ground: Any,
            base_value: int
    ) -> None:
        """
        Инициализирует базовые переменные для расчёта позиции слайдера.

        Args:
            num_slides (int): Количество позиций слайдера.
            labels (Optional[List[str]]): Метки для позиций (если заданы).
            figure (Any): Изображение движущегося элемента.
            back_ground (Any): Объект заднего фона слайдера.
            base_value (int): Начальное значение.
        """
        if self.orientation == "h":
            self.width //= 2
            self.min_pos = figure.width() // 2
            self.max_pos = back_ground.size[0] // 2 - figure.width() // 2
        else:
            self.height //= 2
            self.min_pos = figure.height() // 2
            self.max_pos = back_ground.size[1] // 2 - figure.height() // 2

        self.value_range = num_slides - 1
        self.slider_range = self.max_pos - self.min_pos
        self.value = base_value
        self.position = self.get_position()

    def _init_labels(
            self,
            canvas: tk.Canvas,
            num_slides: int,
            labels: Optional[List[str]],
            x: int,
            y: int,
            hex_color: str,
            anchor: str
    ) -> None:
        """
        Если заданы метки, создаёт дополнительный канвас и размещает текстовые элементы.

        Args:
            canvas (tk.Canvas): Родительский канвас.
            num_slides (int): Количество позиций.
            labels (Optional[List[str]]): Список меток.
            x (int): X-координата.
            y (int): Y-координата.
            hex_color (str): Фоновый цвет для меток.
            anchor (str): Точка привязки.
        """
        save_value = self.value
        self.value = 0
        if labels:
            if len(labels) != num_slides:
                raise ValueError("The number of labels differs from the number of slider positions")
            label_canvas = tk.Canvas(canvas, width=self.width * 1.1, height=self.height * 1.1, background=hex_color,
                                     highlightthickness=0)
            if self.orientation == "h":
                label_canvas.place(x=x, y=y - self.height, anchor=anchor)
                for label in labels:
                    label_canvas.create_text(self.get_position() + self.width * 0.05, self.height, text=label,
                                             anchor="s",
                                             font=(
                                                 constants.get('Base_font')[0],
                                                 int(constants.get('Base_font')[1] / 1.5)))
                    self.value += 1
            else:
                label_canvas.place(x=x - self.width, y=y, anchor=anchor)
                for label in labels:
                    label_canvas.create_text(self.width, self.get_position() + self.height * 0.05, text=label,
                                             anchor="e",
                                             font=(
                                                 constants.get('Base_font')[0],
                                                 int(constants.get('Base_font')[1] / 1.5)))
                    self.value += 1
            self.value = save_value

    def on_drag(self, event: tk.Event) -> None:
        """
        Обработчик перетаскивания слайдера.
        Обновляет позицию слайдера в зависимости от положения курсора.

        Args:
            event (tk.Event): Событие движения мыши.
        """
        current_pos = event.x if self.orientation == "h" else event.y
        self.position = min(max(current_pos, self.min_pos), self.max_pos)

        new_value = self.get_value()
        if new_value != self.value:
            self.value = new_value
            self.position = self.get_position()
            self.update_slider_position()

    def update_slider_position(self) -> None:
        """
        Обновляет координаты движущегося элемента слайдера и его заднего фона.
        """
        if self.orientation == "h":
            self.canvas.coords(self.figure, self.position, self.canvas.coords(self.figure)[1])
            self.canvas.coords(self.back_ground, self.position, self.canvas.coords(self.back_ground)[1])
        else:
            self.canvas.coords(self.figure, self.canvas.coords(self.figure)[0], self.position)
            self.canvas.coords(self.back_ground, self.canvas.coords(self.back_ground)[0], self.position)

    def unpush_logic(self, event: tk.Event) -> None:
        """
        Обработчик отпускания слайдера.
        Вызывает логику слайдера с текущим значением и обновляет визуальное состояние.
        """
        if self.visual.is_available:
            self.button_logic.control_func(self.value)
        self.visual.handler(self.canvas, self.figure, self.label, "<ButtonRelease-1>")

    def get_value(self) -> int:
        """
        Вычисляет и возвращает текущее значение слайдера в диапазоне [0, value_range].

        Returns:
            int: Текущее значение слайдера.
        """
        return int((self.position - self.min_pos) / self.slider_range * self.value_range)

    def get_position(self) -> float:
        """
        Вычисляет позицию слайдера на канвасе, исходя из его значения.

        Returns:
            float: Позиция слайдера.
        """
        return self.min_pos + (self.value / self.value_range) * self.slider_range


def on_mouse_wheel(event: tk.Event) -> None:
    """
    Обработчик прокрутки мыши для Canvas.
    Поддерживает события для Windows/macOS (event.delta) и Linux (event.num).

    Args:
        event (tk.Event): Событие прокрутки.
    """
    widget = event.widget
    if isinstance(widget, tk.Canvas):
        if event.delta:  # Windows/macOS
            widget.yview_scroll(-1 * (event.delta // 120), "units")
        else:  # Linux
            if event.num == 4:  # Колесо вверх
                widget.yview_scroll(-1, "units")
            elif event.num == 5:  # Колесо вниз
                widget.yview_scroll(1, "units")


def copy(event: Optional[tk.Event] = None) -> None:
    """
    Копирует выделенный текст из виджета в буфер обмена.
    Если ничего не выделено, ничего не происходит.

    Args:
        event (Optional[tk.Event]): Событие, вызвавшее копирование.
    """
    widget = event.widget  # type: ignore
    try:
        widget.clipboard_clear()
        widget.clipboard_append(widget.get(tk.SEL_FIRST, tk.SEL_LAST))
    except tk.TclError:
        pass  # Ничего не выделено


def cut(event: Optional[tk.Event] = None) -> None:
    """
    Копирует выделенный текст и удаляет его из виджета.
    Если ничего не выделено, ничего не происходит.

    Args:
        event (Optional[tk.Event]): Событие, вызвавшее вырезание.
    """
    widget = event.widget  # type: ignore
    try:
        widget.clipboard_clear()
        widget.clipboard_append(widget.get(tk.SEL_FIRST, tk.SEL_LAST))
        widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
    except tk.TclError:
        pass  # Ничего не выделено


def paste(event: Optional[tk.Event] = None) -> None:
    """
    Вставляет текст из буфера обмена в виджет.
    Если буфер пуст, ничего не происходит.

    Args:
        event (Optional[tk.Event]): Событие, вызвавшее вставку.
    """
    widget = event.widget  # type: ignore
    try:
        widget.insert(tk.INSERT, widget.clipboard_get())
    except tk.TclError:
        pass  # Буфер обмена пуст
