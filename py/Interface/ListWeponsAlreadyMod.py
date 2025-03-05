import customtkinter as ctk
import tkinter

from Utils import Utils


class ListWeponsAlreadyMod:
    def __init__(self, master, root, detail_window, weapon_list, main_instance):
        self.close_button = None
        self.master = master
        self.root = root
        self.detail_window = detail_window
        self.weapon_list = weapon_list
        self.main_instance = main_instance
        self.master.geometry("280x500")
        self.master.configure(bg="#242424")

        self.run()

    def run(self):
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self.master, fg_color="#242424")
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)  # Colonne centrale plus large
        self.frame.grid_columnconfigure(2, weight=1)

        self.canvas = tkinter.Canvas(self.frame, highlightthickness=0, bg="#242424")
        self.canvas.grid(row=0, column=1, sticky="nsew")

        self.scrollbar = ctk.CTkScrollbar(self.frame, command=self.canvas.yview, fg_color="yellow")
        self.scrollbar.grid(row=0, column=2, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = ctk.CTkFrame(self.canvas, fg_color="#242424")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="n")


        for i in range(3):
            self.inner_frame.grid_columnconfigure(i, weight=1)


        def custom_sort(weapon):
            name = weapon.replace("_mod.json", "")
            return (not name[0].isdigit(), name)


        sorted_weapons = sorted(self.weapon_list, key=custom_sort)

        for idx, weapon in enumerate(sorted_weapons):
            weapon = weapon.replace("_mod.json", "")

            col = idx % 3

            label = ctk.CTkLabel(
                self.inner_frame,
                text=weapon,
                text_color="tomato",
                anchor="center",
                fg_color="#242424"
            )
            label.grid(row=idx // 3, column=col, padx=5, pady=5, sticky="ew")

        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.frame.rowconfigure(0, weight=1)