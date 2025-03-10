import * as fs from "fs";
import * as path from "path";
import {ILogger} from "@spt-aki/models/spt/utils/ILogger";
import {config} from "../config";
import {ItemType} from "../Entity/Enum";


export class JsonFileService {
    private readonly jsonWeaponFolderPath: string;
    private readonly jsonAimingFolderPath: string;
    private readonly jsonAmmoFolderPath: string;
    private readonly logger: ILogger;

    constructor(logger: ILogger) {
        this.jsonWeaponFolderPath = config.jsonWeaponFolderPath;
        this.jsonAimingFolderPath = config.jsonAimingFolderPath;
        this.jsonAmmoFolderPath = config.jsonAmmoFolderPath;
        this.logger = logger;
    }

    /**
     * Checks if the directory exists.
     * @returns `true` if the folder exists, `false` otherwise.
     */
    private doesFolderExist(folderPath:string): boolean {
        if (!fs.existsSync(folderPath)) {
            this.logger.warning(`[AttributMod] [JsonFileService] Folder not found: ${folderPath}`);
            return false;
        }
        return true;
    }

    public loadJsonAimingFile(): { fileName: string; jsonData: any } | null {
        if (!this.doesFolderExist(this.jsonAimingFolderPath)) {
            this.logger.warning("[AttributMod] PMC folder does not exist.");
            return null;
        }
        let jsonFiles: string[];

        try {
            jsonFiles = fs.readdirSync(this.jsonAimingFolderPath)
                .filter(file => file.endsWith("mod.json"));
        } catch (error) {
            this.logger.warning(`[AttributMod] Failed to read directory: ${error}`);
            return null;
        }

        if (jsonFiles.length === 0) {
            this.logger.warning("[AttributMod]  No JSON file found in the PMC folder.");
            return null;
        }

        const file = jsonFiles[0];
        const filePath = path.join(this.jsonAimingFolderPath, file);

        try {
            const rawData = fs.readFileSync(filePath, "utf-8");
            const parsedData = JSON.parse(rawData);

            if (!parsedData || typeof parsedData !== "object") {
                this.logger.warning(`[AttributMod] Invalid JSON format in file: ${file}`);
                return null;
            }

            return {fileName: file, jsonData: parsedData};
        } catch (error) {
            this.logger.warning(`[AttributMod] Error reading or parsing file ${file}: ${error}`);
            return null;
        }
    }

    public loadJsonFiles(itemType: ItemType): { fileName: string; json: any }[] {
        let folderPath: string;
        if (itemType === ItemType.Ammo) {
            folderPath = this.jsonAmmoFolderPath
        }
        else if (itemType === ItemType.Weapon) {
            folderPath = this.jsonWeaponFolderPath
        }
        else {
            return [];
        }

        if (!this.doesFolderExist(folderPath)) {
            this.logger.error(`[AttributMod] Folder does not exist`);
            return [];
        }

        try {
            const files = fs.readdirSync(folderPath);
            const jsonFiles = files.filter(file => file.endsWith("mod.json"));

            if (jsonFiles.length === 0) {
                this.logger.warning("[AttributMod] JSON files found");
                return [];
            }

            const parsedFiles = jsonFiles.map(file => {
                const filePath = path.join(folderPath, file);

                try {
                    const rawData = fs.readFileSync(filePath, "utf-8");
                    return {fileName: file, json: JSON.parse(rawData)};
                } catch (error) {
                    this.logger.warning(`[AttributMod] Error parsing JSON file ${file}: ${error.message}`);
                    return null;
                }
            });

            return parsedFiles.filter(Boolean) as { fileName: string; json: any }[];
        } catch (error) {
            this.logger.warning(`[AttributMod] Error reading directory ${folderPath}: ${error.message}`);
            return [];
        }
    }
}
