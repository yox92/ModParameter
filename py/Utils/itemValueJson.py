import os
import json
from collections import Counter, defaultdict
import config
import time

weapons_path = config.BASE_DIR

new_key = "priceFactor"
new_value = 1.0

import os
import json

from collections import defaultdict
from pathlib import Path

# Liste des dossiers à traiter


# Clé et valeur à ajouter
# new_key = 'priceFactor'
# new_value = 1.0

import os
from pathlib import Path

MAG_PATH = config.JSON_FILES_DIR_MAG
BAG_PATH = config.JSON_FILES_DIR_BAG / "Buff.json"
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
#
# CATEGORY_BOUNDS = {
#     "01-18": (1, 18),
#     "19-24": (19, 24),
#     "25-30": (25, 30),
#     "31-36": (31, 36),
#     "37-48.json": (37, 48)
# }
# def get_category_for_size(size: int) -> str:
#     for label, (min_size, max_size) in CATEGORY_BOUNDS.items():
#         if min_size <= size <= max_size:
#             return label
#     return "unknown"
#
# def extract_backpacks_with_grids_from_file(items_file: Path, output_file: Path) -> None:
#     result = defaultdict(lambda: {
#         "size": 0,
#         "penality": False,
#         "resize": False,
#         "ids": {}
#     })
#
#     try:
#         with open(items_file, "r", encoding="utf-8") as f:
#             data = json.load(f)
#
#         for item_id, item_data in data.items():
#             if item_data.get("_parent") != PARENT_ID_BACKPACK:
#                 continue
#
#             grids = item_data.get("_props", {}).get("Grids", [])
#             grid_data = {}
#             total_size = 0
#
#             for grid in grids:
#                 grid_id = grid.get("_id")
#                 cellsH = grid.get("_props", {}).get("cellsH")
#                 cellsV = grid.get("_props", {}).get("cellsV")
#
#                 if grid_id and cellsH is not None and cellsV is not None:
#                     grid_data[grid_id] = {
#                         "cellsH": cellsH,
#                         "cellsV": cellsV
#                     }
#                     total_size += cellsH * cellsV
#
#             if grid_data:
#                 category = get_category_for_size(total_size)
#
#                 if category == "unknown":
#                     print(f"⚠️  Sac ignoré : id={item_id}, name={item_data.get('_name', 'Inconnu')}, size={total_size}")
#                     continue
#
#                 result[category]["ids"][item_id] = {
#                     "name": item_data.get("_name", "Inconnu"),
#                     "Grids": grid_data
#                 }
#     except Exception as e:
#         print(f"❌ Erreur pendant le traitement de {items_file} : {e}")
#         return
#
#     output_file.parent.mkdir(parents=True, exist_ok=True)
#
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(result, f, indent=2, ensure_ascii=False)
#
#     print(f"✅ Export terminé : {output_file}")

# Clés à extraire
BUFF_KEYS = {
    "BuffsAdrenaline",
    "BuffsGoldenStarBalm",
    "BuffsPropital",
    "BuffsSJ1TGLabs",
    "BuffsSJ6TGLabs",
    "BuffsZagustin",
    "Buffs_2A2bTG",
    "Buffs_3bTG",
    "Buffs_AHF1M",
    "Buffs_Antidote",
    "Buffs_KultistsToxin",
    "Buffs_L1",
    "Buffs_MULE",
    "Buffs_Meldonin",
    "Buffs_Obdolbos",
    "Buffs_Obdolbos2",
    "Buffs_P22",
    "Buffs_PNB",
    "Buffs_Perfotoran",
    "Buffs_SJ12_TGLabs",
    "Buffs_Trimadol"
}


def find_key_recursively(obj, target_key):
    if isinstance(obj, dict):
        if target_key in obj:
            return obj[target_key]
        for value in obj.values():
            result = find_key_recursively(value, target_key)
            if result is not None:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_key_recursively(item, target_key)
            if result is not None:
                return result
    return None

def extract_filtered_buffs() -> dict:
    try:
        start_total = time.perf_counter()

        target_path = (config.BASE_DIR / ".." / "src" / "external" / "server" / "project" / "assets" / "database").resolve()
        globals_path = target_path / "globals.json"

        start_load = time.perf_counter()
        with open(globals_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        end_load = time.perf_counter()

        start_search = time.perf_counter()
        stimulator_data = find_key_recursively(data, "Stimulator")
        end_search = time.perf_counter()

        if not stimulator_data:
            print("❌ Clé 'Stimulator' introuvable.")
            return {}

        buffs_data = stimulator_data.get("Buffs")
        if not buffs_data:
            print("❌ Clé 'Buffs' introuvable dans 'Stimulator'.")
            return {}

        start_filter = time.perf_counter()
        filtered_buffs = {
            key: value for key, value in buffs_data.items() if key in BUFF_KEYS
        }
        end_filter = time.perf_counter()

        end_total = time.perf_counter()

        # Logs de performance
        print("\n Temps d'exécution (secondes) :")
        print(f" Lecture du fichier JSON : {end_load - start_load:.4f}")
        print(f"Recherche de 'Stimulator' : {end_search - start_search:.4f}")
        print(f"Filtrage des buffs : {end_filter - start_filter:.4f}")
        print(f" Temps total : {end_total - start_total:.4f}\n")

        return {"Buffs": filtered_buffs}

    except Exception as e:
        print(f"❌ Erreur lors de l'extraction : {e}")
        return {}
if __name__ == "__main__":
    result = extract_filtered_buffs()

    target_path = (
            config.BASE_DIR / ".." / "src" / "external" / "server" / "project" / "assets" / "database").resolve()
    items_json_path = target_path / "Buff.json"
    output_path = config.JSON_FILES_DIR_BUFF / "Buff.json"

    if result:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        print(f"✅ Fichier généré : {output_path}")
