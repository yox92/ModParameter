import customtkinter as ctk
from Interface import WeaponSelection

class MainWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.setup_ui()

    def setup_ui(self):

        self.app = WeaponSelection(self.root)

    def run(self):
        self.root.mainloop()


def main():
    main_window = MainWindow()

    main_window.run()


if __name__ == "__main__":
    main()

