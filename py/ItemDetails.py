import os
import customtkinter as ctk
import json

from CustomWeapon.py.Entity.Item import Item
from CustomWeapon.py.Entity.ItemProps import create_item_props, ItemProps

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
        self.master = master
        self.main_instance = main_instance
        self.file_path = file_path
        self.item = self.load_item()
        self.original_props = {k: v for k, v in vars(self.item._props).items()}
        self.prop_widgets = {}
        self.display_details()

    def load_item(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            props = create_item_props(data['_props'])
            return Item(id=data['_id'], name=data['_name'], parent=data['_parent'], props=props)

    def display_details(self):
        row = 0
        for attr, value in vars(self.item).items():
            if isinstance(value, ItemProps):
                for prop_name, prop_value in vars(value).items():
                    if isinstance(prop_value, (int, float)) and prop_value != 0:
                        label = ctk.CTkLabel(self.master, text=f"{prop_name}:")
                        label.grid(row=row, column=0, sticky=ctk.W)

                        if isinstance(prop_value, int):
                            one_percent = max(prop_value * 0.01, 1)
                            hundredth_percent = max(prop_value * 2, one_percent + 1)

                            slider = ctk.CTkSlider(self.master, from_=one_percent, to=hundredth_percent,
                                                   command=lambda lambda_value, pname=prop_name:
                                                   self.update_prop_value_int(pname, int(lambda_value)))
                            slider.set(prop_value)
                            slider.grid(row=row, column=1, sticky=ctk.W)
                            percent_label = ctk.CTkLabel(self.master, text=f"{prop_value}")
                            reset_button = ctk.CTkButton(self.master, text="Reset",
                                                         command=lambda pname=prop_name:
                                                         self.reset_slider(pname),
                                                         width=10)
                            reset_button.grid(row=row, column=3, sticky=ctk.W)

                        else:
                            scaled_int, scale_factor = float_to_scaled_int(prop_value)
                            one_percent = scaled_int * 0.01
                            hundredth_percent = scaled_int * 2

                            slider = ctk.CTkSlider(self.master, from_=one_percent, to=hundredth_percent,
                                                   command=lambda lambda_value, pname=prop_name, sf=scale_factor:
                                                   self.update_prop_value_float(pname, lambda_value, sf))
                            slider.set(scaled_int)
                            slider.scale_factor = scale_factor

                            slider.grid(row=row, column=1, sticky=ctk.W)
                            percent_label = ctk.CTkLabel(self.master, text=f"{prop_value:.2f}")

                            reset_button = ctk.CTkButton(self.master, text="Reset",
                                                              command=lambda pname=prop_name:
                                                              self.reset_slider(pname),
                                                              width=10)
                            reset_button.grid(row=row, column=3, sticky=ctk.W)

                        percent_label.grid(row=row, column=2, sticky=ctk.W)
                        self.prop_widgets[prop_name] = (slider, percent_label)
                        row += 1
            else:
                label = ctk.CTkLabel(self.master, text=f"{attr}: {value}")
                label.grid(row=row, column=0, columnspan=3, sticky=ctk.W)
                row += 1

        self.apply_button = ctk.CTkButton(self.master, text="Apply", command=self.apply_changes, state="disabled", fg_color="white")
        self.apply_button.grid(row=row, column=4)
        self.status_label = ctk.CTkLabel(self.master, text="")
        self.status_label.grid(row=row, column=5)

    def update_prop_value_int(self, name, value):
        original_value = self.original_props[name]
        adjusted_value = int(value)
        percentage_change = ((adjusted_value - original_value) / original_value) * 100
        slider, label = self.prop_widgets[name]
        label.configure(text=f"{adjusted_value} ({percentage_change:+.0f}%)")
        self.reset_apply_button()

    def update_prop_value_float(self, name, value, scale_factor):
        adjusted_value = float(value) / float(scale_factor)
        default_value = self.original_props[name]
        percentage_change = ((adjusted_value - default_value) / default_value) * 100
        format_spec = determine_format_spec(adjusted_value)
        adjusted_value_str = f"{adjusted_value:{format_spec}}"
        slider, label = self.prop_widgets[name]
        label.configure(text=f"{adjusted_value_str} ({percentage_change:+.0f}%)")
        self.reset_apply_button()

    def reset_slider(self, name):
        original_value = self.original_props[name]
        slider, label = self.prop_widgets[name]
        if isinstance(original_value, int):
            slider.set(original_value)
            label.configure(text=f"{original_value}")
        else:
            print(original_value)
            format_spec = determine_format_spec(original_value)
            print(format_spec)
            label.configure(text=f"{original_value:{format_spec}}")
            scaled_int, _ = float_to_scaled_int(original_value)
            slider.set(scaled_int)
        self.reset_apply_button()
        self.verify_all_sliders_reset()

    def verify_all_sliders_reset(self):
        all_reset = True
        for name, (slider, label) in self.prop_widgets.items():
            current_value = slider.get()
            original_value = self.original_props[name]

            if isinstance(original_value, int):
                if current_value != original_value:
                    all_reset = False
                    break
            else:
                scaled_original_value, _ = float_to_scaled_int(original_value)
                if abs(current_value - scaled_original_value) > 1e-2:
                    all_reset = False
                    break

        if all_reset:
            self.apply_button.configure(state="disabled", fg_color="white")
            self.status_label.configure(text="")

    def apply_changes(self):
        new_file_path = self.file_path.replace('.json', '_mod.json')
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for prop_name, original_value in self.original_props.items():
            slider, _ = self.prop_widgets[prop_name]
            new_value = slider.get()

            if isinstance(original_value, int):
                new_value = int(new_value)
            elif isinstance(original_value, float):
                new_value = new_value / slider.scale_factor
            data['_props'][prop_name] = new_value

        with open(new_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

        self.check_for_file(new_file_path)

    def check_for_file(self, file_path):
        if os.path.exists(file_path):
            self.apply_button.configure(fg_color="green", hover_color="green")
            self.status_label.configure(text="Changes applied successfully.")
            self.master.after(1500, self.master.destroy)
            self.main_instance.root.attributes('-disabled', False)

        else:
            self.master.after(1000, lambda: self.check_for_file(file_path))

    def reset_apply_button(self):
        self.apply_button.configure(fg_color="blue", hover_color="lightblue", border_color="red", state="enable")  # Remettre la couleur d'origine
        self.status_label.configure(text="")




