📖 AttributMod - Data Modification for SPT-AKI

🚀 Introduction

AttributMod is a mod for SPT-AKI that allows dynamic modification
of weapon statistics, ammunition, and PMC parameters through a graphical interface.

📂 Project Structure

AttributMod/
│── Entity/                 # JSON entity definitions
│── Service/                # Services for processing modifications
│── Utils/                  # Utilities and log management
│── config.ts               # Configuration paths
│── mod.ts                  # Main entry point
│── README.md               # This file

⚙️ Configuration

1️⃣ Using the Modification Tool

The user does not need to manually edit JSON files. Instead, 
they should execute the provided program:📂 Executable Path: py/main/ModParameters.exe

A graphical interface is available, allowing users to make the modifications they need. There are four main options:

Modify a specific weapon

Modify a group of weapons based on their caliber

Modify ammunition parameters

Modify PMC statistics

All changes are automatically saved into .json files for future use.

🏗️ Mod Functionality

📌 1. Loading JSON Files

📁 Service: JsonFileService.ts

Checks if directories exist

Loads and parses JSON files

Validates data integrity

📌 2. Applying Modifications

📁 Service: ItemService.ts and PmcService.ts

updateItems(): Modifies weapons and ammunition

updatePmc(): Modifies PMC parameters

📌 3. Modifying Game Database Values

📁 Service: ItemUpdaterService.ts

Verifies if the item exists in the game database

Validates JSON values

Applies modifications

🛠️ Installation and Usage

1️⃣ Installation

Extract the mod into the user/mods/ folder of SPT-AKI.

Run py/main/ModParameters.exe to access the modification tool.

2️⃣ Usage

Start the executable to open the graphical interface.

Make modifications through the provided options.

Changes will be saved automatically in JSON files.

🔍 Debugging and Logs

📁 Log File: logs.txt

Every applied modification is recorded.

In case of errors, detailed messages are displayed.

🎯 Future Features

✅ Support for additional items and equipment

✅ Advanced customization of statistics

🚀 User interface improvements for better usability

📝 Author

👤 Developed by: Netnikogo
📧 Contact: Discord ==> 

🚀 Thank you for using AttributMod! 🎯


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
