import {ILogger} from "@spt/models/spt/utils/ILogger";
import {SaveServer} from "@spt/servers/SaveServer";
import {WeaponCloneRegistry} from "../Entity/WeaponCloneRegistry";
import {AmmoCloneRegistry} from "../Entity/AmmoCloneRegistry";
import {ISptProfile} from "@spt/models/eft/profile/ISptProfile";
import {IItem} from "@spt/models/eft/common/tables/IItem";
import {IInsuredItem} from "@spt/models/eft/common/tables/IBotBase";
import {ItemHelper} from "@spt/helpers/ItemHelper";
import {ITemplateItem} from "@spt/models/eft/common/tables/ITemplateItem";
import {LocaleService} from "@spt/services/LocaleService";

export class ClearCloneService {
    private readonly logger: ILogger;
    private readonly saveServer: SaveServer;
    private readonly itemHelper: ItemHelper;
    private readonly localeService: LocaleService;
    private readonly GREEN: string = "\x1b[32m";
    private readonly RESET: string = "\x1b[0m";
    private readonly CYAN: string = "\x1b[36m";


    constructor(logger: ILogger, saveServer: SaveServer, itemHelper: ItemHelper, localeService: LocaleService) {
        this.logger = logger;
        this.saveServer = saveServer;
        this.itemHelper = itemHelper;
        this.localeService = localeService
    }

    /**
     * Removes unused cloned weapons and ammo from player inventories and insured items.
     * First, it checks which cloned items are still present in the game and filters them out.
     * Then, it iterates over all player profiles to replace obsolete clones with their original IDs.
     */
    public clearAmmoWeaponNotUseAnymore(): void {
        const map_weapon_idOriginal_vs_idClone = new Map(Object.entries(WeaponCloneRegistry.id_and_cloneId));
        const map_ammo_idOriginal_vs_idClone = new Map(Object.entries(AmmoCloneRegistry.id_and_cloneId));
        const {ammoStatusMap, weaponStatusMap} = this.differentiateClones();
        const profiles: Record<string, ISptProfile> = this.saveServer.getProfiles();

        // 🔍 Filtrer les clones encore en jeu
        this.filterExistingClones(map_ammo_idOriginal_vs_idClone, ammoStatusMap);
        this.filterExistingClones(map_weapon_idOriginal_vs_idClone, weaponStatusMap);

        // LOG
        this.logExistingClones(weaponStatusMap, ammoStatusMap)
        this.logger.debug(`Starting cleanup of cloned weapons and ammo... ${Object.keys(profiles).length} profiles detected.`);

        for (const profileId in profiles) {
            const profile: ISptProfile = profiles[profileId];
            const inventory: IItem[] = profile.characters.pmc.Inventory.items;
            const insuredItems: IInsuredItem[] = profile.characters.pmc.InsuredItems;

            this.logger.debug(`[ModParameter] Processing profile: ${profile.info.username} (ID: ${profileId})`);

            // INVENTORY
            let serialisedInventory = JSON.stringify(inventory);
            let modificationsWeapon = 0;
            let modificationsAmmo = 0;
            // 🔫
            modificationsWeapon = this.clearWeaponClone(map_weapon_idOriginal_vs_idClone, serialisedInventory, modificationsWeapon)
            // 🔥
            modificationsAmmo = this.clearAmmoClone(map_ammo_idOriginal_vs_idClone, serialisedInventory, modificationsAmmo)
            profile.characters.pmc.Inventory.items = JSON.parse(serialisedInventory);


            // INSURANCE
            let serialisedInsuredItems = JSON.stringify(insuredItems);
            let clearCountInsurance = 0;
            // 🔫
            clearCountInsurance = this.clearWeaponClone(map_weapon_idOriginal_vs_idClone, serialisedInsuredItems, clearCountInsurance)
            // 🔥
            clearCountInsurance = this.clearAmmoClone(map_ammo_idOriginal_vs_idClone, serialisedInsuredItems, clearCountInsurance)
            profile.characters.pmc.InsuredItems = JSON.parse(serialisedInsuredItems);

            // DEBUG des modifications
            this.debugLog(modificationsWeapon, modificationsAmmo, clearCountInsurance, profile.info.username)
        }
    }

    /**
     * Replaces cloned ammo with their original counterparts in the provided JSON string.
     * @param map - A map containing original IDs mapped to their cloned versions.
     * @param json - The JSON string representing the inventory or insured items.
     * @param index - The counter for the number of replacements made.
     * @returns Updated count of modifications made.
     */
    private clearAmmoClone(map: Map<string, string>, json: string, index: number): number {
        for (const [originalId, cloneId] of map) {

            if (json.includes(`"${cloneId}"`)) {

                this.logger.debug(`[ModParameter] Munition assurée clonée détectée ${cloneId} → Remplacement par ${originalId}`);
                const regex = new RegExp(`"${cloneId}"`, "g");
                json = json.replace(regex, `"${originalId}"`);
                index++;
            }
        }
        return index;
    }

    /**
     * Replaces cloned weapons with their original counterparts in the provided JSON string.
     * @param map - A map containing original IDs mapped to their cloned versions.
     * @param json - The JSON string representing the inventory or insured items.
     * @param index - The counter for the number of replacements made.
     * @returns Updated count of modifications made.
     */
    private clearWeaponClone(map: Map<string, string>, json: string, index: number): number {
        for (const [originalId, cloneId] of map) {

            if (json.includes(`"${cloneId}"`)) {

                this.logger.debug(`[ModParameter] Arme assurée clonée détectée ${cloneId} → Remplacement par ${originalId}`);
                const regex = new RegExp(`"${cloneId}"`, "g");
                json = json.replace(regex, `"${originalId}"`);
                index++;
            }
        }
        return index;

    }

    /**
     * Logs the number of modifications made during the cleanup process.
     * @param modificationsWeapon - Number of weapon modifications.
     * @param modificationsAmmo - Number of ammo modifications.
     * @param clearCountInsurance - Number of insured item modifications.
     * @param profileName - The name of the profile being processed.
     */
    private debugLog(modificationsWeapon: number,
                     modificationsAmmo: number,
                     clearCountInsurance: number,
                     profileName: string): void {
        if (modificationsWeapon > 0) {
            this.logger.debug(`[ModParameter] ${modificationsWeapon} weapons corrected for ${profileName}`);
        } else {
            this.logger.debug(`[ModParameter] No cloned weapons found for ${profileName}`);
        }

        if (modificationsAmmo > 0) {
            this.logger.debug(`[ModParameter] ${modificationsAmmo} ammo corrected for ${profileName}`);
        } else {
            this.logger.debug(`[ModParameter] No cloned ammo found for ${profileName}`);
        }

        if (clearCountInsurance > 0) {
            this.logger.debug(`[ModParameter] ${clearCountInsurance} insured items (weapons + ammo) corrected for ${profileName}`);
        } else {
            this.logger.debug(`[ModParameter] No cloned insured items found for ${profileName}`);
        }
    }

    /**
     * Determines which cloned items are still present in the game.
     * Populates maps that classify each item as "existing" or "missing".
     * @returns Two maps: `ammoStatusMap` and `weaponStatusMap`.
     */
    private differentiateClones(): {
        ammoStatusMap: Map<string, "existing" | "missing">,
        weaponStatusMap: Map<string, "existing" | "missing">
    } {
        const ammoStatusMap = new Map<string, "existing" | "missing">();
        const weaponStatusMap = new Map<string, "existing" | "missing">();

        // 🔥
        for (const cloneId of Object.values(AmmoCloneRegistry.id_and_cloneId)) {
            const [exists] = this.itemHelper.getItem(cloneId);
            ammoStatusMap.set(cloneId, exists ? "existing" : "missing");
        }

        // 🔫
        for (const cloneId of Object.values(WeaponCloneRegistry.id_and_cloneId)) {
            const [exists] = this.itemHelper.getItem(cloneId);
            weaponStatusMap.set(cloneId, exists ? "existing" : "missing");
        }

        return {ammoStatusMap, weaponStatusMap};
    }

    /**
     * Filters out cloned items that are still present in the game.
     * Removes them from the provided map to prevent unnecessary replacements.
     * @param map - The map containing cloned items.
     * @param statusMap - A map indicating whether an item is "existing" or "missing".
     */
    private filterExistingClones(map: Map<string, string>, statusMap: Map<string, "existing" | "missing">): void {
        for (const [originalId, cloneId] of [...map.entries()]) {
            if (statusMap.get(cloneId) === "existing") {
                map.delete(originalId);
            }
        }
    }

    /**
     * Logs weapons and ammo clones that are still present in the game.
     * Retrieves the localized names of the original items from the locale database.
     * Displays weapon and ammo names in green and prefixes the log entry with "[ModParameter]".
     *
     * @param weaponStatusMap - A map indicating whether each weapon clone is "existing" or "missing".
     * @param ammoStatusMap - A map indicating whether each ammo clone is "existing" or "missing".
     */
    private logExistingClones(weaponStatusMap: Map<string, "existing" | "missing">, ammoStatusMap: Map<string, "existing" | "missing">): void {
        for (const [originalId, cloneId] of Object.entries(WeaponCloneRegistry.id_and_cloneId)) {

            if (weaponStatusMap.get(cloneId) === "existing") {
                const localeDb = this.localeService.getLocaleDb();
                const result = localeDb[`${originalId} ShortName`];

                this.logger.info(`[ModParameter] ${this.CYAN} Weapon MOD and Clone in game: ${this.RESET}${this.GREEN}${result}${this.RESET}`);
            }
        }

        for (const [originalId, cloneId] of Object.entries(AmmoCloneRegistry.id_and_cloneId)) {

            if (ammoStatusMap.get(cloneId) === "existing") {
                const localeDb = this.localeService.getLocaleDb();
                const result = localeDb[`${originalId} Name`];

                this.logger.info(`[ModParameter] ${this.CYAN}Ammo MOD and Clone in game: ${this.RESET}${this.GREEN}${result}${this.RESET}`);
            }
        }
    }


}