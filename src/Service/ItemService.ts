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
import {creatTracer, Tracer} from "../Entity/Tracer";
import {createMedic, Medic} from "../Entity/Medic";
import {Mag, MagJsonFile} from "../Entity/Mag";
import {Bag, BagCat} from "../Entity/Bag";

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
        this.itemUpdaterService = new ItemUpdaterService(logger, dataService, itemHelper);
        this.itemClonerService = new ItemClonerService(logger,
            dataService,
            customItemService,
            itemHelper);
    }

    private caseWeapons(jsonWeaponsFiles: { fileName: string; json: any }[]): void {
        for (const {fileName, json} of jsonWeaponsFiles) {
            if (!json) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing weapon JSON data: ${fileName}`);
                continue;
            }

            const templateJson: Templates<ItemProps> = json;

            if (!templateJson.locale) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing template Weapon: ${fileName}`);
                continue;
            }

            const locale: Locale = templateJson.locale

            if (!templateJson.item) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing template Weapon: ${fileName}`);
                continue;
            }

            const itemsJson: Item<ItemProps> = templateJson.item;

            if (!itemsJson._props) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing item Weapon: ${fileName}`);
                continue;
            }

            const itemsPropsJson: ItemProps = itemsJson._props;

            if (!itemsPropsJson) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing ItemProps Weapon: ${fileName}`);
                continue;
            }

            const weaponProps: ItemProps = createItemProps(itemsPropsJson);

            const partialWeaponProps: Partial<ItemProps> = this.itemUpdaterService.constructWeaponsProps(
                weaponProps,
                itemsJson._id,
                locale.ShortName)

            if (!partialWeaponProps) {
                this.logger.debug(`[ModParameter] [ModParameter] No clone weapon will be generate for : ${fileName}`);
            } else {
                this.itemClonerService.applyClone(
                    partialWeaponProps,
                    itemsJson._id,
                    locale.Name,
                    locale.ShortName,
                    ItemTypeEnum.Weapon)

            }
        }
    }

    private caseAmmo(jsonAmmoFiles: { fileName: string; json: any }[]) {
        for (const {fileName, json} of jsonAmmoFiles) {
            if (!json) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing ammo JSON data: ${fileName}`);
                continue;
            }

            const templateJson: Templates<Ammo> = json;

            if (!templateJson.item) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing template Ammo: ${fileName}`);
                continue;
            }

            if (!templateJson.locale) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing template Ammo: ${fileName}`);
                continue;
            }

            const locale: Locale = templateJson.locale


            const itemsJson: Item<Ammo> = templateJson.item;

            if (!itemsJson._props) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing item Ammo: ${fileName}`);
                continue;
            }

            const itemsPropsJson: Ammo = itemsJson._props;

            if (!itemsPropsJson) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing ItemProps Ammo: ${fileName}`);
                continue;
            }

            const ammoProps: Ammo = createItemAmmo(itemsPropsJson);

            if (!ammoProps) {
                this.logger.debug(`[ModParameter] Invalid Json Ammo update.`);
                return;
            }

            const partialAmmoProps = this.itemUpdaterService.applyAmmoModifications(
                ammoProps,
                itemsJson._id,
                locale.Name)

            if (!partialAmmoProps) {
                this.logger.debug(`[ModParameter] No clone ammo will be generate for : ${fileName}`);
            } else {
                this.itemClonerService.applyClone(
                    partialAmmoProps,
                    itemsJson._id,
                    locale.Name,
                    locale.ShortName,
                    ItemTypeEnum.Ammo)

            }
        }
    }

    private caseMedic(jsonMedicFiles: { fileName: string; json: any }[]) {
        for (const {fileName, json} of jsonMedicFiles) {
            if (!json) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing Medic JSON data: ${fileName}`);
                continue;
            }

            const templateJson: Templates<Medic> = json;
            const clone: boolean = typeof json.clone === "boolean" ? json.clone : false;

            if (!templateJson.item) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing template Medic: ${fileName}`);
                continue;
            }

            if (!templateJson.locale) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing template Medic: ${fileName}`);
                continue;
            }

            const locale: Locale = templateJson.locale


            const medicItem: Item<Medic> = templateJson.item;

            if (!medicItem._props) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing item Medic: ${fileName}`);
                continue;
            }

            const itemsPropsJson: Medic = medicItem._props;

            if (!itemsPropsJson) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing ItemProps Medic: ${fileName}`);
                continue;
            }

            const medic: Medic = createMedic(itemsPropsJson);

            if (!medic) {
                this.logger.debug(`[ModParameter] Invalid Json Medic update.`);
                return;
            }

            const partialAmmoProps = this.itemUpdaterService.applyMedicModifications(
                medic,
                clone,
                medicItem._id,
                locale.Name)

            if (!partialAmmoProps) {
                this.logger.debug(`[ModParameter] No clone Medic will be generate for : ${fileName}`);
            } else {
                this.itemClonerService.applyClone(
                    partialAmmoProps,
                    medicItem._id,
                    locale.Name,
                    locale.ShortName,
                    ItemTypeEnum.Medic)

            }
        }
    }

    private caseMag(jsonMagFiles: Array<{ fileName: string; json: MagJsonFile }>) {
        for (const {fileName, json} of jsonMagFiles) {
            if (!json) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing Mag JSON data: ${fileName}`);
                continue;
            }

            for (const [name, magJson] of Object.entries(json)) {
                const mag = new Mag(name, magJson);
                this.itemUpdaterService.applyMagMod(mag);
            }
        }
    }

    private caseBag(jsonBagFiles: Array<{ fileName: string; json: MagJsonFile }>) {
        for (const {fileName, json} of jsonBagFiles) {
            if (!json) {
                this.logger.debug(`[ModParameter] Skipping invalid or missing Bag JSON data: ${fileName}`);
                continue;
            }

            try {
                const firstKey = Object.keys(json)[0];
                const bagCat: BagCat = BagCat.fromJson(json[firstKey]);
                this.itemUpdaterService.applyBagMod(bagCat);
            } catch (err) {
                this.logger.debug(`[ModParameter] Failed parsing JSON to BagCat: ${fileName} — ${err}`);
            }
        }
    }

    /**
     * clone Items : First Weapons because new ammo need compatibility with new weapon ofc
     */
    public cloneItems(): void {
        this.caseWeapons(this.loadJsonFiles(ItemTypeEnum.Weapon));
        this.caseAmmo(this.loadJsonFiles(ItemTypeEnum.Ammo));
        this.caseMedic(this.loadJsonFiles(ItemTypeEnum.Medic))
    }

    public apply_mod_item(): void {
        this.caseMag(this.loadJsonFiles(ItemTypeEnum.Mag));
        this.caseBag(this.loadJsonFiles(ItemTypeEnum.Bag));
    }

    private loadJsonFiles<T>(itemType: ItemTypeEnum): Array<{ fileName: string; json: T }> {
        const jsonFiles: Array<{ fileName: string; json: T }> = this.jsonFileService.loadJsonFiles(itemType);

        if (jsonFiles.length === 0) {
            this.logger.debug(`[ModParameter] No ${itemType} mod found. Skipping ${itemType} updates.`);
        }
        return jsonFiles;
    }

    public allTracer(): void {
        const jsonTracer: { fileName: string; json: any }[] = this.jsonFileService.loadJsonFiles(ItemTypeEnum.Tracer);
        if (jsonTracer.length > 0 && jsonTracer[0].json) {
            const tracer: Tracer = creatTracer(jsonTracer[0].json);
            this.itemUpdaterService.applyAllTracerAllAmmoDB(tracer);
        } else {
            this.logger.debug("[ModParameter] No tracer JSON data found.");
        }
    }
}