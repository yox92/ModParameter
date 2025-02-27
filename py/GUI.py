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

        self.create_image_var()
        self.create_frame_row_root()
        self.create_frame_top()
        self.create_buttons_for_choice()
        self.framesBotRecherche = []
        self.framesBotCaliber = []

    def create_image_var(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Répertoire où se trouve ce script
        image_path_caliber = os.path.join(script_dir, "..", "image",
                                          "ammo.jpg")  # Générer le chemin absolu pour ammo.jpg
        image_path_weapon = os.path.join(script_dir, "..", "image",
                                         "weapon.jpg")  # Générer le chemin absolu pour ammo.jpg
        self.ammo_image = ctk.CTkImage(Image.open(image_path_caliber), size=(150, 150))
        self.weapon_image = ctk.CTkImage(Image.open(image_path_weapon), size=(150, 150))


    def create_frame_row_root(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=2)

        self.root.grid_columnconfigure(0, weight=1)
        self.frames = []

        fram1 = ctk.CTkFrame(self.root)
        fram2 = ctk.CTkFrame(self.root)
        fram1.grid(row=0, column=0, sticky="nsew")
        fram2.grid(row=1, column=0, sticky="nsew")
        self.frames.append(fram1)
        self.frames.append(fram2)

    def create_frame_top(self):
        self.frames[0].grid_columnconfigure(0, weight=1)
        self.frames[0].grid_columnconfigure(1, weight=1)
        self.frames[0].grid_rowconfigure(0, weight=1)
        self.frame_top_left = ctk.CTkFrame(self.frames[0])
        self.frame_top_right = ctk.CTkFrame(self.frames[0])
        self.frame_top_left.grid(row=0, column=0, sticky="nsew")
        self.frame_top_right.grid(row=0, column=1, sticky="nsew")

    def create_frame_bot_for_reseach(self):
        self.framesBotRecherche.clear()
        self.frames[1].grid_columnconfigure(0, weight=1)
        self.frames[1].grid_rowconfigure(0, weight=1)
        self.frames[1].grid_rowconfigure(1, weight=2)
        self.frame_bot_left = ctk.CTkFrame(self.frames[1], bg_color='red')
        self.frame_bot_right = ctk.CTkFrame(self.frames[1], bg_color='blue')
        self.frame_bot_left.grid(row=0, column=0, sticky="nsew")
        self.frame_bot_right.grid(row=1, column=0, sticky="nsew")
        self.framesBotRecherche.append(self.frame_bot_left)
        self.framesBotRecherche.append(self.frame_bot_right)

    def creat_5x4_bottom(self):
        self.framesBotCaliber.clear()
        self.create_grid_row_col_config(1, 4, 5)
        for i in range(4):
            for y in range(5):
                button = ctk.CTkFrame(self.frames[1], bg_color="red")
                button.grid(row=i, column=y, padx=5, pady=5)
                self.framesBotCaliber.append(button)

    def show_search(self):
        self.buttonWeapon.configure(state="disabled")
        self.buttonCaliber.configure(state="normal")
        self.reset_frame(self.frames[1])
        self.create_frame_bot_for_reseach()
        self.entry = ctk.CTkEntry(self.frame_bot_left, placeholder_text="Weapons text ...", width=400)
        self.entry.pack(side="top", anchor="center")
        

    def hide_search(self):
        self.buttonCaliber.configure(state="disabled")
        self.buttonWeapon.configure(state="normal")
        self.reset_frame(self.frames[1])
        self.creat_5x4_bottom()
        self.create_buttons_for_calibers()

    def reset_frame(self, frame):
        for child in frame.winfo_children():
            child.destroy()
        for i in range(frame.grid_size()[0]):
            frame.grid_columnconfigure(i, weight=0)
        for i in range(frame.grid_size()[1]):
            frame.grid_rowconfigure(i, weight=0)

    def create_buttons_for_calibers(self):
        row = 1
        column = 0
        colors = ["dodgerblue", "peru", "mediumseagreen", "khaki"]
        for idx, caliber in enumerate(Caliber):
            color = colors[idx % 4]
            # Créer un bouton pour chaque calibre
            button = ctk.CTkButton(
                self.framesBotCaliber[idx],
                text=str(caliber.value),  # Utiliser la valeur du calibre comme texte du bouton
                width=150,
                text_color="black",
                fg_color=color)
            button.pack(side="top", anchor="center")
            # Organiser les boutons en colonnes et lignes pour une meilleure disposition
            column += 1
            if column > 4:  # Passer à la ligne suivante après 6 colonnes
                column = 0
                row += 1

    def create_buttons_for_choice(self):
        self.buttonWeapon = ctk.CTkButton(
            self.frame_top_left,
            image=self.weapon_image,
            text="Specific Weapon",
            compound="bottom",
            fg_color="transparent",
            text_color="green",
            hover_color="whitesmoke",
            command=self.show_search
        )
        self.buttonWeapon.pack(side="top", anchor="center",
                               expand=True, fill="both")

        self.buttonCaliber = ctk.CTkButton(
            self.frame_top_right,
            image=self.ammo_image,
            text="Caliber Weapons",
            compound="bottom",
            fg_color="transparent",
            text_color="red",
            hover_color="lightcoral",
            command=self.hide_search
        )
        self.buttonCaliber.pack(side="top", anchor="center",
                                expand=True, fill="both")

    def create_grid_row_col_config(self, frames_number, number_row, number_column):
        for i in range(number_row):
            self.frames[frames_number].grid_rowconfigure(i, weight=1)
        for j in range(number_column):
            self.frames[frames_number].grid_columnconfigure(j, weight=1)
