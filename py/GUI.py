import json
import os
import re
from tkinter import Canvas

import customtkinter as ctk

from PIL import Image

from CustomWeapon.py.Entity.AllWeaponsDetails import AllWeaponsDetails
from CustomWeapon.py.Entity.Caliber import Caliber
from CustomWeapon.py.ItemDetails import ItemDetails


class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CustomWeapon App")  # Définir le titre
        self.root.geometry("800x600")  # Définir la taille de la fenêtre
        ctk.set_appearance_mode("dark")

        self.create_json_path()
        self.loaded_data = self.load_json_files()
        self.create_image_var()
        self.create_frame_row_root()
        self.create_frame_top()
        self.create_buttons_for_choice()
        self.framesBotRecherche = []
        self.framesBotCaliber = []
        self.framesButtonRecherche = []
        self.message_not_find = []

    def create_json_path(self):
        self.directory_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'output')
        self.directory_path = os.path.normpath(self.directory_path)

    def search_name(self, event=None):
        name_to_search = self.entry.get()
        if len(name_to_search) >= 2:
            self.clear_recherche_frame()
            results = self.find_name_in_loaded_data(name_to_search)
            if results:
                self.populate_buttons(results)
            else:
                label = ctk.CTkLabel(self.frame_bot_right, text="Aucun nom correspondant trouvé.")
                label.grid(row=0, column=0, sticky="nsew")
                self.message_not_find.append(label)
        else:
            self.clear_recherche_frame()

    def find_name_in_loaded_data(self, name):
        matches = []
        for data in self.loaded_data:
            name_field = data.get("locale", {}).get("Name")
            if isinstance(name_field, str) and name.lower() in name_field.lower():
                cleaned_name = (data.get("locale", {}).get("ShortName"))
                matches.append(cleaned_name)
        return matches

    def populate_buttons(self, results):
        max_items = 20
        items_per_row = 5
        total_rows = (max_items + items_per_row - 1) // items_per_row

        for i in range(total_rows):
            self.frame_bot_right.grid_rowconfigure(i, weight=1)
        for i in range(items_per_row):
            self.frame_bot_right.grid_columnconfigure(i, weight=1)

        for idx, result in enumerate(results[:max_items]):
            frame_recherche_m = ctk.CTkFrame(self.frame_bot_right)
            row, col = divmod(idx, items_per_row)
            frame_recherche_m.grid(row=row,
                                   column=col,
                                   padx=5,
                                   pady=5,
                                   sticky="nsew")
            self.framesBotRecherche.append(frame_recherche_m)

            button = ctk.CTkButton(frame_recherche_m,
                                   text=result,
                                   command=lambda r=result: self.on_click_result(r),
                                   font=("Arial", 20, "bold"),
                                   text_color="black",)
            button.pack(expand=True)
            self.framesButtonRecherche.append(button)

    def on_click_result(self, result):
        # Recherche le chemin en utilisant le nom stocké lors du chargement initial
        for data in self.loaded_data:
            if data['locale']['ShortName'] == result:
                file_path = data['file_path']  # Récupère directement le chemin stocké
                self.open_detail_window(file_path, True)
                break
        else:
            print(f"Fichier ignoré : {result}")

    def open_detail_window(self, send_value, ony_weapon):
        detail_window = ctk.CTkToplevel(self.root)
        detail_window.title("Fenêtre Détails")

        window_width = 800
        window_height = 600

        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        position_x = root_x + root_width + 10  # Ajouter un espace de 10 pixels à droite
        position_y = root_y + (root_height // 2) - (
                window_height // 2)  # Centrer verticalement par rapport à la fenêtre principale

        detail_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        detail_window.grab_set()
        detail_window.focus_force()
        self.root.attributes('-disabled', True)

        detail_window.protocol("WM_DELETE_WINDOW", lambda: self.close_detail_window(detail_window))

        label = ctk.CTkLabel(detail_window, text="Fenêtre de détails !")
        label.grid(pady=20)
        close_button = ctk.CTkButton(detail_window, text="Fermer",
                                     command=lambda: self.close_detail_window(detail_window))
        close_button.grid(pady=20)
        if ony_weapon:
            ItemDetails(detail_window, send_value, self)
        else:
            AllWeaponsDetails(detail_window, send_value, self)


    def close_detail_window(self, detail_window):
        detail_window.grab_release()
        detail_window.destroy()
        self.root.attributes('-disabled', False)


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
        self.frame_bot_left = ctk.CTkFrame(self.frames[1], bg_color='green')
        self.frame_bot_right = ctk.CTkFrame(self.frames[1], fg_color='blue')
        self.frame_bot_left.grid(row=0, column=0, sticky="nsew")
        self.frame_bot_right.grid(row=1, column=0, sticky="nsew")


    def creat_5x4_bottom(self, frame1, frame2):
        frame1.clear()
        for i in range(4):
            for y in range(5):
                button = ctk.CTkFrame(frame2)
                button.grid(row=i, column=y, padx=5, pady=5)
                frame1.append(button)


    def show_search(self):
        self.buttonWeapon.configure(state="disabled")
        self.buttonCaliber.configure(state="normal")
        self.reset_and_impl_frame(self.frames[1])
        self.create_frame_bot_for_reseach()
        self.create_grid_row_col_config(self.frame_bot_left, 1, 1)
        self.create_grid_row_col_config(self.frame_bot_right, 3, 3)
        self.creat_bind_entry_bar(self.frame_bot_left)
        self.entry.bind("<KeyRelease>", self.search_name)


    def hide_search(self):
        self.buttonCaliber.configure(state="disabled")
        self.buttonWeapon.configure(state="normal")
        self.reset_and_impl_frame(self.frames[1])
        self.create_grid_row_col_config(self.frames[1], 4, 5)
        self.creat_5x4_bottom(self.framesBotCaliber, self.frames[1])
        self.create_buttons_for_calibers()


    def creat_bind_entry_bar(self, frame):
        self.entry = ctk.CTkEntry(frame, placeholder_text="Weapons text ...", width=400)
        self.entry.pack(side="top", anchor="center")


    def reset_and_impl_frame(self, frame):
        for child in frame.winfo_children():
            child.destroy()
        for i in range(frame.grid_size()[0]):
            frame.grid_columnconfigure(i, weight=1)
        for i in range(frame.grid_size()[1]):
            frame.grid_rowconfigure(i, weight=1)


    def create_buttons_for_calibers(self):
        row = 1
        column = 0
        colors = ["dodgerblue", "peru", "mediumseagreen", "khaki"]

        if len(self.framesBotCaliber) < len(Caliber):
            print("Erreur : 'framesBotCaliber' no enought frames")
            return

        for idx, caliber in enumerate(Caliber):
            color = colors[idx % 4]
            button = ctk.CTkButton(
                self.framesBotCaliber[idx],
                text=caliber.get_label(),
                width=150,
                text_color="black",
                fg_color=color,
                font=("Arial", 15, "bold"),
                command=lambda r=caliber.get_code(): self.open_detail_window(r, False))
            button.pack(side="top", anchor="center")

            column += 1
            if column > 4:
                column = 0
                row += 1


    def create_buttons_for_choice(self):
        self.buttonWeapon = ctk.CTkButton(
            self.frame_top_left,
            image=self.weapon_image,
            text="One Specific Weapon",
            compound="bottom",
            fg_color="transparent",
            text_color="green",
            hover_color="whitesmoke",
            font=("Arial", 23, "bold"),
            command=self.show_search
        )
        self.buttonWeapon.pack(side="top", anchor="center",
                               expand=True, fill="both")

        self.buttonCaliber = ctk.CTkButton(
            self.frame_top_right,
            image=self.ammo_image,
            text="Weapons by Ballistics",
            compound="bottom",
            fg_color="transparent",
            text_color="red",
            hover_color="lightcoral",
            font=("Arial", 23, "bold"),
            command=self.hide_search
        )
        self.buttonCaliber.pack(side="top", anchor="center",
                                expand=True, fill="both")


    def create_grid_row_col_config(self, frames, number_row, number_column):
        for i in range(number_row):
            frames.grid_rowconfigure(i, weight=1)
        for j in range(number_column):
            frames.grid_columnconfigure(j, weight=1)


    def clear_recherche_frame(self):
        for frame in self.framesBotRecherche:
            frame.destroy()
        for frame in self.framesButtonRecherche:
            frame.destroy()
        for frame in self.message_not_find:
            frame.destroy()
        self.framesBotRecherche.clear()
        self.framesButtonRecherche.clear()
        self.message_not_find.clear()


    def load_json_files(self):
        data_list = []
        for filename in os.listdir(self.directory_path):
            if filename.endswith('.json') and not filename.endswith('_mod.json'):
                file_path = os.path.join(self.directory_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        if "locale" in data and "Name" in data["locale"]:
                            data['file_path'] = file_path
                            data_list.append(data)
                except Exception as e:
                    print(f"Erreur lors du chargement {filename}: {e}")
        return data_list
