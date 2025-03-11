# ModParameter App

## Table of Contents
1. [Project Overview](#project-overview)
2. [Main Features](#main-features)
3. [Launching the Application](#launching-the-application)
4. [Project Structure](#python-project-structure)
5. [General Usage](#general-usage)
6. [Key Classes Overview](#key-classes-overview)
   - [ModSelectionWindow](#ModSelectionWindow-)
   - [CaliberWeaponsMod](#CaliberWeaponsMod-)
   - [SingleWeaponMod](#SingleWeaponMod-)
   - [AmmoMod](#AmmoMod-)
   - [ListItemAlreadyMod](#ListItemAlreadyMod-)
7. [Utils](#Utils)
   - [JsonUtils](#JsonUtils)
   - [Utils](#Utils)
8. [Config](#Config)
9. [Examples](#JSON-File-Examples)

10. [Dependencies](#dependencies)

---

## Project Overview
1. **ModParameter App** is a Python application designed to create and manage “mod” files (`*_mod.json`) 
related to various game elements (weapons, ammo, PMC). It uses **[customtkinter](https://github.com/TomSchimansky/CustomTkinter)** 
for its graphical interface and manipulates **JSON files** to load, modify, or delete configuration values.
2. The `*_mod.json` files are later retrieved by the TypeScript project to be mapped into the `SPT Database` objects.

---
## Main Features

1. **Intuitive Graphical Interface**  
   - Main menu with modification options (weapons, ammo, PMC).  
   - Dedicated windows for configuring a single object or a group of objects.

2. **Centralized Mod Management**  
   - Automatic creation of `*_mod.json` files to separate modifications from base files.
   - The `*_mod.json` files are placed by Python into:
     - JsonFiles/Weapons
     - JsonFiles/Ammo
     - JsonFiles/PMC
   - Targeted or global deletion of `*_mod.json` files, allowing a return to the “vanilla” state.

3. **Search and Sorting**  
   - Filter weapons by name.  
   - Select all weapons of the same caliber.
   - Select bullets by their caliber.
   - List all modified weapons and ammo.

4. **Deletion**  
   - Delete `*_mod.json` files for weapons/ammo/PMC:
     - Global deletion.
     - Targeted deletion.
     - Restore original values = delete `*_mod.json`.

5. **Editing and Control**  
   - Sliders to adjust numerical values in percentage %.  
   - Input fields to manually set values.  
   - Boolean switch.
   - Indicators for possible threshold violations (safety limits) or input errors.

6. **Visual Feedback**  
   - Progress bars to display operation progress.  
   - Status labels (e.g., “Changes applied successfully” or “All modifications removed”).

---

# Launching the Application
⚙️
## Python
- Navigate to the project root directory.
- The `main.py` file is located in the `main` directory.
- The ModParameter App window will appear, providing various modification options.

## .EXE File
- The entire packaging process is done using `pyinstaller`.
- A `buildExeFile.bat` script is available to generate the `*.exe` file.
- By default, it is generated in the `py` folder at the project root.

- The `.exe` file is configured to run within the subdirectory structure defined in `config.py`.
- The required structure is as follows:

  - **NameModeFolder** <==> `*.exe`
    - **py**
      - JsonFiles
        - Weapons  **(JSON Files Here)**
        - Ammo     **(JSON Files Here)**
        - Calibers **(JSON Files Here)**
        - PMC      **(JSON Files Here)**
    - **src** (TypeScript SPT)

---


# python-project-structure

📂 Project Structure
.
├── Entity/
│   ├── Caliber.py         
│   ├── EnumProps.py       
│   ├── EnumAmmo.py        
│   ├── Item.py
│   ├── ItemManager.py     
│   ├── ItemProps.py
│   ├── Logger.py
│   ├── Root.py
│   └── WindowType.py
├── Utils/
│   ├── ImageUtils.py
│   ├── JsonUtils.py
│   ├── Utils.py
│   └── WindowUtils.py
├── WindowComponent/
├── JsonFiles/
│   ├── Ammo/
│   ├── Calibers/
│   ├── PMC/
│   ├── Weapons/
├── Images/
│   ├── AmmoMod.py            
│   ├── CaliberWeaponsMod.py  
│   ├── ListItemAlreadyMod.py s
│   ├── PmcMod.py
│   ├── ModSelectionWindow.py     
│   ├── ProgressBar.py
│   └── SingleWeaponMod.py    
├── requirements.txt
└── main.py                   

---

# General Usage

### Main Menu

- **One Specific Weapon**: Find and adjust a single weapon.
- **Weapons by Ballistics**: Sort weapons by caliber.
- **Ammo Attributes**: Modify ammunition attributes.
- **PMC Attributes**: Adjust character attributes.

### Modification

- Depending on the open window, you will find sliders (percentage) or text fields (absolute values).
- Click **Apply** to create or update the `*_mod.json` file.

- At the bottom of the main window, buttons display the list of already modified weapons or ammunition.
- You can delete some or all `*_mod.json` files.
- You also have the option to apply the "tracer bullets" property to all bullets in the game.

### Returning or Closing
- Close the secondary window to return to the main menu.
- Exit the application or select another action.

### Mod List and Deletion
- At the bottom of the main window, buttons allow you to display the list of already modified weapons or ammunition.
- You can delete some or all `*_mod.json` files.

# key-classes-overview

## **ModSelectionWindow** – Main Menu
- **File**: `ModSelectionWindow.py`
- **Role**: Creates the main window with 8 possible choices (including 5 leading to specialized classes).
- **Key Points**:
  - Management of buttons **All Saved Weapons Mod, All Saved Ammo Mod**, etc.
  - Opening and closing of secondary windows (`Toplevel`).
  - Global deletion of Mods (all `*_mod.json` of a certain type).

## **CaliberWeaponsMod** Group Modification by Caliber
- **File**: `WindowComponent/CaliberWeaponsMod.py`
- **Role**: Lists all weapons of a given caliber and applies massive changes (e.g., +20% damage).
- **Key Points**:
  - Selection/deselection of weapons.
  - Sliders to adjust attributes (damage, recoil, accuracy, etc.).
  - Automatic creation/deletion of `*_mod.json` files.
  - For this module, a configuration file = one caliber
    - Located in: `JsonFiles/Calibers`

## **SingleWeaponMod** – Targeted Modification of a Single Weapon
- **File**: `WindowComponent/SingleWeaponMod.py`
- **Role**: Manages the modification of a specific weapon (via search bar or global list).
- **Key Points**:
  - Loads the original JSON file and checks for an existing `*_mod.json`.
  - Sliders for percentage adjustments.
  - Reset possible if all values return to the original state.

## **AmmoMod** – Ammunition Modification
- **File**: `WindowComponent/AmmoMod.py`
- **Role**: Customizes ammunition attributes (penetration, damage, tracer, etc.).
- **Key Points**:
  - Text fields (e.g., penetration) and switch (e.g., ammo tracer on/off).
  - Validity control (upper/lower limits).
  - Creation/deletion of a `*_mod.json` file to enable/disable the mod.

## **ListItemAlreadyMod** – *List and delete mod files*
- **File**: `WindowComponent/ListItemAlreadyMod.py`
- **Role**: Displays all weapons or ammunition that already have a `*_mod.json`, or, depending on the *WindowType*, allows deleting these files in one click.
- **Key Points**:
  1. **Scrolling list**
     - Each item is represented by a button.
  2. **Viewing / Deletion**
     - **Viewing**: For `WEAPON` or `AMMO`, clicking a button opens the detail window (via `SingleWeaponMod`, `AmmoMod`, etc.).
     - **Deletion**: Clicking a button immediately deletes the corresponding `*_mod.json` file (weapon or ammunition).
       - The list updates (refreshes) after deletion so that the item is no longer displayed.
  3. **Display Modes**:
     - Adjusts the interface (window size, button colors) based on the type of item (weapon or ammo) and action (simple viewing or deletion).
  4. **Parameters**:
     - `window_type`: an enumerator (`WindowType`) distinguishing the expected operation (WEAPON, AMMO, DELETE).
     - `weapon_list`: list of elements (weapons or tuples) already modified and detected as `*_mod.json`.


**Exemple d’usage** :
- Depuis la fenêtre principale, vous cliquez sur “All Saved Weapons Mod” :  
  - `ListItemAlreadyMod` est ouverte avec `window_type=WEAPON`, affichant la liste de tous les fichiers `_mod.json` existants pour les armes.  
  - Un clic sur un item ouvre `SingleWeaponMod` pour cette arme.  
- Depuis la fenêtre principale, vous cliquez sur “Select mod to DELETE” :  
  - `ListItemAlreadyMod` est lancée avec `window_type=DELETE`.  
  - Tous les `*_mod.json` (armes et munitions) sont listés et un clic sur l’un d’eux le supprime instantanément. 
  - La liste est automatiquement rafraîchie.

---
# Utils
## JsonUtils

- **File**: `Utils/JsonUtils.py`  
- **Role**: Centralizes all operations on JSON files, including:
  - **Loading** and **saving** data (creating/deleting `_mod.json`).
  - **Manipulating** specific attributes (updates, value multiplications, etc.).
  - **Searching** for corresponding files (e.g., `find_json_file_with_name`, `find_caliber_json_config`).

- **Key Features**:  
  1. **Loading and Validating JSON**  
     - Methods like `load_json` or `load_json_and_add_path` ensure that the file exists and contains valid JSON.  
     - If a file is missing or contains unreadable content, an exception is raised (e.g., `FileNotFoundError`, `ValueError`).  
  
  2. **Managing `_mod.json` Files**  
     - `file_mod_exist(file_path)`, `return_json_mod(file_path)` check and return an associated `_mod.json` file for a base JSON.  
     - `save_json_as_new_file(data, file_path_new_json)` creates a `_mod.json` file, deleting the old one if it already exists.  
  
  3. **CRUD Operations (Create, Read, Update, Delete)**  
     - **Create**: `save_json_as_new_file` or `write_json` generates a new file, either from scratch or by overwriting an existing one.  
     - **Read**: `load_json`, `find_caliber_json_config`, and other methods locate a file within directories (`JSON_FILES_DIR_WEAPONS`, etc.).  
     - **Update**:  
       - `update_json_value` and `update_json_caliber` modify key-value pairs based on `WindowType` (weapon, ammo, caliber, PMC, etc.).  
       - `update_json_in_new_file_multi_choice` adds a partial path in the JSON hierarchy (`["item", "_props", key]`) to apply the new value.  
       - `update_or_multiply_final_key` handles percentage-based value multiplication for weapons with *WindowType.CALIBER* (e.g., +20%).  
     - **Delete**:  
       - `delete_file_if_exists` removes a file if present.  
       - `delete_all_mod` (for `WindowType.AMMO` or `WindowType.WEAPON`) deletes all existing `_mod.json` files in a directory.  
  
  4. **Filtering and Bulk Retrieval**  
     - Methods like `load_all_json_files_without_mod`, `load_all_json_files_weapons_mod`, or `load_all_json_ammo` facilitate batch loading of files.  
     - `load_all_name_json_mod` returns all weapons and ammunition as a list, useful for the `ListItemAlreadyMod` class.  
  
- **Usage Examples**:  
  - **Creating a new mod**: First, load the original JSON using `load_json(...)`. Then, modify the structure with `update_json_in_new_file_multi_choice`, and finally, `save_json_as_new_file(...)` generates the `_mod.json` file.  
  - **Deletion**: In the UI, clicking a *Delete* button calls `delete_file_if_exists(...)` to remove the `*_mod.json` file, triggering an interface update.  
  - **Batch Modification**: For all weapons of a specific caliber, retrieve their original JSON files, apply modifications with a coefficient, and save each weapon with `_mod.json`.  

# JsonUtils Module

The **JsonUtils** module is at the core of your application, as it standardizes access to **JSON** data and its updates. It also simplifies the implementation of new rules or support for new object types by ensuring a consistent read/write interface.

---
## Utils
- **File**: `Utils/Utils.py`  
- **Purpose**: Provides various generic or specialized functions useful for interface handling and data manipulation.  

### Main Responsibilities

1. **Interface Management**  
   - **Widget Cleanup and Configuration**:  
     - `clear_frame`: Clears the contents of a frame and resets its row/column layout.  
     - `configure_grid`, `create_grid_row_col_config`: Helps configure grids (rows, columns, resizing weight, etc.).
   - **Helper Functions for Sub-frame Creation** (e.g., `create_5x4_bottom`) to dynamically organize panels or buttons.

2. **Numeric Value Handling**  
   - `float_to_scaled_int`: Converts a float into a *scaled_int* integer and a *scale_factor*.
   - `determine_format_spec`: Calculates a format (`.2f`, `.3f`, etc.) to display a number with the appropriate decimal precision.

3. **File Filtering and Moving**  
   - `remove_file_by_name`, `move_file_between_lists`, `transfer_file_between_lists`: These methods manage file path lists (e.g., moving a file from a "source" list to a "target" list).
   - `transform_list_of_strings`, `remove_json_extension`, etc.: Auxiliary functions to standardize file names (lowercase, removing `.json`, etc.).

4. **Limit Value Checking**  
   - `is_value_outside_limits_weapons`, `is_value_outside_limits_ammo`, `is_value_outside_limits_aiming`: Determines whether a percentage or value (e.g., ammo damage, fire rate) exceeds a threshold.
   - Thresholds are defined in specific `dicts` (e.g., min/max damage = `(1, 450)`).

5. **Interface Management in Case of Errors**  
   - `block_all_input_before_correction`, `disable_all_widgets_recursive`, `enable_all_widgets_recursive`: Allows mass **disabling/enabling** of widgets (buttons, sliders, etc.) in a hierarchical manner.
   - `unlock_all`, `unlock_all_buttons_recursive`: Restores user interaction after an error is resolved.

6. **Specific Methods for Tracer Ammunition**  
   - `apply_tracer_to_ammo_no_mod_again`, `apply_tracer_to_ammo_with_mod_exist_already`: Applies the "tracer" property (boolean or color) to all ammunition, including those that already have a `*_mod.json`.

### Usage Examples
- **Window Management**: In `ModSelectionWindow`, `Utils.clear_frame` is called to clear the area before recreating buttons.
- **Input Validation**: In `AmmoMod`, if the user enters an out-of-range value, `Utils.is_value_outside_limits_ammo` returns `True`, blocking controls and displaying an error message.
- **Global Modification**: In `apply_tracer_to_ammo_no_mod_again`, each ammunition file is processed, `JsonUtils` is used to load and save, and the "tracer = true + red/green" info is inserted via `Utils.modify_json_value`.

### Summary
In summary, **`Utils.py`** acts as a toolbox for other classes (interface or data manipulation) to avoid code duplication and centralize "utility" logic in one place.
---
## Config

- **File**: `config.py`
- **Purpose**:
  - Centralize paths to project directories (e.g., `JsonFiles/Weapons`, `JsonFiles/Ammo`, etc.).  
  - Ensure the project structure is consistent (existing and non-empty folders).  
  - Validate JSON files (e.g., correct certain default values for calibers).

#### Main Variables
1. **`BASE_DIR`**: The base directory, determined based on whether the application is executed as a `.exe` ("frozen" mode) or as a standard Python script.
2. **`JSON_FILES_DIR_*`**: References to subdirectories containing weapons (`Weaps`), calibers (`Calibers`), NPCs (`PMC`), ammo (`Ammo`), etc.
3. **`IMAGES_DIR`**: Contains graphical resources (icons, images).

#### Main Functions
1. **`check_project_structure()`**  
   - Checks for the existence of directories listed in `REQUIRED_DIRS`.  
   - Ensures they are not empty.  
   - Also validates the JSON format of all `*.json*` files in each directory (raises an error if a file is corrupted).

2. **`check_and_fix_json_caliber_files()`**  
   - Iterates through all JSON files related to calibers.  
   - If a numerical value (int/float) is too low or zero, it corrects it to `1.0` to prevent division by zero or invalid configurations.  
   - Displays a summary of modified files, missing files, or additional files based on an expected threshold (`caliber_max_min_count`).

3. **`check_json_files(directory)`**  
   - Validates each file in the given directory to ensure it contains valid JSON (e.g., no `JSONDecodeError`).

4. **`relative_path(path)`**  
   - Returns a path relative to `BASE_DIR`, useful for displaying shorter paths in logs.

#### Usage Examples

- **At Startup**: In `main.py` (or equivalent), these functions are called to verify the project structure (folders and JSON files) and possibly correct values for calibers.
- **Executable Mode**: The logic detects whether the application is launched as a `.exe` (PyInstaller or similar). In that case, the root path (`BASE_DIR`) is adjusted accordingly.
- **Logging**: When folders are missing or JSON files are unreadable, the script logs error messages and may halt execution to prevent later crashes.

This **`config.py`** file is essential for maintaining a consistent environment: it ensures that all resources (JSON files or folders) are in place and valid before starting the core of the application.

---

## JSON-File-Examples

This application relies on JSON files to describe objects (weapons, ammunition, etc.) that you want to modify. Below are two example files: one for ammunition (`.json` to be placed in `JsonFiles/Ammo/`) and another for a weapon (`.json` to be placed in `JsonFiles/Weapons/`).

### Example: Ammunition

#### File: `45_ACP_AP.json`

```json
{
  "item": {
    "_id": "5efb0cabfb3e451d70735af5",
    "_name": "patron_1143x23_acp_ap",
    "_props": {
      "ArmorDamage": 48,
      "Caliber": "Caliber1143x23ACP",
      "Damage": 66,
      "InitialSpeed": 299,
      "PenetrationPower": 38,
      "StackMaxSize": 50,
      "Tracer": false,
      "TracerColor": "red"
    }
  },
  "locale": {
    "Name": ".45 ACP AP",
    "ShortName": "AP"
  }
}
```

### Example: Weapon

#### File: `weapon_kbp_9a91_9x39.json`

```json
{
  "item": {
    "_id": "644674a13d52156624001fbc",
    "_name": "weapon_kbp_9a91_9x39",
    "_props": {
      "CameraSnap": 2.2,
      "AimSensitivity": 0.65,
      "Ergonomics": 50,
      "RecoilCamera": 0.05,
      "RecoilForceBack": 280,
      "RecoilForceUp": 110,
      "RecolDispersion": 14,
      "Weight": 0.92,
      "ammoCaliber": "Caliber9x39",
      "bFirerate": 700
    }
  },
  "locale": {
    "Name": "KBP 9A-91 9x39 compact assault rifle",
    "ShortName": "9A-91"
  }
}
```

With this structured format, the application can easily identify each object (via `item._id` and `item._name`), retrieve and display its properties (`_props`), then create (or update) separate mods (`*_mod.json`) to ensure your original files remain untouched.

### Explanation
- When a JSON file is loaded, its values are extracted and used to initialize an `Ammo` object.
- `props.get(EnumAmmo.DAMAGE.label, None)` retrieves the attribute's value from the JSON file.
- Each property is stored as a tuple containing the value and its original label to ensure clear tracking.
- The `convert_to_boolean` method is used to convert certain attributes (`TracerColor`) from String to Boolean format as needed.

This model is also used for `Weapon` objects, following the same logic of linking JSON data to Python objects handled within the application.
---
## Dependencies
- **Python** 3.9+
- **customtkinter**
- **CTkMessagebox**
- **Pillow**
- (See `requirements.txt` for the full list of required libraries.)