import {ItemUpdaterService} from "./ItemUpdaterService";
import {JsonFileService} from "./JsonFileService";
import {ILogger} from "@spt-aki/models/spt/utils/ILogger";
import {IDatabaseTables} from "@spt-aki/models/spt/server/IDatabaseTables";
import {Item} from "../Entity/Item";
import {ItemProps} from "../Entity/ItemProps";
import {Templates} from "../Entity/Templates";
import {Ammo, createItemAmmo} from "../Entity/Ammo";
import {ItemType} from "../Entity/Enum";
import {Locale} from "../Entity/Locale";

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
        this.itemClonerService = new ItemUpdaterService(logger);
    }

    private caseWeapons(jsonWeaponsFiles): void {
        for (const {fileName, json} of jsonWeaponsFiles) {
            if (!json) {
                this.logger.warning(`[AttributMod] Skipping invalid or missing weapon JSON data: ${fileName}`);
                continue;
            }

            const templateJson: Templates<ItemProps> = json;

            if (!templateJson.locale) {
                this.logger.warning(`[AttributMod] Skipping invalid or missing template Weapon: ${fileName}`);
                continue;
            }

            const locale: Locale = templateJson.locale

            if (!templateJson.item) {
                this.logger.warning(`[AttributMod] Skipping invalid or missing template Weapon: ${fileName}`);
                continue;
            }

            const itemsJson: Item<ItemProps> = templateJson.item;

            if (!itemsJson._props) {
                this.logger.warning(`[AttributMod] Skipping invalid or missing item Weapon: ${fileName}`);
                continue;
            }

            const itemsPropsJson: ItemProps = itemsJson._props;

            if (!itemsPropsJson) {
                this.logger.warning(`[AttributMod] Skipping invalid or missing ItemProps Weapon: ${fileName}`);
                continue;
            }

            this.itemUpdaterService.applyWeaponsModifications(
                itemsPropsJson,
                itemsJson._id,
                locale.ShortName,
                this.iDatabaseTables)
        }
    }

    private caseAmmo(jsonAmmoFiles) {
        for (const {fileName, json} of jsonAmmoFiles) {
            if (!json) {
                this.logger.warning(`[AttributMod] Skipping invalid or missing ammo JSON data: ${fileName}`);
                continue;
            }

            const templateJson: Templates<Ammo> = json;

            if (!templateJson.item) {
                this.logger.warning(`[AttributMod] Skipping invalid or missing template Ammo: ${fileName}`);
                continue;
            }

            if (!templateJson.locale) {
                this.logger.warning(`[AttributMod] Skipping invalid or missing template Weapon: ${fileName}`);
                continue;
            }

            const locale: Locale = templateJson.locale


            const itemsJson: Item<Ammo> = templateJson.item;

            if (!itemsJson._props) {
                this.logger.warning(`[AttributMod] Skipping invalid or missing item Ammo: ${fileName}`);
                continue;
            }

            const itemsPropsJson: Ammo = itemsJson._props;

            if (!itemsPropsJson) {
                this.logger.warning(`[AttributMod] Skipping invalid or missing ItemProps Ammo: ${fileName}`);
                continue;
            }

            const ammoProps: Ammo = createItemAmmo(itemsPropsJson);

            if (!ammoProps) {
                this.logger.warning(`[AttributMod] [AimingService] Invalid Json PMC update.`);
                return;
            }

            this.itemUpdaterService.applyAmmoModifications(
                ammoProps,
                itemsJson._id,
                locale.Name,
                this.iDatabaseTables)
        }
    }

    /**
     * Load JSON and apply mod into SPT weapon in game
     */
    public updateItems(): void {
        const jsonWeaponsFiles = this.jsonFileService.loadJsonFiles(ItemType.Weapon);
        const jsonAmmoFiles = this.jsonFileService.loadJsonFiles(ItemType.Ammo);


        if (jsonWeaponsFiles.length === 0) {
            this.logger.info("[AttributMod] No weapon mod found. Skipping weapon updates.");
        }

        if (jsonAmmoFiles.length === 0) {
            this.logger.info("[AttributMod]  No ammo found. Skipping ammo updates.");
        }

        this.caseWeapons(jsonWeaponsFiles);
        this.caseAmmo(jsonAmmoFiles);

    }

    public cloneItems(): void {
        const jsonAmmoFiles = this.jsonFileService.loadJsonFiles(ItemType.Ammo);
        this.itemClonerService.applyAmmoModifications(
                ammoProps,
                itemsJson._id,
                locale.Name,
                this.iDatabaseTables)
    }

}