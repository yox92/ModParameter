# ModParameter App

## Project Overview

1. **ModParameter** is a mod for **SPT-AKI** that allows users to dynamically modify **weapon statistics, ammunition properties, and PMC attributes** through a **graphical Python interface** with an executable `.exe` file. This mod enhances gameplay customization by enabling direct item and character modifications within the game.
2. The Python program will automatically generate JSON files that can be retrieved, corrected, and used to implement objects in the SPT database. Automation can only take place if the file structure is strictly followed, ensuring that the Python program has full visibility on the generated files.
   👉 "Read the README.md file for more information."
---


## 📂 TypeScript Project Structure

```
ModParameter/
│-- ModParameter.exe       # Python exe file
│-- py/                    # Python GUI files
│-- │--JsonFiles           # JsonFiles Stock Modif. HERE
│-- │--│--Weapons           
│-- │--│--Ammo
│-- │--│--PMC
│-- src/                   # TypeScript source code
│   │-- Entity/            # Game entity definitions
│   │-- ListIdItem/        # Item ID management
│   │-- Service/           # Core services for modifying data
│   │   │-- AimingService.ts
│   │   │-- ItemService.ts
│   │   │-- ItemUpdaterService.ts
│   │   │-- JsonFileService.ts
│   │   │-- PmcService.ts
│   │-- Utils/             # Utility functions
│   │   │-- ValidateUtils.ts
│   │-- caliber.ts         # Ammunition calibers
│   │-- config.ts          # Configuration settings
│   │-- mod.ts             # Main mod entry point
│   │-- scrap_ammo.ts      # Ammunition modification script
│   │-- scrap_weapon.ts    # Weapon modification script
│-- README.md
│-- package.json           # Project dependencies
│-- tsconfig.json          # TypeScript configuration
```

---

## 🔧 Core Components & Features

### **AttributMod (Main Mod Class)**

The `AttributMod` class implements the `IPostDBLoadMod` interface for **SPT-AKI**. It modifies game data **after the database is loaded**, using `ItemService` and `PmcService` to apply changes.

#### ✅ Features:
- **Dependency Injection:** Uses `tsyringe` to inject required services.
- **Game Data Modification:** Alters **Weapons, ammunition, and PMC attributes**.
- **Error Handling:** Ensures essential dependencies (`DatabaseServer`, `ILogger`) are available.

#### 🔹 Key Method:
```typescript
postDBLoad(dependencyContainer: DependencyContainer): void
```
- Loads dependencies and retrieves game data.
- Applies modifications through `updateItems()` and `updatePmc()`.

#### 📌 Dependencies:
- **`DatabaseServer`** – Access to game database tables.
- **`ILogger`** – Logs information and errors.
- **`ItemService`** – Handles item modifications.
- **`PmcService`** – Manages PMC attribute updates.

---

### **PmcService (PMC Attribute Management)**

Handles **Player Main Character (PMC) attribute updates**, utilizing external services for data management.

#### ✅ Features:
- Reads **JSON configuration files** via `JsonFileService`.
- Applies **aiming modifications** using `AimingService`.
- Logs updates and errors with `ILogger`.

#### 🔹 Key Method:
```typescript
updatePmc(): void
```
- Loads **aiming configuration JSON**.
- Parses and applies modifications to **PMC aiming attributes**.

#### 📌 Dependencies:
- **`ILogger`** – Logging service.
- **`JsonFileService`** – Loads JSON configurations.
- **`AimingService`** – Applies aiming changes.

---
# ItemService

## Overview
The `ItemService` class is responsible for loading JSON files containing item data (weapons and ammunition) and applying modifications to them within the SPT game environment. This service ensures that the JSON data follows the required structure and applies appropriate updates using the `ItemUpdaterService`.

## Features
- Loads JSON data for weapons and ammunition.
- Validates the structure of the JSON files before processing.
- Applies modifications to weapons and ammunition.
- Logs warnings when encountering invalid or missing data.

## Class Methods
### `updateItems()`
This method initiates the process of updating weapons and ammunition:
- Loads JSON files using `JsonFileService`.
- Calls `caseWeapons()` to process weapon modifications.
- Calls `caseAmmo()` to process ammunition modifications.

### `caseWeapons(jsonWeaponsFiles)`
Processes weapon JSON files:
- Checks for missing or invalid weapon data.
- Extracts `ItemProps` and `Locale` from the JSON.
- Applies modifications using `ItemUpdaterService`.

### `caseAmmo(jsonAmmoFiles)`
Processes ammunition JSON files:
- Validates ammo data structure.
- Extracts `Ammo` properties.
- Creates `Ammo` instances using `createItemAmmo`.
- Applies modifications using `ItemUpdaterService`.

## Usage
To use the `ItemService`, instantiate it with a logger and database reference:

---
# ItemUpdaterService

## Overview
The `ItemUpdaterService` class is responsible for applying modifications to in-game items in the SPT (Single Player Tarkov) ecosystem. It maps JSON-defined modifications onto existing SPT items, ensuring that only valid values are applied.

This service primarily works with two types of items:
- **Ammunition (`Ammo`)**
- **Weapons (`ItemProps`)**

## Functionality
The `ItemUpdaterService` processes item updates through two main methods:
1. **applyAmmoModifications**: Updates ammunition properties such as damage, penetration power, initial speed, and tracer attributes.
2. **applyWeaponsModifications**: Updates weapon attributes like recoil, ergonomics, fire rate, and aiming sensitivity.

### How it Works
- The service extracts the relevant item from the SPT database (`iDatabaseTables`).
- It validates and casts each modification from the JSON input using `ValidateUtils`.
- If any value is invalid, the modification is skipped, and a warning is logged.
- If all values are valid, they are applied to the item's `_props`.
- The service logs success or failure messages accordingly.

## Notes
- This service only modifies properties that exist within `_props` of an `ITemplateItem`.
- If the database structure is invalid or an item is missing, the modification process is aborted.


### **AimingService (Aiming Attribute Adjustments)**

Handles **aiming-related parameters** for the **PMC**, ensuring valid values are assigned.

#### ✅ Features:
- Modifies **aiming attributes** (e.g., **recoil, aim stability**).
- Uses `ValidateUtils` for data validation.
- Logs changes for debugging purposes.

#### 🔹 Key Method:
```typescript
applyModifications(aimingJson: Aiming, iDatabaseTables: IDatabaseTables): boolean
```
- Reads **JSON aiming data** and updates the **game’s aiming attributes**.

---


# Pattern Database item props structure

DatabaseServer
├── templates
│   ├── items                
│   │   ├── weapon_XXX      
│   │   │   ├── _id: string
│   │   │   ├── _name: string
│   │   │   ├── _props: ItemProps
│   │   │   │   ├── CameraSnap: number
│   │   │   │   ├── AimSensitivity: number
│   │   │   │   ├── Ergonomics: number
│   │   │   │   ├── RecoilCamera: number
│   │   │   │   ├── RecoilForceBack: number
│   │   │   │   ├── RecoilForceUp: number
│   │   │   │   ├── RecolDispersion: number
│   │   │   │   ├── Weight: number
│   │   │   │   ├── ammoCaliber: string
│   │   │   │   ├── bFirerate: number
│   │   ├── ammo_XXX        
│   │   │   ├── _id: string
│   │   │   ├── _name: string
│   │   │   ├── _props: Ammo
│   │   │   │   ├── ArmorDamage: number
│   │   │   │   ├── Caliber: string
│   │   │   │   ├── Damage: number
│   │   │   │   ├── InitialSpeed: number
│   │   │   │   ├── PenetrationPower: number
│   │   │   │   ├── StackMaxSize: number
│   │   │   │   ├── Tracer: boolean
│   │   │   │   ├── TracerColor: string
├── globals
│   ├── config
│   │   ├── Aiming
│   │   │   ├── AimPunchMagnitude: number
│   │   │   ├── RecoilDamping: number
│   │   │   ├── RecoilHandDamping: number
│   │   │   ├── RecoilIntensityStanding: number
│   │   │   ├── RecoilIntensityCrouching: number
│   │   │   ├── RecoilIntensityProne: number
│   │   │   ├── RecoilXIntensityByPose
│   │   │   │   ├── x: number
│   │   │   │   ├── y: number
│   │   │   │   ├── z: number
│   │   │   ├── RecoilYIntensityByPose
│   │   │   │   ├── x: number
│   │   │   │   ├── y: number
│   │   │   │   ├── z: number
│   │   │   ├── RecoilZIntensityByPose
│   │   │   │   ├── x: number
│   │   │   │   ├── y: number
│   │   │   │   ├── z: number




