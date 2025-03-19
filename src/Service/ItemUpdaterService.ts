import {ItemProps} from "../Entity/ItemProps";
import {ILogger} from "@spt/models/spt/utils/ILogger";
import {Ammo} from "../Entity/Ammo";
import {ITemplates} from "@spt/models/spt/templates/ITemplates";
import {IProps, ITemplateItem} from "@spt/models/eft/common/tables/ITemplateItem";
import {ValidateUtils} from "../Utils/ValidateUtils";
import {DatabaseService} from "@spt/services/DatabaseService";
import {ItemService} from "./ItemService";


export class ItemUpdaterService {
    private BUCKSHOT: string = "buckshot";
    private MACHINEGUN: string[] = ["5d70e500a4b9364de70d38ce", "5cde8864d7f00c0010373be1", "5d2f2ab648f03550091993ca"];
    private readonly GREEN: string = "\x1b[32m";
    private readonly RESET: string = "\x1b[0m";

    private readonly logger: ILogger;
    private readonly dataService: DatabaseService;

    constructor(logger: ILogger, dataService: DatabaseService) {
        this.logger = logger;
        this.dataService = dataService;

    }

    /**
     * Applies modifications from a JSON item to an SPT item structure.
     * If any value is invalid, skipped for that item.
     * @param ammoProps Ammo extract from JSON
     * @param id_item_to_modify id from the JSON
     * @param name_item_to_modify name from the JSON
     * @returns true if the item was modified, false if skipped
     */
    public applyAmmoModifications(ammoProps: Ammo,
                                  id_item_to_modify: string,
                                  name_item_to_modify: string): Partial<Ammo> {
        const validateUtils = new ValidateUtils();

        const templates: ITemplates | undefined = this.dataService.getTemplates();
        const items: Record<string, ITemplateItem> | undefined = templates?.items;

        if (!templates || !items) {
            this.logger.debug("[ModParameter] Invalid dataService structure. Modification aborted");
            return null;
        }

        const sptItem: ITemplateItem | undefined = items[id_item_to_modify];

        if (!sptItem) {
            this.logger.debug(`[ModParameter] Item with ID '${id_item_to_modify}' not found in templates DB.`);
            return null;
        }

        const sptItemProps: IProps | undefined = sptItem._props;

        if (!sptItemProps) {
            this.logger.debug(`[ModParameter] Item with ID '${id_item_to_modify}' has no _props on DB`);
            return null;
        }

        let updatedProps: Partial<Ammo> = {};

        updatedProps.ArmorDamage = validateUtils.validateAndCastInt(ammoProps.ArmorDamage);
        updatedProps.Damage = validateUtils.validateAndCastInt(ammoProps.Damage);
        updatedProps.PenetrationPower = validateUtils.validateAndCastInt(ammoProps.PenetrationPower);
        updatedProps.StackMaxSize = validateUtils.validateAndCastInt(ammoProps.StackMaxSize);
        updatedProps.Tracer = validateUtils.validateBoolean(ammoProps.Tracer);
        updatedProps.TracerColor = validateUtils.validateTracerColor(ammoProps.TracerColor);
        updatedProps.InitialSpeed = validateUtils.validateAndCastInt(ammoProps.InitialSpeed);
        updatedProps.ammoAccr = validateUtils.validateAndCastIntNegatifCase(ammoProps.ammoAccr);
        updatedProps.ammoRec = validateUtils.validateAndCastIntNegatifCase(ammoProps.ammoRec);
        updatedProps.BallisticCoeficient = validateUtils.validateIntToFloatFromValueWithThousandMulti(ammoProps.BallisticCoeficient);
        updatedProps.BulletMassGram = validateUtils.validateBulletMassGram(ammoProps.BulletMassGram);
        updatedProps.ProjectileCount = validateUtils.validateAndCastInt(ammoProps.ProjectileCount);
        updatedProps.BackgroundColor = "blue";

        if (sptItemProps.HasGrenaderComponent) {
            updatedProps.ExplosionStrength = validateUtils.validateAndCastInt(ammoProps.ExplosionStrength)
            updatedProps.MaxExplosionDistance = validateUtils.validateAndCastInt(ammoProps.MaxExplosionDistance)
            updatedProps.FuzeArmTimeSec = validateUtils.validateIntToFloatFromValueWithThousandMulti(ammoProps.FuzeArmTimeSec)
        }


        const invalidProps = Object.entries(updatedProps).filter(([_, value]) => value === null);

        // check value if not null before assignation
        if (invalidProps.length > 0) {
            this.logger.debug(`[ModParameter] Skipping ammo: ${name_item_to_modify} due to invalid values: ${invalidProps.map(([key]) => key).join(", ")}`);
            return null;
        }

        //case buckshot ammo
        if (sptItemProps.ProjectileCount !== updatedProps.ProjectileCount
            && sptItemProps.ammoType === this.BUCKSHOT) {
            updatedProps.buckshotBullets = updatedProps.ProjectileCount
        }

        //case nerf machine gun ammo IA
        if (this.MACHINEGUN.includes(sptItem._id)) {

            if (Object.values(updatedProps).some(value => value !== undefined)) {
                this.logger.info(`[ModParameter] Nerf : ${this.GREEN}'${sptItem._name}'${this.RESET}`);
            }

            for (const key in updatedProps) {
                if (updatedProps[key] !== undefined) {
                    (sptItemProps as any)[key] = updatedProps[key];
                }
            }
            return null;
        }
        return updatedProps;
    }

    /**
     * Applies modifications from a JSON item.
     * If any value is invalid, skipped for that item.
     * @param weaponItem Weapon extract from JSON
     * @param dataService data from the SPT database
     * @param id_item_to_modify id from the JSON
     * @param name_item_to_modify name from the JSON
     * @returns true if the item was modified, false if skipped
     */
    public constructWeaponsProps(weaponItem: ItemProps,
                                 id_item_to_modify: string,
                                 name_item_to_modify: string): Partial<ItemProps> {
        const validateUtils = new ValidateUtils();

        const templates: ITemplates | undefined = this.dataService.getTemplates();
        const itemsSpt: Record<string, ITemplateItem> | undefined = templates?.items;

        if (!templates || !itemsSpt) {
            this.logger.debug("[ModParameter] Invalid dataService structure. Modification aborted");
            return null;
        }

        const sptItem: ITemplateItem | undefined = itemsSpt[id_item_to_modify];

        if (!sptItem) {
            this.logger.debug(`[ModParameter] Item with ID '${id_item_to_modify}' not found in templates DB.`);
            return null;
        }

        const sptItemProps: IProps | undefined = sptItem._props;

        if (!sptItemProps) {
            this.logger.debug(`[ModParameter] Item with ID '${id_item_to_modify}' has no _props on DB`);
            return null;
        }

        let updatedProps: Partial<ItemProps> = {};

        updatedProps.CameraSnap = validateUtils.validateAndCastFloatItem(weaponItem.CameraSnap, 2);
        updatedProps.AimSensitivity = validateUtils.validateAndCastFloatItem(weaponItem.AimSensitivity, 2);
        updatedProps.Ergonomics = validateUtils.validateAndCastInt(weaponItem.Ergonomics);
        updatedProps.RecoilCamera = validateUtils.validateAndCastFloatItem(weaponItem.RecoilCamera, 3);
        updatedProps.RecolDispersion = validateUtils.validateAndCastInt(weaponItem.RecolDispersion);
        updatedProps.RecoilForceBack = validateUtils.validateAndCastInt(weaponItem.RecoilForceBack);
        updatedProps.RecoilForceUp = validateUtils.validateAndCastInt(weaponItem.RecoilForceUp);
        updatedProps.Weight = validateUtils.validateAndCastFloatItem(weaponItem.Weight, 2);
        updatedProps.bFirerate = validateUtils.validateValidationFireRate(weaponItem.bFirerate);
        updatedProps.BackgroundColor = "blue";

        const invalidProps = Object.entries(updatedProps).filter(([_, value]) => value === null);

        // check value if not null before assignation
        if (invalidProps.length > 0) {
            this.logger.debug(`[ModParameter] Skipping: ${name_item_to_modify} due to invalid values: ${invalidProps.map(([key]) => key).join(", ")}`);
            return null;
        }

        return updatedProps;
    }

}
