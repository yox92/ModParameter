import json
import os
from PIL import Image

import customtkinter as ctk
import tkinter as tk

from CustomWeapon.py.Entity.Caliber import Caliber

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CustomWeapon App")  # Définir le titre
        self.root.geometry("800x600")  # Définir la taille de la fenêtre
        ctk.set_appearance_mode("dark")

        self.create_image_var()
        self.create_json_path()
        self.create_frame_row_root()
        self.create_frame_top()
        self.create_buttons_for_choice()
        self.framesBotRecherche = []
        self.framesBotCaliber = []
        self.framesButtonRecherche = []

    def search_name(self, event=None):
        name_to_search = self.entry.get()
        if len(name_to_search) >= 3:
            results = self.find_name_in_files(name_to_search)
            if results:
                  self.populate_buttons(results)
            else:
                label = ctk.CTkLabel(self.frame_bot_right, text="Aucun nom correspondant trouvé.")
                label.pack(side="top", anchor="center")

    def find_name_in_files(self, name):
        matches = []
        for filename in os.listdir(self.directory_path):
            if filename.endswith('.json'):
                file_path = os.path.join(self.directory_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if name.lower() in data.get("_name", "").lower():
                        cleaned_name = (
                            data['_name']
                            .replace('.json', '')
                            .replace('weapon_', '')
                            .replace('izhmash_', '')
                        )
                        matches.append(cleaned_name)
        return matches

    def populate_buttons(self, results):
        for widget in self.framesBotRecherche:
            self.reset_frame(widget)
        max_items = 9
        max_columns = 3
        total_items = min(len(results), max_items)
        total_rows = (total_items // max_columns) + (
            1 if total_items % max_columns != 0 else 0)

        # Ajout dynamique des items
        for idx, result in enumerate(results[:max_items]):  # Limiter aux 9 premiers résultats
            current_frame = self.framesBotRecherche[idx]

            # Créer un sous-frame pour chaque bouton si nécessaire
            sub_frame = ctk.CTkFrame(self.frame_bot_right, fg_color="gray")
            sub_frame.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky="nsew")

            button = ctk.CTkButton(
                current_frame,  # Ajouter le bouton à la frame existante
                text=result
            )

            button.grid(row=0, column=0, sticky="nsew")  # Bouton centré dans sa sous-frame

    def on_click_result(self, file_path):
        # Action pour le clic sur un bouton
        print(f"Button clicked! File path: {file_path}")








    def create_json_path(self):
        self.directory_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'output')
        self.directory_path = os.path.normpath(self.directory_path)

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
        self.root.grid_rowconfigure(1, weight=8)

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
        self.frames[1].grid_columnconfigure(0, weight=1)
        self.frames[1].grid_rowconfigure(0, weight=1)
        self.frames[1].grid_rowconfigure(1, weight=10)
        self.frame_bot_left = ctk.CTkFrame(self.frames[1], bg_color='red')
        self.frame_bot_right = ctk.CTkFrame(self.frames[1], fg_color='blue')
        self.frame_bot_left.grid(row=0, column=0, sticky="nsew")

    def creat_5x4_bottom(self, frame1, frame2):
        frame1.clear()
        for i in range(4):
            for y in range(5):
                button = ctk.CTkFrame(frame2, bg_color="red")
                button.grid(row=i, column=y, padx=5, pady=5)
                frame1.append(button)

    def creat_3x3_bottom(self, frame1, frame2):
        frame1.clear()
        for i in range(3):
            for y in range(3):
                button = ctk.CTkFrame(frame2, fg_color="red")
                button.grid(row=i, column=y, padx=5, pady=5)
                frame1.append(button)

    def show_search(self):
        self.buttonWeapon.configure(state="disabled")
        self.buttonCaliber.configure(state="normal")
        self.reset_frame(self.frames[1])
        self.create_frame_bot_for_reseach()
        self.entry = ctk.CTkEntry(self.frame_bot_left, placeholder_text="Weapons text ...", width=400)
        self.entry.pack(side="top", anchor="center")
        self.create_grid_row_col_config(self.frame_bot_right, 3, 3)
        self.creat_3x3_bottom(self.framesBotRecherche, self.frame_bot_right)
        self.entry.bind("<KeyRelease>", self.search_name)


    def hide_search(self):
        self.buttonCaliber.configure(state="disabled")
        self.buttonWeapon.configure(state="normal")
        self.reset_frame(self.frames[1])
        self.create_grid_row_col_config(self.frames[1], 4, 5)
        self.creat_5x4_bottom(self.framesBotCaliber, self.frames[1])
        self.create_buttons_for_calibers(enumerate(Caliber))

    def reset_frame(self, frame):
        for child in frame.winfo_children():
            child.destroy()
        for i in range(frame.grid_size()[0]):
            frame.grid_columnconfigure(i, weight=0)
        for i in range(frame.grid_size()[1]):
            frame.grid_rowconfigure(i, weight=0)

    def reset_frame_scroll(self, frame):
        for child in frame.winfo_children():
            child.destroy()
        self.frame_bot_right.grid_rowconfigure(0, weight=1)
        self.frame_bot_right.grid_columnconfigure(0, weight=1)

    def create_buttons_for_calibers(self, param1):
        list = param1
        print(list)
        row = 1
        column = 0
        colors = ["dodgerblue", "peru", "mediumseagreen", "khaki"]
        for idx, caliber in list:
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

    def create_grid_row_col_config(self, frames, number_row, number_column):
        for i in range(number_row):
            frames.grid_rowconfigure(i, weight=1)
        for j in range(number_column):
            frames.grid_columnconfigure(j, weight=1)
