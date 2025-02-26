import os
import customtkinter as ctk  # Utiliser l'alias ctk pour customtkinter
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
    elif abs_value < 1e-9:
        return ".10f"
    elif abs_value < 1e-8:
        return ".9f"
    elif abs_value < 1e-7:
        return ".8f"
    elif abs_value < 1e-6:
        return ".7f"
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
    def __init__(self, master, file_path):
        self.master = master
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
        resolution = 1
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

                        else:
                            scaled_int, scale_factor = float_to_scaled_int(prop_value)
                            one_percent = scaled_int * 0.01
                            hundredth_percent = scaled_int * 2

                            slider = ctk.CTkSlider(self.master, from_=one_percent, to=hundredth_percent,
                                                   command=lambda lambda_value, pname=prop_name, sf=scale_factor:
                                                   self.update_prop_value_float(pname, lambda_value, sf))
                            slider.set(scaled_int)

                            slider.grid(row=row, column=1, sticky=ctk.W)
                            percent_label = ctk.CTkLabel(self.master, text=f"{prop_value:.2f}")

                            self.original_props[prop_name] = (scaled_int, scale_factor)

                            self.reset_button = ctk.CTkButton(self.master, text="Reset",
                                                         command=lambda pname=prop_name: self.reset_slider(pname),
                                                         width=50, fg_color="red", hover_color="darkred")
                            self.reset_button.grid(row=row, column=3, sticky=ctk.W)

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
        """Remet le slider et le label à la valeur initiale correcte."""
        scaled_int, scale_factor = self.original_props[name]  # ✅ Récupérer les valeurs originales

        slider, label = self.prop_widgets[name]

        # ✅ Appliquer scale_factor SEULEMENT si nécessaire
        if scale_factor is not None:
            reset_value = scaled_int / scale_factor
        else:
            reset_value = scaled_int  # ✅ Pour les entiers, pas de scale_factor

        # ✅ Remettre le slider à la vraie valeur initiale
        slider.set(reset_value)

        # ✅ Mettre à jour le label avec le bon format
        format_spec = determine_format_spec(reset_value)
        label.configure(text=f"{reset_value:{format_spec}}")

        # ✅ Désactiver le bouton Apply si tout est revenu à la normale
        self.apply_button.configure(state="disabled")
        self.status_label.configure(text="")

    def apply_changes(self):
        new_file_path = self.file_path.replace('.json', '_mod.json')
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for prop_name in self.original_props.keys():
            slider, _ = self.prop_widgets[prop_name]
            new_value = slider.get()
            data['_props'][prop_name] = new_value
        with open(new_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        self.check_for_file(new_file_path)

    def check_for_file(self, file_path):
        if os.path.exists(file_path):
            self.apply_button.configure(fg_color="green", hover_color="green")
            self.status_label.configure(text="Changes applied successfully.")
        else:
            self.master.after(1000, lambda: self.check_for_file(file_path))

    def reset_apply_button(self):
        self.apply_button.configure(fg_color="blue", hover_color="lightblue", border_color="red", state="enable")  # Remettre la couleur d'origine
        self.status_label.configure(text="")


