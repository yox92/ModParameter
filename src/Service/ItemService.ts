import {ItemUpdaterService} from "./ItemUpdaterService";
import {JsonFileService} from "./JsonFileService";
import {ILogger} from "@spt-server/models/spt/utils/ILogger";
import {IDatabaseTables} from "@spt-server/models/spt/server/IDatabaseTables";


export class ItemService {
    private readonly logger: ILogger;
    private readonly iDatabaseTables: IDatabaseTables;
    private readonly jsonFileService: JsonFileService;
    private readonly itemUpdaterService: ItemUpdaterService;

    constructor(logger: ILogger, iDatabaseTables: IDatabaseTables) {
        this.logger = logger;
        this.iDatabaseTables = iDatabaseTables;

        this.jsonFileService = new JsonFileService(logger);
        this.itemUpdaterService = new ItemUpdaterService(logger);
    }

    /**
     * Load JSON and apply mod into SPT weapon in game
     */
    public updateItems(): void {
        const jsonWeaponsFiles = this.jsonFileService.loadJsonWeaponsFiles();
        const jsonAmmoFiles = this.jsonFileService.loadJsonAmmoFiles();
        let countModified = 0;


        if (jsonWeaponsFiles.length === 0) {
            this.logger.info("[WeaponService] No weapon mod found. Skipping weapon updates.");}

        if (jsonAmmoFiles.length === 0) {
            this.logger.info("[ItemService] No ammo found. Skipping ammo updates.");}

        for (const {fileName, data} of jsonWeaponsFiles) {
            const itemId = data.item._id;
            if (!data || !data.item || !data.item._id) {
                this.logger.info(`[WeaponService] Skipping invalid or missing weapon: ${fileName}`);
                continue;
            }

            if (this.itemUpdaterService.applyModifications(data, this.iDatabaseTables)) {
                countModified++;
            }
        }

        for (const {fileName, data} of jsonAmmoFiles) {
            const itemId = data.item._id;
            if (!data || !data.item || !data.item._id) {
                this.logger.warning(`[ItemService] Skipping invalid or missing ammo: ${fileName}`);
                continue;
            }

            if (!tables.templates.items[itemId]) {
                this.logger.warning(`[ItemService] No ammo found in DB for name: ${fileName}, ID: ${itemId}`);
                continue;
            }

            const sptItem = tables.templates.items[itemId];

            if (this.itemUpdaterService.applyModifications(data, sptItem)) {
                countModified++;
            }

            this.logger.info(`[WeaponService] Modifications applied to ${countModified} item(s).`);
        }
    }
}