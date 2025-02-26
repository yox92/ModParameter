import tkinter as tk

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple GUI")

        # Définition de la taille de la fenêtre à la moitié de 1080p
        self.root.geometry('960x540')

        # Création d'un cadre pour contenir le champ de saisie et le centrer
        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        # Création du champ de saisie de texte
        self.entry = tk.Entry(frame, font=('Arial', 14), width=48)  # La largeur en caractères peut être ajustée
        self.entry.pack(pady=20)

        # Création d'un label qui affiche du texte
        self.label = tk.Label(root, text="Hello, World!", font=("Arial", 14))
        self.label.pack(pady=20)

        # Création d'un bouton qui quitte l'application
        self.quit_button = tk.Button(root, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=20)