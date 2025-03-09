from operator import truediv

import customtkinter as ctk

from Entity import EnumProps, EnumAiming, EnumAmmo, ItemManager
from Entity.WindowType import WindowType


class Utils:
    def __init__(self, root):
        self.root = root

    @staticmethod
    def configure_grid(frame, rows, cols, weight):
        for r in range(rows):
            frame.grid_rowconfigure(r, weight=weight)
        for c in range(cols):
            frame.grid_columnconfigure(c, weight=weight)

    @staticmethod
    def clear_frame(frame):
        for child in frame.winfo_children():
            child.destroy()
        rows, cols = frame.grid_size()
        for i in range(cols):
            frame.grid_columnconfigure(i, weight=0)
        for j in range(rows):
            frame.grid_rowconfigure(j, weight=0)

    @staticmethod
    def clear_config_row_col(frame):
        for i in range(frame.grid_size()[1]):
            frame.grid_rowconfigure(i, weight=0)

        for j in range(frame.grid_size()[0]):
            frame.grid_columnconfigure(j, weight=0)

    @staticmethod
    def create_5x4_bottom(frame1, frame2):
        frame1.clear()
        for i in range(4):
            for y in range(5):
                button = ctk.CTkFrame(frame2, fg_color="transparent")
                button.grid(row=i, column=y, padx=5, pady=5)
                frame1.append(button)

    @staticmethod
    def create_grid_row_col_config(frames, number_row, number_column):
        for i in range(number_row):
            frames.grid_rowconfigure(i, weight=1)
        for j in range(number_column):
            frames.grid_columnconfigure(j, weight=1)

    @staticmethod
    def float_to_scaled_int(value: float):
        if isinstance(value, int):
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

    @staticmethod
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

    @staticmethod
    def lower_and_replace_space_str(name_json: str) -> str:
        return name_json.lower().replace(" ", "_")

    @staticmethod
    def replace_space_str(name_json: str) -> str:
        return name_json.replace(" ", "_")

    @staticmethod
    def transform_list_of_strings(name_list: list[str]) -> list[str]:
        return [Utils.lower_and_replace_space_str(name) for name in name_list]

    @staticmethod
    def remove_jon_extension(name_json: str) -> str:
        return name_json.rsplit('.json', 1)[0].lower()

    @staticmethod
    def remove_file_by_name(list_of_file_path_json, file_name: str):
        file_name_without_space = Utils.replace_space_str(file_name)
        removed_files = []
        i = 0
        while i < len(list_of_file_path_json):
            if list_of_file_path_json[i].endswith(f"\\{file_name_without_space}.json"):
                removed_files.append(list_of_file_path_json[i])
                del list_of_file_path_json[i]
            else:
                i += 1
        return removed_files

    @staticmethod
    def move_file_between_lists(file_path: str, file_path_list_remove: list, file_path_list_add: list):
        file_name = file_path.split("\\")[-1].replace(".json", "")

        removed_files = Utils.remove_file_by_name(file_path_list_remove, file_name)

        if removed_files and file_path not in file_path_list_add:
            file_path_list_add.append(file_path)

        return removed_files

    @staticmethod
    def transfer_file_between_lists(file_name: str,
                                    list_source: list,
                                    list_target: list):
        file_name_without_space = Utils.replace_space_str(file_name)

        i = 0
        while i < len(list_source):
            if list_source[i].endswith(f"\\{file_name_without_space}.json"):
                item_to_transfer = list_source[i]

                del list_source[i]

                list_target.append(item_to_transfer)
            else:
                i += 1

    @staticmethod
    def is_value_outside_limits_weapons(name, value):
        limits = {
            EnumProps.FIRE_RATE.label: (-30, 50),
            EnumProps.CAMERA_SNAP.label: (-30, 30),
            EnumProps.ERGONOMICS.label: (-80, 80),
        }

        if name in limits:
            min_value, max_value = limits[name]
            return value < min_value or value > max_value
        return False

    @staticmethod
    def is_value_outside_limits_aiming(name, value):
        limits = {
            EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_STANDING.label: (0.15, 2.0),
            EnumAiming.RECOIL_DAMPING.label: (0.1, 0.8),
            EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_CROUCHING.label: (0.1, 1.2),
            EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_PRONE.label: (0.1, 1.0),
            EnumAiming.RECOIL_INTENSITY_BY_POSE_STANDING.label: (0.2, 2.0),
            EnumAiming.RECOIL_INTENSITY_BY_POSE_CROUCHING.label: (0.1, 1.0),
            EnumAiming.RECOIL_INTENSITY_BY_POSE_PRONE.label: (0.1, 1.0),
            EnumAiming.RECOIL_HAND_DAMPING.label: (0.01, 0.90),
        }

        if name in limits:
            min_value, max_value = limits[name]
            return value < min_value or value > max_value
        return False

    @staticmethod
    def is_value_outside_limits_ammo(name, value):
        limits = {
            EnumAmmo.ARMOR_DAMAGE.label: (1, 500),
            EnumAmmo.DAMAGE.label: (1, 450),
            EnumAmmo.PENETRATION_POWER.label: (1, 70),
            EnumAmmo.INITIAL_SPEED.label: (100, 2000),
            EnumAmmo.STACK_MAX_SIZE.label: (1, 9999)
        }
        if name in limits:
            min_value, max_value = limits[name]
            return value <= min_value or value >= max_value
        return False

    @staticmethod
    def is_value_for_input_text(name):
        int_to_input_text = {
            EnumAmmo.ARMOR_DAMAGE.label,
            EnumAmmo.DAMAGE.label,
            EnumAmmo.PENETRATION_POWER.label,
            EnumAmmo.STACK_MAX_SIZE.label,
            EnumAmmo.INITIAL_SPEED.label,
        }
        return name in int_to_input_text

    @staticmethod
    def disable_all_buttons_recursive(frame_to_not_block, main_frame):
        for child in main_frame.winfo_children():
            if ((isinstance(child, ctk.CTkButton)
                    or isinstance(child, ctk.CTkSlider))
            and not frame_to_not_block == child):
                child.configure(state="disabled")
            elif child.winfo_children():
                Utils.disable_all_buttons_recursive(frame_to_not_block, child)

    @staticmethod
    def disable_all_widgets_recursive(frame_to_not_block, main_frame, frame_to_not_block_current_focus):
        if main_frame == frame_to_not_block_current_focus:
            return
        for child in main_frame.winfo_children():
            if child == frame_to_not_block or child == frame_to_not_block_current_focus:
                continue
            if isinstance(child, (ctk.CTkButton, ctk.CTkSlider, ctk.CTkSwitch, ctk.CTkEntry)):
                child.configure(state="disabled")

            if child.winfo_children():
                Utils.disable_all_widgets_recursive(frame_to_not_block, child, frame_to_not_block_current_focus)

    @staticmethod
    def enable_all_widgets_recursive(main_frame, frame_to_not_unlock):
        for child in main_frame.winfo_children():
            if child == frame_to_not_unlock:
                return
            if isinstance(child, (ctk.CTkButton, ctk.CTkSlider, ctk.CTkSwitch, ctk.CTkEntry)):
                child.configure(state="normal")

            if child.winfo_children():

                Utils.enable_all_widgets_recursive(child, frame_to_not_unlock)

    @staticmethod
    def unlock_all_buttons_recursive(frame, widget):
        for child in widget.winfo_children():
            if ((isinstance(child, ctk.CTkButton)
                    or isinstance(child, ctk.CTkSlider))
            and not frame == child):
                child.configure(state="normal")
            elif child.winfo_children():
                Utils.disable_all_buttons_recursive(frame, child)

    @staticmethod
    def no_all_value_are_load_from_save(value_save: ItemManager, value_change_from_load_data:ItemManager):
        return value_save != value_change_from_load_data


    @staticmethod
    def case_on_app_bol_on_file_string_transform_bool(value: bool):
        if isinstance(value, bool):
            if value:
                return  "green"
            else: return "red"
        else:
            raise KeyError(f"value '{value}' must be boolean for apply app.")

    @staticmethod
    def block_all_input_before_correction(frame, widget, apply_button, current):
        Utils.disable_all_widgets_recursive(frame, widget, current)
        apply_button.configure(fg_color="red")

    @staticmethod
    def block_all_input_apply_setting(frame, widget, current):
        Utils.disable_all_widgets_recursive(frame, widget, current)

    @staticmethod
    def unlock_all(main_frame, apply_button):
        Utils.enable_all_widgets_recursive(main_frame, apply_button)

    @staticmethod
    def is_exception_for_string_to_boolean(from_json, from_app):
        if isinstance(from_json, str) and isinstance(from_app, bool):
            return True
        else:
            return False




