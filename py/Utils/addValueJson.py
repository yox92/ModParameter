import os
import json

import config

weapons_path = config.JSON_FILES_DIR_WEAPONS
ammo_path = config.JSON_FILES_DIR_AMMO
medic_path = config.JSON_FILES_DIR_MEDIC

new_key = "priceFactor"
new_value = 1.0

import os
import json

# Liste des dossiers à traiter
folders = [config.JSON_FILES_DIR_MEDIC]

# Clé et valeur à ajouter
# new_key = 'priceFactor'
# new_value = 1.0

#               Racine
# for folder_path in folders:
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".json"):
#             file_path = os.path.join(folder_path, filename)
#
#             with open(file_path, "r", encoding="utf-8") as f:
#                 data = json.load(f)
#                 data[new_key] = new_value
#
#                 with open(file_path, "w", encoding="utf-8") as f:
#                     json.dump(data, f, indent=2)
#                     print(f"{filename} ➜ modifié ")
#  Props
# for folder_path in folders:
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".json"):
#             file_path = os.path.join(folder_path, filename)
#
#             with open(file_path, "r", encoding="utf-8") as f:
#                 data = json.load(f)
#
#             if "item" in data and "_props" in data["item"]:
#                 data["item"]["_props"][new_key] = new_value
#
#                 with open(file_path, "w", encoding="utf-8") as f:
#                     json.dump(data, f, indent=2)
#                     print(f"{filename} ➜ modifié")
#             else:
#                 print(f"{filename} ➜ structure inattendue, pas modifié")

# clone
# new_key = "clone"
# new_value = True
#
# for folder_path in folders:
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".json"):
#             file_path = os.path.join(folder_path, filename)
#
#             with open(file_path, "r", encoding="utf-8") as f:
#                 data = json.load(f)
#
#             data[new_key] = new_value
#
#             with open(file_path, "w", encoding="utf-8") as f:
#                 json.dump(data, f, indent=2)
#                 print(f"{filename} ➜ 'clone: true' inséré")


import json

# JSON original (simplifié ici, remplacer par le JSON complet dans un cas réel)

MAG_PATH = config.JSON_FILES_DIR_MAG / "Mag.json"

with open(MAG_PATH, "r", encoding="utf-8") as f:
    original_data = json.load(f)

transformed_data = {
    category: {
        "value": None,
        "items": ids
    } for category, ids in original_data.items()
}

# Sauvegarde du nouveau JSON
with open(MAG_PATH, "w", encoding="utf-8") as f:
    json.dump(transformed_data, f, indent=2, ensure_ascii=False)

print("Traitement terminé.")
