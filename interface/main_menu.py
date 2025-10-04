import tkinter as tk
from functools import partial
from multiprocessing import Process
from tkinter import ttk
from typing import Any

from constants import constants
from form import input_library_with_nums
from interface.Interface_logic import (
    BasicButton,
    Logic_FrameAndText,
    Logic_Frame,
    ButtonVisual_PIL,
    Animated_PIL_Button_Visual,
    Slider,
    CustomLogic,
    Button_Panel,
    SettingsChanger,
    on_mouse_wheel,
    show_message
)
from interface.animated_canvas_panel import AnimatedCanvas_Panel
from interface.image_handler import (
    create_figureimage,
    create_dynamic_button_images,
    Image,
    ImageTk,
    create_static_button_images,
    darken_image,
    collage_extraction,
    slider_image
)
from writer import remove_cache_file, get_results


class MainMenu:
    """
    Класс MainMenu отвечает за создание и управление главным меню приложения.

    Атрибуты:
        root (tk.Tk): Корневое окно приложения.
        conditions_window (Any): Объект, отвечающий за переход к следующему экрану или условиям (имеет метод activate).
        main_frame (tk.Frame): Основной фрейм, содержащий элементы главного меню.
        main_canvas (tk.Canvas): Канвас для размещения кнопок и элементов меню.
        description_canvas (AnimatedCanvas_Panel): Панель для отображения описания выбранного пункта.
    """

    root: tk.Tk
    conditions_window: Any
    main_frame: tk.Frame
    main_canvas: tk.Canvas
    descritption_canvas: tk.Canvas  # Заметьте, что в коде используется переменная description_canvas

    def __init__(self, root: tk.Tk, conditions_window: Any) -> None:
        """
        Инициализирует главное меню и запускает его инициализацию.

        Args:
            root (tk.Tk): Корневое окно приложения.
            conditions_window (Any): Объект для перехода к следующему этапу (должен содержать метод activate).
        """
        self.root = root
        self.conditions_window = conditions_window
        self.main_menu_init()

    def main_menu_init(self) -> None:
        """
        Инициализирует компоненты главного меню:
        - Создает основной фрейм и канвас.
        - Инициализирует панель описания.
        - Настраивает скроллинг, панель настроек и кнопку для работы с кешем.
        """
        self.main_frame = tk.Frame(self.root, width=constants.get('Width_main'), height=constants.get('Height_main'))
        self.main_frame.place(x=0, y=0)
        self.main_frame.pack_propagate(False)

        self.main_canvas = tk.Canvas(self.main_frame)
        self.main_canvas.pack(side="left", fill="both", expand=True)

        # Создание "фейкового" прямоугольника для начальной заливки белым цветом
        self.main_canvas.create_rectangle(0, 0, 0, 0, fill="White", outline="White")
        self._description_canvas_init()
        self._scroll_init()
        self._setting_init()
        self._cache_button_init()

    def _create_cache_window(self) -> None:
        """
        Запускает независимое окно с таблицей кеша в отдельном процессе.
        """
        process = Process(target=create_table_window)
        process.start()

    def _clear_cache(self) -> None:
        """
        Очищает кеш, удаляя файл кеша, и выводит сообщение об успешной очистке.
        """
        remove_cache_file()
        show_message("Кеш очищен!")

    def _setting_init(self) -> None:
        """
        Инициализирует панель настроек, которая включает:
        - Слайдеры для настройки времени ожидания функции и размера кеша.
        - Панель выбора разрешения экрана.
        - Кнопки для сохранения настроек и очистки кеша.
        """

        def size_panel_logic(self, setting_panel_width: int, setting_panel_height: int) -> None:
            """
            Инициализирует панель выбора разрешения экрана.

            Создает кнопки для выбора из предопределённого списка разрешений,
            а также кнопки для сохранения настроек и очистки кеша.

            Args:
                setting_panel_width (int): Ширина панели настроек.
                setting_panel_height (int): Высота панели настроек.
            """
            list_of_sizes = [(1920, 1080), (1600, 900), (1366, 768), (1280, 720), (800, 600)]
            button_size = int(setting_panel_width * 0.6), int(setting_panel_height * 0.07)
            center_width = setting_panel_width // 2

            # Создаем изображение кнопки с закруглёнными углами для фона панели
            figure = create_figureimage("rounded_rectangle",
                                        Image.new("RGBA", button_size, constants.get('Base_button_color')),
                                        constants.get('Round_radius'))
            panel_size = button_size[0], int(len(list_of_sizes) * button_size[1])
            active_figure = darken_image(figure, 0.5)
            figure, active_figure = map(ImageTk.PhotoImage, (figure, active_figure))
            visual = ButtonVisual_PIL(figure, active_figure, active_figure)

            sizes_panel = Button_Panel(
                self.setting_canvas.panel,
                center_width,
                setting_panel_height * 0.55,
                panel_size,
                constants.get('Base_back_ground'),
                constants.get('Base_white_color'),
                figure,
                visual,
                f"{constants.get('Width_main')}x{constants.get('Height_main')}",
                text_color="White",
                panel_mode="v"
            )

            # Подготовка изображений для боковых кнопок
            side_button_img = create_figureimage("rounded_rectangle",
                                                 Image.new("RGBA", button_size, constants.get('Base_white_color')),
                                                 constants.get('Round_radius'))
            active_side_button_img = darken_image(side_button_img, 0.5)
            side_button_img, active_side_button_img = map(ImageTk.PhotoImage, (side_button_img, active_side_button_img))
            side_button_visual = ButtonVisual_PIL(side_button_img, active_side_button_img, active_side_button_img)

            y_offset = button_size[1] // 2

            for width, height in list_of_sizes:
                text = f"{width}x{height}"
                func = partial(SettingsChanger.change_resolution, width=width, height=height)
                logic = Logic_FrameAndText(
                    sizes_panel.side_panel,
                    "Open/Close",
                    sizes_panel.label,
                    text,
                    sizes_panel.canvas,
                    func
                )
                BasicButton(
                    sizes_panel.side_panel.panel,
                    button_size[0] // 2,
                    y_offset,
                    side_button_img,
                    side_button_visual,
                    logic,
                    text,
                    anchor="center",
                    text_color="Black"
                )
                y_offset += button_size[1]

            # Добавляем текст-заголовок для панели разрешения
            self.setting_canvas.panel.create_text(
                center_width,
                setting_panel_height * 0.5,
                text="Разрешение",
                font=constants.get('Base_font')
            )

            # Создаем кнопку "Сохранить" и кнопку "Очистить кеш"
            offset = (0, 5)
            save_button_img = Image.new("RGBA", (int(button_size[0] * 0.6), button_size[1]),
                                        constants.get('Base_button_color'))
            save_button_img = create_figureimage("rounded_rectangle", save_button_img,
                                                 radius=constants.get('Round_radius'))
            collage = create_dynamic_button_images(save_button_img, *offset)
            visual = ButtonVisual_PIL(*collage, offset=offset)
            logic = SettingsChanger("Save")
            font = (constants.get('Base_font')[0], int(constants.get('Base_font')[1] * 0.8))
            anchor = "center"
            BasicButton(
                self.setting_canvas.panel,
                center_width * 0.5,
                setting_panel_height * 0.8,
                collage[0],
                visual,
                logic,
                "Сохранить",
                font=font,
                anchor=anchor
            )

            clear_logic = CustomLogic(self._clear_cache)
            BasicButton(
                self.setting_canvas.panel,
                center_width * 1.5,
                setting_panel_height * 0.8,
                collage[0],
                visual,
                clear_logic,
                "Очистить кеш",
                font=font,
                anchor=anchor
            )

        def _sliders_logic(self, setting_panel_width: int, setting_panel_height: int) -> None:
            """
            Инициализирует слайдеры для настройки времени ожидания функции и размера кеша.

            Создает задний фон для слайдеров, устанавливает базовые значения и подписывает слайдеры
            соответствующими метками.

            Args:
                setting_panel_width (int): Ширина панели настроек.
                setting_panel_height (int): Высота панели настроек.
            """
            width_center = setting_panel_width // 2
            slider_width = int(setting_panel_width * 0.7)
            slider_height = int(setting_panel_height * 0.045)
            # Формируем фон слайдера с использованием специальной функции slider_image
            slider_background = slider_image(constants.get('Base_button_color'), constants.get('Base_white_color'),
                                             slider_width * 2, slider_height)
            slider_button = create_figureimage(
                "circle",
                Image.new("RGBA", (slider_height, slider_height), (150, 150, 150))
            )
            slider_button, darker_button, pushed_button = map(
                ImageTk.PhotoImage,
                (
                    slider_button,
                    darken_image(slider_button, 0.8),
                    darken_image(slider_button, 0.5)
                )
            )
            waiting_logic = SettingsChanger("Waiting_time")
            visual = ButtonVisual_PIL(slider_button, darker_button, pushed_button)
            waiting_base_value = SettingsChanger.get_key_from_value(SettingsChanger.waiting_time_values,
                                                                    constants.get('Waiting_time'))
            waiting_labels = SettingsChanger.waiting_time_values.values()
            Slider(
                self.setting_canvas.panel,
                slider_background,
                constants.get('Base_back_ground'),
                width_center,
                setting_panel_height * 0.2,
                slider_button,
                len(waiting_labels),
                visual,
                waiting_logic,
                waiting_labels,
                base_value=waiting_base_value
            )
            self.setting_canvas.panel.create_text(
                width_center,
                setting_panel_height * 0.1,
                text="Время ожидания функции",
                font=constants.get('Base_font')
            )

            cache_logic = SettingsChanger("Cache")
            cache_base_value = SettingsChanger.get_key_from_value(SettingsChanger.cache_size_values,
                                                                  constants.get('Maximum_cache_size'))
            cache_labels = SettingsChanger.cache_size_values.values()
            Slider(
                self.setting_canvas.panel,
                slider_background,
                constants.get('Base_back_ground'),
                width_center,
                setting_panel_height * 0.4,
                slider_button,
                len(cache_labels),
                visual,
                cache_logic,
                cache_labels,
                base_value=cache_base_value
            )
            self.setting_canvas.panel.create_text(
                width_center,
                setting_panel_height * 0.3,
                text="Размер кеша",
                font=constants.get('Base_font')
            )

        # Инициализация панели настроек
        size_button = int(constants.get('Height_main') / 25)
        button_place = constants.get('Height_main') / 100
        setting_panel_width = int(constants.get('Width_main') / 5)
        setting_panel_height = int(constants.get('Height_main') / 2)
        setting_panel = tk.Canvas(self.main_frame, width=setting_panel_width, height=setting_panel_height)
        self.setting_canvas = AnimatedCanvas_Panel(
            setting_panel,
            setting_panel_width,
            constants.get('Height_main') - (size_button * 2 + button_place * 4),
            # Формула для корректного отображения центрального экрана
            "h"
        )

        # Инициализация заднего фона панели настроек с закругленными углами
        back_ground_image = Image.new("RGBA", (setting_panel_width, setting_panel_height),
                                      constants.get('Base_back_ground'))
        back_ground_image = create_figureimage("rounded_rectangle", back_ground_image,
                                               radius=constants.get('Round_radius'))
        tk_image = ImageTk.PhotoImage(back_ground_image)
        setting_panel.image = tk_image
        setting_panel.create_image(setting_panel_width // 2, setting_panel_height // 2, image=tk_image)

        # Инициализация и привязка кнопки для открытия/закрытия окна настроек
        setting_button_canvas = tk.Canvas(self.main_frame, width=size_button, height=size_button)
        setting_button_canvas.place(x=button_place, y=button_place)
        collage = collage_extraction(constants.get('Path_to_setting_collage'), ".png", size_button, size_button)
        base_image = collage[0]
        figure = base_image
        visual = Animated_PIL_Button_Visual(collage, 0.54, base_image)
        logic = Logic_Frame(self.setting_canvas, "Open/Close")
        BasicButton(setting_button_canvas, 2, 2, figure, visual, logic, anchor="nw")

        # Инициализация слайдеров и панели выбора разрешения
        _sliders_logic(self, setting_panel_width, setting_panel_height)
        size_panel_logic(self, setting_panel_width, setting_panel_height)

    def _description_canvas_init(self) -> None:
        """
        Инициализирует панель описания для отображения подробного описания выбранного пункта меню.

        Создает канвас с фоновым изображением и добавляет:
        - Кнопку для сворачивания/разворачивания описания.
        - Кнопку "Продолжить" для перехода к следующему экрану.
        """
        description_canvas_width = int(constants.get('Width_main') / 1.3)
        description_canvas_height = int(constants.get('Height_main') / 7)
        center_width = int(description_canvas_width / 2)
        center_height = int(description_canvas_height / 2)

        panel = tk.Canvas(self.main_frame, width=description_canvas_width, height=description_canvas_height)
        back_ground_image = Image.new("RGBA", (description_canvas_width, description_canvas_height),
                                      constants.get('Base_back_ground'))
        back_ground_image = create_figureimage("rounded_rectangle", back_ground_image,
                                               radius=constants.get('Round_radius'))
        tk_image = ImageTk.PhotoImage(back_ground_image)
        panel.image = tk_image
        panel.create_image(center_width, center_height, image=tk_image)

        self.description_canvas = AnimatedCanvas_Panel(panel, description_canvas_width, description_canvas_height, "v+")
        self.description_canvas.label_description = panel.create_text(center_width, center_height, text="",
                                                                      font=constants.get('Base_font'))

        # Создание кнопки для сворачивания/разворачивания описания
        figure_height = int(description_canvas_height / 5.5)
        rounded_offset = constants.get('Round_radius') + 10
        original_image = Image.new("RGBA", (description_canvas_width - rounded_offset, figure_height),
                                   constants.get('Base_back_ground'))
        original_image = create_figureimage("rounded_rectangle", original_image, radius=constants.get('Round_radius'))
        collage = create_static_button_images(original_image, 0.8)
        visual = ButtonVisual_PIL(*collage)
        font_size = int(figure_height * 0.6)
        figure = collage[0]
        logic = Logic_Frame(self.description_canvas, "Close")
        BasicButton(panel, center_width, 0, figure, visual, logic, "⇓", text_color="Black",
                    font=(constants.get('Base_font')[0], font_size))

        # Кнопка "Продолжить" для активации следующего окна
        offset = (0, 5)
        continue_button_img = Image.new(
            "RGBA",
            (int(description_canvas_width * 0.12), int(description_canvas_height * 0.25)),
            constants.get('Base_button_color')
        )
        continue_button_img = create_figureimage("rounded_rectangle", continue_button_img,
                                                 radius=constants.get('Round_radius'))
        collage = create_dynamic_button_images(continue_button_img, *offset)
        visual = ButtonVisual_PIL(*collage, offset=offset)
        logic = CustomLogic(self.conditions_window.activate)
        BasicButton(
            self.description_canvas.panel,
            description_canvas_width * 0.93,
            description_canvas_height * 0.78,
            collage[0],
            visual,
            logic,
            "Продолжить",
            anchor="center"
        )

    def _scroll_init(self) -> None:
        """
        Инициализирует вертикальную прокрутку основного канваса и создает кнопки для каждого элемента
        из input_library_with_nums. При нажатии на кнопку обновляется описание и выполняется дополнительная логика.
        """
        butt_step = int(constants.get('Height_main') / 20)
        y_offset = int(constants.get('Height_main') / 75)

        lenght = int(constants.get('Width_main') / 2)
        need_x = int(constants.get('Width_main') / 2)
        height = int(constants.get('Height_main') / 31)
        offset = (0, 5)

        # Создаем вертикальную прокрутку и привязываем обработчики для событий прокрутки (учитывая особенности ОС)
        scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.main_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.main_canvas.configure(yscrollcommand=scrollbar.set)

        self.main_canvas.bind("<MouseWheel>", on_mouse_wheel)  # Windows/macOS
        self.main_canvas.bind("<Button-4>", on_mouse_wheel)  # Linux
        self.main_canvas.bind("<Button-5>", on_mouse_wheel)  # Linux

        # Подготовка изображения кнопки для элементов списка
        original_image = Image.new("RGBA", (lenght, height), constants.get('Base_button_color'))
        original_image = create_figureimage("rounded_rectangle", original_image, radius=constants.get('Round_radius'))
        collage = create_dynamic_button_images(original_image, *offset)
        visual = ButtonVisual_PIL(*collage, offset)

        # Создаем кнопку для каждого пункта меню, используя нумерацию и словарь input_library_with_nums
        for i, (key, value) in enumerate(input_library_with_nums.items(), 1):
            extra_func = partial(self._change_key, self.conditions_window, key)
            figure = collage[0]
            label = f"{i}. {key}"
            logic = Logic_FrameAndText(
                self.description_canvas,
                "Open/Close",
                self.description_canvas.label_description,
                value[-1],
                extra_func=extra_func
            )
            BasicButton(self.main_canvas, need_x, y_offset, figure, visual, logic, label)
            y_offset += butt_step

        self.main_canvas.config(scrollregion=self.main_canvas.bbox("all"))

    def _cache_button_init(self) -> None:
        """
        Инициализирует кнопку для работы с кешем.
        При нажатии открывается окно с таблицей кеша.
        """
        size = constants.get('Height_main') // 18
        button_canvas = tk.Canvas(self.main_canvas, height=size, width=size)
        button_canvas.place(x=constants.get('Width_main') - size, y=size // 1.5, anchor="center")
        button_image = Image.open(constants.get('Path_to_cache_button')).resize((size, size))
        active_button_img = darken_image(button_image, 0.8)
        button_image, active_button_img = map(ImageTk.PhotoImage, [button_image, active_button_img])
        visual = ButtonVisual_PIL(button_image, active_button_img, active_button_img)
        logic = CustomLogic(self._create_cache_window)
        BasicButton(button_canvas, 0, 0, button_image, visual, logic, anchor="nw")

    def _change_key(self, atribut: Any, key: str) -> None:
        """
        Изменяет ключ атрибута для перехода к выбранному пункту меню.

        Args:
            atribut (Any): Объект, содержащий атрибут key.
            key (str): Новое значение для ключа.
        """
        atribut.key = key


def create_table_window() -> None:
    """
    Создает окно с таблицей, отображающее результаты кеша.

    Внутри определены две вспомогательные функции:
        - sort_column: сортирует данные DataFrame по указанной колонке.
        - update_treeview: обновляет содержимое Treeview на основе DataFrame.

    Если кеш пуст, выводится соответствующее сообщение.
    """

    def sort_column(tree: ttk.Treeview, df: Any, col: str, reverse: bool) -> None:
        """
        Сортирует данные DataFrame по заданной колонке и обновляет Treeview.

        Args:
            tree (ttk.Treeview): Виджет для отображения таблицы.
            df (Any): DataFrame с данными.
            col (str): Название колонки для сортировки.
            reverse (bool): Флаг, определяющий порядок сортировки (обратный или нет).
        """
        if col != 'Output':
            sorted_df = df.sort_values(by=col, ascending=not reverse)
            update_treeview(tree, sorted_df)
            # Переназначаем обработчик для сортировки при следующем клике по заголовку
            tree.heading(col, command=lambda: sort_column(tree, sorted_df, col, not reverse))

    def update_treeview(tree: ttk.Treeview, df: Any) -> None:
        """
        Обновляет содержимое Treeview на основе переданного DataFrame.

        Очищает текущие данные и заполняет таблицу новыми данными.

        Args:
            tree (ttk.Treeview): Виджет таблицы.
            df (Any): DataFrame с обновлёнными данными.
        """
        tree.delete(*tree.get_children())
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

    df = get_results()

    if df is None:
        return show_message("Кеш пуст.")

    # Создаем новое окно для отображения таблицы
    window = tk.Tk()
    window.title("Table Window")
    window.geometry(f"{constants.get('Width_main')}x{constants.get('Height_main')}")
    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True)

    # Настраиваем стиль для таблицы
    style = ttk.Style()
    rowheight = constants.get('Base_font')[1]*3
    style.configure("Treeview", font=constants.get('Base_font'), rowheight=rowheight)
    style.configure("Treeview.Heading", font=constants.get('Base_font'))

    # Создаем Treeview для отображения данных
    columns = df.columns.tolist()
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    max_lengths = df.apply(lambda col: col.astype(str).map(len).max())

    # Установка заголовков и ширины колонок
    for col, lenght in zip(columns, max_lengths):
        tree.heading(col, text=col, command=lambda c=col: sort_column(tree, df, c, False))
        tree.column(col, width=max(int(lenght * 8.61), 200))

    # Горизонтальная полоса прокрутки
    scrollbar_h = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    scrollbar_h.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=scrollbar_h.set)

    # Вертикальная полоса прокрутки
    scrollbar_v = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar_v.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar_v.set)

    tree.pack(side="left", fill=tk.BOTH, expand=True)
    update_treeview(tree, df)

    window.mainloop()
