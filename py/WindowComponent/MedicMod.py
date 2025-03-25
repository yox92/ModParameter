

import customtkinter as ctk

from Entity import Logger, Root, Item, Medic, WindowType, Locale
from Entity.EffectDamage import EffectDamage
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
        self.window_protocol = WindowUtils.window_protocol(self.detail_window,
                                                           self.detail_window,
                                                           self.root, self.main_instance)
        self.root_item: Root = self.load_data_root()
        self.data_from_json_no_save: Medic = self.load_data_medic()
        self.data_from_json_save: Medic = self.load_data_save()
        self.param_main_root()
        self.create_frame_left()
        self.create_frame_right()

        self.prop_widgets = {}
        self.run()


    def load_data_medic(self):
        data = JsonUtils.load_json_Weapon_Ammo_Medic(self.file_path)
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
            root: Root = Root.from_data(data_save, WindowType.MEDIC)
            item: Item = root.item
            medic: Medic = item.props
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
                             text=self.root_item.locale.Name,
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

    def run(self):
        self.generate_information_from_weapon()
        if self.data_save_load:
            medic : Medic = self.data_from_json_save
        else:
            medic : Medic = self.data_from_json_no_save
        row = 0
        for enum_field in EnumMedic:
            label_name = enum_field.label
            value = getattr(medic, label_name, None)
            if label_name != EnumMedic.EFFECTS_DAMAGE.label:
                if isinstance(value, tuple) and len(value) == 2:
                    raw_value = value[0]
                else:
                    raw_value = value

                self.right_main.grid_rowconfigure(row, weight=1)

                label = ctk.CTkLabel(self.right_main, text=f"{EnumMedic.get_code_by_label(label_name)}:")
                label.grid(row=row, column=0, sticky=ctk.W, padx=10)

                label.configure(font=("Arial", 14, "bold"), text_color="Peru")
                    #
                    # if isinstance(value, bool):
                    #     self.switch_button(value, row, prop_value)

                if isinstance(raw_value, int):
                    self.entry_input(raw_value, row, label_name)

                    row += 1

                # self.apply_button = ctk.CTkButton(
                # self.right_main,
                # text="Apply",
                # command=self.apply_changes,
                # state="disabled",
                # fg_color="white"
                # )
                # self.apply_button.grid(row=row, column=1, sticky="nsew")
                # self.status_label = ctk.CTkLabel(self.right_main, text="")
                # self.status_label.grid(row=row + 1, column=1, sticky="nsew")
        self.right_main.grid_rowconfigure(row +1, weight=1)
        self.title_effect = ctk.CTkLabel(self.right_main,
                                   text="effect :",
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

            lbl_widget = ctk.CTkLabel(self.effect_edit_frame, text=label)
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
            from tkinter import messagebox

            for prop, entry in self.effect_entries.items():
                text = entry.get().strip()

                if text == "":
                    continue

                try:
                    val = int(text)
                except ValueError:
                    messagebox.showerror("Erreur", f"Le champ '{prop}' doit être un nombre.")
                    return

                if Utils.is_value_outside_limits_effect(prop, val):
                    messagebox.showerror("Erreur", f"La valeur pour '{prop}' est hors limites autorisées.")
                    return

                if Utils.is_value_outside_hpMax(self.root_item.item.props.MaxHpResource[0], val):
                    messagebox.showerror("Erreur", f"Ce n'est pas possible de retirer '{val}' de point a un objet qui a : {self.root_item.item.props.MaxHpResource[0]} de ressource maximal")
                    return
                setattr(effect, prop, val)

            self.data_from_json_no_save.effects_damage.add_effect(effect_name, effect)

            self.effect_frame.destroy()
            self.display_effect_buttons(row - 1)
            self.effect_edit_frame.destroy()

        def delete_effect():
            if effect_name in self.data_from_json_no_save.effects_damage.effects:
                del self.data_from_json_no_save.effects_damage.effects[effect_name]

            self.effect_frame.destroy()
            self.display_effect_buttons(row - 1)
            self.effect_edit_frame.destroy()

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

    def get_entry_value(self, event, prop_value, value):
        input_text = self.prop_widgets[prop_value][0].get()
        try:
            int_input_text = int(input_text)
        except ValueError:
            # self.error_number_prompt()
            self.logger.log("warning", "Number please ...")
            self.block_system_error_detect = True
            Utils.block_all_input_before_correction(self.close_button,
                                                    self.master,
                                                    self.apply_button,
                                                    self.prop_widgets[prop_value][0])
            return
        if isinstance(int_input_text, (int,float)):
            if not Utils.is_value_outside_limits_ammo(prop_value, int_input_text):
                # self.reset_apply_button()
                # self.data_from_json_no_save.update_from_props_json(prop_value, int_input_text)
                if self.block_system_error_detect:
                    Utils.unlock_all(self.master, self.apply_button)
                    self.block_system_error_detect = False
            else:
                # self.error_number_out_limit(prop_value)
                self.block_system_error_detect = True
                # Utils.block_all_input_before_correction(self.close_button,
                #                                         self.master,
                #                                         self.apply_button,
                #                                         self.prop_widgets[prop_value][0])

    def apply_changes(self):
        if not self.block_system_error_detect:
            if not self.data_save_load:
                print(self.data_save_load)
                # self.apply_save_data_from_change_by_user()
            else:
                print("")
                # self.apply_case_save_detect()
        else:
            self.status_label.configure(text="Error detect, \n can't Apply change ", text_color="red")
            # self.change_list_ammo_mod()
