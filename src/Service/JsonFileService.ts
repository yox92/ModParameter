import * as fs from "fs";
import * as path from "path";
import {ILogger} from "@spt/models/spt/utils/ILogger";
import {config} from "../config";
import {ItemTypeEnum} from "../Entity/ItemTypeEnum";


export class JsonFileService {
    private readonly jsonWeaponFolderPath: string;
    private readonly jsonAimingFolderPath: string;
    private readonly jsonAmmoFolderPath: string;
    private readonly jsonMedicFolderPath: string;
    private readonly jsonMagFolderPath: string;
    private readonly jsonBagFolderPath: string;
    private readonly jsonBuffFolderPath: string;
    private readonly jsonFastFolderPath: string;
    private readonly logger: ILogger;

    constructor(logger: ILogger) {
        this.jsonWeaponFolderPath = config.jsonWeaponFolderPath;
        this.jsonAimingFolderPath = config.jsonAimingFolderPath;
        this.jsonAmmoFolderPath = config.jsonAmmoFolderPath;
        this.jsonMedicFolderPath = config.jsonMedicFolderPath;
        this.jsonMagFolderPath = config.jsonMagFolderPath;
        this.jsonBagFolderPath = config.jsonBagFolderPath;
        this.jsonBuffFolderPath = config.jsonBuffFolderPath;
        this.jsonFastFolderPath = config.jsonFastFolderPath;
        this.logger = logger;
    }

    /**
     * Checks if the directory exists.
     * @returns `true` if the folder exists, `false` otherwise.
     */
    private doesFolderExist(folderPath: string): boolean {
        if (!fs.existsSync(folderPath)) {
            this.logger.debug(`[ModParameter] [JsonFileService] Folder not found: ${folderPath}`);
            return false;
        }
        return true;
    }

    public loadJsonAimingFile(): { fileName: string; jsonData: any } | null {
        if (!this.doesFolderExist(this.jsonAimingFolderPath)) {
            this.logger.debug("[ModParameter] PMC folder does not exist.");
            return null;
        }
        let jsonFiles: string[];

        try {
            jsonFiles = fs.readdirSync(this.jsonAimingFolderPath)
                .filter(file => file.endsWith("mod.json"));
        } catch (error) {
            this.logger.debug(`[ModParameter] Failed to read directory: ${error}`);
            return null;
        }

        if (jsonFiles.length === 0) {
            this.logger.debug("[ModParameter]  No JSON file found in the PMC folder.");
            return null;
        }

        const file = jsonFiles[0];
        const filePath = path.join(this.jsonAimingFolderPath, file);

        try {
            const rawData = fs.readFileSync(filePath, "utf-8");
            const parsedData = JSON.parse(rawData);

            if (!parsedData || typeof parsedData !== "object") {
                this.logger.debug(`[ModParameter] Invalid JSON format in file: ${file}`);
                return null;
            }

            return {fileName: file, jsonData: parsedData};
        } catch (error) {
            this.logger.debug(`[ModParameter] Error reading or parsing file ${file}: ${error}`);
            return null;
        }
    }

    public loadJsonFiles<T>(itemType: ItemTypeEnum): Array<{ fileName: string; json: T }> {
        let folderPath: string;
        if (itemType === ItemTypeEnum.Ammo || itemType === ItemTypeEnum.Tracer) {
            folderPath = this.jsonAmmoFolderPath
        } else if (itemType === ItemTypeEnum.Weapon) {
            folderPath = this.jsonWeaponFolderPath
        } else if (itemType === ItemTypeEnum.Medic) {
            folderPath = this.jsonMedicFolderPath
        } else if (itemType === ItemTypeEnum.Mag) {
            folderPath = this.jsonMagFolderPath
        } else if (itemType === ItemTypeEnum.Bag) {
            folderPath = this.jsonBagFolderPath
        } else if (itemType === ItemTypeEnum.Buff) {
            folderPath = this.jsonBuffFolderPath
        } else if (itemType === ItemTypeEnum.Fast) {
            folderPath = this.jsonFastFolderPath
        } else {
            return [];
        }

        if (!this.doesFolderExist(folderPath)) {
            this.logger.debug(`[ModParameter] Folder does not exist`);
            return [];
        }

        try {
            const files: string[] = fs.readdirSync(folderPath);
            let jsonFiles: string[];
            if (itemType === ItemTypeEnum.Tracer) {
                jsonFiles = files.filter(file => file.includes("tracer.json"));
            } else if (itemType === ItemTypeEnum.Mag) {
                jsonFiles = files.filter(file => file.includes("Mag.json"));
             } else if (itemType === ItemTypeEnum.Fast) {
                jsonFiles = files.filter(file => file.includes("Fast.json"));
            } else {
                jsonFiles = files.filter(file => file.endsWith("mod.json"));
            }

            if (jsonFiles.length === 0) {
                this.logger.debug(`"[ModParameter] No JSON files found for ${itemType}"`);
                return [];
            }

            const parsedFiles: Array<{ fileName: string; json: T } | null> = jsonFiles.map((file: string): {
                fileName: string; json: T
            } | null => {
                const filePath = path.join(folderPath, file);

                try {
                    const rawData = fs.readFileSync(filePath, "utf-8");
                    return {fileName: file, json: JSON.parse(rawData)};
                } catch (error) {
                    this.logger.debug(`[ModParameter] Error parsing JSON file ${file}: ${error.message}`);
                    return null;
                }
            });

            return parsedFiles.filter((f): f is { fileName: string; json: T } => f !== null)
        } catch (error) {
            this.logger.debug(`[ModParameter] Error reading directory ${folderPath}: ${error.message}`);
            return [];
        }
    }
}
