import {ItemUpdaterService} from "./ItemUpdaterService";
import {JsonFileService} from "./JsonFileService";
import path from "path";
import {IDatabaseServer} from "../Entity/DatabaseServer";
import {ILogger} from "../Entity/Logger";


export class WeaponService {
    private readonly logger: ILogger;
    private readonly database: IDatabaseServer;
    private readonly jsonFileService: JsonFileService;
    private readonly itemUpdaterService: ItemUpdaterService;

    constructor(logger: ILogger, database: IDatabaseServer) {
        this.logger = logger;
        this.database = database;
        const jsonFolderPath = path.join(__dirname, "..", "py", "JsonFiles");

        this.jsonFileService = new JsonFileService(jsonFolderPath, logger);
        this.itemUpdaterService = new ItemUpdaterService(logger);
    }

    /**
     * Load JSON and apply mod into SPT weapon in game
     */
    public updateWeapons(): void {
        const tables = this.database.getTables();
        const jsonFiles = this.jsonFileService.loadJsonFiles();
        let countModified = 0;

        for (const {fileName, data} of jsonFiles) {
            const itemId = data.item._id;

            if (!tables.templates.items[itemId]) {
                this.logger.warning(`[WeaponService] No item found in DB for name : ${fileName} ,  ID: ${itemId}`);
                continue;
            }

            const sptItem = tables.templates.items[itemId];

            if (this.itemUpdaterService.applyModifications(data, sptItem)) {
                countModified++;
            }
        }

        this.logger.info(`[WeaponService] Modifications applied to ${countModified} weapon(s).`);
    }
}