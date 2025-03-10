import {ItemProps} from "../Entity/ItemProps";
import {ILogger} from "@spt-aki/models/spt/utils/ILogger";
import {Ammo} from "../Entity/Ammo";
import {IDatabaseTables} from "@spt-aki/models/spt/server/IDatabaseTables";
import {ITemplates} from "@spt-aki/models/spt/templates/ITemplates";
import {IProps, ITemplateItem} from "@spt-aki/models/eft/common/tables/ITemplateItem";
import {ValidateUtils} from "../Utils/ValidateUtils";


export class ItemUpdaterService {
    private readonly logger: ILogger;

    constructor(logger: ILogger) {
        this.logger = logger;
    }

    /**
     * Applies modifications from a JSON item to an SPT item.
     * If any value is invalid, the modification is skipped for that item.
     * @param ammoProps Ammo extract from JSON
     * @param iDatabaseTables data from the SPT database
     * @param id_item_to_modify id from the JSON
     * @param name_item_to_modify name from the JSON
     * @returns true if the item was modified, false if skipped
     */
    public applyAmmoModifications(ammoProps: Ammo,
                                  id_item_to_modify: string,
                                  name_item_to_modify: string,
                                  iDatabaseTables: IDatabaseTables): boolean {
        const validateUtils = new ValidateUtils();

        const templates: ITemplates | undefined = iDatabaseTables?.templates;
        const items: Record<string, ITemplateItem> | undefined = templates?.items;

        if (!templates || !items) {
            this.logger.error("[AttributMod] Invalid iDatabaseTables structure. Modification aborted");
            return false;
        }

        const sptItem: ITemplateItem | undefined = items[id_item_to_modify];

        if (!sptItem) {
            this.logger.warning(`[AttributMod] Item with ID '${id_item_to_modify}' not found in templates DB.`);
            return false;
        }

        const sptItemProps: IProps | undefined = sptItem._props;

        if (!sptItemProps) {
            this.logger.warning(`[AttributMod] Item with ID '${id_item_to_modify}' has no _props on DB`);
            return false;
        }


        let updatedProps: Partial<Ammo> = {};

        updatedProps.ArmorDamage = validateUtils.validateAndCastInt(ammoProps.ArmorDamage);
        updatedProps.Damage = validateUtils.validateAndCastInt(ammoProps.Damage);
        updatedProps.InitialSpeed = validateUtils.validateAndCastInt(ammoProps.InitialSpeed);
        updatedProps.PenetrationPower = validateUtils.validateAndCastInt(ammoProps.PenetrationPower);
        updatedProps.StackMaxSize = validateUtils.validateAndCastInt(ammoProps.StackMaxSize);
        updatedProps.Tracer = validateUtils.validateBoolean(ammoProps.Tracer);
        updatedProps.TracerColor = validateUtils.validateString(ammoProps.TracerColor, true);


        const invalidProps = Object.entries(updatedProps).filter(([_, value]) => value === null);

        // check value if not null before assignation
        if (invalidProps.length > 0) {
            this.logger.warning(`[AttributMod] Skipping ammo: ${name_item_to_modify} due to invalid values: ${invalidProps.map(([key]) => key).join(", ")}`);
            return false;
        }

        // assignation
        for (const key in updatedProps) {
            sptItem._props[key] = updatedProps[key];
        }

        this.logger.info(`[AttributMod] Successfully updated ${name_item_to_modify}`);

        return true;
    }

    /**
     * Applies modifications from a JSON item to an SPT item.
     * If any value is invalid, the modification is skipped for that item.
     * @param weaponItem Weapon extract from JSON
     * @param iDatabaseTables data from the SPT database
     * @param id_item_to_modify id from the JSON
     * @param name_item_to_modify name from the JSON
     * @returns true if the item was modified, false if skipped
     */
    public applyWeaponsModifications(weaponItem: ItemProps,
                                     id_item_to_modify: string,
                                     name_item_to_modify: string,
                                     iDatabaseTables: IDatabaseTables): boolean {
        const validateUtils = new ValidateUtils();

        const templates: ITemplates | undefined = iDatabaseTables?.templates;
        const itemsSpt: Record<string, ITemplateItem> | undefined = templates?.items;

        if (!templates || !itemsSpt) {
            this.logger.error("[AttributMod] Invalid iDatabaseTables structure. Modification aborted");
            return false;
        }

        const sptItem: ITemplateItem | undefined = itemsSpt[id_item_to_modify];

        if (!sptItem) {
            this.logger.warning(`[AttributMod] Item with ID '${id_item_to_modify}' not found in templates DB.`);
            return false;
        }

        const sptItemProps: IProps | undefined = sptItem._props;

        if (!sptItemProps) {
            this.logger.warning(`[AttributMod] Item with ID '${id_item_to_modify}' has no _props on DB`);
            return false;
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
        updatedProps.bFirerate = validateUtils.validateAndCastInt(weaponItem.bFirerate);

        const invalidProps = Object.entries(updatedProps).filter(([_, value]) => value === null);

        // check value if not null before assignation
        if (invalidProps.length > 0) {
            this.logger.warning(`[AttributMod] Skipping ammo: ${name_item_to_modify} due to invalid values: ${invalidProps.map(([key]) => key).join(", ")}`);
            return false;
        }

        // assignation
        for (const key in updatedProps) {
            sptItem._props[key] = updatedProps[key];
        }

        this.logger.info(`[AttributMod] [AttributMod] Successfully updated ${name_item_to_modify} ammo`);

        return true;
    }

}
