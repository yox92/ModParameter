import json
import os

from config import JSON_FILES_DIR


class JsonUtils:

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
    def update_json_value(data, path_for_attribut_json, new_value, from_all_weapons):
        if isinstance(new_value, (int, float)):
            current = JsonUtils.get_nested_value(data, path_for_attribut_json)

            final_key = path_for_attribut_json[-1]
            JsonUtils.update_or_multiply_final_key(current, final_key, new_value, from_all_weapons)

        return data

    @staticmethod
    def update_or_multiply_final_key(current, final_key, new_value, from_all_weapons):
        if final_key in current:
            if from_all_weapons:
                current[final_key] *= int(new_value)  # Multiply (all weapons)
            else:
                current[final_key] = new_value  # Remplace (one weapon specific)
        else:
            raise KeyError(f"Chemin invalide : la clé finale '{final_key}' n'existe pas.")

    @staticmethod
    def get_nested_value(data, path_for_attribut_json):
        current = data
        for key in path_for_attribut_json[:-1]:  # Parcourir jusqu'à l'avant-dernière clé
            if key in current:
                current = current[key]
            else:
                raise KeyError(f"Chemin invalide : la clé '{key}' n'existe pas.")
        return current












    @staticmethod
    def delete_file_if_exists(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    @staticmethod
    def save_json_as_new_file(data, file_path_new_json):
        base_name, ext = os.path.splitext(file_path_new_json)
        new_file_path = f"{base_name}_mod{ext}"

        JsonUtils.delete_file_if_exists(new_file_path)

        with open(new_file_path, "w") as new_file:
            json.dump(data, new_file, indent=4)

        return new_file_path

    @staticmethod
    def load_all_json_files_without_mod():
        json_dir_path = JSON_FILES_DIR
        data_list = []
        for filename in os.listdir(json_dir_path):

            if filename.endswith('.json') and not filename.endswith('mod.json'):
                file_path = json_dir_path / filename
                data_list.append(JsonUtils.load_json_and_add_path(file_path))

        return data_list

    @staticmethod
    def return_list_json_path(name_json):
        list_of_json = []
        for filename in os.listdir(JSON_FILES_DIR):
            if filename.endswith('.json') and not filename.endswith('mod.json'):
                base_name = filename.rsplit('.json', 1)[0]
                if base_name in name_json:
                    list_of_json.append(os.path.join(JSON_FILES_DIR, filename))
        return list_of_json

    @staticmethod
    def update_json_in_new_file(key, new_value, data, from_all_weapons):
        path_props_json = ["item", "_props", key]
        return JsonUtils.update_json_value(data, path_props_json, new_value, from_all_weapons)

    @staticmethod
    def file_exist(file_path):
        return os.path.exists(file_path)

    @staticmethod
    def all_file_exist(all_file_path):
        return all(os.path.exists(file) for file in all_file_path)






