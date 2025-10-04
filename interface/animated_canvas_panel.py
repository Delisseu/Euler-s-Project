from constants import constants
import dataclasses
import tkinter as tk
from typing import Any, Callable, Tuple, Union


@dataclasses.dataclass
class AnimatedCanvas_Panel:
    """
    Класс для создания анимированного панели (canvas) с возможностью плавного открытия и закрытия.

    Атрибуты:
      panel (tk.Tk): Виджет (обычно Frame или Canvas), который будет анимироваться.
      width (int): Ширина панели.
      height (int): Высота панели.
      orientation (str): Направление анимации. Допустимые значения:
                         "h"  – анимация по горизонтали (слева направо),
                         "h+" – анимация по горизонтали (справа налево),
                         "v"  – анимация по вертикали (сверху вниз),
                         "v+" – анимация по вертикали (снизу вверх).
      main_width (int): Ширина основного окна (по умолчанию берётся из константы Width_main).
      main_height (int): Высота основного окна (по умолчанию берётся из константы Height_main).
      x_y (tuple): Если задан, содержит координаты (x, y) базового положения панели.
      panel_open (bool): Флаг, показывающий, открыта ли панель. Устанавливается автоматически.
      running_panel (bool): Флаг, указывающий, выполняется ли в данный момент анимация.
    """
    panel: tk.Tk
    width: int
    height: int
    orientation: str
    main_width: int = constants.get('Width_main')
    main_height: int = constants.get('Height_main')
    x_y: Union[Tuple[int, int], bool] = False
    panel_open: bool = dataclasses.field(init=False)
    running_panel: bool = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        """
        Метод __post_init__ вызывается после инициализации dataclass.
        Здесь происходит выбор функции анимации в зависимости от ориентации, установка базовых координат (base_x, base_y)
        и конечных координат (need_x, need_y) для открытой панели.
        Если параметр x_y не задан, вычисляются стандартные позиции, иначе берутся переданные.
        В конце панель размещается в базовом (скрытом) положении.
        """
        # Словарь, сопоставляющий режим анимации с соответствующим методом
        dict_func: dict[str, Callable[[bool], None]] = {
            "h": self.animate_panel_horiz,
            "h+": self.animate_panel_horiz_reverse,
            "v": self.animate_panel_vert,
            "v+": self.animate_panel_vert_reverse
        }
        self.running_panel = False
        self.panel_open = False
        # Запрещаем автоматическое изменение размера (pack_propagate) для корректного управления положением
        self.panel.pack_propagate(False)

        # Вычисляем базовые координаты панели, если x_y не задан
        if not self.x_y:
            if self.orientation == "h":
                self.base_x = -self.width
                self.base_y = (self.main_height - self.height) // 2
            elif self.orientation == "h+":
                self.base_x = self.main_width
                self.base_y = (self.main_height - self.height) // 2
            elif self.orientation == "v":
                self.base_x = (self.main_width - self.width) // 2
                self.base_y = -self.height
            elif self.orientation == "v+":
                self.base_x = (self.main_width - self.width) // 2
                self.base_y = self.main_height
        else:
            self.base_x, self.base_y = self.x_y

        # Вычисляем координаты конечного положения панели при открытии
        if self.orientation == "h":
            self.need_x, self.need_y = self.base_x + self.width, self.base_y
        elif self.orientation == "h+":
            self.need_x, self.need_y = self.base_x - self.width, self.base_y
        elif self.orientation == "v":
            self.need_x, self.need_y = self.base_x, self.base_y + self.height
        elif self.orientation == "v+":
            self.need_x, self.need_y = self.base_x, self.base_y - self.height

        self.current_animation = dict_func[self.orientation]
        # Размещаем панель в базовом (скрытом) положении
        self.panel.place(x=self.base_x, y=self.base_y)

    def toggle_panel(self) -> None:
        """
        Переключает состояние панели (открытие или закрытие).
        Если анимация не запущена, устанавливает флаг running_panel и запускает соответствующую анимацию.
        """
        if not self.running_panel:
            self.running_panel = True
            if self.panel_open:
                self.panel_open = False
                self.current_animation(closing=True)  # Анимация закрытия
            else:
                self.panel_open = True
                self.current_animation()  # Анимация открытия

    def animate_panel_horiz(self, closing: bool = False) -> None:
        """
        Анимация панели по горизонтали (слева направо).

        Если closing=True, панель перемещается к базовому положению (скрывается);
        иначе — открывается, перемещаясь к need_x.
        Плавность обеспечивается за счёт рекурсивного вызова с задержкой.
        """
        current_x = self.panel.winfo_x()
        if closing:
            # Вычисляем дистанцию от текущего положения до базового
            distance = self.base_x - current_x
            if current_x > self.base_x:
                # step выбирается как наименьшее значение между -1 и 10% от дистанции
                step = min(-1, distance * 0.1)
                new_x = current_x + step
                self.panel.place(x=new_x, y=self.base_y)
                self.panel.after(10, self.animate_panel_horiz, closing)
            else:
                self.running_panel = False
                self.panel.place(x=self.base_x, y=self.base_y)
        else:
            distance = current_x - self.need_x
            if current_x < self.need_x:
                step = min(-1, distance * 0.1)
                new_x = current_x - step
                self.panel.place(x=new_x, y=self.base_y)
                self.panel.after(10, self.animate_panel_horiz)
            else:
                self.running_panel = False
                self.panel.place(x=self.need_x, y=self.base_y)

    def animate_panel_horiz_reverse(self, closing: bool = False) -> None:
        """
        Анимация панели по горизонтали (справа налево).

        Если closing=True, панель перемещается к базовому положению (скрывается);
        иначе — открывается, перемещаясь к need_x.
        """
        current_x = self.panel.winfo_x()
        if closing:
            distance = self.base_x - current_x
            if current_x < self.base_x:
                step = max(1, distance * 0.1)
                new_x = current_x + step
                self.panel.place(x=new_x, y=self.base_y)
                self.panel.after(10, self.animate_panel_horiz_reverse, closing)
            else:
                self.running_panel = False
                self.panel.place(x=self.base_x, y=self.base_y)
        else:
            distance = current_x - self.need_x
            if current_x > self.need_x:
                step = max(1, distance * 0.1)
                new_x = current_x - step
                self.panel.place(x=new_x, y=self.base_y)
                self.panel.after(10, self.animate_panel_horiz_reverse)
            else:
                self.running_panel = False
                self.panel.place(x=self.need_x, y=self.base_y)

    def animate_panel_vert_reverse(self, closing: bool = False) -> None:
        """
        Анимация панели по вертикали с "обратным" замедлением.

        При закрытии панель опускается к базовому положению, при открытии – поднимается к need_y.
        """
        current_y = self.panel.winfo_y()
        if closing:
            distance = self.base_y - current_y
            if current_y < self.base_y:
                step = max(1, distance * 0.15)
                new_y = current_y + step
                self.panel.place(x=self.base_x, y=new_y)
                self.panel.after(10, self.animate_panel_vert_reverse, closing)
            else:
                self.running_panel = False
                self.panel.place(x=self.base_x, y=self.base_y)
        else:
            distance = current_y - self.need_y
            if current_y > self.need_y:
                step = max(1, distance * 0.15)
                new_y = current_y - step
                self.panel.place(x=self.base_x, y=new_y)
                self.panel.after(10, self.animate_panel_vert_reverse)
            else:
                self.running_panel = False
                self.panel.place(x=self.base_x, y=self.need_y)

    def animate_panel_vert(self, closing: bool = False) -> None:
        """
        Анимация панели по вертикали (прямое направление).

        При закрытии панель перемещается к базовому положению, при открытии – к need_y.
        Помимо изменения положения, изменяется и высота панели.
        """
        current_y = self.panel.winfo_y()
        if closing:
            distance = self.base_y - current_y
            if current_y > self.base_y:
                step = min(-1, distance * 0.15)
                new_y = current_y + step
                self.panel.place(x=self.base_x, y=new_y)
                # Изменяем высоту панели для эффекта анимации
                self.panel.config(height=self.panel.winfo_height() + step)
                self.panel.after(10, self.animate_panel_vert, closing)
            else:
                self.running_panel = False
                self.panel.place(x=self.base_x, y=self.base_y)
        else:
            distance = current_y - self.need_y
            if current_y < self.need_y:
                step = min(-1, distance * 0.15)
                new_y = current_y - step
                self.panel.place(x=self.base_x, y=new_y)
                self.panel.config(height=self.panel.winfo_height() - step)
                self.panel.after(10, self.animate_panel_vert)
            else:
                self.running_panel = False
                self.panel.place(x=self.base_x, y=self.need_y)


class PanelButtonAnim(AnimatedCanvas_Panel):
    """
    Класс PanelButtonAnim расширяет AnimatedCanvas_Panel и связывает анимацию панели с
    дополнительным канвасом (main_canvas). Это позволяет, например, изменять размеры основного канваса
    во время анимации боковой панели.
    """

    def __init__(
            self,
            panel: tk.Tk,
            main_canvas: tk.Tk,
            width: int,
            height: int,
            orientation: str,
            main_width: int,
            main_height: int,
            x_y: Any = False
    ) -> None:
        super().__init__(panel, width, height, orientation, main_width, main_height)
        self.main_canvas = main_canvas

    def animate_panel_vert(self, closing: bool = False) -> None:
        """
        Переопределённая анимация вертикальной панели с обновлением высоты main_canvas.
        При закрытии высота main_canvas уменьшается до нуля, а при открытии восстанавливается до self.height.
        """
        current_y = self.panel.winfo_y()
        if closing:
            distance = self.base_y - current_y
            if current_y >= self.base_y:
                step = min(-1, distance * 0.15)
                new_y = current_y + step
                self.panel.place(x=self.base_x, y=new_y)
                self.main_canvas.config(height=self.main_canvas.winfo_height() + step)
                self.panel.after(10, self.animate_panel_vert, closing)
            else:
                self.running_panel = False
                self.main_canvas.config(height=0)
                self.panel.place(x=self.base_x, y=self.base_y)
        else:
            distance = current_y - self.need_y
            if current_y <= self.need_y:
                step = min(-1, distance * 0.15)
                new_y = current_y - step
                self.panel.place(x=self.base_x, y=new_y)
                self.main_canvas.config(height=self.main_canvas.winfo_height() - step)
                self.panel.after(10, self.animate_panel_vert)
            else:
                self.running_panel = False
                self.main_canvas.config(height=self.height)
                self.panel.place(x=self.base_x, y=self.need_y)

    def animate_panel_vert_reverse(self, closing: bool = False) -> None:
        """
        Переопределённая анимация вертикальной панели (реверс) с обновлением высоты main_canvas.
        """
        current_y = self.panel.winfo_y()
        if closing:
            distance = self.base_y - current_y
            if current_y < self.base_y:
                step = max(1, distance * 0.15)
                new_y = current_y + step
                self.panel.place(x=self.base_x, y=new_y)
                self.main_canvas.config(height=self.main_canvas.winfo_height() - step)
                self.panel.after(10, self.animate_panel_vert_reverse, closing)
            else:
                self.running_panel = False
                self.main_canvas.config(height=0)
                self.panel.place(x=self.base_x, y=self.base_y)
        else:
            distance = current_y - self.need_y
            if current_y > self.need_y:
                step = max(1, distance * 0.15)
                new_y = current_y - step
                self.panel.place(x=self.base_x, y=new_y)
                self.main_canvas.config(height=self.main_canvas.winfo_height() + step)
                self.panel.after(10, self.animate_panel_vert_reverse)
            else:
                self.running_panel = False
                self.main_canvas.config(height=self.height)
                self.panel.place(x=self.base_x, y=self.need_y)

    def animate_panel_horiz(self, closing: bool = False) -> None:
        """
        Переопределённая анимация горизонтальной панели с обновлением ширины main_canvas.
        """
        current_x = self.panel.winfo_x()
        if closing:
            distance = self.base_x - current_x
            if current_x > self.base_x:
                step = min(-1, distance * 0.1)
                new_x = current_x + step
                self.panel.place(x=new_x, y=self.base_y)
                self.main_canvas.config(width=self.main_canvas.winfo_width() + step)
                self.panel.after(10, self.animate_panel_horiz, closing)
            else:
                self.running_panel = False
                self.main_canvas.config(width=0)
                self.panel.place(x=self.base_x, y=self.base_y)
        else:
            distance = current_x - self.need_x
            if current_x < self.need_x:
                step = min(-1, distance * 0.1)
                new_x = current_x - step
                self.panel.place(x=new_x, y=self.base_y)
                self.main_canvas.config(width=self.main_canvas.winfo_width() - step)
                self.panel.after(10, self.animate_panel_horiz)
            else:
                self.running_panel = False
                self.main_canvas.config(width=self.width)
                self.panel.place(x=self.need_x, y=self.base_y)

    def animate_panel_horiz_reverse(self, closing: bool = False) -> None:
        """
        Переопределённая анимация горизонтальной панели (реверс) с обновлением ширины main_canvas.
        """
        current_x = self.panel.winfo_x()
        if closing:
            distance = self.base_x - current_x
            if current_x < self.base_x:
                step = max(1, distance * 0.1)
                new_x = current_x + step
                self.panel.place(x=new_x, y=self.base_y)
                self.main_canvas.config(width=self.main_canvas.winfo_width() - step)
                self.panel.after(10, self.animate_panel_horiz_reverse, closing)
            else:
                self.running_panel = False
                self.main_canvas.config(width=0)
                self.panel.place(x=self.base_x, y=self.base_y)
        else:
            distance = current_x - self.need_x
            if current_x > self.need_x:
                step = max(1, distance * 0.1)
                new_x = current_x - step
                self.panel.place(x=new_x, y=self.base_y)
                self.main_canvas.config(width=self.main_canvas.winfo_width() + step)
                self.panel.after(10, self.animate_panel_horiz_reverse)
            else:
                self.running_panel = False
                self.main_canvas.config(width=self.width)
                self.panel.place(x=self.need_x, y=self.base_y)
