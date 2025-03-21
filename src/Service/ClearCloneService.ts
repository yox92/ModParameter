import {ILogger} from "@spt/models/spt/utils/ILogger";
import {SaveServer} from "@spt/servers/SaveServer";
import {WeaponCloneRegistry} from "../Entity/WeaponCloneRegistry";
import {AmmoCloneRegistry} from "../Entity/AmmoCloneRegistry";
import {ISptProfile} from "@spt/models/eft/profile/ISptProfile";
import {IItem} from "@spt/models/eft/common/tables/IItem";
import {IInsuredItem} from "@spt/models/eft/common/tables/IBotBase";
import {ItemHelper} from "@spt/helpers/ItemHelper";
import {LocaleService} from "@spt/services/LocaleService";
import {ValidateUtils} from "../Utils/ValidateUtils";
import {ITemplateItem} from "@spt/models/eft/common/tables/ITemplateItem";
import {Baseclass} from "../Entity/Baseclass";
import {DatabaseService} from "@spt/services/DatabaseService";

export class ClearCloneService {
    private readonly logger: ILogger;
    private readonly saveServer: SaveServer;
    private readonly itemHelper: ItemHelper;
    private readonly localeService: LocaleService;
    private readonly dataService: DatabaseService;
    private readonly GREEN: string = "\x1b[32m";
    private readonly RESET: string = "\x1b[0m";
    private readonly RED: string = "\x1b[31m";
    private readonly CYAN: string = "\x1b[36m";
    private readonly INVENTORY: string = "Inventory";
    private readonly INSURED: string = "insured";


    constructor(logger: ILogger,
                saveServer: SaveServer,
                itemHelper: ItemHelper,
                localeService: LocaleService,
                dataService: DatabaseService) {
        this.logger = logger;
        this.saveServer = saveServer;
        this.itemHelper = itemHelper;
        this.localeService = localeService;
        this.dataService = dataService
    }

    /**
     * Replace unused cloned weapons and ammo to original from player inventories and insured items.
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
            // Server dedicace no profil
            if (profile) {
                if (profile.characters.pmc.Inventory && profile.characters.pmc.InsuredItems) {
                    const inventoryItems: IItem[] = profile.characters.pmc.Inventory.items;
                    const insuredItems: IInsuredItem[] = profile.characters.pmc.InsuredItems;

                    this.logger.debug(`[ModParameter] Processing profile: ${profile.info.username} (ID: ${profileId})`);

                    // INVENTORY
                    let serialisedInventory: string = JSON.stringify(inventoryItems);
                    let modificationsWeapon: { value: number } = {value: 0};  // mutable
                    let modificationsAmmo: { value: number } = {value: 0};  // mutable
                    // 🔫
                    serialisedInventory = this.clearWeaponClone(map_weapon_idOriginal_vs_idClone, serialisedInventory, modificationsWeapon, this.INVENTORY)
                    // 🔥
                    serialisedInventory = this.clearAmmoClone(map_ammo_idOriginal_vs_idClone, serialisedInventory, modificationsAmmo, this.INVENTORY)
                    profile.characters.pmc.Inventory.items = JSON.parse(serialisedInventory);


                    // INSURANCE
                    let serialisedInsuredItems: string = JSON.stringify(insuredItems);
                    let clearCountInsurance: { value: number } = {value: 0};
                    // 🔫
                    serialisedInsuredItems = this.clearWeaponClone(map_weapon_idOriginal_vs_idClone, serialisedInsuredItems, clearCountInsurance, this.INSURED)
                    // 🔥
                    serialisedInsuredItems = this.clearAmmoClone(map_ammo_idOriginal_vs_idClone, serialisedInsuredItems, clearCountInsurance, this.INSURED)
                    profile.characters.pmc.InsuredItems = JSON.parse(serialisedInsuredItems);

                    // DEBUG des modifications
                    this.debugLog(modificationsWeapon, modificationsAmmo, clearCountInsurance, profile.info.username)
                }

            }

        }
    }

    /**
     * Check ig all Ammo Are Tracer or Not
     */
    public checkTracerAllAmmoDB(): void {
        let allHaveTracer = true;
        const validateUtils = new ValidateUtils();

        const items: ITemplateItem[] = validateUtils.checkTemplateItems(this.dataService, this.logger)

        if (!items) {
            return;
        }

        const ammos: ITemplateItem[] = items.filter(item =>
            item?._id && this.itemHelper.isOfBaseclass(item._id, Baseclass.AMMO)
        );

        for (const ammo of ammos) {
            if (!ammo._props) {
                this.logger.debug(`[ModParameter] Warning: Ammo ${ammo._id} has no _props.`);
                continue;
            }
            const ammoProps = ammo._props;

            if (ammoProps.Tracer === undefined || ammoProps.Tracer == null) {
                this.logger.debug(`[ModParameter] Warning: Ammo ${ammo._id} is missing Tracer property.`);
                continue;
            }
            if (!ammoProps.Tracer) {
                allHaveTracer = false;
                break;
            }
        }
        if (allHaveTracer) {
            this.logger.info(`[ModParameter] ${this.CYAN}All ammo are${this.RESET} ${this.GREEN}Tracer${this.RESET}`);
        } else {
            this.logger.debug("[ModParameter] At least one ammo object is missing Tracer or has it set to false.");
        }
    }

    /**
     * Replaces cloned ammo with their original counterparts in the provided JSON string.
     * @param map - A map containing original IDs mapped to their cloned versions.
     * @param json - The JSON string representing the inventory or insured items.
     * @param index - The counter for the number of replacements made. MUTABLE
     * @param location -  Inventory / Assurance
     * @returns json because MUTABLE.
     */
    private clearAmmoClone(map: Map<string, string>, json: string, index: { value: number }, location: string): string {
        for (const [originalId, cloneId] of map) {

            if (json.includes(`"${cloneId}"`)) {
                const localeDb = this.localeService.getLocaleDb();
                const result = localeDb[`${originalId} Name`];

                this.logger.info(`[ModParameter] ${this.CYAN}Cloned AMMO detected in ${this.RESET}${this.RED}${location}${this.RESET} : ${this.RESET}${this.GREEN}${result}${this.RESET} → Replaced with the Orignal`);
                const regex = new RegExp(`"${cloneId}"`, "g");
                json = json.replace(regex, `"${originalId}"`);
                index.value++;
            }
        }
        return json;
    }

    /**
     * Replaces cloned weapons with their original counterparts in the provided JSON string.
     * @param map - A map containing original IDs mapped to their cloned versions.
     * @param json - The JSON string representing the inventory or insured items.
     * @param index - The counter for the number of replacements made. MUTABLE
     * @param location -  Inventory / Assurance
     * @returns json because MUTABLE.
     */
    private clearWeaponClone(map: Map<string, string>, json: string, index: {
        value: number
    }, location: string): string {
        for (const [originalId, cloneId] of map) {

            if (json.includes(`"${cloneId}"`)) {
                const localeDb = this.localeService.getLocaleDb();
                const result = localeDb[`${originalId} Name`];

                this.logger.info(`[ModParameter] ${this.CYAN}Cloned WEAPON detected in ${this.RESET}${this.RED}${location}${this.RESET} : ${this.RESET}${this.GREEN}${result}${this.RESET} → Replaced with the Orignal`);
                const regex = new RegExp(`"${cloneId}"`, "g");
                json = json.replace(regex, `"${originalId}"`);
                index.value++;
            }
        }
        return json;
    }

    /**
     * Logs the number of modifications made during the cleanup process.
     * @param modificationsWeapon - Number of weapon modifications.
     * @param modificationsAmmo - Number of ammo modifications.
     * @param clearCountInsurance - Number of insured item modifications.
     * @param profileName - The name of the profile being processed.
     */
    private debugLog(modificationsWeapon: { value: number },
                     modificationsAmmo: { value: number },
                     clearCountInsurance: { value: number },
                     profileName: string): void {
        if (modificationsWeapon.value > 0) {
            this.logger.debug(`[ModParameter] ${modificationsWeapon.value} weapons corrected for ${profileName}`);
        } else {
            this.logger.debug(`[ModParameter] No cloned weapons found for ${profileName}`);
        }

        if (modificationsAmmo.value > 0) {
            this.logger.debug(`[ModParameter] ${modificationsAmmo.value} ammo corrected for ${profileName}`);
        } else {
            this.logger.debug(`[ModParameter] No cloned ammo found for ${profileName}`);
        }

        if (clearCountInsurance.value > 0) {
            this.logger.debug(`[ModParameter] ${clearCountInsurance.value} insured items (weapons + ammo) corrected for ${profileName}`);
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