import path from "path";
import {LogTextColor} from "./Entity/LogTextColor";
import {LogBackgroundColor} from "@spt/models/spt/logging/LogBackgroundColor";

/**
 * path to file config weapons.
 */
export const config = {
    jsonWeaponFolderPath: path.join(__dirname, "..", "py", "JsonFiles", "Weapons"),
    jsonWCaliberFolderPath: path.join(__dirname, "..", "py", "JsonFiles", "Calibers"),
    jsonAimingFolderPath: path.join(__dirname, "..", "py", "JsonFiles", "PMC"),
    jsonAmmoFolderPath: path.join(__dirname, "..", "py", "JsonFiles", "Ammo"),
    jsonAmmoFolderPathNew: path.join(__dirname, "..", "py", "JsonFiles", "AmmoNew"),
};

export const debug = true;
export const colorTextDebug = LogTextColor.GRAY;
export const colorBackgroundDebug = LogBackgroundColor.BLACK;

