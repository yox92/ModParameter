import customtkinter as ctk
from CustomWeapon.py.GUI import SimpleGUI
from CustomWeapon.py.NameSearcher import NameSearcher


class MainWindow:
    def __init__(self):
        # Création de la fenêtre principale
        self.root = ctk.CTk()
        self.setup_ui()

    def setup_ui(self):
        self.app = SimpleGUI(self.root)  # Fenêtre principale

    def run(self):
        self.root.mainloop()


def main():
    main_window = MainWindow()
    main_window.run()


if __name__ == "__main__":
    main()

