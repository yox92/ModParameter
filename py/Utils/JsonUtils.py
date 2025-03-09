import json
import os

import Utils
from Entity import EnumAmmo, Logger
from Entity.WindowType import WindowType
from config import JSON_FILES_DIR_WEAPONS, JSON_FILES_DIR_CALIBER, JSON_FILES_DIR_PMC, JSON_FILES_DIR_AMMO
from Utils.Utils import Utils


class JsonUtils:
    logger = Logger()

    @staticmethod
    def file_exist(file_path):
        return os.path.exists(file_path)

    @staticmethod
    def file_mod_exist(file_path):
        json_file_path_mod = file_path.replace(".json", "_mod.json")
        return JsonUtils.file_exist(json_file_path_mod)

    @staticmethod
    def return_json_mod(file_path):
        json_file_path_mod = file_path.replace(".json", "_mod.json")
        return JsonUtils.load_json(json_file_path_mod)

    @staticmethod
    def all_file_exist(all_file_path):
        return all(os.path.exists(file) for file in all_file_path)

    @staticmethod
    def load_json(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as fileReadable:
                data = json.load(fileReadable)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Le fichier '{file_path}' est introuvable.")
        except json.JSONDecodeError:
            raise ValueError(f"Le fichier '{file_path}' contient un JSON invalide.")

    @staticmethod
    def get_file_path_json_pmc():
        for filename in os.listdir(JSON_FILES_DIR_PMC):
            if filename.endswith('.json') and not filename.endswith('mod.json'):
                file_path = os.path.join(JSON_FILES_DIR_PMC, filename)
                return file_path
        return None

    @staticmethod
    def get_file_path_json_pmc_save():
        for filename in os.listdir(JSON_FILES_DIR_PMC):
            if filename.endswith('_mod.json'):
                file_path = os.path.join(JSON_FILES_DIR_PMC, filename)
                return file_path
        return None

    @staticmethod
    def write_json(data, file_path):
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def load_json_and_add_path(file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                data['file_path'] = str(file_path.resolve())
                return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Le fichier '{file_path}' est introuvable.")
        except json.JSONDecodeError:
            raise ValueError(f"Le fichier '{file_path}' contient un JSON invalide.")

    @staticmethod
    def find_caliber_json_config(caliber_name):
        data = []
        for filename in os.listdir(JSON_FILES_DIR_CALIBER):
            if filename.endswith('.json') and caliber_name in filename:
                file_path = os.path.join(JSON_FILES_DIR_CALIBER, filename)
                data = JsonUtils.load_json(file_path)
                return data, file_path
        if not data:
            raise FileNotFoundError(f"Config caliber json file '{caliber_name}' not find.")
        return None, None

    @staticmethod
    def load_all_json_files_without_mod():
        json_dir_path = JSON_FILES_DIR_WEAPONS
        data_list = []
        for filename in os.listdir(json_dir_path):

            if filename.endswith('.json') and not filename.endswith('mod.json'):
                file_path = json_dir_path / filename
                data_list.append(JsonUtils.load_json_and_add_path(file_path))

        return data_list

    @staticmethod
    def load_all_json_files_without_mod_ammo():
        json_dir_path = JSON_FILES_DIR_AMMO
        data_list = []
        for filename in os.listdir(json_dir_path):

            if filename.endswith('.json') and not filename.endswith('mod.json'):
                file_path = json_dir_path / filename
                data_list.append(JsonUtils.load_json_and_add_path(file_path))

        return data_list

    @staticmethod
    def load_all_json_files_weapons_mod():
        json_dir_path = JSON_FILES_DIR_WEAPONS
        data_list = []
        for filename in os.listdir(json_dir_path):

            if filename.endswith('_mod.json'):
                data_list.append(filename)
        return data_list

    @staticmethod
    def load_all_json_files_ammo_mod():
        json_dir_path = JSON_FILES_DIR_AMMO
        data_list = []
        for filename in os.listdir(json_dir_path):

            if filename.endswith('_mod.json'):
                data_list.append(filename)
        return data_list

    @staticmethod
    def load_all_json_files_ammo_mod():
        json_dir_path = JSON_FILES_DIR_AMMO
        data_list = []
        for filename in os.listdir(json_dir_path):

            if filename.endswith('_mod.json'):
                data_list.append(filename)
        return data_list

    @staticmethod
    def load_all_json_ammo():
        json_dir_path = JSON_FILES_DIR_AMMO
        data: list[dict] = []
        file_paths: list[str] = []

        for filename in os.listdir(json_dir_path):
            if filename.endswith('.json') and not filename.endswith('mod.json'):
                file_path = os.path.join(json_dir_path, filename)
                file_paths.append(file_path)
                data.append(JsonUtils.load_json(file_path))

        if not data:
            raise FileNotFoundError(f"Ammo JSON files not found in '{json_dir_path}'.")

        return data, file_paths

    @staticmethod
    def udate_json_caliber(path_to_json_calibber, new_value_change):
        data = JsonUtils.load_json(path_to_json_calibber)
        for key, value in new_value_change.items():
            data[key] = value
        JsonUtils.write_json(data, path_to_json_calibber)

    @staticmethod
    def update_json_value(data, path_for_attribut_json, new_value, window_type: WindowType):
        if isinstance(new_value, (int, float, bool)):
            current = JsonUtils.get_nested_value(data, path_for_attribut_json)

            final_key = path_for_attribut_json[-1]
            JsonUtils.update_or_multiply_final_key(current, final_key, new_value, window_type)
        return data

    @staticmethod
    def update_or_multiply_final_key(current, final_key, new_value, window_type):
        if final_key not in current:
            raise KeyError(f"Error on apply value. : key : '{final_key}' value to update do not existe on target.")

        if not isinstance(current[final_key], (int, float, bool)):
            if not Utils.is_exception_for_string_to_boolean(current[final_key], new_value):
                raise TypeError(f"The value associated with {final_key} must be of type int, float, bool")

        if window_type == window_type.CALIBER:
            original_value = current[final_key]

            if isinstance(original_value, int):
                min_value = 1
                new_value_calculated = int(original_value * new_value)
                if new_value_calculated < min_value:
                    new_value_calculated = min_value
                current[final_key] = new_value_calculated

            elif isinstance(original_value, float):
                if not (0.01 <= new_value <= 2.0):
                    return

                original_str = str(original_value).rstrip("0")
                decimal_places = len(original_str.split(".")[1]) if "." in original_str else 2
                decimal_places = max(decimal_places, 1)

                min_value = round(10 ** -decimal_places, decimal_places)

                new_value_calculated = original_value * new_value

                if 0 < new_value_calculated < min_value:
                    new_value_calculated = min_value

                new_value_calculated = round(new_value_calculated, decimal_places)

                current[final_key] = new_value_calculated

        elif window_type == window_type.WEAPON or window_type == window_type.PMC:
            current[final_key] = (
                int(new_value)
                if isinstance(current[final_key], int)
                else new_value
            )
        elif window_type == window_type.AMMO:
            if isinstance(new_value, bool):
                if final_key == EnumAmmo.TRACERCOLOR.label:
                    current[final_key] = Utils.case_on_app_bol_on_file_string_transform_bool(new_value)
                else:
                    current[final_key] = new_value
            elif isinstance(new_value, int):
                current[final_key] = new_value
            elif isinstance(new_value, float):
                current[final_key] = int(new_value)
            else:
                raise KeyError(f"Error on apply app. {new_value} need to be boolean or number to be update")

    @staticmethod
    def get_nested_value(data, path_for_attribut_json):
        current = data
        for key in path_for_attribut_json[:-1]:  # last key - 1
            if key in current:
                current = current[key]
            else:
                raise KeyError(
                    f"Error on apply value way. An attributs try to be find on original JSON file. But do not exist")
        return current

    @staticmethod
    def delete_file_if_exists(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def delete_file_mod_if_exists(file_path):
        json_file_path_mod = file_path.replace(".json", "_mod.json")
        if os.path.exists(json_file_path_mod):
            os.remove(json_file_path_mod)

    @staticmethod
    def save_json_as_new_file(data, file_path_new_json):
        base_name, ext = os.path.splitext(file_path_new_json)
        new_file_path = f"{base_name}_mod{ext}"

        JsonUtils.delete_file_if_exists(new_file_path)

        with open(new_file_path, "w") as new_file:
            json.dump(data, new_file, indent=4)

        return new_file_path

    @staticmethod
    def return_list_json_path(name_json):
        list_of_json = []
        clean_name_json = Utils.transform_list_of_strings(name_json)
        for filename in os.listdir(JSON_FILES_DIR_WEAPONS):
            if filename.endswith('.json') and not filename.endswith('mod.json'):
                base_name = Utils.remove_jon_extension(filename)
                if base_name in clean_name_json:
                    list_of_json.append(os.path.join(JSON_FILES_DIR_WEAPONS, filename))
        return list_of_json

    @staticmethod
    def update_json_in_new_file_weapon(key, new_value, data, window_type: WindowType):
        path_props_json = ["item", "_props", key]
        return JsonUtils.update_json_value(data, path_props_json, new_value, window_type)

    @staticmethod
    def update_json_in_new_file_aiming(key, new_value, data, window_type):
        path_props_json = [key]
        return JsonUtils.update_json_value(data, path_props_json, new_value, window_type)

    @staticmethod
    def update_json_caliber_from_new_value_change(path_to_json_calibber, new_value_change):
        JsonUtils.udate_json_caliber(path_to_json_calibber, new_value_change)
