# ModParameter App

## 📖 Table of Contents  

- [🎮ModParameter App](#modparameter-app)  
- [📝Note](#Notes)
- [📌Features](#Features)  
  - [Assign Tracers to Bullets]()
  - [Search for a Weapon](#1-search-for-a-weapon-by-its-name-using-a-search-bar-to-mod-it)  
  - [Modify Weapons by Caliber](#2-select-a-group-of-weapons-based-on-their-calibers-to-mod-all)  
  - [Modify Ammunition](#3-organize-bullet-search-based-on-their-caliber-categories-to-allow-modifications)  
  - [Modify PMC Attributes](#4-modifying-pmc-attributes-in-eft)
  - [Save Modifications](#6-saving-your-modifications-made-to)  
  - [Deletion Options](#7-deletion)
- [🎯 Main Classe](#Main-Classe)
- [📂 Project Structure](#-typescript-project-structure)  
- [📂Database Structure](#-pattern-database-item-props-structure)  
- [🔍Weapon & Ammo Data Fetcher](#weapon--ammo-data-fetcher)  
- [📝License](#license)  
- [🌐Author & Contact](#author)

# Project Overview

**ModParameter** is a mod for **SPT** that allows users to dynamically modify **weapon statistics, ammunition properties, and PMC attributes** through a **graphical Python interface** with an executable `.exe` file. This mod enhances gameplay customization by enabling direct modifications to cloned items within the game.

The Python program automatically generates JSON files that define the properties of the cloned objects. These files can be retrieved, edited, and applied to the SPT database. Automation is only possible if the file structure is strictly followed, ensuring that the Python program can properly read and apply changes to the generated files.

📌 **"Read the README.md file for more information."**

---

## Notes

#### Saving mod' item strategy

- This mod no longer modifies your original items. All changes are applied to a copy of the item you choose to modify, preserving the game's original balance. Copies have a unique identifier, so even if you disconnect,
they remain in your inventory. Modifications won't delete your copied item but will simply update its newly defined properties. If you decide to remove a modification,
on your next login, the mod will detect the missing copy and replace it with the original version.
- If you decide to DELETE this mod, please remove all modifications and log in one last time to allow the mod to restore everything properly.

-  If this value is set to true, then the following scenario will apply:
  * You mod an object
  * You play the game
  * You disconnect
  * You disable the modding of the object 
  * Upon your next login, the object will be deleted
Hope this is clear enough! 😄
---

## Features

####  Ability to assign "tracer" to all bullets in the game and choose their color

### 1. Search and Modify Weapons
- Search for a **weapon** by its name using a search bar to modify it.
- Select a group of **weapons** based on their calibers to modify them all at once.
- Any modifications apply to a **cloned version** of the weapon instead of the original.

#### 📌 **Weapon Attributes**
- **CameraSnap**: Speed at which the camera moves during recoil.
- **AimSensitivity**: Sensitivity while aiming.
- **AimProceduralIntensity**: Movement while walking with a scope (stability movement).
- **Ergonomics**: The weapon's ergonomics.
- **RecoilCamera**: Upward camera movement when firing.
- **RecoilDispersion**: Barrel dispersion when firing.
- **RecoilForceBack**: Horizontal recoil.
- **RecoilForceUp**: Vertical recoil.
- **Weight**: The weapon's weight.
- **bFirerate**: Rate of fire.

### 2. Modify Ammunition Attributes
- Organize bullet search based on their caliber categories for easy modifications.
- Any modifications apply to a **cloned version** of the ammunition instead of the original.

#### 📌 **Ammo Attributes**
- **ArmorDamage**: Damage dealt by the bullet to armor.
- **Damage**: Raw damage a bullet deals to flesh (excluding armor absorption).
- **PenetrationPower**: Bullet penetration power.
- **InitialSpeed**: Bullet speed.
- **Tracer**: Defines whether the bullet has tracer properties.
- **TracerColor**: Specifies the tracer bullet color if applicable.
- **StackMaxSize**: Maximum number of bullets per stack in the stash and during a raid.
- **Ballistic Coefficient** – Determines bullet aerodynamics and impact over distance.
- **Bullet Mass** : Take into account the bullet's velocity during its trajectory and fall
- **Ammo Accuracy Bonus** – Bonus ammo , Modifies shot accuracy.
- **Recoil Bonus ammo** : Adjusts weapon kickback for better control.
- **Projectile Count** – Defines the number of pellets per shot (useful for shotguns)
  * 💣 💣 💣 Be careful with this parameter 50 rounds can be fired at the same time with single bullet bullets. With tracers, it creates a beautiful fireworks display, but your RAM and CPU usage will suffer if the value is too high.

### 3. Modify PMC Attributes in Escape from Tarkov
Modify various PMC attributes to fine-tune gameplay. Changes only affect the **cloned versions** of related entities.

#### 📌 **PMC Attributes**
- **AimPunchMagnitude**: Intensity of the camera movement when hit by a bullet.
- Reduce **movement on aiming** while you **walking** (**stability** on walking on scope)
- **RecoilHandDamping**: Forward and backward camera movement when firing.
- **RecoilDamping**: Vertical animation of the weapon when firing.
- **ProceduralIntensity**: Defines player stability when aiming. Initially set at 1 (100%).
  - **ProceduralIntensityByPoseStanding**: Sway while standing.
  - **ProceduralIntensityByPoseCrouching**: Sway while crouching.
  - **ProceduralIntensityByPoseProne**: Sway while prone.
    * **Recommended**: Modify **ProceduralIntensityByPoseStanding** as it serves as the reference value. Adjusting this will affect the others proportionally.

- **RecoilIntensity**: Player's overall recoil across all weapons. Follows the same logic as **ProceduralIntensity**.
  - **RecoilIntensityStanding**: Recoil while standing.
  - **RecoilIntensityCrouching**: Recoil while crouching.
  - **RecoilIntensityProne**: Recoil while prone.

---

## Installation
1. Download the latest version of **ModParameter**.
2. Extract the files into your `spt/user/mods` folder.
3. Run the Python interface executable (`.exe` file) to configure your modifications.
4. Start the game and enjoy your customized **cloned** items!
 * 🛠️ Use console `cmd`/ `PowerShell` to show terminal to execute `ModParameter.exe` 🛠️
---

### 6. Saving your modifications made to:
   * A group of weapons
   * A specific weapon
   * A specific bullet
   * Attributes PMC
- When you return to modify an item / PMC, your changes are saved. If you delete the modification, the save is removed.

### 7. Deletion
- Reset to default values ==> removes the save and all modifications (Weapons / Bullets / PMC)
- Delete a specific item
- Delete all weapon modifications
- Delete all bullet modifications
---
## Schéma fonctionnement
````
----------------+          +---------------+       +-------------+       +--------------+
|  Python Script  | ======> | JsonFiles Dir | ====> |  mod.js     | ====> |  SPT DB      |
|  (Generate .json) |       | (Store files) |       | (Load JSON) |       | (Map data)   |
+------------------+       +---------------+       +-------------+       +--------------+
````

---
# Main Classe

## ItemClonerService

**ItemClonerService** is a service that enables dynamic cloning of **weapons and ammunition** in **SPT**. Instead of modifying the original items, this class creates **cloned versions** with customized properties, ensuring safe and flexible game modifications. It integrates seamlessly with the database, handles validation, and ensures that cloned items are correctly registered in the game mechanics. The service supports:

- Cloning **ammo and weapons** based on modified properties.
- Ensuring compatibility with traders and game mechanics.
- Managing localized names and attributes.
- Logging errors and debugging missing parameters.

## ItemUpdaterService

The **ItemUpdaterService** class is responsible for applying modifications to weapons and ammunition properties in the **SPT-AKI** game database. It ensures data validation and prevents invalid modifications by leveraging utility functions. This service retrieves item templates from the database, validates user-defined modifications, and applies changes only if all values are valid. The class supports updating key attributes such as recoil, damage, penetration power, ergonomics, and rate of fire while maintaining game integrity.

## ClonerUtils

**ClonerUtils** is a utility class for **SPT** that manages the cloning and distribution of weapons and ammunition. It ensures that cloned items are correctly assigned to traders while preserving barter schemes and loyalty levels. Additionally, it propagates compatibility adjustments for cloned items, updating magazine and weapon slot filters to include the newly cloned IDs. This maintains consistency and seamless integration of cloned items within the game's ecosystem.

## ClearCloneService

The ClearCloneService ensures that unused cloned weapons and ammunition are automatically replace to original from player inventories and insured items.
It identifies cloned items still present in the game and filters them out, replacing obsolete clones with their original counterparts.
- Preserves Game Balance: Clones are replaced with their original versions if removed.
- Automatic Inventory Cleanup: Detects and removes outdated cloned items upon login.
- Safe and Efficient: Prevents unnecessary modifications while maintaining player progress.

## 📂 TypeScript Project Structure

```
ModParameter/
│-- ModParameter.exe       # Python exe file 
│-- package.json           # Project dependencies
│-- tsconfig.json          # TypeScript configuration
│-- node_modules           # Dependancies
│-- py/                    # Python GUI files
│-- │--JsonFiles           # JsonFiles Stock Modif. HERE
│-- │--│--Weapons           
│-- │--│--Ammo
│-- │--│--PMC
│-- │--│--Calibers
│-- src/                   # TypeScript source code
│   │-- external/          # (optional) import SPT-server
│   │-- Entity/            # Game entity definitions
│   │-- ListIdItem/        # Item ID management
│   │-- ToolsTypeScript/   # (optional) Script for me to update itemID/generate mongoID
│   │-- Utils/             # Class Utils
│   │-- Service/           # Core services for modifying data
│   │   │-- AimingService.ts
│   │   │-- ItemService.ts
│   │   │-- ItemUpdaterService.ts
│   │   │-- ItemClonerService.ts
│   │   │-- JsonFileService.ts
│   │   │-- EnumUtils.ts
│   │   │-- PmcService.ts
│   │   │-- ValidateUtils.ts
│   │-- caliber.ts         # generate json calibers data
│   │-- config.ts          # Configuration settings
│   │-- mod.ts             # Main mod entry point
│   │-- scrap_ammo.ts      # Ammunition scrap data script
│   │-- scrap_weapon.ts    # Weapon scrap data script
│   │-- README.md

```

---

# Pattern Database item props structure
```
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
│   │   │   ├── AimProceduralIntensity: number
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
│   │   │   │   ├── RecoilIntensity: Same pattern than RecoilIntensityByPose
```
---
# Weapon & Ammo Data Fetcher
#### MongoDB ID Generator simple ID
This TypeScript module generates unique MongoDB ObjectIDs for weapons and ammunition in the SPT modding environment. It ensures that each item in predefined lists (WeaponEnum, AmmoEnum) receives a unique identifier while maintaining consistency across sessions by storing the mappings in JSON files. The script verifies existing mappings, generates new IDs if necessary, and saves them persistently. This utility facilitates data management by preventing duplicate ID assignments and ensuring reliable referencing of cloned game items.
#### MongoDB ID Generator ipl trader
Cette classe TypeScript permet d'extraire et de générer des identifiants MongoDB-like pour les objets du jeu **SPT-AKI** (armes et munitions) en créant des clones des éléments originaux. Elle scanne les fichiers de marchands dans la base de données du serveur, identifie les objets à dupliquer, et associe de nouveaux identifiants uniques aux clones. Le programme sauvegarde ces mappings dans un fichier JSON, garantissant une traçabilité et une persistance des modifications.
- Lecture et analyse des fichiers de marchands (`assort.json`).
- Création d'IDs uniques via `mongoid-js`.
- Gestion des mappings (_id original -> nouvel ID) et sauvegarde dans un fichier JSON.
---
## License
- This project follows the applicable license terms set by the SPT modding framework.
---
## Author

👤 **Yox**  
📧 Email: [vivien.hoyaux@gmail.com](mailto:vivien.hoyaux@gmail.com)  
   GitHub: [gitlab](https://github.com/yox92/ModParameter.git)
   Discord : yox_92 1235644139

Feel free to contact me for any questions!


