import os
import json
from collections import Counter, defaultdict
import config

weapons_path = config.BASE_DIR

new_key = "priceFactor"
new_value = 1.0

import os
import json

from collections import defaultdict
from pathlib import Path

# Liste des dossiers à traiter
folders = [config.BASE_DIR]

# Clé et valeur à ajouter
# new_key = 'priceFactor'
# new_value = 1.0

import os
from pathlib import Path

target_path = (config.BASE_DIR / ".." / "src" / "external" / "server" / "project" / "assets" / "database" / "templates").resolve()
MAG_PATH = config.JSON_FILES_DIR_MAG
BAG_PATH = config.JSON_FILES_DIR_BAG / "Bag.json"
PARENT_ID_MAGAZINE = "5448bc234bdc2d3c308b4569"
PARENT_ID_BACKPACK = "5448e53e4bdc2d60728b4567"

# def group_ids_by_range(json_objects: dict, parent_id: str) -> dict:
#     grouped = defaultdict(list)
#
#     for item_id, item_data in json_objects.items():
#         if item_data.get("_parent") == parent_id:
#             cartridges = item_data.get("_props", {}).get("Cartridges", [])
#             for cartridge in cartridges:
#                 max_count = cartridge.get("_max_count")
#                 if max_count is None:
#                     continue
#
#                 # Déterminer la tranche
#                 if 1 <= max_count <= 9:
#                     key = "01–09"
#                 elif 10 <= max_count <= 19:
#                     key = "10–19"
#                 elif 20 <= max_count <= 29:
#                     key = "20–29"
#                 elif 30 <= max_count <= 39:
#                     key = "30–39"
#                 elif 40 <= max_count <= 49:
#                     key = "40–49"
#                 elif 50 <= max_count <= 59:
#                     key = "50–59"
#                 elif 60 <= max_count <= 69:
#                     key = "60–69"
#                 elif 70 <= max_count <= 79:
#                     key = "70–79"
#                 elif 80 <= max_count <= 89:
#                     key = "80–89"
#                 elif 90 <= max_count <= 100:
#                     key = "90–100"
#                 else:
#                     key = ">100"
#
#                 grouped[key].append(item_id)
#
#     return dict(grouped)
#
# def extract_all_ids(traders_path: Path, parent_id: str) -> dict:
#     all_grouped = defaultdict(list)
#
#     for file in traders_path.rglob("*.json"):
#         try:
#             with open(file, "r", encoding="utf-8") as f:
#                 json_data = json.load(f)
#
#             grouped_ids = group_ids_by_range(json_data, parent_id)
#
#             for key, ids in grouped_ids.items():
#                 all_grouped[key].extend(ids)
#
#         except Exception as e:
#             print(f"Erreur dans le fichier {file}: {e}")
#
#     return dict(all_grouped)
#
# if __name__ == "__main__":
#
#     grouped_id_data = extract_all_ids(target_path, PARENT_ID)
#
#     output_path = directory / "Mag.json"
#     output_path.parent.mkdir(parents=True, exist_ok=True)
#
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(grouped_id_data, f, indent=2, ensure_ascii=False)
#
#     print(f"\n✅ JSON écrit dans : {output_path}")

def extract_backpacks_with_grids_from_file(items_file: Path, output_file: Path) -> None:
    result = {}

    try:
        with open(items_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item_id, item_data in data.items():
            if item_data.get("_parent") != PARENT_ID_BACKPACK:
                continue

            grids = item_data.get("_props", {}).get("Grids", [])
            grid_data = {}

            for grid in grids:
                grid_id = grid.get("_id")
                cellsH = grid.get("_props", {}).get("cellsH")
                cellsV = grid.get("_props", {}).get("cellsV")

                if grid_id and cellsH is not None and cellsV is not None:
                    grid_data[grid_id] = {
                        "cellsH": cellsH,
                        "cellsV": cellsV
                    }

            if grid_data:
                result[item_id] = {"Grids": grid_data}

    except Exception as e:
        print(f"❌ Erreur pendant le traitement de {items_file.name} : {e}")
        return

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ Export terminé : {output_file}")

# Exemple d'utilisation
if __name__ == "__main__":

    items_json_path = target_path / "items.json"
    output_path = config.JSON_FILES_DIR_BAG / "Bag.json"

    extract_backpacks_with_grids_from_file(items_json_path, output_path)

