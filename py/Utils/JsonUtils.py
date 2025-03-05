import json
import os

import Utils
from config import JSON_FILES_DIR_WEAPONS, JSON_FILES_DIR_CALIBER
from Utils.Utils import Utils


class JsonUtils:

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
    def load_all_json_files_mod():
        json_dir_path = JSON_FILES_DIR_WEAPONS
        data_list = []
        for filename in os.listdir(json_dir_path):

            if filename.endswith('_mod.json'):
                data_list.append(filename)
        return data_list

    @staticmethod
    def udate_json_caliber(path_to_json_calibber, new_value_change):
        data = JsonUtils.load_json(path_to_json_calibber)
        for key, value in new_value_change.items():
            data[key] = value
        JsonUtils.write_json(data, path_to_json_calibber)

    @staticmethod
    def update_json_value(data, path_for_attribut_json, new_value, from_all_weapons):
        if isinstance(new_value, (int, float)):
            current = JsonUtils.get_nested_value(data, path_for_attribut_json)

            final_key = path_for_attribut_json[-1]
            JsonUtils.update_or_multiply_final_key(current, final_key, new_value, from_all_weapons)

        return data

    @staticmethod
    def update_or_multiply_final_key(current, final_key, new_value, from_all_weapons):
        if final_key not in current:
            raise KeyError(f"Invalid path: the final key {final_key} does not exist")

        if not isinstance(current[final_key], (int, float)):
            raise TypeError(f"The value associated with {final_key} must be of type int or float")

        if from_all_weapons:
            current[final_key] = (
                int(current[final_key] * new_value)
                if isinstance(current[final_key], int)
                else current[final_key] * new_value
            )
        else:
            current[final_key] = (
                int(new_value)
                if isinstance(current[final_key], int)
                else new_value
            )

    @staticmethod
    def get_nested_value(data, path_for_attribut_json):
        current = data
        for key in path_for_attribut_json[:-1]:  # last key - 1
            if key in current:
                current = current[key]
            else:
                raise KeyError(f"Chemin invalide : la clé '{key}' n'existe pas.")
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
    def update_json_in_new_file(key, new_value, data, from_all_weapons):
        path_props_json = ["item", "_props", key]
        return JsonUtils.update_json_value(data, path_props_json, new_value, from_all_weapons)

    @staticmethod
    def update_json_caliber_from_new_value_change(path_to_json_calibber, new_value_change):
        JsonUtils.udate_json_caliber(path_to_json_calibber, new_value_change)
