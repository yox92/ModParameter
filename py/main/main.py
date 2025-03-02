import customtkinter as ctk

class MainWindow:
    def __init__(self):
        # Création de la fenêtre principale
        self.root = ctk.CTk()
        self.setup_ui()

    def setup_ui(self):
        from Interface import SimpleGUI
        self.app = SimpleGUI(self.root)  # Fenêtre principale

    def run(self):
        self.root.mainloop()


def main():
    main_window = MainWindow()

    main_window.run()


if __name__ == "__main__":
    main()

