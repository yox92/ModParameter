import customtkinter as ctk
from CustomWeapon.py.GUI import SimpleGUI
from CustomWeapon.py.NameSearcher import NameSearcher


def main():
    root = ctk.CTk()  # Utilise CTk au lieu de tk.Tk pour l'intégration complète de customtkinter
    app = SimpleGUI(root)
    # Assurez-vous que NameSearcher est également mis à jour pour utiliser customtkinter si nécessaire
    searcher = NameSearcher(root, app.entry)  # Utilise l'entry de SimpleGUI
    root.mainloop()

if __name__ == "__main__":
    main()
