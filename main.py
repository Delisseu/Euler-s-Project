import tkinter as tk

from constants import constants
from interface.condtitons_window import ConditionsWindow
from interface.main_menu import MainMenu
from tester import create_process


class AppInterface:
    root: tk.Tk
    main_menu: MainMenu
    active_frame: tk.Tk

    def __init__(self, root):
        self.root = root
        self.root.tk.call('tk', 'scaling', 1.5)
        self.root.geometry(
            str(constants.get('Width_main')) + "x" + str(constants.get('Height_main')))  # Устанавливаем размеры окна
        self.root.title("Euler's Project")
        self.root.option_add("*Font", constants.get('Base_font'))
        self.root.resizable(width=False, height=False)
        self.conditions_window = ConditionsWindow(self.root)
        self.main_menu = MainMenu(self.root, self.conditions_window)
        self.conditions_window.main_menu_frame = self.main_menu.main_frame
        self.root.mainloop()


if __name__ == "__main__":
    create_process()
    AppInterface(tk.Tk())
