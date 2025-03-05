import customtkinter as ctk

from Interface.ProgressBar import ProgressBar
from Utils import JsonUtils, Utils
from Entity.ItemManager import ItemManager
from Entity import EnumProps


class CaliberWeaponsModWindow:
    def __init__(self, master, root, detail_window, caliber, main_instance):
        self.close_button = None
        self.root = root
        self.left_bot_frame_list_weapons = None
        self.right_bot_frame = None
        self.left_top_frame_title = None
        self.master = master
        self.main_instance = main_instance
        self.master.title(caliber + ' Weapons')
        self.caliber = caliber
        self.detail_window = detail_window
        self.detail_window.protocol("WM_DELETE_WINDOW", lambda: self.close_detail_window(self.detail_window))
        self.progress_bar = None
        self.status_label = None
        self.apply_button = None
        self.left_main = None
        self.right_main = None

        self.all_path = []
        self.manager = ItemManager()
        self.originale_value_from_JSON = ItemManager()
        self.json_caliber_path = ''
        self.load_data_save_json()
        self.list_buttons_weapons = []

        self.param_main_root()
        self.create_frame_left()
        self.create_frame_right()
        self.create_left_top_frame_title()
        self.create_left_bot_frame_list_weapons()
        self.list_weapons = self.get_weapons_by_calibre()
        self.list_file_path_json = JsonUtils.return_list_json_path(self.list_weapons)
        self.list_file_path_json_remove = []
        self.prop_widgets = {}
        self.add_frame_left_title_and_weapons()
        self.run()


    def param_main_root(self):
        self.master.grid_columnconfigure(0, weight=0)
        self.master.grid_columnconfigure(1, weight=8)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.close_button = ctk.CTkButton(self.master,
                                          text="Close",
                                          command=lambda:
                                          self.close_detail_window(self.master))
        self.close_button.grid(row=1,column=0)

    def create_frame_right(self):
        self.right_main = ctk.CTkFrame(self.master, fg_color="transparent")
        self.right_main.grid(row=0, column=1, sticky="nsew")
        self.right_main.grid_columnconfigure(0, weight=1) # props description
        self.right_main.grid_columnconfigure(1, weight=1) # slider
        self.right_main.grid_columnconfigure(2, weight=1) # value
        self.right_main.grid_columnconfigure(3, weight=1) # reset button

    def create_frame_left(self):
        self.left_main = ctk.CTkFrame(self.master, fg_color="transparent")
        self.left_main.grid(row=0, column=0, sticky="nsew")
        self.left_main.grid_columnconfigure(0, weight=1)
        self.left_main.grid_rowconfigure(0, weight=1) # title
        self.left_main.grid_rowconfigure(1, weight=10) # weapons list

    def create_left_top_frame_title(self):
        self.left_top_frame_title = ctk.CTkFrame(self.left_main, fg_color="transparent")
        self.left_top_frame_title.grid(row=0, column=0, sticky="nsew")
        self.left_top_frame_title.grid_rowconfigure(0, weight=1) # title
        self.left_top_frame_title.grid_rowconfigure(1, weight=1) # title
        self.left_top_frame_title.grid_rowconfigure(2, weight=1) # title
        self.left_top_frame_title.grid_rowconfigure(3, weight=1) # title
        self.left_top_frame_title.grid_columnconfigure(0, weight=1) # title

    def create_left_bot_frame_list_weapons(self):
        self.left_bot_frame_list_weapons = ctk.CTkFrame(self.left_main, fg_color="transparent")
        self.left_bot_frame_list_weapons.grid(row=1, column=0, sticky="nsew")
        self.left_bot_frame_list_weapons.grid_columnconfigure(0, weight=1)


    def add_frame_left_title_and_weapons(self):
        self.add_title()
        self.add_weapons_list()

    def add_weapons_list(self):
        max_rows_per_column = 10
        max_buttons = 20
        for idx, result in enumerate(self.list_weapons):
            if idx >= max_buttons:
                break

            col_index = idx // max_rows_per_column
            row_index = idx % max_rows_per_column

            self.left_bot_frame_list_weapons.grid_rowconfigure(row_index, weight=1)
            self.left_bot_frame_list_weapons.grid_columnconfigure(col_index, weight=1)

            button = ctk.CTkButton(
                self.left_bot_frame_list_weapons,
                text=result,
                height=10,
                width=10,
                font=("Arial", 18, "bold"),
                text_color="black",
                fg_color="blue",
                hover_color="red",
                command=lambda index=idx, name=result: self.delete_add_weapons_to_list(index, name)
            )
            button.grid(row=row_index, column=col_index, pady=10, padx=10, sticky="n")

            self.list_buttons_weapons.append(button)
            button.state = True

    def add_title(self):
        title_label1 = ctk.CTkLabel(self.left_top_frame_title,
                                   text="Weapons Will Be Modified :",
                                   font=("Arial", 20, "bold"),
                                   text_color="tomato")
        title_label1.grid(row=0, column=0, pady=0, sticky="n")
        title_label2 = ctk.CTkLabel(self.left_top_frame_title,
                                    text="Click to :",
                                    font=("Arial", 18, "bold"),
                                    text_color="tomato")
        title_label2.grid(row=1, column=0, pady=0, sticky="n")
        title_label3 = ctk.CTkLabel(self.left_top_frame_title,
                                    text="REMOVE(red)",
                                    font=("Arial", 15, "bold"),
                                    text_color="red")
        title_label3.grid(row=2, column=0, pady=0, sticky="n")
        title_label4 = ctk.CTkLabel(self.left_top_frame_title,
                                    text="ADD(blue)",
                                    font=("Arial", 15, "bold"),
                                    text_color="blue")
        title_label4.grid(row=3, column=0, pady=0, sticky="n")


    def delete_add_weapons_to_list(self, idx, name_weapon):
        button = self.list_buttons_weapons[idx]
        if button.state:
            Utils.transfer_file_between_lists(name_weapon,
                                              self.all_path,
                                              self.list_file_path_json_remove)

            button.configure(fg_color="red", font=("Arial", 10, "italic"), hover_color="blue")
            button.state = False
        else:
            Utils.transfer_file_between_lists(name_weapon,
                                              self.list_file_path_json_remove,
                                              self.all_path)
            button.configure(fg_color="blue", font=("Arial", 18, "bold"), hover_color="red")
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

    def load_data_save_json(self):
        data, self.json_caliber_path = JsonUtils.find_caliber_json_config(self.caliber)
        self.originale_value_from_JSON.update_from_json(data)
        self.manager.update_from_json(data)

    def run(self):
        row = 0
        manager_inverse_value: ItemManager = ItemManager()
        self.manager.copy_to_with_inverted_values(manager_inverse_value)
        for row, (props, number) in enumerate(manager_inverse_value.iterate_key_and_values()):
            if props != EnumProps.AMMO_CALIBER.label:
                self.right_main.grid_rowconfigure(row, weight=1)

                label = ctk.CTkLabel(self.right_main, text=f"{EnumProps.get_code_by_label(props)}:")
                label.grid(row=row, column=0, sticky=ctk.W, padx=10)
                slider = ctk.CTkSlider(
                    self.right_main,
                    from_=-99,
                    to=+99,
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

                self.color_risky_range(props, number, percent_label)
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
        self.color_risky_range(name, value, label)
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
            1.0)
        self.reset_apply_button()
        self.verify_all_sliders_reset()

    def verify_all_sliders_reset(self):
        if self.manager == self.originale_value_from_JSON:
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
            for key, value in self.manager.iterate_key_values_where_key_ve_change(self.originale_value_from_JSON):
                data_json_to_update = JsonUtils.update_json_in_new_file(key, value, data_json_to_update, True)

            list_path_new_json.append(JsonUtils.save_json_as_new_file(data_json_to_update, file_path))

        self.modify_save_json_file_caliber()
        self.wait_modify_json()
        self.check_wait_modify_json(list_path_new_json)


    def modify_save_json_file_caliber(self):
        data_json_to_update = dict(
            self.manager.iterate_key_values_where_key_ve_change(self.originale_value_from_JSON)
        )
        JsonUtils.update_json_caliber_from_new_value_change(self.json_caliber_path, data_json_to_update)

    def check_wait_modify_json(self, list_path_new_json, attempts=0, max_attempts=60):
        if attempts >= max_attempts:
            self.progress_bar.configure(progress_color="green")
            self.check_for_all_files(list_path_new_json)
        if self.progress_bar.is_progress_running():
            print("Progression en cours...")
            self.root.after(1000, lambda: self.check_wait_modify_json(list_path_new_json, attempts + 1))
        else:
            print("Progression terminée.")
            self.progress_bar.configure(progress_color="green")
            self.check_for_all_files(list_path_new_json)

    def wait_modify_json(self):
        Utils.disable_all_buttons_recursive(self.close_button, self.master)
        self.progress_bar = ProgressBar(self.right_main)
        self.progress_bar.start()

    def check_for_all_files(self, list_path_new_json):
        if list_path_new_json and JsonUtils.all_file_exist(list_path_new_json):
            self.apply_button.configure(fg_color="green", hover_color="green")
            self.status_label.configure(text="Changes applied successfully.")
            self.master.after(1500, self.master.destroy)
            self.main_instance.root.attributes('-disabled', False)
        else:
            self.status_label.configure(text="Error: One or more JSON files are missing.", text_color="red")
            self.apply_button.configure(fg_color="red", hover_color="red")
            self.master.after(3000, self.master.destroy)
            self.main_instance.root.attributes('-disabled', False)

    @staticmethod
    def color_risky_range(name, value, label):
        if Utils.is_value_outside_limits(name, value):
            label.configure(text_color="red")
        else:
            label.configure(text_color="white")

    def close_detail_window(self, detail_window):
        detail_window.grab_release()
        detail_window.destroy()
        self.root.attributes('-disabled', False)