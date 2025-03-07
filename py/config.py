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

    else:
        print("\n Everything is in order! The project structure is correct")
        print("------------------------------------------------------------")
        print(f" Directory containing `main.py`: {relatif_path(MAIN_DIR)}")
        print(f" JSON directory (JsonFiles): {relatif_path(JSON_FILES_DIR_WEAPONS)}")
        print(f" JSON directory (JsonFiles): {relatif_path(JSON_FILES_DIR_CALIBER)}")
        print(f" JSON directory (JsonFiles): {relatif_path(JSON_FILES_DIR_PMC)}")
        print(f" Image directory (JsonFiles): {relatif_path(IMAGES_DIR)}")
        print("------------------------------------------------------------\n")


check_project_structure()