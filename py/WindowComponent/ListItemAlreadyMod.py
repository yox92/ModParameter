import customtkinter as ctk
import tkinter

from Entity.Logger import Logger
from Entity.Root import Root
from Entity.Locale import Locale
from Entity.WindowType import WindowType
from Utils import WindowUtils, JsonUtils

BIG_WINDOW = "1000x600"
SMALL_WINDOW = "600x600"


class ListItemAlreadyMod:
    def __init__(self, master, root, detail_window, weapon_list, main_instance, window_type):
        self.json_path_name_button = []
        self.logger = Logger()
        self.close_button = None
        self.master = master
        self.root = root
        self.detail_window = detail_window
        self.weapon_list = weapon_list
        self.main_instance = main_instance
        self.window_type : WindowType = window_type
        self.master.title('Select')
        if window_type != WindowType.WEAPON:
            self.master.geometry(BIG_WINDOW)
        else:
            self.master.geometry(SMALL_WINDOW)
        self.master.configure(bg="#242424")
        self.window_protocol = WindowUtils.window_protocol(self.detail_window,
                                                           self.detail_window,
                                                           self.root, self.main_instance)

        self.create_json_name_button()
        self.run()

    def create_json_name_button(self):
        windowType: WindowType

        if self.window_type == WindowType.DELETE:
            for [json, windowType] in self.weapon_list:
                data = JsonUtils.load_json_Weapon_Ammo_Medic(json)
                root: Root = Root.from_data(data, windowType)
                local: Locale = root.locale

                if windowType == WindowType.AMMO:
                    self.json_path_name_button.append((json, local.name, windowType))
                if windowType == WindowType.WEAPON:
                    self.json_path_name_button.append((json, local.short_name, windowType))
                if windowType == WindowType.MEDIC:
                    self.json_path_name_button.append((json, local.short_name, windowType))

        else:
            for json in self.weapon_list:
                data = JsonUtils.load_json_Weapon_Ammo_Medic(json)
                root: Root = Root.from_data(data, self.window_type)
                local: Locale = root.locale

                if self.window_type == WindowType.AMMO:
                    self.json_path_name_button.append((json, local.name, self.window_type))
                if self.window_type == WindowType.WEAPON:
                    self.json_path_name_button.append((json, local.short_name, self.window_type))
                if self.window_type == WindowType.MEDIC:
                    self.json_path_name_button.append((json, local.short_name, self.window_type))

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
        if self.window_type == WindowType.DELETE:
            self.master.grid_rowconfigure(2, weight=1)
            title_label = ctk.CTkLabel(self.master,
                                       text="Click on Ammo/Weapon to Delete :",
                                       font=("Arial", 15, "bold"),
                                       text_color="red")
            title_label.grid(row=2, column=0, pady=0, sticky="n")

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

        self.create_frame_button()

    def create_frame_button(self):
        sorted_items = sorted(self.json_path_name_button, key=lambda x: x[1].lower())

        for i in range(3):
            self.inner_frame.grid_columnconfigure(i, weight=1)

        for idx, (json_name, name_button, windowsType) in enumerate(sorted_items):
            if self.window_type == WindowType.WEAPON:
                itm_short = name_button[:10]
            else:
                itm_short = name_button[:20]

            col = idx % 3
            button_weapon = ctk.CTkButton(
                self.inner_frame,
                text=itm_short,
                compound="top",
                fg_color="#00fdff",
                text_color="black",
                hover_color="yellow",
                font=("Arial", 15, "bold"),
                command=lambda pname=json_name: self.open_specific_window(pname)
            )

            button_weapon.grid(row=idx // 3,
                               column=col,
                               padx=5,
                               pady=5,
                               sticky="ew")

            if self.window_type != WindowType.WEAPON:
                button_weapon.configure(font=("Arial", 11, "bold"))
            if self.window_type == WindowType.DELETE:
                button_weapon.configure(command=lambda pname=json_name, short_name=itm_short:
                self.delete_specific(pname, short_name))
                if windowsType == WindowType.AMMO:
                    button_weapon.configure(fg_color="dodgerblue")
                elif windowsType == WindowType.WEAPON:
                    button_weapon.configure(fg_color="peru")
                elif windowsType == WindowType.MEDIC:
                    button_weapon.configure(fg_color="green")

        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.frame.rowconfigure(0, weight=1)

    def open_specific_window(self, pname):
        self.main_instance.open_weapon_specific_window_from_list(pname, self.window_type)
        WindowUtils.close_window(self.detail_window,
                                 self.root, self.main_instance)

    def delete_specific(self, pname, short_name):
        file_path = JsonUtils.find_json_file_with_name(pname, self.window_type)

        if not file_path:
            print(f"No mod found for: {pname}")
        else:
            JsonUtils.delete_file_if_exists(file_path)
            self.logger.log("info", f"{short_name} mod deleted")

            if not JsonUtils.file_exist(file_path):

                for idx, (json_name, _, _) in enumerate(self.json_path_name_button):
                    if json_name == pname:
                        self.json_path_name_button.pop(idx)
                        break

                for widget in self.inner_frame.winfo_children():
                    if widget.cget("text") == short_name:
                        widget.destroy()
                        break
