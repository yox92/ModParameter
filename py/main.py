import tkinter as tk
from CustomWeapon.py.GUI import SimpleGUI
from CustomWeapon.py.NameSearcher import NameSearcher

def main():
    root = tk.Tk()
    app = SimpleGUI(root)
    searcher = NameSearcher(root, app.entry, app.label)  # Utilise l'entry et le label de SimpleGUI
    root.mainloop()

if __name__ == "__main__":
    main()
