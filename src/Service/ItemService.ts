import {ItemUpdaterService} from "./ItemUpdaterService";
import {JsonFileService} from "./JsonFileService";
import {ILogger} from "@spt/models/spt/utils/ILogger";
import {Item} from "../Entity/Item";
import {createItemProps, ItemProps} from "../Entity/ItemProps";
import {Templates} from "../Entity/Templates";
import {Ammo, createItemAmmo} from "../Entity/Ammo";
import {ItemTypeEnum} from "../Entity/ItemTypeEnum";
import {Locale} from "../Entity/Locale";
import {CustomItemService} from "@spt/services/mod/CustomItemService";
import {ItemClonerService} from "./ItemClonerService";
import {ItemHelper} from "@spt/helpers/ItemHelper";
import {DatabaseService} from "@spt/services/DatabaseService";

export class ItemService {
    private readonly logger: ILogger;
    private readonly customItemService: CustomItemService;
    private readonly dataService: DatabaseService;
    private readonly jsonFileService: JsonFileService;
    private readonly itemUpdaterService: ItemUpdaterService;
    private readonly itemClonerService: ItemClonerService;
    private readonly itemHelper: ItemHelper;

    constructor(logger: ILogger,
                dataService: DatabaseService,
                customItemService: CustomItemService,
                itemHelper: ItemHelper) {
        this.logger = logger;
        this.dataService = dataService;
        this.customItemService = customItemService;
        this.itemHelper = itemHelper;

        this.jsonFileService = new JsonFileService(logger);
        this.itemUpdaterService = new ItemUpdaterService(logger, dataService);
        this.itemClonerService = new ItemClonerService(logger,
            dataService,
            customItemService,
            itemHelper);
    }

    private caseWeapons(jsonWeaponsFiles:{ fileName: string; json: any }[], clone: boolean): void {
        for (const {fileName, json} of jsonWeaponsFiles) {
            if (!json) {
                this.logger.debug(`[AttributMod] Skipping invalid or missing weapon JSON data: ${fileName}`);
                continue;
            }

            const templateJson: Templates<ItemProps> = json;

            if (!templateJson.locale) {
                this.logger.debug(`[AttributMod] Skipping invalid or missing template Weapon: ${fileName}`);
                continue;
            }

            const locale: Locale = templateJson.locale

            if (!templateJson.item) {
                this.logger.debug(`[AttributMod] Skipping invalid or missing template Weapon: ${fileName}`);
                continue;
            }

            const itemsJson: Item<ItemProps> = templateJson.item;

            if (!itemsJson._props) {
                this.logger.debug(`[AttributMod] Skipping invalid or missing item Weapon: ${fileName}`);
                continue;
            }

            const itemsPropsJson: ItemProps = itemsJson._props;

            if (!itemsPropsJson) {
                this.logger.debug(`[AttributMod] Skipping invalid or missing ItemProps Weapon: ${fileName}`);
                continue;
            }

            const weaponProps: ItemProps = createItemProps(itemsPropsJson);

            const partialWeaponProps: Partial<ItemProps> = this.itemUpdaterService.constructWeaponsProps(
                weaponProps,
                itemsJson._id,
                locale.ShortName)

            this.itemClonerService.applyClone(
                partialWeaponProps,
                itemsJson._id,
                locale.Name,
                locale.ShortName,
                ItemTypeEnum.Weapon)

        }
    }

    private caseAmmo(jsonAmmoFiles:{ fileName: string; json: any }[], clone: boolean) {
        for (const {fileName, json} of jsonAmmoFiles) {
            if (!json) {
                this.logger.debug(`[AttributMod] Skipping invalid or missing ammo JSON data: ${fileName}`);
                continue;
            }

            const templateJson: Templates<Ammo> = json;

            if (!templateJson.item) {
                this.logger.debug(`[AttributMod] Skipping invalid or missing template Ammo: ${fileName}`);
                continue;
            }

            if (!templateJson.locale) {
                this.logger.debug(`[AttributMod] Skipping invalid or missing template Weapon: ${fileName}`);
                continue;
            }

            const locale: Locale = templateJson.locale


            const itemsJson: Item<Ammo> = templateJson.item;

            if (!itemsJson._props) {
                this.logger.debug(`[AttributMod] Skipping invalid or missing item Ammo: ${fileName}`);
                continue;
            }

            const itemsPropsJson: Ammo = itemsJson._props;

            if (!itemsPropsJson) {
                this.logger.debug(`[AttributMod] Skipping invalid or missing ItemProps Ammo: ${fileName}`);
                continue;
            }

            const ammoProps: Ammo = createItemAmmo(itemsPropsJson);

            if (!ammoProps) {
                this.logger.debug(`[AttributMod] [AimingService] Invalid Json PMC update.`);
                return;
            }

            const partialAmmoProps = this.itemUpdaterService.applyAmmoModifications(
                ammoProps,
                itemsJson._id,
                locale.Name)

            this.itemClonerService.applyClone(
                partialAmmoProps,
                itemsJson._id,
                locale.Name,
                locale.ShortName,
                ItemTypeEnum.Ammo)

        }
    }

    /**
     * clone Items : First Weapons because new ammo need compatibility with new weapon ofc
     */
    public cloneItems(): void {
        this.caseWeapons(this.loadJsonFiles(ItemTypeEnum.Weapon), true);
        this.caseAmmo(this.loadJsonFiles(ItemTypeEnum.Ammo), true);
    }

    private loadJsonFiles(itemType: ItemTypeEnum): any {
        const jsonFiles:{ fileName: string; json: any }[] = this.jsonFileService.loadJsonFiles(itemType);

        if (jsonFiles.length === 0) {
            this.logger.debug(`[AttributMod] No ${itemType} mod found. Skipping ${itemType} updates.`);
        }
        return jsonFiles;
    }

}