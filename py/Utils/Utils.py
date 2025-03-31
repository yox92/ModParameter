import copy

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from Entity import EnumProps, EnumAiming, EnumAmmo, ItemManager
from Entity.Bag import Bag
from Entity.Buff import Buff
from Entity.BuffGroup import BuffGroup
from Entity.EnumBagSize import EnumBagSize
from Entity.EnumBuffTypeSkillName import EnumBuffTypeSkillName
from Entity.EnumEffect import EnumEffect
from Entity.EnumEffectName import EnumEffectName
from Entity.EnumMagSize import EnumMagSize
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
        elif choice_window == WindowType.BUFF:
            total_buttons = 21
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
    def create_1x5_bottom(frame1, frame2):
        frame1.clear()
        total_buttons: int
        total_buttons = 5
        count = 0
        for y in range(5):
            if count >= total_buttons:
                return
            button = ctk.CTkFrame(frame2, fg_color="transparent")
            button.grid(row=0, column=y, padx=5, pady=5)
            frame1.append(button)
            count += 1

    @staticmethod
    def create_1x2_bottom(frame1, frame2):
        frame1.clear()
        total_buttons: int
        total_buttons = 2
        count = 0
        for y in range(2):
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
            EnumEffect.DURATION: (-1, 2001),
            EnumEffect.FADEOUT: (-1, 101),
            EnumEffect.COST: (-1, 251),
            EnumEffect.HEALTHPENALTYMAX: (2, 101),
            EnumEffect.HEALTHPENALTYMIN: (1, 100)
        }

        if prop in limits:
            min_val, max_val = limits[prop]
            return value < min_val or value > max_val

    @staticmethod
    def is_value_outside_hpMax(hp_max: int, value: int, prop: str) -> bool:
        return value > hp_max

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
    def is_value_outside_limits_medic(name, value):
        limits = {
            EnumMedic.MEDUSETIME.label: (0, 21),
            EnumMedic.HPRESOURCERATE.label: (-1, 1001),
            EnumMedic.MAXHPRESOURCE.label: (1, 10001),
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

    @staticmethod
    def enum_to_lock(parent_id, label_name):
        if label_name == EnumMedic.EFFECTS_DAMAGE.label:
            return False

        if label_name == EnumMedic.HPRESOURCERATE.label:
            return parent_id == "5448f39d4bdc2d0a728b4568"

        return True

    @staticmethod
    def switch_mag(result, switch_value):
        print(result)
        print(switch_value)

    @staticmethod
    def size_magazine(result):
        if result in (EnumMagSize.CAT_01_09.value,
                      EnumMagSize.CAT_10_19.value,
                      EnumMagSize.CAT_20_29.value):
            return "Resize 2 slots to 1 slot"
        elif result in (EnumMagSize.CAT_30_39.value,
                        EnumMagSize.CAT_40_49.value,
                        EnumMagSize.CAT_50_59.value,
                        EnumMagSize.CAT_60_69.value,
                        EnumMagSize.CAT_70_79.value,
                        EnumMagSize.CAT_80_89.value,
                        EnumMagSize.CAT_90_100.value,
                        EnumMagSize.CAT_GT_100):
            return "Resize 3 slots to 2 slots"

    @staticmethod
    def slider_start(result):
        if result == EnumMagSize.CAT_01_09.value:
            return 1
        elif result == EnumMagSize.CAT_10_19.value:
            return 10
        elif result == EnumMagSize.CAT_20_29.value:
            return 20
        elif result == EnumMagSize.CAT_30_39.value:
            return 30
        elif result == EnumMagSize.CAT_40_49.value:
            return 40
        elif result == EnumMagSize.CAT_50_59.value:
            return 50
        elif result == EnumMagSize.CAT_60_69.value:
            return 60
        elif result == EnumMagSize.CAT_70_79.value:
            return 70
        elif result == EnumMagSize.CAT_80_89.value:
            return 80
        elif result == EnumMagSize.CAT_90_100.value:
            return 90
        elif result == EnumMagSize.CAT_GT_100.value:
            return 100
        else:
            return 1

    @staticmethod
    def save_mag_values(data, result, switch_var, switch_var2, switch_var3, slider):
        from Utils.JsonUtils import JsonUtils
        data[result]["penality"] = switch_var.get()
        data[result]["resize"] = switch_var2.get()
        data[result]["fastLoad"] = switch_var3.get()
        data[result]["counts"] = int(slider.get())
        JsonUtils.save_mag_preset(data, result)

    @staticmethod
    def save_buff_values(slider, slider2, entry, name, buff):
        from Utils.JsonUtils import JsonUtils

        if JsonUtils.buff_mod_exist():
            data = JsonUtils.load_buff_mod()
        else:
            data = JsonUtils.load_buff()

        new_duration = int(slider.get())
        new_delay = int(slider2.get())
        new_value = entry.get()

        buff_group = data.get("Buffs", {}).get(name, [])

        for b in buff_group:
            if b["BuffType"] == buff.buff_type and b["SkillName"] == buff.skill_name:
                b["Duration"] = new_duration
                b["Delay"] = new_delay
                b["Value"] = new_value
                if b.get("add") is None:
                    b["change"] = True
                    continue
                if b.get("change") is None:
                    continue
                break

        JsonUtils.save_buff_mod(data)

        print(f" Buff '{buff.buff_type}' update on '{name}' et save.")

    @staticmethod
    def reset_mag(result, count, data):
        from Utils.JsonUtils import JsonUtils
        data[result]["penality"] = False
        data[result]["resize"] = False
        data[result]["fastLoad"] = False
        data[result]["counts"] = count
        JsonUtils.save_mag_preset(data, result)

    @staticmethod
    def reset_all_mag():
        from Utils.JsonUtils import JsonUtils
        data = JsonUtils.load_mag()
        for result in EnumMagSize.list_values():
            data[result]["penality"] = False
            data[result]["resize"] = False
            data[result]["fastLoad"] = False
            data[result]["counts"] =  Utils.slider_start(result)
            JsonUtils.save_mag_preset(data, result)

    @staticmethod
    def apply_bag_value(result, switch_var, switch_var2, slider):
        from Utils.JsonUtils import JsonUtils
        data = JsonUtils.load_bag(result)
        change_number = int(slider.get())
        boolean = bool(switch_var.get())
        boolean2 = bool(switch_var2.get())
        if boolean or boolean2 or change_number > 0:
            bags = []
            for ids, bag_info in data.get(result).get("ids", {}).items():
                Grids = bag_info.get("Grids", {})
                bag = Bag(
                    ids=ids,
                    name=bag_info.get("name"),
                    Grids=Grids)
                bags.append(bag)
            if change_number > 0:
                for bag in bags:
                    old_grids = {gid: grid.copy() for gid, grid in bag.Grids.items()}
                    bag.resize_backpacks(change_number)
                    bag.display_resize_info(old_grids)
                    data[result]["resize"] = True
                    data[result]["size"] = change_number
                    data[result]["ids"][bag.ids]["Grids"] = bag.Grids
            if boolean:
                data[result]["penality"] = True
            if boolean2:
                data[result]["excludedFilter"] = True
            JsonUtils.create_mod_bag(data, result)
        else:
            print("no change")

    @staticmethod
    def max_min_slider_bag(result: str):
        if EnumBagSize.from_value(result) == EnumBagSize.CAT_S:
            return 0, 300
        elif EnumBagSize.from_value(result) in (EnumBagSize.CAT_M1, EnumBagSize.CAT_M2):
            return 0, 150
        elif EnumBagSize.from_value(result) == EnumBagSize.CAT_L:
            return 0, 100
        elif EnumBagSize.from_value(result) == EnumBagSize.CAT_XL:
            return 0, 80

    @staticmethod
    def max_min_slider_mag(result: str):
        if EnumMagSize.from_value(result) in (EnumMagSize.CAT_01_09,
                                              EnumMagSize.CAT_10_19,
                                              EnumMagSize.CAT_20_29,
                                              EnumMagSize.CAT_30_39,
                                              EnumMagSize.CAT_40_49):
            return 1, 100
        elif EnumMagSize.from_value(result) in (EnumMagSize.CAT_50_59,
                                                EnumMagSize.CAT_60_69,
                                                EnumMagSize.CAT_70_79):
            return 1, 150
        elif EnumMagSize.from_value(result) in (EnumMagSize.CAT_80_89,
                                                EnumMagSize.CAT_90_100,
                                                EnumMagSize.CAT_GT_100):
            return 1, 200

    @staticmethod
    def get_buffs_by_group_name(buff_groups: list[BuffGroup], name: str) -> list[Buff]:
        for group in buff_groups:
            if group.name.value == name:
                return group.buffs
        return []

    @staticmethod
    def error_number_prompt(appender: []):
        appender[1].configure(text="Error ! : Valide number please ", text_color="red")
        appender[2].configure(fg_color="red", state="disabled")

    @staticmethod
    def is_value_outside_limits(value, min_value, max_value):
        return value > max_value or value < min_value

    @staticmethod
    def reset_buff_in_mod(name: str, buff):
        from Utils.JsonUtils import JsonUtils

        if not JsonUtils.buff_mod_exist():
            print("ℹ️ Aucun fichier Buff_mod.json à réinitialiser.")
            return

        original_data = JsonUtils.load_buff()
        mod_data = JsonUtils.load_buff_mod()

        original_group = original_data.get("Buffs", {}).get(name, [])
        mod_group = mod_data.get("Buffs", {}).get(name, [])

        original_buff = next(
            (b for b in original_group if b["BuffType"] == buff.buff_type and b["SkillName"] == buff.skill_name),
            None
        )

        if original_buff is None:
            print(f"❌ Buff original introuvable pour '{buff.buff_type}' / '{buff.skill_name}'")
            return

        for b in mod_group:
            if b["BuffType"] == buff.buff_type and b["SkillName"] == buff.skill_name:
                b["Duration"] = original_buff["Duration"]
                b["Delay"] = original_buff["Delay"]
                b["Value"] = original_buff["Value"]
                b["change"] = False
                break

        all_buffs = [
            b for group in mod_data.get("Buffs", {}).values()
            for b in group
        ]

        if all(not b.get("change", False) for b in all_buffs):
            JsonUtils.delete_buff_mod()
            print("Tous les buffs modifiés ont été réinitialisés. Buff_mod.json supprimé.")
        else:
            JsonUtils.save_buff_mod(mod_data)
            print(f" Buff '{buff.buff_type}' remis à zéro dans Buff_mod.json.")

    @staticmethod
    def add_buff(buff: Buff, name: str):
        from Utils.JsonUtils import JsonUtils
        if JsonUtils.buff_mod_exist():
            data = JsonUtils.load_buff_mod()
        else:
            data = JsonUtils.load_buff()

        data["Buffs"][name].append(Utils.to_dict(buff))
        JsonUtils.save_buff_mod(data)

    @staticmethod
    def to_dict(buff: Buff):
        return {
            "AbsoluteValue": buff.absolute_value,
            "BuffType": buff.buff_type,
            "Chance": buff.chance,
            "Delay": buff.delay,
            "Duration": buff.duration,
            "SkillName": buff.skill_name,
            "Value": buff.value,
            "add": True
        }

    @staticmethod
    def is_duplicate(buff1: Buff, buff2: Buff) -> bool:
        return buff1.buff_type == buff2.buff_type and buff1.skill_name == buff2.skill_name

    @staticmethod
    def remove_buff_from_list(buff: Buff, name: str):
        from Utils.JsonUtils import JsonUtils
        data = JsonUtils.load_buff_mod() if JsonUtils.buff_mod_exist() else JsonUtils.load_buff()
        if name not in data.get("Buffs", {}):
            print(f"Error : No buff find on {name}")
            return

        buff_list = data["Buffs"][name]
        data["Buffs"][name] = [
            b for b in buff_list
            if not (b.get("BuffType") == buff.buff_type and b.get("SkillName") == buff.skill_name)
        ]

        JsonUtils.save_buff_mod(data)

    @staticmethod
    def on_reset_buff(name: str):
        from Utils.JsonUtils import JsonUtils
        data = JsonUtils.load_buff()
        if name not in data.get("Buffs", {}):
            print(f"Error : No buff find on {name}")
            return

        original = data["Buffs"][name]
        if not JsonUtils.buff_mod_exist():
            return
        mod_data = JsonUtils.load_buff_mod() if JsonUtils.buff_mod_exist() else {"Buffs": {}}
        mod_data["Buffs"][name] = original
        JsonUtils.save_buff_mod(mod_data)

    @staticmethod
    def buff_group_has_changes(name: str, current_buffs: list["Buff"]) -> bool:
        from Utils.JsonUtils import JsonUtils
        from Entity.BuffGroup import BuffGroup

        original_data = JsonUtils.load_buff()
        original_buffs_data = original_data.get("Buffs", {}).get(name, [])
        original_group = BuffGroup.from_data(name, original_buffs_data)

        current_group = BuffGroup(name=original_group.name, buffs=current_buffs)

        if len(original_group.buffs) != len(current_group.buffs):
            return True

        return any(
            buff.change is True or getattr(buff, "add", None) is not None
            for buff in current_group.buffs
        )

    @staticmethod
    def check_before_apply_buff(slider, slider2, entry, buff) -> bool:
        new_duration = int(slider.get())
        new_delay = int(slider2.get())
        try:
            new_value = float(entry.get())
        except ValueError:
            return False

        if new_duration == buff.duration and new_delay == buff.delay and float(buff.value) == new_value:
            print("No change buff")
            return False
        else:
            print("change buff")
            return True

    @staticmethod
    def max_min_input_value_buff(value: str):
        if "SkillRate" in value or "MaxStamina" in value:
            return -30, 50
        elif value in (EnumBuffTypeSkillName.HydrationRate.value,
                       EnumBuffTypeSkillName.EnergyRate.value):
            return -2.0, 2.0
        elif value in (EnumBuffTypeSkillName.Contusion.value,
                       EnumBuffTypeSkillName.HandsTremor.value,
                       EnumBuffTypeSkillName.QuantumTunnelling.value,
                       EnumBuffTypeSkillName.RemoveAllBloodLosses.value,
                       EnumBuffTypeSkillName.Antidote.value,
                       EnumBuffTypeSkillName.UnknownToxin.value):
            return 0, 0
        elif value in EnumBuffTypeSkillName.StaminaRate.value:
            return -2, 3
        elif value in EnumBuffTypeSkillName.WeightLimit.value:
            return 0.01, 1.0
        elif value in EnumBuffTypeSkillName.DamageModifier.value:
            return 0.01, 10.0
        elif value in EnumBuffTypeSkillName.BodyTemperature.value:
            return -4, 6
        elif value in EnumBuffTypeSkillName.HealthRate.value:
            return -600, 50
        else:
            print(value)
        return -100, 100

    @staticmethod
    def delete_mod(window_type: WindowType, result):
        from Utils.JsonUtils import JsonUtils
        if window_type == WindowType.BUFF:
            msg_choice = CTkMessagebox(title="remove all Buff ?",
                                       message="Are you sure to DELETE all Buffs modifications ? ",
                                       icon="warning", option_1="No", option_2="Yes")
            response = msg_choice.get()
            if response == "Yes":
                if JsonUtils.buff_mod_exist():
                    JsonUtils.delete_buff_mod()
            elif response == "No":
                print("No delete")

        if window_type == WindowType.MAG:
            msg_choice = CTkMessagebox(title="remove all Magazines ?",
                                       message="Are you sure to DELETE all Magazines modifications ? ",
                                       icon="warning", option_1="No", option_2="Yes")
            response = msg_choice.get()
            if response == "Yes":
                Utils.reset_all_mag()
            elif response == "No":
                print("No delete")

        if window_type == WindowType.BAG:
            msg_choice = CTkMessagebox(title="remove all Bag ?",
                                       message="Are you sure to DELETE all BackPack modifications ? ",
                                       icon="warning", option_1="No", option_2="Yes")
            response = msg_choice.get()
            if response == "Yes":
                JsonUtils.delete_all_bag_mod()
            elif response == "No":
                print("No delete")

