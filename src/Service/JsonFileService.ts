import * as fs from "fs";
import * as path from "path";
import {ILogger} from "../Entity/Logger";
import {config} from "../config";


export class JsonFileService {
    private readonly jsonWeaponFolderPath: string;
    private readonly jsonAimingFolderPath: string;
    private readonly logger: ILogger;

    constructor(logger: ILogger) {
        this.jsonWeaponFolderPath = config.jsonWeaponFolderPath;
        this.jsonAimingFolderPath = config.jsonAimingFolderPath;
        this.logger = logger;
    }

    /**
     * Checks if the directory exists.
     * @returns `true` if the folder exists, `false` otherwise.
     */
    private doesFolderExist(): boolean {
        if (!fs.existsSync(this.jsonWeaponFolderPath)) {
            this.logger.warning(`[JsonFileService] Folder not found: ${this.jsonWeaponFolderPath}`);
            return false;
        }
        return true;
    }

    /**
     * Loads all JSON files from the specified directory.
     * @returns An array of objects containing file names and parsed JSON data.
     */
    public loadJsonWeaponsFiles(): { fileName: string; data: any }[] {
        if (!this.doesFolderExist()) {
            return [];
        }

        const jsonFiles = fs.readdirSync(this.jsonWeaponFolderPath).filter(file => file.endsWith("mod.json"));

        return jsonFiles.map(file => {
            const filePath = path.join(this.jsonWeaponFolderPath, file);
            try {
                const rawData = fs.readFileSync(filePath, "utf-8");
                return {fileName: file, data: JSON.parse(rawData)};
            } catch (error) {
                this.logger.error(`[JsonFileService] Error reading file ${file}: ${error}`);
                return null;
            }
        }).filter(Boolean) as { fileName: string; data: any }[];
    }

    public loadJsonAimingFile(): { fileName: string; data: any } | null {
        if (!this.doesFolderExist()) {
            this.logger.warning("[JsonFileService] PMC folder does not exist.");
            return null;
        }
        let jsonFiles: string[];

        try {
            jsonFiles = fs.readdirSync(this.jsonAimingFolderPath)
                .filter(file => file.endsWith("mod.json"));
        } catch (error) {
            this.logger.error(`[JsonFileService] Failed to read directory: ${error}`);
            return null;
        }

        if (jsonFiles.length === 0) {
            this.logger.warning("[JsonFileService] No JSON file found in the PMC folder.");
            return null;
        }

        const file = jsonFiles[0];
        const filePath = path.join(this.jsonAimingFolderPath, file);

        try {
            const rawData = fs.readFileSync(filePath, "utf-8");
            const parsedData = JSON.parse(rawData);

            if (!parsedData || typeof parsedData !== "object") {
                this.logger.error(`[JsonFileService] Invalid JSON format in file: ${file}`);
                return null;
            }

            return {fileName: file, data: parsedData};
        } catch (error) {
            this.logger.error(`[JsonFileService] Error reading or parsing file ${file}: ${error}`);
            return null;
        }
    }

}
