import path from "path";
import {LogTextColor} from "./Entity/LogTextColor";
import {LogBackgroundColor} from "@spt/models/spt/logging/LogBackgroundColor";

/**
 * path to file config weapons.
 */
export const config = {
    jsonWeaponFolderPath: path.join(__dirname, "..", "py", "JsonFiles", "Weapons"),
    jsonWeaponFolderPathNew: path.join(__dirname, "..", "py", "JsonFiles", "WeaponsNew"),
    jsonWCaliberFolderPath: path.join(__dirname, "..", "py", "JsonFiles", "Calibers"),
    jsonAimingFolderPath: path.join(__dirname, "..", "py", "JsonFiles", "PMC"),
    jsonAmmoFolderPath: path.join(__dirname, "..", "py", "JsonFiles", "Ammo"),
    jsonAmmoFolderPathNew: path.join(__dirname, "..", "py", "JsonFiles", "AmmoNew"),
    jsonMedicFolderPath: path.join(__dirname, "..", "py", "JsonFiles", "Medic"),
    jsonMagFolderPath: path.join(__dirname, "..", "py", "JsonFiles", "Mag"),
};

export const debug = true;
export const colorTextDebug = LogTextColor.GRAY;
export const colorBackgroundDebug = LogBackgroundColor.BLACK;

