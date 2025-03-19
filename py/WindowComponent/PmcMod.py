import copy

import customtkinter as ctk

from Entity import Aiming, Logger
from Entity.WindowType import WindowType
from Utils import JsonUtils, Utils, WindowUtils
from Entity.AimingManager import EnumAiming, AimingManager

DETAIL_WINDOW = "800x700"


class PmcMod:
    def __init__(self, master, root, detail_window, main_instance):
        self.logger = Logger()
        self.status_label = None
        self.apply_button = None
        self.save_pmc_exist: bool = False
        self.reset_after_load_save_and_value_reset: bool = False
        self.close_button = None
        self.master = master
        self.root = root
        self.detail_window = detail_window
        self.main_instance = main_instance
        self.window_protocol = WindowUtils.window_protocol(self.detail_window,
                                                           self.detail_window,
                                                           self.root, self.main_instance)
        self.aiming_manager_pmc_save: None
        self.aiming_manager_pmc: AimingManager = AimingManager()
        self.json_save_pmc_file_path: str = ''
        self.json_pmc_file_path: str = ''
        self.right_main = None
        self.prop_widgets = {}
        self.master.geometry(DETAIL_WINDOW)
        self.master.configure(bg="#242424")
        self.param_main_root()
        self.create_frame_right()
        self.load_data()
        self.aiming_manager_pmc_originale_value: AimingManager = copy.deepcopy((self.aiming_manager_pmc))
        self.run()
        if self.save_pmc_exist:
            self.apply_save_file_mod_user_change()

    def apply_save_file_mod_user_change(self):
        for key, value in self.aiming_manager_pmc_save.iterate_key_and_values():
            slider, label = self.prop_widgets[key]
            self.update_props_value(key, value, self.aiming_manager_pmc_originale_value.get_value(key))

            slider.set(value)
        self.aiming_manager_pmc = self.aiming_manager_pmc_save
        self.status_label.configure(text="Existing data has been found and loaded")

    def param_main_root(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.under_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        self.under_frame.grid(row=1, column=0, sticky="nsew")
        self.under_frame.rowconfigure(0, weight=1)
        self.under_frame.columnconfigure(0, weight=1)
        self.under_frame.columnconfigure(1, weight=1)
        self.under_frame.columnconfigure(2, weight=20)
        self.close_button = ctk.CTkButton(self.under_frame,
                                          text="Close",
                                          command=lambda:
                                          WindowUtils.close_window(self.detail_window,
                                                                   self.root, self.main_instance))
        self.close_button.grid(row=0, column=2)
        self.note_label = ctk.CTkLabel(self.under_frame,
                                   text="* 0 = Infinite :",
                                    text_color="green",
                                   font=("Arial", 11, "bold"))
        self.note_label.grid(row=0, column=0)
        self.note_label2 = ctk.CTkLabel(self.under_frame,
                                   text="* 0 = Remove Effect :",
                                    text_color="orange",
                                   font=("Arial", 11, "bold"))
        self.note_label2.grid(row=0, column=1)

    def create_frame_right(self):
        self.right_main = ctk.CTkFrame(self.master, fg_color="transparent")
        self.right_main.grid(row=0, column=0, sticky="nsew")
        self.right_main.grid_columnconfigure(0, weight=1)  # props description
        self.right_main.grid_columnconfigure(1, weight=1)  # slider
        self.right_main.grid_columnconfigure(2, weight=1)  # value
        self.right_main.grid_columnconfigure(3, weight=1)  # reset button

    def load_data(self):
        self.json_pmc_file_path = JsonUtils.get_file_path_json_pmc()
        self.json_save_pmc_file_path = JsonUtils.get_file_path_json_pmc_save()

        aiming: Aiming

        if self.json_save_pmc_file_path:
            self.load_save_data()
        aiming = self.load_json_file(self.json_pmc_file_path)

        for key, (numerical_value, code) in vars(aiming).items():
            self.aiming_manager_pmc.update_from_props_json(code, numerical_value)

    def load_json_file(self, file_path):
        data = JsonUtils.load_json(file_path)
        aiming: Aiming = Aiming.from_data(data)
        return aiming

    def load_save_data(self):
        aiming_save: Aiming
        self.save_pmc_exist = True
        aiming_save = self.load_json_file(self.json_save_pmc_file_path)
        self.aiming_manager_pmc_save = AimingManager()
        for key, (numerical_value, code) in vars(aiming_save).items():
            self.aiming_manager_pmc_save.update_from_props_json(code, numerical_value)

    def run(self):
        row = 0
        for row, (props, number) in enumerate(self.aiming_manager_pmc.iterate_key_and_values()):
            self.right_main.grid_rowconfigure(row, weight=1)  # apply

            label = ctk.CTkLabel(self.right_main,
                                 text=f"{EnumAiming.get_code_by_label(props)}:",
                                 height=20)
            label.grid(row=row,
                       column=0,
                       sticky="ew",
                       pady=10)
            if Utils.pmc_color_orange(props):
                label.configure(font=("Arial", 12, "bold"), text_color="orange")
            elif Utils.pmc_color_olive(props):
                label.configure(font=("Arial", 9, "bold"), text_color="darkOliveGreen")
            elif Utils.pmc_color_yellow(props):
                label.configure(font=("Arial", 9, "bold"), text_color="Peru")
            elif Utils.pmc_color_green(props):
                label.configure(font=("Arial", 12, "bold"), text_color="green")
            elif Utils.pmc_color_cyan(props):
                label.configure(font=("Arial", 12, "bold"), text_color="DodgerBlue")
            elif Utils.pmc_color_lime(props):
                label.configure(font=("Arial", 12, "bold"), text_color="Lime")

            if Utils.is_value_under_one(props):
                percent_label, slider = self.create_slider_down_one_down_value(row, props, number)
            elif Utils.is_value_for_upper(props):
                percent_label, slider = self.create_slider_upper_value(row, props, number)
            elif Utils.is_value_for_under_big_number(props):
                percent_label, slider = self.create_slider_up_two(row, props, number)
            else:
                percent_label, slider = self.create_slider_down_one_down_value(row, props, number)

            self.prop_widgets[props] = (slider, percent_label)

            WindowUtils.frame_color_risky_range(props, number, percent_label)
            row += 1

        self.apply_button = ctk.CTkButton(self.right_main, text="Apply",
                                          command=self.apply_changes,
                                          state="disabled",
                                          fg_color="white")
        self.apply_button.grid(row=row, column=1, sticky="nsew")
        self.status_label = ctk.CTkLabel(self.right_main, text="")
        self.status_label.grid(row=row + 1, column=1, sticky="nsew")

    def create_slider_down_one_down_value(self, row, props, number):
        if props == EnumAiming.STAMINA_SPRINT.label:
            slider = ctk.CTkSlider(
                self.right_main,
                from_=0,
                to=4,
                command=lambda lambda_value, pname=props:
                self.update_props_value(pname, lambda_value, number))
        else:
            slider = ctk.CTkSlider(
                self.right_main,
                from_=0,
                to=1.0,
                command=lambda lambda_value, pname=props:
                self.update_props_value(pname, lambda_value, number))

        slider.grid(row=row, column=1, sticky=ctk.W, padx=10)
        slider.set(number)
        percentage_change = ((number / number) - 1) * 100 if number != 0 else 0

        if props == EnumAiming.RECOIL_HAND_DAMPING.label:
            percent_label = ctk.CTkLabel(self.right_main, text=f"{number:.2f} ({percentage_change:+.0f}%)",
                                         font=("Arial", 15, "bold"))
        else:
            percent_label = ctk.CTkLabel(self.right_main, text=f"{number:.1f} ({percentage_change:+.0f}%)",
                                         font=("Arial", 15, "bold"))
        percent_label.grid(row=row, column=2, sticky=ctk.W, padx=10)

        reset_button = ctk.CTkButton(self.right_main, text="Reset",
                                     command=lambda pname=props:
                                     self.reset_slider(pname),
                                     width=10)
        reset_button.grid(row=row, column=3, sticky=ctk.W, padx=10)

        return percent_label, slider

    def create_slider_upper_value(self, row, props, number):
        slider = ctk.CTkSlider(
            self.right_main,
            from_=4,
            to=20,
            command=lambda lambda_value, pname=props:
            self.update_props_value(pname, lambda_value, number))

        slider.grid(row=row, column=1, sticky=ctk.W, padx=10)
        slider.set(number)
        percentage_change = ((number / number) - 1) * 100 if number != 0 else 0

        percent_label = ctk.CTkLabel(self.right_main, text=f"{number:.1f} ({percentage_change:+.0f}%)",
                                     font=("Arial", 15, "bold"))
        percent_label.grid(row=row, column=2, sticky=ctk.W, padx=10)

        reset_button = ctk.CTkButton(self.right_main, text="Reset",
                                     command=lambda pname=props:
                                     self.reset_slider(pname),
                                     width=10)
        reset_button.grid(row=row, column=3, sticky=ctk.W, padx=10)

        return percent_label, slider

    def create_slider_up_two(self, row, props, number):
        slider = ctk.CTkSlider(
            self.right_main,
            from_=0,
            to=14.4,
            command=lambda lambda_value, pname=props:
            self.update_props_value(pname, lambda_value, number))

        slider.set(number)
        slider.grid(row=row, column=1, sticky=ctk.W, padx=10)
        percentage_change = ((number / number) - 1) * 100 if number != 0 else 0

        percent_label = ctk.CTkLabel(self.right_main, text=f"{number:.1f} ({percentage_change:+.0f}%)",
                                     font=("Arial", 15, "bold"))
        percent_label.grid(row=row, column=2, sticky=ctk.W, padx=10)

        reset_button = ctk.CTkButton(self.right_main, text="Reset",
                                     command=lambda pname=props:
                                     self.reset_slider(pname),
                                     width=10)
        reset_button.grid(row=row, column=3, sticky=ctk.W, padx=10)

        return percent_label, slider

    def update_props_value(self, pname, lambda_value, initial_value):
        slider, percent_label = self.prop_widgets[pname]
        WindowUtils.frame_color_risky_range(pname, lambda_value, percent_label)

        percentage_change = ((lambda_value / initial_value) - 1) * 100 if initial_value != 0 else 0

        if pname == EnumAiming.RECOIL_HAND_DAMPING.label:
            percent_label.configure(text=f"{lambda_value:.2f} ({percentage_change:+.0f}%)")
            transforme_value = round(lambda_value, 2)
        else:
            percent_label.configure(text=f"{lambda_value:.1f} ({percentage_change:+.0f}%)")
            transforme_value = round(lambda_value, 1)
        if Utils.is_value_outside_limits_aiming(pname, lambda_value):
            percent_label.configure(text_color="red")
        else:
            percent_label.configure(text_color="white")
        self.aiming_manager_pmc.update_from_props_json(pname, transforme_value)
        self.reset_apply_button()

    def reset_slider(self, name):
        slider, label = self.prop_widgets[name]
        for key, value in self.aiming_manager_pmc_originale_value.iterate_key_and_values():
            if key == name:
                self.update_props_value(key, value, value)
                slider.set(value)
        self.reset_apply_button()
        self.verify_all_sliders_reset()

    def reset_apply_button(self):
        self.apply_button.configure(fg_color="blue", hover_color="lightblue", border_color="red",
                                    state="enable")
        self.status_label.configure(text="Ready to apply changes")

    def verify_all_sliders_reset(self):
        if self.save_pmc_exist:
            if self.aiming_manager_pmc_originale_value == self.aiming_manager_pmc:
                self.apply_button.configure(fg_color="#a569bd",
                                            hover_color="lightblue",
                                            border_color="blue",
                                            state="enable")
                self.status_label.configure(
                    text="Same as the original values \n You will get back the \n original values",
                    text_color="pink", font=("Arial", 13, "italic"))
                self.reset_after_load_save_and_value_reset = True
        else:
            if self.aiming_manager_pmc_originale_value == self.aiming_manager_pmc:
                self.apply_button.configure(state="disabled", fg_color="white")
                self.status_label.configure(text="")

    def apply_changes(self):
        if self.aiming_manager_pmc_originale_value != self.aiming_manager_pmc:
            data_json_to_update = JsonUtils.load_json(self.json_pmc_file_path)

            for name_props_to_modify, value_modify in self.aiming_manager_pmc.iterate_key_and_values():
                data_json_to_update = JsonUtils.update_json_in_new_file_aiming(name_props_to_modify, value_modify,
                                                                               data_json_to_update, WindowType.PMC)
            file_path_update = JsonUtils.save_json_as_new_file(data_json_to_update, self.json_pmc_file_path)
            self.check_for_file(file_path_update)
        else:
            if self.save_pmc_exist:
                JsonUtils.delete_file_mod_if_exists(self.json_pmc_file_path)
            self.apply_button.configure(fg_color="green", hover_color="green")
            self.status_label.configure(text="All PMC modifications have been removed.")
            self.detail_window.after(3000, lambda: WindowUtils.close_window(self.detail_window,
                                                                            self.root, self.main_instance))

    def check_for_file(self, new_file_path, attempts=0, max_attempts=10):
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

    def lower_two_value(self):
        return EnumAiming.AIM_PUNCH_MAGNITUDE.label
