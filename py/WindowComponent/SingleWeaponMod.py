import copy
from typing import TextIO
import customtkinter as ctk

from Entity import Logger
from Entity.Root import Root
from Entity.ItemProps import ItemProps
from Entity.EnumProps import EnumProps
from Entity.Item import Item
from Entity.ItemManager import ItemManager
from Entity.WindowType import WindowType
from Utils import JsonUtils, Utils, WindowUtils

file: TextIO


class SingleWeaponMod:
    def __init__(self, detail_window, root, file_path, main_instance):
        self.logger = Logger()
        self.close_button = None
        self.status_label = None
        self.right_main = None
        self.left_main = None
        self.apply_button = None
        self.json_mod_user_save_exist = False
        self.reset_after_load_save_and_value_reset = False

        self.detail_window = detail_window
        self.root = root
        self.main_instance = main_instance
        self.window_protocol = WindowUtils.window_protocol(self.detail_window,
                                                           self.detail_window,
                                                           self.root, self.main_instance)
        self.file_path = file_path
        self.jsonFile = {}

        self.data_from_json_mod_save_user: ItemManager = ItemManager(EnumProps)
        self.lambda_save_from_user_vs_originale: ItemManager = ItemManager(EnumProps)
        self.data_from_json_no_save: ItemManager = ItemManager(EnumProps)

        self.rootJSON = self.load_root()
        self.original_value_before_change_by_slider_or_local_save = copy.deepcopy(self.data_from_json_no_save)

        self.param_main_root()
        self.create_frame_left()
        self.create_frame_right()

        self.prop_widgets = {}
        self.apply_json_data_to_slider()
        if self.json_mod_user_save_exist:
            self.apply_save_file_mod_user_change()

    def apply_save_file_mod_user_change(self):
        for key, value in self.data_from_json_mod_save_user.iterate_key_and_values():
            if isinstance(value, (float, int)):
                slider, label = self.prop_widgets[key]

                if isinstance(value, int):
                    self.update_prop_value_int(key, value)
                    slider.set(value)

                elif isinstance(value, float):
                    scale_factor = getattr(slider, "scale_factor", 1)

                    slider.set(value * scale_factor)
                    self.update_prop_value_float(key, value * scale_factor, scale_factor)

    def param_main_root(self):
        self.detail_window.grid_columnconfigure(0, weight=0)
        self.detail_window.grid_columnconfigure(1, weight=8)
        self.detail_window.grid_rowconfigure(0, weight=1)
        self.detail_window.grid_rowconfigure(1, weight=1)
        self.close_button = ctk.CTkButton(self.detail_window,
                                          text="Close",
                                          command=lambda:
                                          WindowUtils.close_window(self.detail_window,
                                                                   self.root, self.main_instance))
        self.close_button.grid(row=1, column=0)

    def create_frame_left(self):
        self.left_main = ctk.CTkFrame(self.detail_window, fg_color="transparent")
        self.left_main.grid(row=0, column=0, sticky="nsew")

    def create_frame_right(self):
        self.right_main = ctk.CTkFrame(self.detail_window, fg_color="transparent")
        self.right_main.grid(row=0, column=1, sticky="nsew")
        self.right_main.grid_columnconfigure(0, weight=1)
        self.right_main.grid_columnconfigure(1, weight=1)
        self.right_main.grid_columnconfigure(2, weight=1)

    def load_root(self):
        if JsonUtils.file_mod_exist(self.file_path):
            self.load_old_modification_from_user()

        root: Root = self.load_originale_value()
        self.lambda_save_from_user_vs_originale = self.data_from_json_mod_save_user.lambda_value(
            self.data_from_json_no_save)

        return root

    def load_old_modification_from_user(self):
        self.json_mod_user_save_exist = True
        root_mod: Root

        data_from_mod = JsonUtils.return_json_mod(self.file_path)
        root_mod = self.create_item_manager_from_json(data_from_mod, self.data_from_json_mod_save_user,
                                                      WindowType.WEAPON)

    def load_originale_value(self):
        data = JsonUtils.load_json(self.file_path)
        root: Root = self.create_item_manager_from_json(data, self.data_from_json_no_save, WindowType.WEAPON)
        self.jsonFile = data
        return root

    def generate_information_from_weapon(self):
        title_label = ctk.CTkLabel(self.left_main,
                                   text="You have chosen :",
                                   font=("Arial", 18, "bold"))
        title_label.pack(side="top",
                         anchor="center")
        name = ctk.CTkButton(self.left_main,
                             text=self.rootJSON.locale.ShortName,
                             font=("Arial", 16, "bold"))
        name.pack(side="top", anchor="center")
        id_label = ctk.CTkLabel(self.left_main,
                                text="ID:",
                                font=("Arial", 18, "bold"))
        id_label.pack(side="top",
                      anchor="center")
        id_button = ctk.CTkButton(self.left_main,
                                  text=self.rootJSON.item.id)
        id_button.pack(side="top", anchor="center")

    def calcul_gap_originale_vs_mod(self):
        self.lambda_save_from_user_vs_originale = self.data_from_json_no_save.lambda_value(
            self.data_from_json_mod_save_user)

    def apply_json_data_to_slider(self):
        self.generate_information_from_weapon()
        row = 0
        for prop_value, number in self.data_from_json_no_save.iterate_key_and_values():
            prop_value: EnumProps
            if isinstance(number, (int, float)) and number != 0:
                self.right_main.grid_rowconfigure(row, weight=1)
                label = ctk.CTkLabel(self.right_main, text=f"{EnumProps.get_code_by_label(prop_value)}:")
                label.grid(row=row, column=0, sticky=ctk.W, padx=10)

                if isinstance(number, int):
                    percent_label, slider = self.slider_integer(number, row, prop_value)

                else:
                    percent_label, slider = self.slider_float(number, row, prop_value)

                percent_label.grid(row=row, column=2, sticky=ctk.W, padx=10)
                self.prop_widgets[prop_value] = (slider, percent_label)
                row += 1
            row += 1

        self.apply_button = ctk.CTkButton(self.right_main,
                                          text="Apply",
                                          command=self.apply_changes,
                                          state="disabled",
                                          fg_color="white")
        self.apply_button.grid(row=row, column=1, sticky="nsew")
        self.status_label = ctk.CTkLabel(self.right_main, text="")
        self.status_label.grid(row=row + 1, column=1, sticky="nsew")

    def slider_integer(self, number, row, prop_value: EnumProps):
        one_percent = max(number * 0.01, 1)
        hundredth_percent = max(number * 2, one_percent + 1)

        slider = ctk.CTkSlider(self.right_main, from_=one_percent, to=hundredth_percent,
                               command=lambda lambda_value, pname=prop_value:
                               self.update_prop_value_int(pname, int(lambda_value)))

        slider.set(number)
        slider.grid(row=row, column=1, sticky=ctk.W, padx=10)
        percent_label = ctk.CTkLabel(self.right_main, text=f"{number}", font=("Arial", 15, "bold"))
        reset_button = ctk.CTkButton(self.right_main, text="Reset",
                                     command=lambda pname=prop_value:
                                     self.reset_slider(pname),
                                     width=10)
        reset_button.grid(row=row, column=3, sticky=ctk.W, padx=10)
        return percent_label, slider

    def slider_float(self, number, row, prop_value: EnumProps):
        scaled_int, scale_factor = Utils.float_to_scaled_int(number)
        one_percent = scaled_int * 0.1
        hundredth_percent = scaled_int * 2

        slider = ctk.CTkSlider(self.right_main, from_=one_percent, to=hundredth_percent,
                               command=lambda lambda_value, pname=prop_value, sf=scale_factor:
                               self.update_prop_value_float(pname, lambda_value, sf))
        slider.set(scaled_int)
        slider.scale_factor = scale_factor

        slider.grid(row=row, column=1, sticky=ctk.W, padx=10)
        percent_label = ctk.CTkLabel(self.right_main, text=f"{number:.2f}",
                                     font=("Arial", 15, "bold"))

        reset_button = ctk.CTkButton(self.right_main, text="Reset",
                                     command=lambda pname=prop_value:
                                     self.reset_slider(pname),
                                     width=10)
        reset_button.grid(row=row, column=3, sticky=ctk.W, padx=10)
        return percent_label, slider

    def update_prop_value_int(self, name, value):
        props: ItemProps = self.rootJSON.item.props
        original_value = props.get_value_by_label(name)
        adjusted_value = int(value)
        percentage_change = ((adjusted_value - original_value) / original_value) * 100
        slider, label = self.prop_widgets[name]
        if Utils.is_value_outside_limits_weapons(name, percentage_change):
            label.configure(text_color="red")
        else:
            label.configure(text_color="white")

        label.configure(text=f"{adjusted_value} ({percentage_change:+.0f}%)")
        self.data_from_json_no_save.update_from_props_json(name, adjusted_value)
        self.reset_apply_button()

    def update_prop_value_float(self, name, value, scale_factor):
        adjusted_value = float(value) / float(scale_factor)
        props: ItemProps = self.rootJSON.item.props
        originial_value = props.get_value_by_label(name)

        if originial_value is None:
            raise ValueError(f"No default value found for '{name}'.")
        if isinstance(originial_value, int):
            adjusted_value = int(adjusted_value)
        else:
            adjusted_value = float(
                adjusted_value
            )
        percentage_change = ((adjusted_value - originial_value) / originial_value) * 100
        format_spec = Utils.determine_format_spec(adjusted_value)
        adjusted_value_str = f"{adjusted_value:{format_spec}}"
        slider, label = self.prop_widgets[name]

        if Utils.is_value_outside_limits_weapons(name, percentage_change):
            label.configure(text_color="red")
        else:
            label.configure(text_color="white")

        label.configure(text=f"{adjusted_value_str} ({percentage_change:+.0f}%)")

        self.data_from_json_no_save.update_from_props_json(name, float(adjusted_value_str))
        self.reset_apply_button()

    def reset_slider(self, name):
        props: ItemProps = self.rootJSON.item.props
        original_value = props.get_value_by_label(name)
        slider, label = self.prop_widgets[name]

        if isinstance(original_value, int):
            slider.set(original_value)
            label.configure(text=f"{original_value}")
            self.data_from_json_no_save.update_from_props_json(name, original_value)
            label.configure(text_color="white")
        else:
            format_spec = Utils.determine_format_spec(original_value)
            label.configure(text=f"{original_value:{format_spec}}")
            self.data_from_json_no_save.update_from_props_json(name, original_value)
            scaled_int, _ = Utils.float_to_scaled_int(original_value)
            label.configure(text_color="white")
            slider.set(scaled_int)

        self.reset_apply_button()
        self.verify_all_sliders_reset()

    def verify_all_sliders_reset(self):
        if self.json_mod_user_save_exist:
            if self.original_value_before_change_by_slider_or_local_save == self.data_from_json_no_save:
                self.apply_button.configure(fg_color="#a569bd",
                                            hover_color="lightblue",
                                            border_color="blue",
                                            state="enable")
                self.status_label.configure(
                    text="Same as the original values \n You will get back the \n original values",
                    text_color="pink", font=("Arial", 13, "italic"))
                self.reset_after_load_save_and_value_reset = True
        else:
            if self.original_value_before_change_by_slider_or_local_save == self.data_from_json_no_save:
                self.apply_button.configure(state="disabled", fg_color="white")
                self.status_label.configure(text="")

    def apply_changes(self):
        if self.original_value_before_change_by_slider_or_local_save != self.data_from_json_no_save:
            data_json_to_update = JsonUtils.load_json(self.file_path)

            for name_props_to_modify, value_modify in self.data_from_json_no_save.iterate_key_and_values():
                data_json_to_update = JsonUtils.update_json_in_new_file_multi_choice(name_props_to_modify, value_modify,
                                                                                     data_json_to_update, WindowType.WEAPON)

            file_path_update = JsonUtils.save_json_as_new_file(data_json_to_update, self.file_path)
            self.check_for_file(file_path_update)

        else:
            JsonUtils.delete_file_mod_if_exists(self.file_path)
            self.main_instance.list_json_name_mod_weapons = JsonUtils.load_all_json_files_weapons_mod()
            if self.main_instance.list_json_name_mod_weapons:
                self.main_instance.button_view_all_weapons_mod.configure(text="All Saved Weapons Mod")
            else:
                self.main_instance.button_view_all_weapons_mod.configure(text="No weapons mod find")

            self.apply_button.configure(fg_color="green", hover_color="green")
            self.status_label.configure(text="All weapon modifications have been removed.")
            self.detail_window.after(3000, lambda: WindowUtils.close_window(self.detail_window,
                                                                            self.root, self.main_instance))

    def check_for_file(self, new_file_path, attempts=0, max_attempts=10):
        self.main_instance.list_json_name_mod_weapons = JsonUtils.load_all_json_files_weapons_mod()
        if self.main_instance.list_json_name_mod_weapons:
            self.main_instance.button_view_all_weapons_mod.configure(text="All Saved Weapons Mod")
        else:
            self.main_instance.button_view_all_weapons_mod.configure(text="No weapons mod find")

        Utils.disable_all_buttons_recursive(self.close_button, self.detail_window)
        if JsonUtils.file_exist(new_file_path):
            self.apply_button.configure(fg_color="green", hover_color="green")
            self.status_label.configure(text="Changes applied successfully.")
            self.detail_window.after(3000, lambda: WindowUtils.close_window(self.detail_window,
                                                                            self.root, self.main_instance))

        elif attempts < max_attempts:
            self.status_label.configure(text=f"Checking for file... Attempt {attempts + 1}/{max_attempts}")
            self.detail_window.after(2000, lambda: self.check_for_file(new_file_path, attempts + 1, max_attempts))
        else:
            self.status_label.configure(text="Failed to detect the file. Please try again.", text_color="red")
            self.apply_button.configure(fg_color="red", hover_color="gray")
            self.main_instance.root.attributes('-disabled', False)
            self.detail_window.after(3000, lambda: WindowUtils.close_window(self.detail_window,
                                                                            self.root, self.main_instance))

    def reset_apply_button(self):
        self.apply_button.configure(fg_color="blue", hover_color="lightblue", border_color="red",
                                    state="enable")
        self.status_label.configure(text="Ready to apply changes")

    @staticmethod
    def create_item_manager_from_json(data, item_manager: ItemManager, wt: WindowType):
        root: Root = Root.from_data(data, wt)
        item: Item = root.item
        item_props: ItemProps = item.props

        for key, (numerical_value, code) in vars(item_props).items():
            item_manager.update_from_props_json(code, numerical_value)

        return root
