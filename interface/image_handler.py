import os
import re
import tkinter as tk
from typing import Any, List, Optional, Tuple, Union

from PIL import Image, ImageTk, ImageDraw, ImageEnhance

from constants import constants  # Предполагается, что здесь определены такие константы, как Base_font и др.


# ------------------------------------------------------------------------------
# Функции для создания фигур и текста на Canvas
# ------------------------------------------------------------------------------

def create_figure_with_text(
        canvas: tk.Canvas,
        shape: str,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str = "",
        text_x: Optional[int] = None,
        text_y: Optional[int] = None,
        font: Tuple[str, int] = constants.get('Base_font'),
        radius: Optional[int] = None,
        **kwargs: Any
) -> Union[int, Tuple[int, int]]:
    """
    Создаёт фигуру (овальную или прямоугольную) на заданном canvas и, при необходимости,
    добавляет текст по центру фигуры.

    Args:
        canvas (tk.Canvas): Канвас для отрисовки.
        shape (str): Тип фигуры. Допустимые значения: "oval", "circle", "rectangle".
        x (int): X-координата верхнего левого угла фигуры.
        y (int): Y-координата верхнего левого угла фигуры.
        width (int): Ширина фигуры.
        height (int): Высота фигуры.
        text (str, optional): Текст, который будет помещён внутри фигуры. По умолчанию пустая строка.
        text_x (Optional[int], optional): X-координата текста. Если не задано – вычисляется автоматически.
        text_y (Optional[int], optional): Y-координата текста. Если не задано – вычисляется автоматически.
        font (Tuple[str, int], optional): Шрифт для текста. По умолчанию Base_font.
        radius (Optional[int], optional): Радиус закругления (для кругов/овалов или закруглённых прямоугольников).
        **kwargs (Any): Дополнительные аргументы для методов create_oval или create_rectangle.

    Returns:
        Union[int, Tuple[int, int]]:
            Если задан текст – возвращается кортеж (ID фигуры, ID текста);
            иначе – возвращается ID созданной фигуры.
    """
    if shape in ("oval", "circle"):
        radius = radius or 10
        # Для круга ширина и высота должны совпадать
        figure = canvas.create_oval(
            x, y, x + width, x + (width if shape == "circle" else height), **kwargs
        )
    elif shape == "rectangle":
        figure = canvas.create_rectangle(x, y, x + width, y + height, **kwargs)
    else:
        raise ValueError(f"Unknown shape: {shape}")

    # Если задан текст, создаём текстовый элемент внутри фигуры
    if text:
        label = create_text_figure(canvas, text, x, y, width, height, font, text_y, text_x)
        return figure, label

    return figure


def create_text_figure(
        canvas: tk.Canvas,
        text: str,
        x: int,
        y: int,
        width: int,
        height: int,
        font: Tuple[str, int],
        text_y: Optional[int] = None,
        text_x: Optional[int] = None
) -> int:
    """
    Создаёт текстовый элемент на canvas по центру заданной области.

    Args:
        canvas (tk.Canvas): Канвас для отрисовки текста.
        text (str): Текст для отображения.
        x (int): X-координата области.
        y (int): Y-координата области.
        width (int): Ширина области.
        height (int): Высота области.
        font (Tuple[str, int]): Шрифт и размер текста.
        text_y (Optional[int], optional): Y-координата текста. Если не задано, вычисляется как центр области.
        text_x (Optional[int], optional): X-координата текста. Если не задано, вычисляется как центр области.

    Returns:
        int: ID созданного текстового элемента.
    """
    text_x = text_x or (x + width) // 2
    text_y = text_y or (y + height) // 2
    label = canvas.create_text(text_x, text_y, text=text, font=font)
    return label


# ------------------------------------------------------------------------------
# Функции для работы с изображениями (PIL)
# ------------------------------------------------------------------------------

def create_figureimage(
        shape: str,
        original_image: Image.Image,
        radius: Optional[int] = None,
        **kwargs: Any
) -> Image.Image:
    """
    Создаёт изображение с заданной формой (округленный прямоугольник или круг) на основе оригинального изображения.

    Args:
        shape (str): Тип фигуры. Допустимые значения: "rounded_rectangle", "circle".
        original_image (Image.Image): Исходное изображение.
        radius (Optional[int], optional): Радиус закругления. Если не задан – используется значение 10.
        **kwargs (Any): Дополнительные параметры для отрисовки.

    Returns:
        Image.Image: Изображение с примененной маской.
    """
    width, height = original_image.size
    radius = radius or 10
    transparent_bg = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    if shape == "rounded_rectangle":
        draw.rounded_rectangle((0, 0, width, height), fill=255, radius=radius)
    elif shape == "circle":
        draw.ellipse((0, 0, width, height), fill=255)
    else:
        raise ValueError(f"Unknown shape for image: {shape}")
    result_image = Image.composite(original_image, transparent_bg, mask)
    return result_image


def image_overlay(
        image_1: Image.Image,
        image_2: Image.Image,
        x_offset: int = 0,
        y_offset: int = 0,
        mode: str = "ON"
) -> Image.Image:
    """
    Накладывает одно изображение (image_2) на другое (image_1) с заданным смещением.

    Args:
        image_1 (Image.Image): Фоновое изображение.
        image_2 (Image.Image): Изображение, которое накладывается.
        x_offset (int, optional): Смещение по оси X. По умолчанию 0 (с небольшим увеличением для плавности).
        y_offset (int, optional): Смещение по оси Y. По умолчанию 0.
        mode (str, optional): Режим наложения. "ON" – поверх, "UNDER" – под основным изображением.

    Returns:
        Image.Image: Результирующее изображение после наложения.
    """
    x_offset += 1  # Для более плавного наложения
    new_width = max(image_1.width, image_2.width) + x_offset
    new_height = max(image_1.height, image_2.height) + y_offset
    temporary_image = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 0))
    if mode == "ON":
        temporary_image.paste(image_1, (0, 0), image_1)
        temporary_image.paste(image_2, (x_offset, y_offset), image_2)
    elif mode == "UNDER":
        temporary_image.paste(image_2, (x_offset, y_offset), image_2)
        temporary_image.paste(image_1, (0, 0), image_1)
    else:
        raise ValueError(f"Unknown mode: {mode}")
    return temporary_image


def darken_image(image: Image.Image, factor: float = -10) -> Image.Image:
    """
    Затемняет изображение с помощью изменения яркости.

    Args:
        image (Image.Image): Исходное изображение.
        factor (float, optional): Фактор яркости. Значения меньше 1 затемняют изображение.
                                   По умолчанию -10 (обычно передают положительные значения, например, 0.6).

    Returns:
        Image.Image: Затемнённое изображение.
    """
    return ImageEnhance.Brightness(image).enhance(factor)


def create_pressed_button_image(
        base_image: Image.Image,
        contrast_factor: float = 2
) -> Image.Image:
    """
    Создаёт изображение для нажатой кнопки, усиливая текстуру изображения.

    Args:
        base_image (Image.Image): Исходное изображение кнопки.
        contrast_factor (float, optional): Коэффициент контрастности для усиления текстуры. По умолчанию 2.

    Returns:
        Image.Image: Изменённое изображение для эффекта нажатия.
    """
    textured_image = enhance_texture(base_image, contrast_factor)
    return textured_image


def enhance_texture(image: Image.Image, factor: float = 2) -> Image.Image:
    """
    Усиливает текстуру изображения посредством увеличения контрастности.

    Args:
        image (Image.Image): Исходное изображение.
        factor (float, optional): Коэффициент усиления контрастности (значение > 1 усиливает текстуру).

    Returns:
        Image.Image: Изображение с усиленной текстурой.
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def create_dynamic_button_images(
        image: Image.Image,
        x_offset: int = 0,
        y_offset: int = 5,
        mode: str = "UNDER"
) -> Tuple[ImageTk.PhotoImage, ImageTk.PhotoImage, ImageTk.PhotoImage]:
    """
    Создаёт три варианта изображения кнопки для динамической смены состояний:
    базовое изображение с 3D-эффектом, активное изображение и изображение для нажатой кнопки.

    Args:
        image (Image.Image): Исходное изображение кнопки.
        x_offset (int, optional): Смещение по оси X для создания 3D-эффекта.
        y_offset (int, optional): Смещение по оси Y для создания 3D-эффекта.
        mode (str, optional): Режим наложения ("UNDER" или "ON").

    Returns:
        Tuple[ImageTk.PhotoImage, ImageTk.PhotoImage, ImageTk.PhotoImage]:
            Кортеж из трёх изображений для различных состояний кнопки.
    """
    dark = darken_image(image)
    image_3d = image_overlay(image, dark, x_offset=x_offset, y_offset=y_offset, mode=mode)
    active_image_3d = darken_image(image_3d, 0.6)
    # Преобразуем в объекты PhotoImage для использования в tkinter
    dark, image_3d, active_image_3d = map(
        ImageTk.PhotoImage,
        (image_3d, active_image_3d, create_pressed_button_image(dark))
    )
    return dark, image_3d, active_image_3d


def create_static_button_images(
        image: Image.Image,
        factor: float
) -> Tuple[ImageTk.PhotoImage, ImageTk.PhotoImage, ImageTk.PhotoImage]:
    """
    Создаёт пару статичных изображений кнопки – базовое и затемнённое.
    Возвращаются два экземпляра затемнённого изображения для имитации активного состояния.

    Args:
        image (Image.Image): Исходное изображение.
        factor (float): Коэффициент затемнения.

    Returns:
        Tuple[ImageTk.PhotoImage, ImageTk.PhotoImage, ImageTk.PhotoImage]:
            Кортеж: (базовое изображение, затемнённое изображение, затемнённое изображение).
    """
    darker = darken_image(image, factor)
    darker, image = map(ImageTk.PhotoImage, (darker, image))
    return image, darker, darker


def collage_extraction(
        folder_path: str,
        extension: str,
        width: int,
        height: int
) -> List[ImageTk.PhotoImage]:
    """
    Загружает все изображения с заданным расширением из папки, сортирует их в естественном порядке,
    изменяет размер каждого изображения и преобразует в PhotoImage.

    Args:
        folder_path (str): Путь к папке с изображениями.
        extension (str): Расширение файлов (например, ".png").
        width (int): Новая ширина изображений.
        height (int): Новая высота изображений.

    Returns:
        List[ImageTk.PhotoImage]: Список преобразованных изображений.
    """

    def extract_number(file_name: str) -> Union[int, float]:
        match = re.search(r'\d+', file_name)  # Ищет число в имени файла
        return int(match.group()) if match else float('inf')

    files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(extension)],
        key=extract_number
    )

    return [
        ImageTk.PhotoImage(
            Image.open(os.path.join(folder_path, f)).resize((width, height))
        )
        for f in files
    ]


def slider_background(
        figure_color: Union[Tuple[int, int, int], str],
        back_ground: Image.Image
) -> List[ImageTk.PhotoImage]:
    """
    Создаёт задний фон для слайдера. На основе исходного фона создаётся наложенное изображение с овалом,
    которое затемняется с использованием маски.

    Args:
        figure_color (Union[Tuple[int, int, int], str]): Цвет фигуры (например, для заливки).
        back_ground (Image.Image): Исходное изображение фона.

    Returns:
        List[ImageTk.PhotoImage]: Список из двух изображений (оригинальный фон и обработанный фон).
    """
    width, height = back_ground.size
    width //= 2
    image = Image.new("RGBA", (width, height), figure_color)
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    center_x, center_y = image.size[0] // 2, image.size[1] // 2
    oval_width, oval_height = int(width), int(height * 0.7)
    draw.rounded_rectangle(
        (
            center_x - oval_width // 2,
            center_y - oval_height // 2,
            center_x + oval_width // 2,
            center_y + oval_height // 2
        ),
        fill=255,
        radius=50
    )
    # Инвертируем маску для корректного применения прозрачности
    mask = Image.eval(mask, lambda px: 255 - px)
    image.putalpha(mask)
    return list(map(ImageTk.PhotoImage, (back_ground, image)))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Преобразует значения RGB в Hex-код для использования в tkinter.

    Args:
        r (int): Компонента красного цвета.
        g (int): Компонента зелёного цвета.
        b (int): Компонента синего цвета.

    Returns:
        str: Строка в формате Hex (например, "#ff00aa").
    """
    return f"#{r:02x}{g:02x}{b:02x}"


def slider_image(
        first_color: Union[Tuple[int, int, int], str],
        second_color: Union[Tuple[int, int, int], str],
        width: int,
        height: int
) -> Image.Image:
    """
    Создаёт изображение для слайдера, состоящее из двух половин,
    окрашенных в разные цвета.

    Args:
        first_color (Union[Tuple[int, int, int], str]): Цвет для левой половины.
        second_color (Union[Tuple[int, int, int], str]): Цвет для правой половины.
        width (int): Общая ширина слайдера.
        height (int): Высота слайдера.

    Returns:
        Image.Image: Сформированное изображение слайдера.
    """
    main_image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    first_image = Image.new("RGBA", (width // 2, height), first_color)
    second_image = Image.new("RGBA", (width // 2, height), second_color)
    main_image.paste(first_image, (0, 0))
    main_image.paste(second_image, (width // 2, 0))
    return main_image
