import os
import re

import customtkinter as ctk

from CustomWeapon.py.Entity.ItemProps import ItemProps


class AllWeaponsDetails:
    def __init__(self, master, calibre, main_instance):
        self.master = master
        self.main_instance = main_instance
        self.calibre = re.sub(r"\.|mm", "", calibre)
        self.master.title(calibre + ' Weapons')
        self.param_main_root()
        self.create_frame_left()
        self.create_frame_right()
        self.directory_path = self.main_instance.directory_path
        self.list_of_weapons = self.get_weapons_by_calibre()
        self.list_of_file_path_json = self.get_list_of_json_name()
        self.prop_widgets = {}
        self.display_details()

        for idx, result in enumerate(self.list_of_weapons):
            self.left_main.grid_columnconfigure(0, weight=1)
            title_label = ctk.CTkLabel(self.left_main,
                                       text="List of Weapons That Will Be Modified",
                                       font=("Arial", 20, "bold"))
            title_label.grid(row=0, column=0, pady=10, sticky="n")
            self.left_main.grid_rowconfigure(idx + 1, weight=1)

            button = ctk.CTkButton(
                self.left_main,
                text=result,
                height=10,
                width=10)
            button.grid(row=idx + 1, column=0, pady=10, sticky="n")
            self.left_main.grid_rowconfigure(len(self.list_of_weapons) + 1, weight=1)

    def get_weapons_by_calibre(self):
        matching_names = []
        for data in self.main_instance.loaded_data:
            if self.calibre in data.get("_name", "").lower():
                matching_names.append(data.get("_name"))
        return matching_names

    def get_list_of_json_name(self):
        list_of_json = []
        for filename in os.listdir(self.directory_path):
            if filename.endswith('.json') and not filename.endswith('_mod.json'):
                base_name = filename.rsplit('.json', 1)[0]
                if base_name in self.list_of_weapons:
                    list_of_json.append(os.path.join(self.directory_path, filename))
        return list_of_json

    def param_main_root(self):
        self.master.grid_columnconfigure(0, weight=0)
        self.master.grid_columnconfigure(1, weight=8)
        self.master.grid_rowconfigure(0, weight=1)

    def create_frame_left(self):
        self.left_main = ctk.CTkFrame(self.master)
        self.left_main.grid(row=0, column=0, sticky="nsew")

    def create_frame_right(self):
        self.right_main = ctk.CTkFrame(self.master)
        self.right_main.grid(row=0, column=1, sticky="nsew")
        self.right_main.grid_columnconfigure(0, weight=1)
        self.right_main.grid_columnconfigure(1, weight=1)
        self.right_main.grid_columnconfigure(2, weight=1)

    def display_details(self):
        props = vars(ItemProps())
        for row, prop_name in enumerate(props):
            print(row)
            self.right_main.grid_rowconfigure(row, weight=1)

            label = ctk.CTkLabel(self.right_main, text=f"{prop_name}:")
            label.grid(row=row, column=0, sticky=ctk.W, padx=10)
            slider = ctk.CTkSlider(
                self.right_main,
                from_=-100,
                to=+100,
                command=lambda lambda_value, pname=prop_name:
                self.update_prop_value_int(pname, lambda_value)
            )
            slider.set(0)
            slider.grid(row=row, column=1, sticky=ctk.W, padx=10)

            percent_label = ctk.CTkLabel(self.right_main, text=f"{0:.2f}%")
            percent_label.grid(row=row, column=2, sticky=ctk.W, padx=10)

            self.prop_widgets[prop_name] = (slider, percent_label)

            row += 1

    def add_action_buttons(self, row):
        self.right_main.grid_rowconfigure(row, weight=1)
        self.apply_button = ctk.CTkButton(
            self.right_main,
            text="Apply",
            command=self.apply_changes,
            state="disabled",
            fg_color="white"
        )
        self.apply_button.grid(row=row, column=4)
        self.right_main.grid_rowconfigure(row + 1, weight=1)
        self.status_label = ctk.CTkLabel(self.right_main, text="")
        self.status_label.grid(row=row, column=5)

    def update_prop_value_int(self, name, value):
        slider, label = self.prop_widgets[name]
        label.configure(text=f"({value:+.0f}%)")
        self.reset_apply_button()

    def reset_apply_button(self):
        self.apply_button.configure(
                                    hover_color="lightblue",
                                    border_color="red",
                                    state="enable")
        self.status_label.configure(text="")

    def apply_changes(self):
        print("applu")

    def get_attr_names_of_item_props(self):
        return [attr for attr in vars(ItemProps()) if
                not attr.startswith('__') and not callable(getattr(ItemProps(), attr))]
