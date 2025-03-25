import customtkinter as ctk

from Entity import EnumProps, EnumAiming, EnumAmmo, ItemManager
from Entity.EnumEffect import EnumEffect
from Entity.EnumEffectName import EnumEffectName
from Entity.EnumMedic import EnumMedic
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
    def create_5x5_bottom(frame1, frame2, choice_window: WindowType):
        frame1.clear()
        total_buttons: int
        if choice_window == WindowType.AMMO:
            total_buttons = 24
        else:
            total_buttons = 22
        count = 0
        for i in range(5):
            for y in range(5):
                if count >= total_buttons:
                    return
                button = ctk.CTkFrame(frame2, fg_color="transparent")
                button.grid(row=i, column=y, padx=5, pady=5)
                frame1.append(button)
                count += 1
    @staticmethod
    def create_1x4_bottom(frame1, frame2):
        frame1.clear()
        total_buttons: int
        total_buttons = 4
        count = 0
        for y in range(4):
                if count >= total_buttons:
                    return
                button = ctk.CTkFrame(frame2, fg_color="transparent")
                button.grid(row=0, column=y, padx=5, pady=5)
                frame1.append(button)
                count += 1

    @staticmethod
    def create_grid_row_col_config(frames, number_row, number_column):
        for i in range(number_row):
            frames.grid_rowconfigure(i, weight=1)
        for j in range(number_column):
            frames.grid_columnconfigure(j, weight=1)

    @staticmethod
    def create_grid_row_col_config_limite(frames, number_row, number_column):
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
            EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_CROUCHING.label: (0.6, 1.0),
            EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_PRONE.label: (0.5, 1.0),
            EnumAiming.RECOIL_INTENSITY_BY_POSE_STANDING.label: (0.1, 1.0),
            EnumAiming.RECOIL_INTENSITY_BY_POSE_CROUCHING.label: (0.5, 1.0),
            EnumAiming.RECOIL_INTENSITY_BY_POSE_PRONE.label: (0.4, 1.0),
            EnumAiming.RECOIL_HAND_DAMPING.label: (0.01, 0.90),
            EnumAiming.AIM_PROCEDURAL_INTENSITY.label: (0.1, 0.7),
        }

        if name in limits:
            min_value, max_value = limits[name]
            return value < min_value or value > max_value
        return False

    @staticmethod
    def is_value_outside_limits_effect(prop: int, value: int) -> bool:
        limits = {
            EnumMedic.STACKMAXSIZE: (-1, 100),
            EnumEffect.DURATION: (-1, 2000),
            EnumEffect.FADEOUT: (-1, 100),
            EnumEffect.COST: (-1, 250),
            EnumEffect.HEALTHPENALTYMAX: (2, 101),
            EnumEffect.HEALTHPENALTYMIN: (1, 100)
        }

        if prop in limits:
            min_val, max_val = limits[prop]
            return value < min_val or value > max_val

    @staticmethod
    def is_value_outside_hpMax(hp_max: int, value: int) -> bool:
        return value <  hp_max

    @staticmethod
    def select_effect_value(effect_name: str) -> list[EnumEffect]:
        excluded_fields = set()

        if effect_name != "DestroyedPart":
            excluded_fields.update({EnumEffect.HEALTHPENALTYMIN, EnumEffect.HEALTHPENALTYMAX})

        if (effect_name == EnumEffectName.DESTROYED_PART.value
            or effect_name == EnumEffectName.HEAVY_BLEEDING.value
            or effect_name == EnumEffectName.LIGHT_BLEEDING.value
            or effect_name == EnumEffectName.FRACTURE.value
        ):
            excluded_fields.add(EnumEffect.DURATION)

        if effect_name == EnumEffectName.PAIN.value or effect_name == EnumEffectName.INTOXICATION.value:
            excluded_fields.add(EnumEffect.COST)

        # Retourne tous les champs sauf ceux exclus
        return [field for field in EnumEffect if field not in excluded_fields]


        return False
    @staticmethod
    def is_value_outside_limits_ammo(name, value):
        limits = {
            EnumAmmo.ARMOR_DAMAGE.label: (0, 500),
            EnumAmmo.DAMAGE.label: (0, 450),
            EnumAmmo.PENETRATION_POWER.label: (-1, 81),
            EnumAmmo.INITIAL_SPEED.label: (70, 2000),
            EnumAmmo.BULLET_MASSGRAM.label: (7, 28000),
            EnumAmmo.STACK_MAX_SIZE.label: (-1, 9999),
            EnumAmmo.BALLISTIC_COEFICIENT.label: (10, 624),
            EnumAmmo.PROJECTILE_COUNT.label: (-1, 101),
            EnumAmmo.AMMO_ACCR.label: (-201, 501),
            EnumAmmo.AMMO_REC.label: (-201, 101),
            EnumAmmo.EXPLOSIONSTRENGTH.label: (-1, 101),
            EnumAmmo.FUZEARMTIMESEC.label: (0, 301),
            EnumAmmo.MAXEXPLOSIONDISTANCE.label: (-1, 11),
            EnumAmmo.PRICEFACTOR.label: (0.009, 101)
        }
        if name in limits:
            min_value, max_value = limits[name]
            return value <= min_value or value >= max_value
        return False

    @staticmethod
    def is_value_outside_limits_weapon(name, value):
        limits = {
            EnumProps.PRICEFACTOR.label: (0.009, 101)
        }
        if name in limits:
            min_value, max_value = limits[name]
            return value <= min_value or value >= max_value
        return False

    @staticmethod
    def is_value_for_input_text(name):
        x = {
            EnumAmmo.ARMOR_DAMAGE.label,
            EnumAmmo.DAMAGE.label,
            EnumAmmo.PENETRATION_POWER.label,
            EnumAmmo.STACK_MAX_SIZE.label,
            EnumAmmo.INITIAL_SPEED.label,
            EnumAmmo.BALLISTIC_COEFICIENT.label,
            EnumAmmo.AMMO_REC.label,
            EnumAmmo.AMMO_ACCR.label,
            EnumAmmo.BULLET_MASSGRAM.label,
            EnumAmmo.PROJECTILE_COUNT.label,
            EnumAmmo.EXPLOSIONSTRENGTH.label,
            EnumAmmo.FUZEARMTIMESEC.label,
            EnumAmmo.MAXEXPLOSIONDISTANCE.label
        }
        return name in x

    @staticmethod
    def is_value_under_one(name):
        x = {
            EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_STANDING.label,
            EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_CROUCHING.label,
            EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_PRONE.label,
            EnumAiming.RECOIL_DAMPING.label,
            EnumAiming.RECOIL_HAND_DAMPING.label,
            EnumAiming.RECOIL_INTENSITY_BY_POSE_PRONE.label,
            EnumAiming.RECOIL_INTENSITY_BY_POSE_STANDING.label,
            EnumAiming.RECOIL_INTENSITY_BY_POSE_CROUCHING.label,
            EnumAiming.AIM_PROCEDURAL_INTENSITY.label,
            EnumAiming.STAMINA_DRAIN.label,
            EnumAiming.STAMINA_SPRINT.label
        }
        return name in x

    @staticmethod
    def pmc_color_olive(name):
        x = {
            EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_CROUCHING.label,
            EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_PRONE.label,
            EnumAiming.RECOIL_INTENSITY_BY_POSE_PRONE.label,
            EnumAiming.RECOIL_INTENSITY_BY_POSE_CROUCHING.label,
        }
        return name in x

    @staticmethod
    def pmc_color_yellow(name):
        x = {
            EnumAiming.AIM_PUNCH_MAGNITUDE.label,
            EnumAiming.RECOIL_DAMPING.label,
            EnumAiming.RECOIL_HAND_DAMPING.label
        }
        return name in x

    @staticmethod
    def pmc_color_orange(name):
        x = {
            EnumAiming.PROCEDURAL_INTENSITY_BY_POSE_STANDING.label,
            EnumAiming.RECOIL_INTENSITY_BY_POSE_STANDING.label,
            EnumAiming.AIM_PROCEDURAL_INTENSITY.label
        }
        return name in x

    @staticmethod
    def pmc_color_green(name):
        x = {
            EnumAiming.STAMINA_SPRINT.label,
            EnumAiming.STAMINA_JUMP.label,
            EnumAiming.STAMINA_STANDUP.label
        }
        return name in x

    @staticmethod
    def pmc_color_cyan(name):
        x = {
            EnumAiming.STAMINA_DRAIN.label
        }
        return name in x

    @staticmethod
    def pmc_color_lime(name):
        x = {
            EnumAiming.STAMINA_RESTORATION.label
        }
        return name in x

    @staticmethod
    def is_value_for_upper(name):
        x = {
            EnumAiming.STAMINA_RESTORATION.label
        }
        return name in x

    @staticmethod
    def is_value_for_under_big_number(name):
        x = {
            EnumAiming.STAMINA_STANDUP.label,
            EnumAiming.STAMINA_JUMP.label,
            EnumAiming.AIM_PUNCH_MAGNITUDE.label
        }
        return name in x

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
    def no_all_value_are_load_from_save(value_save: ItemManager, value_change_from_load_data: ItemManager):
        return value_save != value_change_from_load_data

    @staticmethod
    def case_on_app_bol_on_file_string_transform_bool(value: bool):
        if isinstance(value, bool):
            if value:
                return "tracerGreen"
            else:
                return "red"
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

    @staticmethod
    def apply_tracer_to_ammo_with_mod_exist_already(color):
        from Utils.JsonUtils import JsonUtils
        list_path_ammo_mod_with_mod_at_the_end = JsonUtils.get_file_path_json_all_mod_ammo(False)
        for file_path in list_path_ammo_mod_with_mod_at_the_end:
            data_json_to_modify = JsonUtils.load_json(file_path)
            data_json_to_modify = Utils.modify_json_value(EnumAmmo.TRACER.label,
                                                          True,
                                                          data_json_to_modify)
            data_json_to_modify = Utils.modify_json_value(EnumAmmo.TRACERCOLOR.label,
                                                          color,
                                                          data_json_to_modify)
            file_path = file_path.replace("_mod.json", ".json")
            JsonUtils.save_json_as_new_file(data_json_to_modify, file_path)


    @staticmethod
    def modify_json_value(attribut, value_to_apply, data_json_to_modify):
        from Utils.JsonUtils import JsonUtils
        return JsonUtils.update_json_in_new_file_multi_choice(attribut,
                                                              value_to_apply,
                                                              data_json_to_modify,
                                                              WindowType.AMMO)
    @staticmethod
    def case_fire_rate(adjusted_value, name):
        if name == EnumProps.FIRE_RATE.label:
            if adjusted_value < 300:
                adjusted_value = round(adjusted_value / 10) * 10
            else:
                adjusted_value = round(adjusted_value / 50) * 50

        return adjusted_value