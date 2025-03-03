import copy
import os
from typing import TextIO
import customtkinter as ctk
import json

from Entity import Root, ItemProps, EnumProps, Item
from Utils import ItemManager, JsonUtils

file: TextIO


def float_to_scaled_int(value: float):
    if isinstance(value, int):  # Si c'est déjà un entier, aucun ajustement
        return value, 1

    str_value = f"{value:.10f}".rstrip('0')
    if '.' in str_value:
        decimal_places = len(str_value.split('.')[1])
        scale_factor = 1000 ** decimal_places
    else:
        decimal_places = 0
        scale_factor = 1

    scaled_int = int(value * scale_factor)
    return scaled_int, scale_factor


def determine_format_spec(adjusted_value):
    abs_value = abs(adjusted_value)
    if adjusted_value == int(adjusted_value):
        return ".0f"
    if abs_value == 0:
        return ".2f"
    elif abs_value < 1e-5:
        return ".6f"
    elif abs_value < 1e-4:
        return ".5f"
    elif abs_value < 1e-3:
        return ".4f"
    elif abs_value < 1e-2:
        return ".3f"
    else:
        return ".2f"


class ItemDetails:
    def __init__(self, master, file_path, main_instance):
        self.status_label = None
        self.right_main = None
        self.left_main = None
        self.apply_button = None
        self.master = master
        self.main_instance = main_instance
        self.file_path = file_path
        self.jsonFile = {}
        self.manager = ItemManager()
        self.rootJSON = self.load_root()
        self.original_value_before_change = copy.deepcopy(self.manager)

        self.param_main_root()
        self.create_frame_left()
        self.create_frame_right()
        self.prop_widgets = {}
        self.display_details()

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

    def load_root(self):
        with open(self.file_path, 'r', encoding='utf-8') as fileReadable:
            data = json.load(fileReadable)
            self.jsonFile = data
            root: Root = Root.from_data(data)
            item: Item = root.item
            item_props: ItemProps = item.props
            # modify
            for key, (numerical_value, code) in vars(item_props).items():
                self.manager.update_from_props_json(code, numerical_value)
        return root

    def locale_informations(self):
        title_label = ctk.CTkLabel(self.left_main,
                                   text="You have chosen :",
                                   font=("Arial", 18, "bold"))
        title_label.pack(side="top",
                         anchor="center")
        name = ctk.CTkButton(self.left_main, text=self.rootJSON.locale.ShortName, font=("Arial", 16, "bold"))
        name.pack(side="top", anchor="center")
        id_label = ctk.CTkLabel(self.left_main,
                                text="ID:",
                                font=("Arial", 18, "bold"))
        id_label.pack(side="top",
                      anchor="center")
        id_button = ctk.CTkButton(self.left_main, text=self.rootJSON.item.id)
        id_button.pack(side="top", anchor="center")

    def display_details(self):
        self.locale_informations()
        row = 0
        for prop_value, number in self.manager.iterate_key_and_values():
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

        self.apply_button = ctk.CTkButton(self.right_main, text="Apply", command=self.apply_changes, state="disabled",
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
        scaled_int, scale_factor = float_to_scaled_int(number)
        one_percent = scaled_int * 0.01
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
        label.configure(text=f"{adjusted_value} ({percentage_change:+.0f}%)")
        self.manager.update_from_props_json(name, adjusted_value)
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
        format_spec = determine_format_spec(adjusted_value)
        adjusted_value_str = f"{adjusted_value:{format_spec}}"
        slider, label = self.prop_widgets[name]

        label.configure(text=f"{adjusted_value_str} ({percentage_change:+.0f}%)")

        self.manager.update_from_props_json(name, float(adjusted_value_str))
        self.reset_apply_button()

    def reset_slider(self, name):
        props: ItemProps = self.rootJSON.item.props
        original_value = props.get_value_by_label(name)
        slider, label = self.prop_widgets[name]

        if isinstance(original_value, int):
            slider.set(original_value)
            label.configure(text=f"{original_value}")
            self.manager.update_from_props_json(name, original_value)
        else:
            format_spec = determine_format_spec(original_value)
            label.configure(text=f"{original_value:{format_spec}}")
            self.manager.update_from_props_json(name, original_value)
            scaled_int, _ = float_to_scaled_int(original_value)
            slider.set(scaled_int)

        self.reset_apply_button()
        self.verify_all_sliders_reset()

    def verify_all_sliders_reset(self):
        if self.original_value_before_change == self.manager:
            self.apply_button.configure(state="disabled", fg_color="white")
            self.status_label.configure(text="")

    def apply_changes(self):
        if self.original_value_before_change != self.manager:
            new_file_path = self.file_path.replace('.json', '_mod.json')
            data_json_to_update = JsonUtils.load_json(self.file_path)

            for name_props_to_modify, value_modify in self.manager.iterate_key_and_values():
                data_json_to_update = JsonUtils.update_json_in_new_file(name_props_to_modify, value_modify,
                                                                        data_json_to_update, False)

            new_file_path = JsonUtils.save_json_as_new_file(data_json_to_update, new_file_path)
            self.check_for_file(new_file_path)

    def check_for_file(self, new_file_path):
        if JsonUtils.file_exist(new_file_path):
            self.apply_button.configure(fg_color="green", hover_color="green")
            self.status_label.configure(text="Changes applied successfully.")
            self.master.after(1500, self.master.destroy)
            self.main_instance.root.attributes('-disabled', False)

        else:
            self.master.after(1000, lambda: self.check_for_file(new_file_path))

    def reset_apply_button(self):
        self.apply_button.configure(fg_color="blue", hover_color="lightblue", border_color="red",
                                    state="enable")
        self.status_label.configure(text="Ready to apply changes")
