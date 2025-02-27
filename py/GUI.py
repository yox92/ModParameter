import os
from PIL import Image

import customtkinter as ctk

from CustomWeapon.py.Entity.Caliber import Caliber


class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CustomWeapon App")  # Définir le titre
        self.root.geometry("800x600")  # Définir la taille de la fenêtre
        ctk.set_appearance_mode("dark")

        script_dir = os.path.dirname(os.path.abspath(__file__))  # Répertoire où se trouve ce script
        image_path_caliber = os.path.join(script_dir, "..","image","ammo.jpg")  # Générer le chemin absolu pour ammo.jpg
        image_path_weapon = os.path.join(script_dir, "..","image","weapon.jpg")  # Générer le chemin absolu pour ammo.jpg
        ammo_image = ctk.CTkImage(Image.open(image_path_caliber), size=(100, 100))
        weapon_image = ctk.CTkImage(Image.open(image_path_weapon), size=(100, 100))

        # Configurer trois lignes
        for i in range(2):  # Trois lignes dans la colonne unique
            self.root.grid_rowconfigure(i, weight=1)  # Configuration de la ligne

        # Configurer une seule colonne
        self.root.grid_columnconfigure(0, weight=1)  # Une colonne unique
        self.frames = []

        for i in range(2):
            frame = ctk.CTkFrame(self.root)
            frame.grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
            self.frames.append(frame)  # Ajoute le cadre pour accès ultérieur

        # Exemple : Ajouter un `grid` dans le cadre de la première ligne (frames[0])
        self.frames[0].grid_rowconfigure(0, weight=1)
        self.frames[0].grid_columnconfigure(0, weight=1)
        self.frames[0].grid_columnconfigure(1, weight=1)

        self.buttonWeapon = ctk.CTkButton(
            self.frames[0],
            image=weapon_image,
            text="Specific Weapon",
            compound="bottom",
            fg_color="transparent",
            text_color="green",
            hover_color="whitesmoke",
            width=100,
            height=120,
            command=self.show_search
        )
        self.buttonWeapon.grid(row=1, column=0, pady=50, padx=50, sticky="ew")

        self.buttonCaliber = ctk.CTkButton(
            self.frames[0],
            image=ammo_image,
            text="Caliber Weapons",
            compound="bottom",
            fg_color="transparent",
            text_color="red",
            hover_color="lightcoral",
            width=100,
            height=120,
            command=self.create_buttons_for_calibers
        )
        self.buttonCaliber.grid(row=1, column=1, pady=50, sticky="ew")

        # On peut ajouter un `grid` différent dans la deuxième ligne (frames[1])
        self.frames[1].grid_rowconfigure(0, weight=1)
        self.frames[1].grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self.frames[1], placeholder_text="Weapons text ...", width=400)
        self.entry.grid(row=0, column=0, pady=50)

        self.buttons = []

    def hide_search(self):
        self.entry.grid_forget()

    def hide_frames2(self):
        self.frames[2].grid_remove()

    def show_search(self):
        # Masquer tous les boutons
        for button in self.buttons:
            button.grid_remove()
        self.entry = ctk.CTkEntry(self.frames[1], placeholder_text="Weapons text ...", width=400)
        self.entry.grid(row=0, column=0, pady=50)

        #
        # # Cacher tous les widgets existants dans self.frames[1]
        # for widget in self.frames[1].winfo_children():
        #     widget.grid_remove()

    def create_buttons_for_calibers(self):
        # Exemple de nettoyage ou de réinitialisation (au cas où une grille existait déjà)
        for widget in self.frames[1].winfo_children():
            if isinstance(widget, ctk.CTkFrame):  # Supprimer les cadres déjà existants
                widget.destroy()
        row = 1
        column = 0
        for caliber in Caliber:
            # Créer un bouton pour chaque calibre
            button = ctk.CTkButton(
                self.frames[1],
                text=str(caliber.value),  # Utiliser la valeur du calibre comme texte du bouton
                width=10,
                height=10)
            print(caliber.value)
            button.grid(row=row, column=column, padx=10, pady=10, sticky="ew")
            self.buttons.append(button)
            # Organiser les boutons en colonnes et lignes pour une meilleure disposition
            column += 1
            if column > 5:  # Passer à la ligne suivante après 6 colonnes
                column = 0
                row += 1



    def create_buttons_for_calibers(self):
        # Parcourir les membres de Caliber
        row = 1
        column = 0
        for caliber in Caliber:
            # Créer un bouton pour chaque calibre
            button = ctk.CTkButton(
                self.frames[1],
                text=str(caliber.value),  # Utiliser la valeur du calibre comme texte du bouton
                width=10,
                height=10
            )
            # Ajouter le bouton dans la grille
            button.grid(row=row, column=column, padx=10, pady=10, sticky="ew")
            self.buttons.append(button)

            # Organiser les boutons en colonnes et lignes pour une meilleure disposition
            column += 1
            if column > 2:  # Limiter à 3 colonnes par ligne
                column = 0
                row = 1
