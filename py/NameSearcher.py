import os
import json
import tkinter as tk

from CustomWeapon.py.ItemDetails import ItemDetails


class NameSearcher:
    def __init__(self, master, entry_widget):

        self.directory_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'output')
        self.directory_path = os.path.normpath(self.directory_path)

        self.master = master
        self.entry_widget = entry_widget

        # Configuration de la grille pour l'organisation des widgets
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(master)
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Remplacement de `pack` par `grid` pour organiser les widgets
        self.canvas.grid(row=0, column=0, sticky="nsew")  # Canvas s'étend dans toutes les directions
        self.scrollbar.grid(row=0, column=1, sticky="ns")  # Scrollbar à la droite du canvas

        self.entry_widget.bind("<KeyRelease>", self.search_name)  # Lier l'événement de relâchement de touche

    def search_name(self, event=None):
        name_to_search = self.entry_widget.get()
        # Effacer les résultats précédents
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if len(name_to_search) >= 3:
            results = self.find_name_in_files(name_to_search)
            if results:
                for row, result in enumerate(results):
                    file_path = os.path.join(self.directory_path, result + '.json')
                    button = tk.Button(self.scrollable_frame, text=result,
                                       command=lambda r=result, fp=file_path: self.on_click_result(fp))
                    # Utilisation de `grid` au lieu de `pack`
                    button.grid(row=row, column=0, pady=5, sticky="ew")
            else:
                label = tk.Label(self.scrollable_frame, text="Aucun nom correspondant trouvé.")
                label.grid(row=0, column=0, pady=10)
        else:
            label = tk.Label(self.scrollable_frame, text="")
            label.grid(row=0, column=0, pady=10)

    def find_name_in_files(self, name):
        matches = []
        for filename in os.listdir(self.directory_path):
            if filename.endswith('.json'):
                file_path = os.path.join(self.directory_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if name.lower() in data.get("_name", "").lower():
                        matches.append(data['_name'].replace('.json', ''))
        return matches

    def on_click_result(self, file_path):
        detail_window = tk.Toplevel(self.master)
        detail_window.title("Item Details")
        ItemDetails(detail_window, file_path)