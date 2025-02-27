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

        # script_dir = os.path.dirname(os.path.abspath(__file__))  # Répertoire où se trouve ce script
        # image_path_caliber = os.path.join(script_dir, "..","image","ammo.jpg")  # Générer le chemin absolu pour ammo.jpg
        # image_path_weapon = os.path.join(script_dir, "..","image","weapon.jpg")  # Générer le chemin absolu pour ammo.jpg
        # ammo_image = ctk.CTkImage(Image.open(image_path_caliber), size=(100, 100))
        # weapon_image = ctk.CTkImage(Image.open(image_path_weapon), size=(100, 100))

        # Définir 3 colonnes et 3 lignes
        for i in range(3):  # Parcours des lignes
            self.root.grid_rowconfigure(i, weight=1)  # Configurer chaque ligne

        for j in range(3):  # Parcours des colonnes
            self.root.grid_columnconfigure(j, weight=1)  # Configurer chaque colonne

        # Ajouter des widgets pour tester la structure
        for i in range(3):
            for j in range(3):
                frame = ctk.CTkFrame(self.root, fg_color="blue")
                frame.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")

    #
    #     self.search_frame = ctk.CTkFrame(self.root)
    #     self.search_frame.grid(row=1, column=2)
    #     self.buttons = []
    #
    #     self.buttonWeapon = ctk.CTkButton(self.root, text="Specific Weapon", height=100, command=self.show_search)
    #     self.buttonWeapon = ctk.CTkButton(
    #         self.root,
    #         image=weapon_image,
    #         text="Specific Weapon",
    #         compound="bottom",
    #         fg_color="transparent",
    #         text_color="green",
    #         hover_color="whitesmoke",
    #         width=100,
    #         height=120,
    #         command = self.show_search
    #     )
    #     self.buttonWeapon.grid(row=0, column=1, pady=50, padx=50, sticky="ew")
    #
    #
    #     self.buttonCaliber = ctk.CTkButton(
    #         self.root,
    #         image=ammo_image,
    #         text="Caliber Weapons",
    #         compound="bottom",
    #         fg_color="transparent",
    #         text_color="red",
    #         hover_color="lightcoral",
    #         width=100,
    #         height=120,
    #         command = self.hide_search
    #     )
    #     self.buttonCaliber.grid(row=0, column=2, pady=50, sticky="ew")
    #
    #     self.create_buttons_for_calibers()
    #
    #     # Cadre pour les détails qui est initialement caché
    #     self.detail_frame = ctk.CTkFrame(self.root)
    #
    #     # Widgets pour le cadre de recherche
    #     self.entry = ctk.CTkEntry(self.search_frame, width=400,  placeholder_text="Weapons text ...")
    #     self.entry.grid(row=0, column=0)
    #
    # def show_details(self):
    #     # Cache le cadre de recherche et montre le cadre de détails
    #     self.search_frame.grid_forget()
    #     self.detail_frame.grid(row=0, column=0)
    #     self.load_item_details()
    #
    # def hide_search(self):
    #     self.search_frame.grid_forget()
    #     for button in self.buttons:
    #         button.grid()  # Réafficher chaque bouton.
    #     print("Les boutons sont affichés.")
    #
    #
    # def show_search(self):
    #     self.search_frame.grid(row=1, column=2)
    #     for button in self.buttons:
    #         button.grid_remove()  # Cacher chaque bouton.
    #     print("Les boutons sont cachés.")
    #
    #
    # def load_item_details(self):
    #     # Nettoyons et mettons quelques détails
    #     for widget in self.detail_frame.winfo_children():
    #         widget.destroy()
    #
    #     label = ctk.CTkLabel(self.detail_frame, text="Here are item details!")
    #     label.grid(row=0, column=0)
    #
    #     # Bouton de retour à la recherche
    #     back_button = ctk.CTkButton(self.detail_frame, text="Back to Search", command=self.show_search)
    #     back_button.grid(row=1, column=0)
    #
    # def create_buttons_for_calibers(self):
    #     # Parcourir les membres de Caliber
    #     row = 1
    #     column = 0
    #     for caliber in Caliber:
    #         # Créer un bouton pour chaque calibre
    #         button = ctk.CTkButton(
    #             self.root,
    #             text=str(caliber.value),  # Utiliser la valeur du calibre comme texte du bouton
    #             width=10,
    #             height=10
    #         )
    #         # Ajouter le bouton dans la grille
    #         button.grid(row=row, column=column, padx=10, pady=10, sticky="ew")
    #         self.buttons.append(button)
    #
    #         # Organiser les boutons en colonnes et lignes pour une meilleure disposition
    #         column += 1
    #         if column > 2:  # Limiter à 3 colonnes par ligne
    #             column = 0
    #             row = 1
