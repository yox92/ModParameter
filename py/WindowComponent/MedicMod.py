import copy

import customtkinter as ctk
from tkinter import messagebox

from Entity import Logger, Root, Item, Medic, WindowType
from Entity.EnumEffect import EnumEffect
from Entity.EnumEffectName import EnumEffectName
from Entity.EnumMedic import EnumMedic
from Utils import WindowUtils, JsonUtils, Utils


class MedicMod:
    def __init__(self, master, root, detail_window, file_path, main_instance):
        self.logger = Logger()
        self.data_save_load = False
        self.block_system_error_detect = False
        self.close_button = None
        self.master = master
        self.root = root
        self.detail_window = detail_window
        self.file_path = file_path
        self.main_instance = main_instance
        self.master.configure(bg="#242424")
        self.is_clone: bool = False
        self.window_protocol = WindowUtils.window_protocol(self.detail_window,
                                                           self.detail_window,
                                                           self.root, self.main_instance)
        self.root_item: Root = self.load_data_root()
        self.data_from_json_no_save: Medic = self.load_data_medic()
        self.original_value_copy: Medic = copy.deepcopy(self.data_from_json_no_save)
        self.data_from_json_save: Medic = self.load_data_save()
        self.param_main_root()
        self.create_frame_left()
        self.create_frame_right()

        self.prop_widgets = {}
        self.run()

    def load_data_medic(self):
        data = JsonUtils.load_json_Weapon_Ammo_Medic(self.file_path)
        self.is_clone = data["clone"]
        root: Root = Root.from_data(data, WindowType.MEDIC)
        item: Item = root.item
        medic: Medic = item.props
        return medic

    def load_data_root(self):
        data = JsonUtils.load_json_Weapon_Ammo_Medic(self.file_path)
        root: Root = Root.from_data(data, WindowType.MEDIC)
        return root

    def load_data_save(self):
        exist = JsonUtils.file_mod_exist(self.file_path)
        if exist:
            self.data_save_load = True
            data_save = JsonUtils.return_json_mod(self.file_path)
            self.is_clone = data_save["clone"]
            root: Root = Root.from_data(data_save, WindowType.MEDIC)
            item: Item = root.item
            medic: Medic = item.props
            price = medic.get_value_by_label(EnumMedic.PRICEFACTOR.label)
            if isinstance(price, int):
               medic.set_value(EnumMedic.PRICEFACTOR.label, float(price))
            return medic
        else:
            return None

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

    def generate_information_from_weapon(self):
        title_label = ctk.CTkLabel(self.left_main,
                                   text="You have chosen :",
                                   font=("Arial", 18, "bold"))
        title_label.pack(side="top",
                         anchor="center")
        name = ctk.CTkButton(self.left_main,
                             text=self.root_item.locale.ShortName,
                             font=("Arial", 16, "bold"))
        name.pack(side="top", anchor="center")
        id_label = ctk.CTkLabel(self.left_main,
                                text="ID:",
                                font=("Arial", 18, "bold"))
        id_label.pack(side="top",
                      anchor="center")
        id_button = ctk.CTkButton(self.left_main,
                                  text=self.root_item.item.id)
        id_button.pack(side="top", anchor="center")
        id_label = ctk.CTkLabel(self.left_main,
                                text="Clone/Override ? :",
                                font=("Arial", 18, "bold",))
        id_label.pack(side="top",
                      anchor="center" ,pady=(100, 0))

        clone_text = "New Clone" if self.is_clone else "Replace Original"
        clone_color = "blue" if self.is_clone else "red"

        self.clone_button = ctk.CTkButton(self.left_main,
                                          text=clone_text,
                                          fg_color=clone_color,
                                          command=self.toggle_clone_status)
        self.clone_button.pack(side="top", anchor="center")

    def toggle_clone_status(self):
        self.is_clone = not self.is_clone
        new_text = "Create a Clone" if self.is_clone else "Replace Original Item"
        new_color = "blue" if self.is_clone else "red"
        self.clone_button.configure(text=new_text, fg_color=new_color, hover_color=new_color)

    def change_clone_statut(self, file_path):
        JsonUtils.change_clone_statut(file_path, self.is_clone)

    def run(self):
        self.generate_information_from_weapon()
        if self.data_save_load:
            self.data_from_json_no_save = copy.deepcopy(self.data_from_json_save)
        medic: Medic = self.data_from_json_no_save

        row = 0
        for enum_field in EnumMedic:
            label_name = enum_field.label
            value = getattr(medic, label_name, None)
            if Utils.enum_to_lock(self.root_item.item.parent, label_name):
                if isinstance(value, tuple) and len(value) == 2:
                    raw_value = value[0]
                else:
                    raw_value = value

                self.right_main.grid_rowconfigure(row, weight=1)

                label = ctk.CTkLabel(self.right_main, text=f"{EnumMedic.get_code_by_label(label_name)}:")
                label.grid(row=row, column=0, sticky=ctk.W, padx=10)

                label.configure(font=("Arial", 14, "bold"), text_color="Peru")

                if isinstance(raw_value, (int, float)):
                    self.entry_input(raw_value, row, label_name)

                    row += 1

        self.apply_button = ctk.CTkButton(
                self.left_main,
                text="Apply",
                command=self.apply_changes,
                state="disabled",
                fg_color="white"
            )
        self.apply_button.pack(side="bottom", anchor="center")
        self.status_label = ctk.CTkLabel(self.left_main, text="")
        self.status_label.pack(side="bottom", anchor="center")

        self.right_main.grid_rowconfigure(row +1, weight=1)
        self.title_effect = ctk.CTkLabel(self.right_main,
                                   text="Effect medic item :",
                                   font=("Arial", 18, "bold"))

        self.display_effect_buttons(row + 1 )

    def display_effect_buttons(self, row):
        self.title_effect.grid(row=row, column=0, pady=0, sticky="n")
        self.effect_frame = ctk.CTkFrame(self.right_main, fg_color="transparent")
        self.effect_frame.grid(row=row, column=1, sticky="nsew")

        existing_effects = self.data_from_json_no_save.effects_damage.effects

        existing = []
        missing = []

        for enum_effect in EnumEffectName:
            if enum_effect.value in existing_effects:
                existing.append(enum_effect)
            else:
                missing.append(enum_effect)

        sorted_effects = existing + missing

        for enum_effect in sorted_effects:
            effect_name = enum_effect.value
            is_existing = effect_name in existing_effects

            button_label = f"✔️ {effect_name}" if is_existing else f"(➕ add) {effect_name}"

            btn = ctk.CTkButton(
                self.effect_frame,
                text=button_label,
                fg_color="green" if not is_existing else None,
                command=lambda name=effect_name: self.open_effect_editor(name, row + 1)
            )
            btn.pack(side="top", anchor="center")

    def open_effect_editor(self, effect_name, row):
        from Entity.Effect import Effect

        if hasattr(self, 'effect_edit_frame'):
            self.effect_edit_frame.destroy()

        self.effect_edit_frame = ctk.CTkFrame(self.right_main, fg_color="transparent")
        self.effect_edit_frame.grid(row=row + 1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        effect = self.data_from_json_no_save.effects_damage.get_effect(effect_name)
        if effect is None:
            effect = Effect()

        self.effect_entries = {}
        row_edit = 0

        for enum_effect in Utils.select_effect_value(effect_name):
            label = enum_effect.label
            code = enum_effect.code

            lbl_widget = ctk.CTkLabel(self.effect_edit_frame, text=code)
            lbl_widget.grid(row=row_edit, column=0, padx=10, pady=2, sticky="w")

            entry = ctk.CTkEntry(self.effect_edit_frame)
            value = getattr(effect, label, None)

            if value is not None:
                entry.insert(0, str(value))
            entry.grid(row=row_edit, column=1, padx=10, pady=2, sticky="ew")

            self.effect_entries[label] = entry
            row_edit += 1

        def save_effect():
            from Utils import Utils

            for prop, entry in self.effect_entries.items():
                text = entry.get().strip()

                if text == "":
                    if prop in EnumEffect.HEALTHPENALTYMIN.label:
                        val = 99
                    if prop in EnumEffect.DURATION.label:
                        val = 100
                    elif prop in EnumEffect.HEALTHPENALTYMAX.label:
                        val = 100
                    else:
                        val = 0
                else:
                    try:
                        val = int(text)
                    except ValueError:
                        messagebox.showerror("Erreur", f"Le champ '{prop}' doit être un nombre.")
                        return

                if Utils.is_value_outside_limits_effect(prop, val):
                    messagebox.showerror("Erreur", f"La valeur pour '{prop}' est hors limites autorisées.")
                    return
                if EnumEffect.COST.label in prop:
                    if Utils.is_value_outside_hpMax(self.root_item.item.props.MaxHpResource[0], val, prop):
                        messagebox.showerror("Error",
                                             f"It is not possible to remove '{val}' points from an item that has only {self.root_item.item.props.MaxHpResource[0]} maximum resource."
                                             f" For example, an AI-2 has 100 resource points. If stopping heavy bleeding costs 110, it's not possible."
                                             f" Either increase the resource amount or set the cost to 0.")
                        return
                setattr(effect, prop, val)

            self.data_from_json_no_save.effects_damage.add_effect(effect_name, effect)

            self.effect_frame.destroy()
            self.display_effect_buttons(row - 1)
            self.effect_edit_frame.destroy()
            self.reset_apply_button()

        def cancel_edit():
            self.effect_edit_frame.destroy()
            self.reset_apply_button()
            if hasattr(self, 'current_open_button'):
                self.current_open_button.configure(
                    fg_color="green" if effect_name not in self.data_from_json_no_save.effects_damage.effects else None)
                self.current_open_button = None

        cancel_btn = ctk.CTkButton(self.effect_edit_frame, text="Cancel", fg_color="gray", command=cancel_edit)
        cancel_btn.grid(row=row_edit, column=1, pady=10, padx=10)

        def delete_effect():
            if effect_name in self.data_from_json_no_save.effects_damage.effects:
                del self.data_from_json_no_save.effects_damage.effects[effect_name]

            self.effect_frame.destroy()
            self.display_effect_buttons(row - 1)
            self.effect_edit_frame.destroy()
            self.reset_apply_button()

        save_btn = ctk.CTkButton(self.effect_edit_frame, text="Save", command=save_effect)
        save_btn.grid(row=row_edit, column=0, pady=10, padx=10)

        if effect_name in self.data_from_json_no_save.effects_damage.effects:
            delete_btn = ctk.CTkButton(
                self.effect_edit_frame,
                text="🗑 Delete",
                fg_color="red",
                hover_color="#aa0000",
                command=delete_effect
            )
            delete_btn.grid(row=row_edit, column=1, pady=10, padx=10)

    def entry_input(self, value, row, prop_value: EnumMedic):
        entry = ctk.CTkEntry(
            self.right_main,
            placeholder_text="Enter value...",
            width=70,
            font=("Arial", 14, "bold"),
            justify="center"
        )
        entry.bind("<KeyRelease>", lambda event: self.get_entry_value(event, prop_value, value))
        entry.insert(0, str(value))
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        entry_label = ctk.CTkLabel(
            self.right_main, text=f"{value}", font=("Arial", 15, "bold"))
        entry_label.grid(row=row, column=2, sticky=ctk.W, padx=10)
        reset_button = ctk.CTkButton(self.right_main,
                                     text="Reset", command=lambda pname=prop_value: self.reset_entry(pname, entry),
                                     width=10)
        reset_button.grid(row=row, column=2, padx=5, pady=5, sticky="w")
        self.prop_widgets[prop_value] = (entry, entry_label)

    def reset_entry(self, pname, entry):
        original_value = self.original_value_copy.get_attribute_value(pname)[0]
        entry = self.prop_widgets[pname][0]
        self.prop_widgets[pname][0].delete(0, 'end')
        entry.insert(0, str(original_value))
        self.data_from_json_no_save.set_value(pname, original_value)
        self.reset_apply_button()
        self.verify_all_sliders_reset()


    def get_entry_value(self, event, prop_value, value):
        input_text = self.prop_widgets[prop_value][0].get()
        try:
            if prop_value == EnumMedic.PRICEFACTOR.label:
                int_input_text = float(input_text)
            else:
                int_input_text = int(input_text)
        except ValueError:
            self.error_number_prompt()
            self.logger.log("warning", "Number please ...")
            self.block_system_error_detect = True
            Utils.block_all_input_before_correction(self.close_button,
                                                    self.master,
                                                    self.apply_button,
                                                    self.prop_widgets[prop_value][0])
            return
        if isinstance(int_input_text, (int, float)):
            if not Utils.is_value_outside_limits_medic(prop_value, int_input_text):
                self.reset_apply_button()
                self.data_from_json_no_save.set_value(prop_value, int_input_text)
                if self.block_system_error_detect:
                    Utils.unlock_all(self.master, self.apply_button)
                    self.block_system_error_detect = False
            else:
                self.error_number_out_limit(prop_value)
                self.block_system_error_detect = True
                Utils.block_all_input_before_correction(self.close_button,
                                                        self.master,
                                                        self.apply_button,
                                                        self.prop_widgets[prop_value][0])

    def error_number_out_limit(self, name):
        self.logger.log("error",
                        f"Error with one value load from save ('error_number_out_limit'), Originale value put for : {name}")
        self.status_label.configure(text="Error ! This is the maximum/minimum \n value allowed", text_color="red")
        self.apply_button.configure(fg_color="red", state="disabled")

    def error_number_prompt(self):
        self.status_label.configure(text="Error ! : Valide number please ", text_color="red")
        self.apply_button.configure(fg_color="red", state="disabled")

    def reset_apply_button(self):
        self.apply_button.configure(fg_color="blue", hover_color="lightblue",
                                    state="enable")
        self.status_label.configure(text="Ready to apply changes", text_color="white")
        self.verify_all_sliders_reset()

    def verify_all_sliders_reset(self):
        if self.data_save_load:
            if self.original_value_copy == self.data_from_json_no_save:
                self.apply_button.configure(fg_color="#a569bd",
                                            hover_color="lightblue",
                                            border_color="blue",
                                            state="enable")
                self.status_label.configure(
                    text="Same as the original values \n You will get back the \n original values",
                    text_color="pink", font=("Arial", 13, "italic"))
            if self.data_from_json_no_save == self.data_from_json_save:
                self.apply_button.configure(state="disabled", fg_color="white")
                self.status_label.configure(text="")
        else:
            if self.data_from_json_no_save == self.original_value_copy:
                self.apply_button.configure(state="disabled", fg_color="white")
                self.status_label.configure(text="")

    def apply_changes(self):
        if not self.block_system_error_detect:
            if not self.data_save_load:
                print(self.data_from_json_save)
                self.apply_save_data_from_change_by_user()
            else:
                print(self.data_from_json_no_save)
                self.apply_case_save_detect()
        else:
            self.status_label.configure(text="Error detect, \n can't Apply change ", text_color="red")
            # self.change_list_ammo_mod()

    def apply_case_save_detect(self):
        if self.data_save_load:
            if self.data_from_json_no_save == self.original_value_copy:
                self.load_save_and_modification_are_same_as_original_JSON()
            else:
                self.apply_save_data_from_change_by_user()
        else:
            self.check_for_file(self.file_path.replace(".json", "_mod.json"))

    def load_save_and_modification_are_same_as_original_JSON(self):
        JsonUtils.delete_file_mod_if_exists(self.file_path)
        self.apply_button.configure(fg_color="green", hover_color="green")
        self.status_label.configure(text="All Statistics modifications have been removed.")
        self.detail_window.after(3000, lambda: WindowUtils.close_window(self.detail_window,
                                                                        self.root, self.main_instance))

    def apply_save_data_from_change_by_user(self):
        if self.original_value_copy != self.data_from_json_no_save:
            data_json_to_update = JsonUtils.load_json(self.file_path)

            for name_props_to_modify, value_modify in self.data_from_json_no_save.iterate_key_and_values():
                data_json_to_update = JsonUtils.update_json_in_new_file_multi_choice(name_props_to_modify, value_modify,
                                                                                     data_json_to_update,
                                                                                     WindowType.MEDIC)
            file_path_update = JsonUtils.save_json_as_new_file(data_json_to_update, self.file_path)

            self.check_for_file(file_path_update)
            self.change_clone_statut(file_path_update)
        else:
            self.status_label.configure(text="Error ! : no change detect, \n can't Apply ", text_color="red")

    def check_for_file(self, new_file_path, attempts=0, max_attempts=10):
        Utils.block_all_input_apply_setting(self.close_button, self.master, None)
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
