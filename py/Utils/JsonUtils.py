import json
import os


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
