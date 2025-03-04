import customtkinter as ctk

from Utils import JsonUtils, Utils
from Entity.ItemManager import ItemManager
from Entity import EnumProps


class AllWeaponsDetails:
    def __init__(self, master, caliber, main_instance):
        self.master = master
        self.main_instance = main_instance
        self.master.title(caliber + ' Weapons')
        self.caliber = caliber

        self.status_label = None
        self.apply_button = None
        self.left_main = None
        self.right_main = None

        self.all_path = []
        self.manager = ItemManager()
        self.json_caliber_path = ''
        self.load_data_save_json()
        self.list_buttons_weapons = []

        self.param_main_root()
        self.create_frame_left()
        self.create_frame_right()
        self.list_of_weapons = self.get_weapons_by_calibre()
        self.list_of_file_path_json = JsonUtils.return_list_json_path(self.list_of_weapons)
        self.list_of_file_path_json_remove = []
        self.prop_widgets = {}
        self.add_left_frame()
        self.display_details()

    def load_data_save_json(self):
        data, self.json_caliber_path = JsonUtils.find_caliber_json_config(self.caliber)
        self.manager.update_from_json(data)


    def add_left_frame(self):
        for idx, result in enumerate(self.list_of_weapons):
            self.add_title()
            self.add_weapons_list(idx, result)

    def add_title(self):
        self.left_main.grid_columnconfigure(0, weight=1)
        title_label1 = ctk.CTkLabel(self.left_main,
                                   text="Weapons Will Be Modified :",
                                   font=("Arial", 20, "bold"),
                                   text_color="tomato")
        title_label1.grid(row=0, column=0, pady=2, sticky="n")
        title_label2 = ctk.CTkLabel(self.left_main,
                                    text="Click to :",
                                    font=("Arial", 18, "bold"),
                                    text_color="tomato")
        title_label2.grid(row=1, column=0, pady=0, sticky="n")
        title_label3 = ctk.CTkLabel(self.left_main,
                                    text="REMOVE(red)",
                                    font=("Arial", 15, "bold"),
                                    text_color="red")
        title_label3.grid(row=2, column=0, pady=0, sticky="n")
        title_label4 = ctk.CTkLabel(self.left_main,
                                    text="ADD(blue)",
                                    font=("Arial", 15, "bold"),
                                    text_color="blue")
        title_label4.grid(row=3, column=0, pady=0, sticky="n")

    def add_weapons_list(self, idx, result):
        self.left_main.grid_rowconfigure(idx + 3, weight=1)
        self.left_main.grid_rowconfigure(idx + 4, weight=1)

        button = ctk.CTkButton(
            self.left_main,
            text=result,
            height=10,
            width=10,
            font=("Arial", 18, "bold"),
            text_color="black",
            fg_color="blue",
            command=lambda index=idx: self.delete_add_weapons_to_list(idx, result))
        button.grid(row=idx + 4, column=0, pady=10, sticky="n")

        self.left_main.grid_rowconfigure(len(self.list_of_weapons) + 1, weight=1)
        self.list_buttons_weapons.append(button)
        button.state = True

    def delete_add_weapons_to_list(self, idx, name_weapon):
        button = self.list_buttons_weapons[idx]
        if button.state:
            Utils.transfer_file_between_lists(name_weapon,
                                              self.all_path,
                                              self.list_of_file_path_json_remove)

            button.configure(fg_color="red", font=("Arial", 18, "underline"))
            button.state = False
        else:
            Utils.transfer_file_between_lists(name_weapon,
                                              self.list_of_file_path_json_remove,
                                              self.all_path)
            button.configure(fg_color="blue")
            button.configure(font=("Arial", 18, "bold"))
            button.state = True

        if not self.all_path:
            self.no_weapon_no_mod()


    def no_weapon_no_mod(self):
        self.apply_button.configure(fg_color="red", hover_color="red")
        self.status_label.configure(text="No Weapons Select")
        self.master.after(1500, self.master.destroy)
        self.main_instance.root.attributes('-disabled', False)

    def get_weapons_by_calibre(self):
        matching_names = []
        for data in self.main_instance.loaded_data:
            try:
                if (
                        isinstance(data, dict) and
                        "item" in data and "_props" in data["item"] and
                        "ammoCaliber" in data["item"]["_props"] and
                        self.caliber == data["item"]["_props"]["ammoCaliber"]
                ):
                    try:
                        if "locale" in data and "ShortName" in data["locale"]:
                            matching_names.append(data["locale"]["ShortName"])
                    except KeyError as e:
                        print(f"KeyError about 'locale/ShortName' : {e}")

                    try:
                        if "file_path" in data:
                            self.all_path.append(data["file_path"])
                    except KeyError as e:
                        print(f"KeyError about 'file_path' : {e}")

            except KeyError as e:
                print(f"KeyError detected for main key : {e}")
            except Exception as e:
                print(f"**An unexpected error occurred** : {e}")
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
        for row, (props, number) in enumerate(self.manager.iterate_key_and_values()):
            if props != EnumProps.AMMO_CALIBER.label:
                self.right_main.grid_rowconfigure(row, weight=1)

                label = ctk.CTkLabel(self.right_main, text=f"{EnumProps.get_code_by_label(props)}:")
                label.grid(row=row, column=0, sticky=ctk.W, padx=10)
                slider = ctk.CTkSlider(
                    self.right_main,
                    from_=-100,
                    to=+100,
                    command=lambda lambda_value, pname=props:
                    self.update_props_value(pname, lambda_value)
                )
                slider.set(number)
                slider.grid(row=row, column=1, sticky=ctk.W, padx=10)
                percent_label = ctk.CTkLabel(self.right_main, text=f"{number}%", font=("Arial", 15, "bold"))
                percent_label.grid(row=row, column=2, sticky=ctk.W, padx=10)

                self.prop_widgets[props] = (slider, percent_label)

                reset_button = ctk.CTkButton(self.right_main, text="Reset",
                                             command=lambda pname=props:
                                             self.reset_slider(pname),
                                             width=10)
                reset_button.grid(row=row, column=3, sticky=ctk.W, padx=10)
                row += 1

        self.apply_button = ctk.CTkButton(self.right_main, text="Apply",
                                          command=self.apply_changes_to_all,
                                          state="disabled",
                                          fg_color="white")
        self.apply_button.grid(row=row, column=1, sticky="nsew")
        self.status_label = ctk.CTkLabel(self.right_main, text="")
        self.status_label.grid(row=row + 1, column=1, sticky="nsew")

    def update_props_value(self, name, value):
        slider, label = self.prop_widgets[name]
        if Utils.is_value_outside_limits(name, value):
            label.configure(text_color="red")
        else:
            label.configure(text_color="white")

        label.configure(text=f"({value:+.0f}%)")
        self.manager.set_value_and_transform_like_multi(name, slider.get())
        self.reset_apply_button()

    def reset_slider(self, name):
        name: EnumProps
        slider, label = self.prop_widgets[name]
        slider.set(0)
        label.configure(text=f"{0:+.0f}%")
        label.configure(text_color="white")
        self.manager.update_from_props_json(
            name,
            0)
        self.reset_apply_button()
        self.verify_all_sliders_reset()

    def verify_all_sliders_reset(self):
        if self.manager.all_values_are_zero():
            self.apply_button.configure(state="disabled", fg_color="white")
            self.status_label.configure(text="")


    def reset_apply_button(self):
        self.apply_button.configure(fg_color="blue", hover_color="lightblue", border_color="red",
                                    state="enable")  # Remettre la couleur d'origine
        self.status_label.configure(text="Ready to apply changes")

    def apply_changes_to_all(self):
        list_path_new_json = []
        for file_path in self.all_path:
            data_json_to_update = JsonUtils.load_json(file_path)
            new_file_path = file_path.replace('.json', '_mod.json')

            for key, value in self.manager.iterate_key_values_where_key_ve_change():
                data_json_to_update = JsonUtils.update_json_in_new_file(key, value, data_json_to_update, True)
            JsonUtils.save_json_as_new_file(data_json_to_update, new_file_path)
            list_path_new_json.append(new_file_path)
            self.check_for_all_files(list_path_new_json)

    def check_for_all_files(self, list_path_new_json):
        if list_path_new_json and not JsonUtils.all_file_exist(list_path_new_json):
            self.apply_button.configure(fg_color="green", hover_color="green")
            self.status_label.configure(text="Changes applied successfully.")
            self.master.after(1500, self.master.destroy)
            self.main_instance.root.attributes('-disabled', False)
        else:
            self.status_label.configure(text="Error: One or more JSON files are missing.", fg="red")
            self.apply_button.configure(fg_color="red", hover_color="red")
            self.master.after(3000, self.master.destroy)
            self.main_instance.root.attributes('-disabled', False)
