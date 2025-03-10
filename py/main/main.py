import customtkinter as ctk

from WindowComponent.ModSelectionWindow import ModSelectionWindow

class MainWindow:
    def __init__(self):
        # Création de la fenêtre principale
        self.root = ctk.CTk()
        self.setup_ui()

    def setup_ui(self):

        self.app = ModSelectionWindow(self.root)

    def run(self):
        self.root.mainloop()

def main():
    main_window = MainWindow()

    main_window.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print("❌ Une erreur est survenue !")
        print(traceback.format_exc())  # Affiche le détail de l'erreur
        input("Appuie sur Entrée pour fermer...")  # Pause pour lire l'erreur


