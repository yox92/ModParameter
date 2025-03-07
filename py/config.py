import json
from pathlib import Path
import sys

MAIN_DIR = Path(__file__).resolve().parent / "main"

BASE_DIR = MAIN_DIR.parent

sys.path.append(str(BASE_DIR))

JSON_FILES_DIR = BASE_DIR / "JsonFiles"
JSON_FILES_DIR_WEAPONS = JSON_FILES_DIR / "Weapons"
JSON_FILES_DIR_CALIBER = JSON_FILES_DIR / "Calibers"
JSON_FILES_DIR_PMC = JSON_FILES_DIR / "PMC"
IMAGES_DIR = BASE_DIR / "Images"

REQUIRED_DIRS = [MAIN_DIR, JSON_FILES_DIR]


def relatif_path(path):
    return path.relative_to(BASE_DIR)


def check_empty_directories(directories):
    empty_dirs = []
    for directory in directories:
        if not any(directory.iterdir()):
            empty_dirs.append(directory)
    return empty_dirs


def check_json_files(directory):
    invalid_files = []
    for json_file in directory.glob("*.json"):
        try:
            with json_file.open("r", encoding="utf-8") as f:
                json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            invalid_files.append((json_file, str(e)))

    return invalid_files


def check_and_fix_json_caliber_files():
    modified_files = []
    file_iteration: int = 0
    caliber_max_min_count: int = 20
    for json_file in JSON_FILES_DIR_CALIBER.glob("*.json"):
        file_iteration = file_iteration + 1
        try:
            with json_file.open("r", encoding="utf-8") as f:
                data = json.load(f)

            modified = False

            for key, value in data.items():
                if isinstance(value, (int, float)):
                    if value == 0:
                        new_value = 1.0
                    elif value == 1:
                        new_value = 1.0
                    else:
                        new_value = value

                    if new_value != value:
                        data[key] = new_value
                        modified = True

            if modified:
                with json_file.open("w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                modified_files.append(json_file.name)

        except (json.JSONDecodeError, IOError) as e:
            print(f" ERROR: JSON format error in `{json_file.name}` → {e}")

    if modified_files:
        print("The following caliber JSON files have been corrected:")
        for file in modified_files:
            print(f"   - {file}")
    if caliber_max_min_count > file_iteration:
        print(f" {caliber_max_min_count - file_iteration} Caliber file(s) are missing!")
    elif caliber_max_min_count < file_iteration:
        print(f"There are too many caliber ({file_iteration - caliber_max_min_count}) files!")
    else:
        print("All caliber JSON files are already valid.")


def check_project_structure():
    missing_dirs = [d for d in REQUIRED_DIRS if not d.exists()]
    empty_dirs = check_empty_directories(REQUIRED_DIRS)

    if missing_dirs:
        print("❌ ERROR: Invalid project structure! The following directories are missing:")
        for d in missing_dirs:
            print(f"   - {d}")
        sys.exit(1)
    if empty_dirs:
        print("❌ ERROR: Some directories are empty! The following directories contain no files:")
        for d in empty_dirs:
            print(f"   - {d}")
        sys.exit(1)

    for directory in [JSON_FILES_DIR_WEAPONS, JSON_FILES_DIR_CALIBER, JSON_FILES_DIR_PMC]:
        invalid_json_files = check_json_files(directory)
        if invalid_json_files:
            print(f"❌ ERROR: Invalid JSON files found in {relatif_path(directory)}:")
            for file, error in invalid_json_files:
                print(f"   - {file.name}: {error}")
            sys.exit(1)


    else:
        print("\n Everything is in order! The project structure is correct")
        print("------------------------------------------------------------")
        print(f" Directory containing `main.py`: {relatif_path(MAIN_DIR)}")
        print(f" JSON directory (JsonFiles): {relatif_path(JSON_FILES_DIR_WEAPONS)}")
        print(f" JSON directory (JsonFiles): {relatif_path(JSON_FILES_DIR_CALIBER)}")
        print(f" JSON directory (JsonFiles): {relatif_path(JSON_FILES_DIR_PMC)}")
        print(f" Image directory (JsonFiles): {relatif_path(IMAGES_DIR)}")
        print("------------------------------------------------------------\n")


check_and_fix_json_caliber_files()
check_project_structure()
