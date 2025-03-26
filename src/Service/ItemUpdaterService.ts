import {ItemProps} from "../Entity/ItemProps";
import {ILogger} from "@spt/models/spt/utils/ILogger";
import {Ammo} from "../Entity/Ammo";
import {ITemplates} from "@spt/models/spt/templates/ITemplates";
import {IProps, ITemplateItem} from "@spt/models/eft/common/tables/ITemplateItem";
import {ValidateUtils} from "../Utils/ValidateUtils";
import {DatabaseService} from "@spt/services/DatabaseService";
import {Tracer} from "../Entity/Tracer";
import {Baseclass} from "../Entity/Baseclass";
import {ItemHelper} from "@spt/helpers/ItemHelper";
import {IEffectDamageProps, Medic} from "../Entity/Medic";
import {Mag} from "../Entity/Mag";
import {EnumagCount} from "../Entity/EnumagCount";


export class ItemUpdaterService {
    private BUCKSHOT: string = "buckshot";
    private MACHINEGUN: string[] = ["5d70e500a4b9364de70d38ce", "5cde8864d7f00c0010373be1", "5d2f2ab648f03550091993ca"];
    private readonly GREEN: string = "\x1b[32m";
    private readonly RESET: string = "\x1b[0m";

    private readonly logger: ILogger;
    private readonly dataService: DatabaseService;
    private readonly itemHelper: ItemHelper;

    constructor(logger: ILogger, dataService: DatabaseService, itemHelper: ItemHelper) {
        this.logger = logger;
        this.dataService = dataService;
        this.itemHelper = itemHelper;
    }

    public applyAllTracerAllAmmoDB(tracer: Tracer): void {
        const validateUtils = new ValidateUtils();

        if (tracer.Tracer === undefined || tracer.TracerColor === undefined) {
            this.logger.debug(`[ModParameter] Warning: no Tracer or TracerColor about json Tracer`);
            return;
        }

        if (tracer.Tracer === false) {
            this.logger.debug(`[ModParameter] No Tracer action required`);
            return;
        }

        const items: ITemplateItem[] = validateUtils.checkTemplateItems(this.dataService, this.logger)

        const ammos: ITemplateItem[] = items.filter(item =>
            item?._id && this.itemHelper.isOfBaseclass(item._id, Baseclass.AMMO)
        );

        for (const ammo of ammos) {
            if (ammo._props === undefined || ammo._props === null) {
                this.logger.debug(`[ModParameter] Warning: one ammo leak _props`);
                continue;
            }

            if (ammo._props.Tracer === undefined || ammo._props.Tracer === null || ammo._props.TracerColor === undefined || ammo._props.TracerColor === null) {
                this.logger.debug(`[ModParameter] Warning: Ammo ${ammo._name} is missing Tracer or TracerColor property.`);
                continue;
            }

            ammo._props.Tracer = tracer.Tracer;
            ammo._props.TracerColor = validateUtils.validateTracerColor(tracer.TracerColor);
        }
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

        updatedProps.priceFactor = validateUtils.validatePriceProps(ammoProps.priceFactor);
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

        if (sptItemProps.HasGrenaderComponent &&
            (ammoProps.ExplosionStrength !== undefined && ammoProps.ExplosionStrength !== null &&
                ammoProps.MaxExplosionDistance !== undefined && ammoProps.MaxExplosionDistance !== null &&
                ammoProps.FuzeArmTimeSec !== undefined && ammoProps.FuzeArmTimeSec !== null)
        ) {
            updatedProps.ExplosionStrength = validateUtils.validateAndCastInt(ammoProps.ExplosionStrength);
            updatedProps.MaxExplosionDistance = validateUtils.validateAndCastInt(ammoProps.MaxExplosionDistance);
            updatedProps.FuzeArmTimeSec = validateUtils.validateIntToFloatFromValueWithThousandMulti(ammoProps.FuzeArmTimeSec);
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

    public applyMedicModifications(medic: Medic,
                                   clone: boolean,
                                   id_item_to_modify: string,
                                   name_item_to_modify: string): Partial<Medic> | null {
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

        let updatedProps: Partial<Medic> = {};

        updatedProps.priceFactor = validateUtils.validatePriceProps(medic.priceFactor);
        updatedProps.hpResourceRate = validateUtils.validateAndCastInt(medic.hpResourceRate);
        updatedProps.MaxHpResource = validateUtils.validateAndCastInt(medic.MaxHpResource);
        updatedProps.StackMaxSize = validateUtils.validateAndCastInt(medic.StackMaxSize);
        updatedProps.medUseTime = validateUtils.validateAndCastInt(medic.medUseTime);
        updatedProps.StackObjectsCount = validateUtils.validateAndCastInt(medic.StackObjectsCount);
        updatedProps.BackgroundColor = "blue";

        if (medic.effects_damage && Object.keys(medic.effects_damage).length > 0) {
            const validatedEffects: Record<string, IEffectDamageProps> = {};


            for (const [effectName, effectProps] of Object.entries(medic.effects_damage)) {
                const validatedEffect: Partial<IEffectDamageProps> = {};
                this.logger.debug(`[ModParameter] Contains effect: '${effectName}' about '${name_item_to_modify}'`);

                validatedEffect.delay = validateUtils.validateAndCastInt(effectProps.delay) ?? 0;
                validatedEffect.duration = validateUtils.validateAndCastInt(effectProps.duration) ?? 0;
                validatedEffect.fadeOut = validateUtils.validateAndCastInt(effectProps.fadeOut) ?? 0;
                validatedEffect.cost = validateUtils.validateAndCastInt(effectProps.cost) ?? 0;

                const validatedHealthPenaltyMin = validateUtils.validateAndCastInt(effectProps.healthPenaltyMin);
                const validatedHealthPenaltyMax = validateUtils.validateAndCastInt(effectProps.healthPenaltyMax);

                if (validatedHealthPenaltyMin !== null
                    && validatedHealthPenaltyMin !== undefined
                    && validatedHealthPenaltyMax !== null
                    && validatedHealthPenaltyMax !== undefined) {

                    validatedEffect.healthPenaltyMin = validatedHealthPenaltyMin;
                    validatedEffect.healthPenaltyMax = validatedHealthPenaltyMax;
                } else {
                    this.logger.debug(`[ModParameter] no healthPenalty`);
                }

                const hasValidCore = ["delay", "duration", "fadeOut", "cost"].every(
                    key => validatedEffect[key as keyof IEffectDamageProps] !== null
                );

                if (hasValidCore) {
                    validatedEffects[effectName] = validatedEffect as IEffectDamageProps;
                } else {
                    this.logger.debug(`[ModParameter] Invalid core values for effect '${effectName}' – skipping`);
                }
            }

            if (Object.keys(validatedEffects).length > 0) {
                updatedProps.effects_damage = validatedEffects;
            }
        }

        const invalidProps = Object.entries(updatedProps).filter(([_, value]) => value === null);

        if (invalidProps.length > 0) {
            this.logger.debug(`[ModParameter] Skipping medic: ${name_item_to_modify} due to invalid values: ${invalidProps.map(([key]) => key).join(", ")}`);
            return null;
        }

        if (!clone) {
            for (const key in updatedProps) {
                const value = updatedProps[key];

                if (key === "effects_damage") {
                    if (value && Object.keys(value).length > 0) {
                        this.logger.debug(`[ModParameter] Overwriting 'effects_damage' with ${Object.keys(value).length} effect(s).`);
                        (sptItemProps as any)[key] = value;
                    } else {
                        this.logger.debug("[ModParameter] 'effects_damage' is empty → removing from item.");
                        (sptItemProps as any)[key] = [];
                    }
                } else if (value !== undefined) {
                    this.logger.debug(`[ModParameter] Setting '${key}' = ${value}`);
                    (sptItemProps as any)[key] = value;
                }
            }

        } else {
            return updatedProps
        }
    }

    /**
     * Applies modifications from a JSON item.
     * If any value is invalid, skipped for that item.
     * @param weaponItem Weapon extract from JSON
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

        updatedProps.priceFactor = validateUtils.validatePriceProps(weaponItem.priceFactor);
        updatedProps.priceFactor = validateUtils.validateAndCastFloat(weaponItem.priceFactor, 2);
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

    public applyMagMod(mag: Mag): void {
        const defaultValue: number = EnumagCount[mag.name]

        if (mag.resize === false && mag.penality === false && mag.counts === defaultValue) {
            this.logger.debug(`[ModParameter] Skipping mag : ${mag.name}`);
            return;
        }

        const templates: ITemplates | undefined = this.dataService.getTemplates();
        const items: Record<string, ITemplateItem> | undefined = templates?.items;

        if (!templates || !items) {
            this.logger.debug("[ModParameter] Invalid dataService structure. Modification aborted");
            return null;
        }

        const magazines: ITemplateItem[] = Object.values(items).filter(
            (item: ITemplateItem) =>
                item?._id &&
                this.itemHelper.isOfBaseclass(item._id, Baseclass.MAGAZINE) &&
                mag.ids.includes(item._id));

        for (const magazine of magazines) {
            if (!magazine._props || !Array.isArray(magazine._props.Cartridges)) {
                this.logger.debug(`[ModParameter] Warning: Magazine ${magazine._id} has no Cartridges property.`);
                continue;
            }

            if (mag.fastLoad) {
                if (magazine._props.LoadUnloadModifier) {
                    magazine._props.LoadUnloadModifier = 100;
                }
            }

            if (mag.resize) {
                if (mag.penality) {
                    if (magazine._props.Width) {
                        magazine._props.Width = 2;
                    }
                }
            }

            if (mag.penality) {
                if (magazine._props.Ergonomics && magazine._props.Ergonomics < 0) {
                    magazine._props.Ergonomics = 0
                }
                if (magazine._props.MalfunctionChance) {
                    magazine._props.MalfunctionChance = 0.03
                }
                if (magazine._props.CheckTimeModifier) {
                    magazine._props.CheckTimeModifier = 0
                }
            }

            if (mag.counts !== defaultValue) {

                if (magazine._props && magazine._props.Cartridges && magazine._props.Cartridges[0]) {
                    magazine._props.Cartridges[0]._props.MaxStackCount = mag.counts
                }

            }
        }
    }

}
