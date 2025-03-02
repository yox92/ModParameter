import json
import os

from config import JSON_FILES_DIR


class JsonUtils:

    @staticmethod
    def load_json(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Le fichier '{file_path}' est introuvable.")
        except json.JSONDecodeError:
            raise ValueError(f"Le fichier '{file_path}' contient un JSON invalide.")

    @staticmethod
    def update_json_value(data, path_for_attribut_json, new_value):
        current = data
        for key in path_for_attribut_json[:-1]:  # Parcourir jusqu'à l'avant-dernière clé
            if key in current:
                current = current[key]
            else:
                raise KeyError(f"Chemin invalide : la clé '{key}' n'existe pas.")

        final_key = path_for_attribut_json[-1]
        if final_key in current:
            current[final_key] = new_value
        else:
            raise KeyError(f"Chemin invalide : la clé finale '{final_key}' n'existe pas.")

        return data

    @staticmethod
    def save_json_as_new_file(data, original_file_path):
        base_name, ext = os.path.splitext(original_file_path)  # Diviser nom et extension
        new_file_path = f"{base_name}_mod{ext}"  # Ajouter le suffixe "_mod"

        with open(new_file_path, "w") as new_file:
            json.dump(data, new_file, indent=4)

        return new_file_path

    @staticmethod
    def update_json_value(data, path_list, new_value):
        current = data
        for key in path_list[:-1]:  # Parcourir jusqu'à l'avant-dernière clé
            if key in current:
                current = current[key]
            else:
                raise KeyError(f"Chemin invalide : la clé '{key}' n'existe pas.")

        # Modifier la clé finale
        final_key = path_list[-1]
        if final_key in current:
            current[final_key] = new_value
        else:
            raise KeyError(f"Chemin invalide : la clé finale '{final_key}' n'existe pas.")

        return data

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
    def load_json_and_add_result(file_path):
        data_list = []
        try:
            with file_path.open('r', encoding='utf-8') as file:
                data = json.load(file)
                if "locale" in data and "Name" in data["locale"]:
                    # Stocker le chemin absolu du fichier JSON
                    data['file_path'] = str(file_path.resolve())
                    data_list.append(data)
            return data_list
        except FileNotFoundError:
            raise FileNotFoundError(f"Le fichier '{file_path}' est introuvable.")
        except json.JSONDecodeError:
            raise ValueError(f"Le fichier '{file_path}' contient un JSON invalide.")

    @staticmethod
    def load_all_json_files_without_mod():
        json_dir_path = JSON_FILES_DIR

        for filename in os.listdir(json_dir_path):
            if filename.endswith('.json') and not filename.endswith('_mod.json'):
                file_path = json_dir_path / filename
                return JsonUtils.load_json_and_add_result(file_path)



