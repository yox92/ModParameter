import customtkinter as ctk
import tkinter

from Entity.WindowType import WindowType
from Utils import WindowUtils

DETAIL_WINDOW = "450x500"


class ListWeponsAlreadyMod:
    def __init__(self, master, root, detail_window, weapon_list, main_instance, windowType):
        self.close_button = None
        self.master = master
        self.root = root
        self.detail_window = detail_window
        self.weapon_list = weapon_list
        self.main_instance = main_instance
        self.windowType : WindowType = windowType
        self.master.geometry(DETAIL_WINDOW)
        self.master.configure(bg="#242424")
        self.window_protocol = WindowUtils.window_protocol(self.detail_window,
                                                           self.detail_window,
                                                           self.root, self.main_instance)

        self.run()

    def run(self):
        self.master.grid_rowconfigure(0, weight=8)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.close_button = ctk.CTkButton(self.master,
                                          text="Close",
                                          command=lambda:
                                          WindowUtils.close_window(self.detail_window,
                                                                   self.root, self.main_instance))
        self.close_button.grid(row=1, column=0)

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

        def custom_sort(item):
            name = item.replace("_mod.json", "")
            return (not name[0].isdigit(), name)

        sorted_item = sorted(self.weapon_list, key=custom_sort)

        for idx, item in enumerate(sorted_item):
            itm_short = item.replace("_mod.json", "")[:10]

            col = idx % 3
            buttonWeapon = ctk.CTkButton(
                self.inner_frame,
                text=itm_short,
                compound="top",
                fg_color="#00fdff",
                text_color="black",
                hover_color="yellow",
                font=("Arial", 13, "bold"),
                height=10,
                width=10,
                command=lambda
                    pname=item:
                self.open_weapon_specific_window(pname))
            buttonWeapon.grid(row=idx // 3,
                              column=col,
                              padx=5,
                              pady=5,
                              sticky="ew")

        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.frame.rowconfigure(0, weight=1)

    def open_weapon_specific_window(self, pname):
        self.main_instance.open_weapon_specific_window_from_list(pname, self.windowType)
        WindowUtils.close_window(self.detail_window,
                                     self.root, self.main_instance)


