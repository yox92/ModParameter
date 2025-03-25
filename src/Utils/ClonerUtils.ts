import {Baseclass} from "../Entity/Baseclass";
import {AmmoCloneRegistry} from "../Entity/AmmoCloneRegistry";
import {TradersAmmoWeapon} from "../Entity/TradersAmmoWeapon";
import {TradersMedic} from "../Entity/TradersMedic";
import {ITemplates} from "@spt/models/spt/templates/ITemplates";
import {DatabaseService} from "@spt/services/DatabaseService";
import {ILogger} from "@spt/models/spt/utils/ILogger";
import {ItemHelper} from "@spt/helpers/ItemHelper";
import {ITemplateItem} from "@spt/models/eft/common/tables/ITemplateItem";
import {ITrader} from "@spt/models/eft/common/tables/ITrader";
import {IItem} from "@spt/models/eft/common/tables/IItem";
import {ItemTypeEnum} from "../Entity/ItemTypeEnum";
import {WeaponCloneRegistry} from "../Entity/WeaponCloneRegistry";
import {MedicCloneRegistry} from "../Entity/MedicCloneRegistry";

export class ClonerUtils {
    private readonly logger: ILogger;

    constructor(logger: ILogger) {
        this.logger = logger;
    }

    /**
     * Adds a cloned item to the appropriate trader based on its original template.
     *
     * This method searches for the appropriate trader selling the original item (`id`),
     * clones it, and inserts the new cloned version into the trader's inventory while maintaining
     * consistency in barter schemes and loyalty levels.
     *
     * @param id The template ID (`_tpl`) of the original item to be cloned.
     * @param cloneTpl The template ID (`_tpl`) of the newly created clone.
     * @param dataService The database service used to access trader information.
     * @param name The name of the item being cloned (used for logging).
     * @param itemTypeEnum Enum indicating whether the item is Ammo or Weapon.
     */
    public addToTrader(id: string,
                       cloneTpl: string,
                       dataService: DatabaseService,
                       name: string,
                       itemTypeEnum: ItemTypeEnum): void {
        let traderEnum: typeof TradersMedic | typeof TradersAmmoWeapon;
        if (itemTypeEnum === ItemTypeEnum.Medic) {
            traderEnum = TradersMedic
        } else {
             traderEnum = TradersAmmoWeapon
        }
        let objectFindTrader = false;
        for (const [traderName, traderId] of Object.entries(traderEnum)) {
            const trader: ITrader = dataService.getTraders()[traderId];
            if (!trader) {
                this.logger.debug(`[ModParameter] Trader ${traderId} are undefined, SKIP.`);
                continue;
            }

            if (!trader.assort) {
                this.logger.debug(`[ModParameter] Trader ${traderId} no assort, SKIP.`);
                continue;
            }

            if (!trader.assort.items || !Array.isArray(trader.assort.items)) {
                this.logger.debug(`[ModParameter] Trader ${traderId} does not have items in assort or is not an array, SKIP.`);
                continue;
            }

            const listItemTrader: IItem[] = trader.assort.items;

            let bestItem: IItem | null = null;
            let bestLoyalLevel: number | null = null;
            let bestClonedId: string | undefined = null;
            let bestOriginalId: string | undefined = null;

            for (const item of listItemTrader) {
                if (item.parentId !== 'hideout' || !item.parentId || !item._id || !item._tpl || !item) {
                    continue;
                }

                if (item._tpl === id) {
                    const tplOldItem = item._id;

                    let clonedId: string | undefined;
                    if (itemTypeEnum === ItemTypeEnum.Ammo) {
                        clonedId = AmmoCloneRegistry.getClonedTpl(tplOldItem);
                    } else if (itemTypeEnum === ItemTypeEnum.Weapon) {
                        clonedId = WeaponCloneRegistry.getClonedTpl(tplOldItem);
                    } else if (itemTypeEnum === ItemTypeEnum.Medic) {
                        clonedId = MedicCloneRegistry.getClonedTpl(tplOldItem);
                    }

                    if (!clonedId) {
                        this.logger.debug(`[ModParameter] tpl not found with trader: ${traderName}, with item _id: ${item._id}`);
                        continue;
                    }

                    if (!trader.assort.barter_scheme[tplOldItem] || !trader.assort.loyal_level_items[tplOldItem]) {
                        continue;
                    }

                    const itemLoyalLevel = trader.assort.loyal_level_items[tplOldItem];

                    if (bestLoyalLevel === null || itemLoyalLevel < bestLoyalLevel) {
                        bestLoyalLevel = itemLoyalLevel;
                        bestItem = structuredClone(item);
                        bestItem._id = clonedId;
                        bestItem._tpl = cloneTpl;
                        bestClonedId = clonedId;
                        bestOriginalId = tplOldItem
                    }
                }
            }

            if (bestItem && bestClonedId && bestLoyalLevel && bestOriginalId) {
                trader.assort.items.push(bestItem);
                objectFindTrader = true;
                this.logger.debug(`[ModParameter] Item ${name} added to Trader: ${traderName} with ID: ${bestClonedId}`);

                trader.assort.barter_scheme[bestItem._id] = structuredClone(trader.assort.barter_scheme[bestOriginalId]);
                this.logger.debug(`[ModParameter] Copy of the same structures for: ${bestClonedId} (Trader: ${traderName})`);

                trader.assort.loyal_level_items[bestItem._id] = bestLoyalLevel;
                this.logger.debug(`[ModParameter] Item ${name} added with Trader: ${traderName} and id: ${bestClonedId} with loyalty level ${bestLoyalLevel}`);
            }

        }
        if (!objectFindTrader) {
            this.logger.debug(`[ModParameter] Item ${name} find no trader to add item (blackList ?)`);
        }

    }

    /**
     * Updates the filters of related items to include the newly cloned ID
     * @param originalId ID of the original item
     * @param newId ID of the created clone
     * @param itemHelper to easily find items
     * @param dataService the database
     */
    public propagateAmmoCompatibility(originalId: string, newId: string, itemHelper: ItemHelper, dataService: DatabaseService): void {
        if (!originalId || !newId) {
            this.logger.debug("[ModParameter] Error: originalId or newId is empty.");
            return;
        }

        const tables: ITemplates = dataService.getTemplates();
        if (!tables || typeof tables !== "object") {
            this.logger.debug("[ModParameter] Error: Unable to retrieve templates (tables is undefined or invalid).");
            return;
        }

        const sptItems: Record<string, ITemplateItem> | undefined = tables.items;
        if (!sptItems || typeof sptItems !== "object") {
            this.logger.debug("[ModParameter] Error: Unable to retrieve items (sptItems is undefined or invalid).");
            return;
        }

        const items: ITemplateItem[] = Object.values(sptItems);
        if (!Array.isArray(items) || items.length === 0) {
            this.logger.debug("[ModParameter] Error: No items found in sptItems.");
            return;
        }

        this.updateMagazinesWithNewId(items, itemHelper, originalId, newId);
        this.updateSlotWeaponsWithNewId(items, itemHelper, originalId, newId);


    }

    /**
     * Updates magazine filters to include the newly cloned ammunition ID.
     *
     * This method iterates through all magazines in the provided list and ensures that
     * any cartridge filters referencing the original ammunition ID are updated to also
     * include the cloned ammunition ID. This maintains compatibility between the cloned
     * ammunition and the magazines that previously supported the original.
     *
     * @param items The list of all template items to check for magazines.
     * @param itemHelper Utility to help identify item types.
     * @param originalId The ID of the original ammunition before cloning.
     * @param newId The ID of the newly cloned ammunition.
     */
    private updateMagazinesWithNewId(items: ITemplateItem[], itemHelper: ItemHelper, originalId: string, newId: string): void {
        const magazines: ITemplateItem[] = items.filter((item: ITemplateItem) =>
            item?._id && itemHelper.isOfBaseclass(item._id, Baseclass.MAGAZINE) || itemHelper.isOfBaseclass(item._id, Baseclass.SPRING_DRIVEN_CYLINDER));
        for (const magazine of magazines) {
            if (!magazine._props || !Array.isArray(magazine._props.Cartridges)) {
                this.logger.debug(`[ModParameter] Warning: Magazine ${magazine._id} has no Cartridges property.`);
                continue;
            }

            for (const cartridge of magazine._props.Cartridges) {
                if (!cartridge || !Array.isArray(cartridge._props?.filters)) {
                    this.logger.debug(`[ModParameter] Warning: A cartridge in ${magazine._id} is malformed.`);
                    continue;
                }

                for (const filter of cartridge._props.filters) {
                    if (!filter || !Array.isArray(filter.Filter)) {
                        this.logger.debug(`[ModParameter] Warning: A filter in ${magazine._id} is malformed.`);
                        continue;
                    }

                    if (filter.Filter.includes(originalId)) {
                        filter.Filter.push(newId);
                    }
                }
            }
        }

    }

    /**
     * Updates weapon slot filters to include the newly cloned weapon ID.
     *
     * This method iterates through all weapons in the provided list and ensures that
     * any chamber slot filters referencing the original weapon ID are updated to also include
     * the cloned weapon ID. This ensures that the cloned weapon remains compatible with the same
     * ammunition and attachments as the original.
     *
     * @param items The list of all template items to check for weapons.
     * @param itemHelper Utility to help identify item types.
     * @param originalId The ID of the original weapon before cloning.
     * @param newId The ID of the newly cloned weapon.
     */
    private updateSlotWeaponsWithNewId(items: ITemplateItem[], itemHelper: ItemHelper, originalId: string, newId: string): void {
        const weapons: ITemplateItem[] = items.filter((weaponItem: ITemplateItem) =>
            weaponItem?._id && this.isWeapon(weaponItem._id, itemHelper));

        for (const weapon of weapons) {
            if (!weapon._props || !Array.isArray(weapon._props.Chambers)) {
                this.logger.debug(`Warning: Weapon ${weapon._id} has no Chambers property.`);
                continue;
            }

            for (const chamber of weapon._props.Chambers) {
                if (!chamber || !Array.isArray(chamber._props?.filters)) {
                    this.logger.debug(`Warning: A chamber in ${weapon._id} is malformed.`);
                    continue;
                }

                for (const filter of chamber._props.filters) {
                    if (!filter || !Array.isArray(filter.Filter)) {
                        this.logger.debug(`Warning: A filter in ${weapon._id} is malformed.`);
                        continue;
                    }

                    if (filter.Filter.includes(originalId)) {
                        filter.Filter.push(newId);
                    }
                }
            }
        }

    }

    private isWeapon(itemId: string, itemHelper: ItemHelper): boolean {
        return [
            Baseclass.PISTOL,
            Baseclass.SMG,
            Baseclass.ASSAULT_RIFLE,
            Baseclass.ASSAULT_CARBINE,
            Baseclass.SHOTGUN,
            Baseclass.MARKSMAN_RIFLE,
            Baseclass.SNIPER_RIFLE,
            Baseclass.MACHINE_GUN,
            Baseclass.REVOLVER,
            Baseclass.SPECIAL_WEAPON,
            Baseclass.GRENADE_LAUNCHER,
            Baseclass.WEAPON,
            Baseclass.UBGL
        ].some(baseclass => itemHelper.isOfBaseclass(itemId, baseclass));
    }

}