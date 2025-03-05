import * as fs from "fs";
import * as path from "path";
import {ILogger} from "../Entity/Logger";


export class JsonFileService {
    private readonly folderPath: string;
    private readonly logger: ILogger;

    constructor(folderPath: string, logger: ILogger) {
        this.folderPath = folderPath;
        this.logger = logger;
    }

    /**
     * Checks if the directory exists.
     * @returns `true` if the folder exists, `false` otherwise.
     */
    private doesFolderExist(): boolean {
        if (!fs.existsSync(this.folderPath)) {
            this.logger.warning(`[JsonFileService] Folder not found: ${this.folderPath}`);
            return false;
        }
        return true;
    }

    /**
     * Loads all JSON files from the specified directory.
     * @returns An array of objects containing file names and parsed JSON data.
     */
    public loadJsonFiles(): { fileName: string; data: any }[] {
        if (!this.doesFolderExist()) {
            return [];
        }

        const jsonFiles = fs.readdirSync(this.folderPath).filter(file => file.endsWith("mod.json"));

        return jsonFiles.map(file => {
            const filePath = path.join(this.folderPath, file);
            try {
                const rawData = fs.readFileSync(filePath, "utf-8");
                return { fileName: file, data: JSON.parse(rawData) };
            } catch (error) {
                this.logger.error(`[JsonFileService] Error reading file ${file}: ${error}`);
                return null;
            }
        }).filter(Boolean) as { fileName: string; data: any }[];
    }
}
