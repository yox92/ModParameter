import path from "path";

/**
 * path to file config weapons.
 */
export const config = {
    jsonWeaponFolderPath: path.join(__dirname, "..", "py", "JsonFiles", "Weapons"),
    jsonWCaliberFolderPath: path.join(__dirname, "..", "py", "JsonFiles", "Calibers"),
    jsonAimingFolderPath: path.join(__dirname, "..", "py", "JsonFiles", "PMC"),
    jsonAmmoFolderPath: path.join(__dirname, "..", "py", "JsonFiles", "Ammo"),
};
