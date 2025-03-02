import customtkinter as ctk

from Utils import ItemManager, JsonUtils
from Entity import EnumProps


class AllWeaponsDetails:
    def __init__(self, master, calibre, main_instance):
        self.master = master
        self.main_instance = main_instance
        self.calibre = calibre
        self.all_path = []
        self.manager = ItemManager()
        self.master.title(calibre + ' Weapons')
        self.param_main_root()
        self.create_frame_left()
        self.create_frame_right()
        self.list_of_weapons = self.get_weapons_by_calibre()
        self.list_of_file_path_json = JsonUtils.return_list_json_path(self.list_of_weapons)
        self.prop_widgets = {}
        self.add_left_frame()
        self.display_details()

    def add_left_frame(self):
        for idx, result in enumerate(self.list_of_weapons):
            self.add_title()
            self.add_weapons_list(idx, result)

    def add_title(self):
            self.left_main.grid_columnconfigure(0, weight=1)
            title_label = ctk.CTkLabel(self.left_main,
                                       text="List of Weapons",
                                       font=("Arial", 20, "bold"),
                                       text_color="tomato")
            title_label.grid(row=0, column=0, pady=2, sticky="n")
            title_label2 = ctk.CTkLabel(self.left_main,
                                       text="That Will Be Modified",
                                       font=("Arial", 18, "bold"),
                                        text_color="tomato")
            title_label2.grid(row=1, column=0, pady=2, sticky="n")


    def add_weapons_list(self, idx, result):
        self.left_main.grid_rowconfigure(idx + 1, weight=1)
        self.left_main.grid_rowconfigure(idx + 2, weight=1)

        button = ctk.CTkButton(
            self.left_main,
            text=result,
            height=10,
            width=10,
            font=("Arial", 18, "bold"), text_color="black")
        button.grid(row=idx + 2, column=0, pady=10, sticky="n")
        self.left_main.grid_rowconfigure(len(self.list_of_weapons) + 1, weight=1)

    def get_weapons_by_calibre(self):
        matching_names = []
        for data in self.main_instance.loaded_data:
            if self.calibre == data['item']['_props']['ammoCaliber']:
                matching_names.append(data['locale']['ShortName'])
                self.all_path.append(data['file_path'])
        return matching_names

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
        row = 0
        for row, props in enumerate(EnumProps):
            props: EnumProps
            self.right_main.grid_rowconfigure(row, weight=1)

            label = ctk.CTkLabel(self.right_main, text=f"{props.code}:")
            label.grid(row=row, column=0, sticky=ctk.W, padx=10)
            slider = ctk.CTkSlider(
                self.right_main,
                from_=-100,
                to=+100,
                command=lambda lambda_value, pname=props.label:
                self.update_prop_value_int(pname, lambda_value)
            )
            slider.set(0)
            slider.grid(row=row, column=1, sticky=ctk.W, padx=10)

            percent_label = ctk.CTkLabel(self.right_main, text=f"{0:.2f}%")
            percent_label.grid(row=row, column=2, sticky=ctk.W, padx=10)

            self.prop_widgets[props.label] = (slider, percent_label)

            row += 1

        self.apply_button = ctk.CTkButton(self.right_main, text="Apply",
                                          command=self.apply_changes_to_all,
                                          state="disabled",
                                          fg_color="white")
        self.apply_button.grid(row=row, column=1, sticky="nsew")
        self.status_label = ctk.CTkLabel(self.right_main, text="" )
        self.status_label.grid(row=row+1, column=1, sticky="nsew")

    def update_prop_value_int(self, name, value):
        slider, label = self.prop_widgets[name]
        label.configure(text=f"({value:+.0f}%)")
        self.manager.set_value_and_transform_like_multi(name, slider.get())
        self.reset_apply_button()

    def reset_apply_button(self):
        self.apply_button.configure(fg_color="blue", hover_color="lightblue", border_color="red", state="enable")  # Remettre la couleur d'origine
        self.status_label.configure(text="Ready to apply changes")

    def apply_changes_to_all(self):
        for file_path in self.all_path:
                for key, value in self.manager.iterate_key_values_where_key_ve_change():
                    self.update_json_in_new_file(file_path, key, value)

    def update_json_in_new_file(self, file_path, key, new_value):
        try:
            data = JsonUtils.load_json(file_path)

            path_props_json = ["item", "_props", key]

            updated_data = JsonUtils.update_json_value(data, path_props_json, new_value)

            new_file_path = JsonUtils.save_json_as_new_file(updated_data, file_path)

            print(f"value modify and save into file : {new_file_path}")
        except Exception as e:
            print(f"Erreur : {e}")



