import copy

import customtkinter as ctk

from Entity import Root, Item, Ammo, ItemManager, EnumAmmo
from Entity.WindowType import WindowType
from Utils import WindowUtils, JsonUtils, Utils


class AmmoMod:
    def __init__(self, master, root, detail_window, file_path, main_instance):
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
        self.data_from_json_no_save: ItemManager = ItemManager(EnumAmmo)
        self.data_from_json_mod_save_user: ItemManager = ItemManager(EnumAmmo)
        self.lambda_save_from_user_vs_originale: ItemManager = ItemManager(EnumAmmo)
        self.erreur_list_need_to_resolve = []
        self.json_mod_user_save_exist = False

        self.rootJSON = self.load_data()
        self.original_value_before_change_by_frame_or_local_save = copy.deepcopy(self.data_from_json_no_save)

        self.param_main_root()
        self.create_frame_left()
        self.create_frame_right()

        self.prop_widgets = {}
        self.apply_json_data_to_slider()
        print(self.rootJSON.item.props.TracerColor)

        if self.json_mod_user_save_exist:
            self.apply_save_file_mod_user_change()

    def apply_save_file_mod_user_change(self):
        for name, value in self.data_from_json_mod_save_user.iterate_key_and_values():
            if not name == EnumAmmo.CALIBER.label:
                if name not in self.prop_widgets:
                    print(f"Avertissement : '{name}' n'existe pas dans prop_widgets.")
                    continue
                widget_tuple = self.prop_widgets[name]
                # Switch
                if isinstance(widget_tuple[0], ctk.CTkSwitch):
                    self.update_switch(name, value, True)
                # Entry
                elif isinstance(widget_tuple[0], ctk.CTkEntry):
                    try:
                        int_input_text = int(value)
                    except ValueError:
                        self.error_number_prompt()
                        return
                    if isinstance(int_input_text, int):
                        if not Utils.is_value_outside_limits_ammo(name, int_input_text):
                            self.data_from_json_no_save.update_from_props_json(name, int_input_text)
                            entry, entry_label = widget_tuple
                            entry.delete(0, 'end')
                            entry.insert(0, str(value))
                            entry_label.configure(text=str(value))
                        else:
                            # error with data load from save originale value rescue
                            self.error_number_out_limit(name)
                            entry, entry_label = widget_tuple
                            entry.delete(0, 'end')
                            original_value = self.data_from_json_no_save.get_value(name)
                            entry.insert(0, str(original_value))
                            entry_label.configure(text=str(original_value))


        if Utils.no_all_value_are_load_from_save(self.data_from_json_no_save, self.data_from_json_mod_save_user):
            self.apply_button.configure(fg_color="blue", hover_color="lightblue", border_color="red",
                                        state="enable")
            self.status_label.configure(text="Ready to apply changes")
        else:
            self.apply_button.configure(state="disabled", fg_color="white")
            self.status_label.configure(text="")
        self.status_label.configure(text="Existing data has been found and loaded")

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

    def load_data(self):
        if JsonUtils.file_mod_exist(self.file_path):
            self.load_old_modification_from_user()

        root: Root = self.load_originale_value()
        self.lambda_save_from_user_vs_originale = self.data_from_json_mod_save_user.lambda_value(
            self.data_from_json_no_save)

        return root

    def generate_information_from_weapon(self):
        title_label = ctk.CTkLabel(self.left_main,
                                   text="You have chosen :",
                                   font=("Arial", 18, "bold"))
        title_label.pack(side="top",
                         anchor="center")
        name = ctk.CTkButton(self.left_main,
                             text=self.rootJSON.locale.Name,
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

    def apply_json_data_to_slider(self):
        self.generate_information_from_weapon()
        row = 0

        for prop_value, value in self.data_from_json_no_save.iterate_key_and_values():
            prop_value: EnumAmmo
            if isinstance(value, (int, float, bool)):
                self.right_main.grid_rowconfigure(row, weight=1)

                label = ctk.CTkLabel(self.right_main, text=f"{EnumAmmo.get_code_by_label(prop_value)}:")
                label.grid(row=row, column=0, sticky=ctk.W, padx=10)

                if isinstance(value, bool):
                    self.switch_button(value, row, prop_value)

                elif isinstance(value, int):
                    if Utils.is_value_for_input_text(prop_value):
                        self.entry_input(value, row, prop_value)

                elif isinstance(value, float):
                    print(" Aucun slider float implémenté.")

                row += 1

        self.apply_button = ctk.CTkButton(
            self.right_main,
            text="Apply",
            command=self.apply_changes,
            state="disabled",
            fg_color="white"
        )
        self.apply_button.grid(row=row, column=1, sticky="nsew")
        self.status_label = ctk.CTkLabel(self.right_main, text="")
        self.status_label.grid(row=row + 1, column=1, sticky="nsew")

    def switch_button(self, value, row, prop_value: EnumAmmo):
        switch_var = ctk.BooleanVar(value=value)
        switch = ctk.CTkSwitch(
            self.right_main,
            text="",
            variable=switch_var,
            width=50,
            command=lambda pname=prop_value: self.update_switch(pname, switch_var.get(), False)
        )
        switch.grid(row=row, column=1, padx=5, pady=5, sticky="nsew")
        text_label: str
        if not prop_value == EnumAmmo.TRACERCOLOR.label:
            text_label = "Yes" if value else "No"
        else:
            text_label = "Green" if value else "Red"
        switch_label = ctk.CTkLabel(
            self.right_main,
            text=text_label,
            font=("Arial", 15, "bold"), )
        switch_label.grid(row=row, column=2, padx=10, pady=5, sticky="w")
        self.prop_widgets[prop_value] = (switch, switch_var, switch_label)
        return switch, switch_label

    def update_switch(self, name, value, from_save):
        switch, switch_var, label = self.prop_widgets[name]
        if name == EnumAmmo.TRACERCOLOR.label:
            label.configure(text="Green" if value else "Red")
        else:
            label.configure(text="Yes" if value else "No")
        switch_var.set(value)
        switch.deselect() if not value else switch.select()

        self.data_from_json_no_save.update_from_props_json(name, value)
        if not from_save:
            self.reset_apply_button()

    def entry_input(self, value, row, prop_value: EnumAmmo):
        entry = ctk.CTkEntry(
            self.right_main,
            placeholder_text="Enter value...",
            width=70,
            font=("Arial", 14, "bold"),
            justify="center"
        )
        entry.bind("<KeyRelease>", lambda event: self.get_entry_value(event, prop_value))
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

    def get_entry_value(self, event, prop_value):
        input_text = self.prop_widgets[prop_value][0].get()
        int_input_text: int
        try:
            int_input_text = int(input_text)
        except ValueError:
            self.error_number_prompt()
            print("Error : Valide nombre please.")
            self.block_system_error_detect = True
            Utils.block_all_input_before_correction(self.close_button,
                                                    self.master,
                                                    self.apply_button,
                                                    self.prop_widgets[prop_value][0])
            return
        if isinstance(int_input_text, int):
            if not Utils.is_value_outside_limits_ammo(prop_value, int_input_text):
                self.reset_apply_button()
                self.data_from_json_no_save.update_from_props_json(prop_value, int_input_text)
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

    def reset_entry(self, pname, entry):
        original_value = self.rootJSON.item.props.get_value_by_label(pname)
        entry = self.prop_widgets[pname][0]
        self.prop_widgets[pname][0].delete(0, 'end')
        entry.insert(0, str(original_value))
        self.data_from_json_no_save.update_from_props_json(pname, original_value)
        self.reset_apply_button()
        self.verify_all_sliders_reset()

    def reset_apply_button(self):
        self.apply_button.configure(fg_color="blue", hover_color="lightblue",
                                    state="enable")
        self.status_label.configure(text="Ready to apply changes", text_color="black")
        self.verify_all_sliders_reset()

    def verify_all_sliders_reset(self):
        if self.json_mod_user_save_exist:
            if self.original_value_before_change_by_frame_or_local_save == self.data_from_json_no_save:
                self.apply_button.configure(fg_color="#a569bd",
                                            hover_color="lightblue",
                                            border_color="blue",
                                            state="enable")
                self.status_label.configure(
                    text="Same as the original values \n You will get back the \n original values",
                    text_color="pink", font=("Arial", 13, "italic"))
                self.reset_after_load_save_and_value_reset = True
        else:
            if self.original_value_before_change_by_frame_or_local_save == self.data_from_json_no_save:
                self.apply_button.configure(state="disabled", fg_color="white")
                self.status_label.configure(text="")

    @staticmethod
    def create_item_manager_from_json(data, item_manager: ItemManager, wt: WindowType):
        root: Root = Root.from_data(data, wt)
        item: Item = root.item
        ammo_props: Ammo = item.props
        for key, (numerical_value, code) in vars(ammo_props).items():
            item_manager.update_from_props_json(code, numerical_value)

        return root

    def load_originale_value(self):
        data = JsonUtils.load_json(self.file_path)
        root: Root = self.create_item_manager_from_json(data, self.data_from_json_no_save, WindowType.AMMO)
        self.jsonFile = data
        return root

    def load_old_modification_from_user(self):
        self.json_mod_user_save_exist = True
        root_mod: Root

        data_from_mod_file = JsonUtils.return_json_mod(self.file_path)
        root_mod = self.create_item_manager_from_json(data_from_mod_file,
                                                      self.data_from_json_mod_save_user,
                                                      WindowType.AMMO)

    def apply_changes(self):
        if not self.block_system_error_detect:
            if not self.json_mod_user_save_exist:
                self.apply_save_data_from_change_by_user()
            else:
                self.apply_case_save_detect()
        else:
            self.status_label.configure(text="Error detect, \n can't Apply change ", text_color="red")

    def apply_save_data_from_change_by_user(self):
        if self.original_value_before_change_by_frame_or_local_save != self.data_from_json_no_save:
            data_json_to_update = JsonUtils.load_json(self.file_path)

            for name_props_to_modify, value_modify in self.data_from_json_no_save.iterate_key_and_values():
                print(f"valeur a changer : {name_props_to_modify}, {value_modify}")
                data_json_to_update = JsonUtils.update_json_in_new_file_weapon(name_props_to_modify, value_modify,
                                                                               data_json_to_update, WindowType.AMMO)
            file_path_update = JsonUtils.save_json_as_new_file(data_json_to_update, self.file_path)
            self.check_for_file(file_path_update)
        else:
            self.status_label.configure(text="Error ! : no change detect, \n can't Apply ", text_color="red")

    def apply_case_save_detect(self):
        if self.data_from_json_no_save != self.data_from_json_mod_save_user:
            if self.data_from_json_no_save == self.original_value_before_change_by_frame_or_local_save:
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

    def error_number_prompt(self):
        self.status_label.configure(text="Error ! : Valide number please ", text_color="red")
        self.apply_button.configure(fg_color="red", state="disabled")

    def error_number_out_limit(self, name):
        print(f"Error with one value load from save ('error_number_out_limit'), Originale value put for : {name}")
        self.status_label.configure(text="Error ! This is the maximum/minimum \n value allowed", text_color="red")
        self.apply_button.configure(fg_color="red", state="disabled")
