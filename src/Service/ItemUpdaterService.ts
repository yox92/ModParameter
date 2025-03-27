import {ItemProps} from "../Entity/ItemProps";
import {ILogger} from "@spt/models/spt/utils/ILogger";
import {Ammo} from "../Entity/Ammo";
import {ITemplates} from "@spt/models/spt/templates/ITemplates";
import {IGrid, IGridFilter, IProps, ITemplateItem} from "@spt/models/eft/common/tables/ITemplateItem";
import {ValidateUtils} from "../Utils/ValidateUtils";
import {DatabaseService} from "@spt/services/DatabaseService";
import {Tracer} from "../Entity/Tracer";
import {Baseclass} from "../Entity/Baseclass";
import {ItemHelper} from "@spt/helpers/ItemHelper";
import {IEffectDamageProps, Medic} from "../Entity/Medic";
import {Mag} from "../Entity/Mag";
import {EnumagCount} from "../Entity/EnumagCount";
import {Bag, BagCat, IGridJson} from "../Entity/Bag";


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

        const items: Record<string, ITemplateItem> = validateUtils.getTemplateItems(this.dataService, this.logger)

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

        const items: Record<string, ITemplateItem> = validateUtils.getTemplateItems(this.dataService, this.logger)

        const sptItem: ITemplateItem | undefined = items[id_item_to_modify];

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

        const itemsSpt: Record<string, ITemplateItem> = validateUtils.getTemplateItems(this.dataService, this.logger)

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
        const validateutils = new ValidateUtils();
        const defaultValue: number = EnumagCount[mag.name];

        if (!mag.fastLoad && !mag.resize && !mag.penality && mag.counts === defaultValue) {
            this.logger.warning(`[ModParameter] skip magazines : ` + mag.name);
        }

        const items = validateutils.getTemplateItems(this.dataService, this.logger);

        const magazines: ITemplateItem[] = Object.values(items).filter(
            item =>
                item?._id &&
                this.itemHelper.isOfBaseclass(item._id, Baseclass.MAGAZINE) &&
                mag.ids.includes(item._id)
        );

        for (const magazine of magazines) {

            if (!magazine?._props || !magazine?._name || !magazine._props?.Cartridges) {
                this.logger.debug(`[ModParameter] Warning: Magazine has no good property.`);
                continue;
            }
            const props: IProps = magazine._props;
            const name: string = magazine._name;
            const firstCartridge = props?.Cartridges?.[0];

            if (mag.fastLoad) {
                this.applyMagFastLoad(props, name);
            }

            if (mag.resize) {
                this.applyMagResize(props, name, mag.name);
            }

            if (mag.penality) {
                this.applyMagPenality(props, name);
            }

            if (mag.penality) {
                this.applyMagPenality(props, name);
            }

            if (mag.counts !== defaultValue && firstCartridge?._max_count) {
                firstCartridge._max_count = mag.counts;
            }
        }
    }

    private applyMagFastLoad(props: IProps, name: string): void {
        if (props?.LoadUnloadModifier) {
            props.LoadUnloadModifier = -60;
            this.logger.warning(`[ModParameter] skip magazines ` + name);
            this.logger.debug(`[ModParameter] modify ${name} Load, Unload speed`);
        }
    }

    private applyMagResize(props: IProps, name: string, mag_name: string): void {
        const XS_CATEGORIES = ["01-09", "10-19", "20-29"];
        let categories_XS: boolean = XS_CATEGORIES.includes(mag_name);

        if (props?.Height && props?.Width && props?.ExtraSizeDown) {

            if (props.Height === 3 && props.Width === 1) {
                props.Height = 2;
                props.ExtraSizeDown = 1;
                this.logger.debug(`[ModParameter] modify ${name} slot number Height = 2`);
            } else if (props.Height === 2 && props.Width === 2) {
                props.Height = 2;
                props.Width = 1;
                this.logger.debug(`[ModParameter] modify ${name} slot 2 to slot 2 `);
            } else if (props.Height === 2 && props.Width === 1 && categories_XS) {
                props.Height = 1;
                 props.ExtraSizeDown = 0;
                 this.logger.debug(`[ModParameter] modify ${name} slot 2 to slot 1 `);
            }
        }

    }

    private applyMagPenality(props: IProps, name: string): void {
        if (props?.Ergonomics  !== null && props?.Ergonomics !== undefined  && props.Ergonomics < 0) {
            this.logger.debug(`[ModParameter] modify ${name} Ergonomics`);
            props.Ergonomics = 0
        }
        if (props?.MalfunctionChance !== null && props?.MalfunctionChance !== undefined && props?.MalfunctionChance > 0.03) {
            this.logger.debug(`[ModParameter] modify ${name} MalfunctionChance`);
            props.MalfunctionChance = 0.03
        }
        if (props?.CheckTimeModifier ||  props?.CheckTimeModifier > 0) {
            this.logger.debug(`[ModParameter] modify ${name} CheckTimeModifier`);
            props.CheckTimeModifier = 0
        }
    }


    public applyBagMod(bagCat: BagCat): void {
        const validateutils = new ValidateUtils();
        const items: Record<string, ITemplateItem> = validateutils.getTemplateItems(this.dataService, this.logger)
        const bagIds: string[] = Object.values(bagCat.ids).map(bag => bag.id);

        const backPacks: ITemplateItem[] = Object.values(items).filter(
            (item: ITemplateItem) =>
                item?._id &&
                this.itemHelper.isOfBaseclass(item._id, Baseclass.BACKPACK) &&
                bagIds.includes(item._id)
        );
        if (backPacks.length === 0) {
            this.logger.debug("[ModParameter] No matching backpacks found for modification.");
            return;
        }

        for (const backPack of backPacks) {
            if (backPack?._props && backPack?._id && backPack?._name) {
                const backPackProps: IProps = backPack._props;
                const backPackId: string = backPack._id;
                const name: string = backPack._name;

                if (bagCat.excludedFilter) {
                    this.clearExcludedFilters(backPackProps, name);
                }

                if (bagCat.penality) {
                    this.applyBagPenality(backPackProps, name);
                }

                if (bagCat.resize && bagCat.resize !== 0) {
                    this.applyBagResize(backPackProps, backPackId, bagCat, backPack._name, validateutils);
                }
            }
        }
    }

    private clearExcludedFilters(backPackProps: IProps, name: string): void {
        let modified = false;
        backPackProps.Grids.forEach((grid: IGrid) => {
            grid._props.filters.forEach((filter: IGridFilter) => {
                filter.ExcludedFilter = []
                modified = true;
            })
        })
        if (modified) {
            this.logger.debug(`[ModParameter] Cleared ExcludedFilter(s) for backpack '${name}'`);
        } else {
            this.logger.debug(`[ModParameter] No ExcludedFilter to clear for backpack '${name}'`);
        }
    }

    private applyBagPenality(backPackProps: IProps, name: string): void {
        if (backPackProps.weaponErgonomicPenalty) {
            backPackProps.weaponErgonomicPenalty = 0
            this.logger.debug(`[ModParameter] modify weaponErgonomicPenalty '${name}'`);
        }
        if (backPackProps.mousePenalty) {
            backPackProps.mousePenalty = 0
            this.logger.debug(`[ModParameter] modify mousePenalty '${name}'`);
        }
        if (backPackProps?.Weight) {
            backPackProps.Weight = 0.1
            this.logger.debug(`[ModParameter] modify Weight '${name}'`);
        }
        if (backPackProps.speedPenaltyPercent) {
            backPackProps.speedPenaltyPercent = 0
            this.logger.debug(`[ModParameter] modify speedPenaltyPercent '${name}'`);
        }
    }

    private applyBagResize(backPackProps: IProps, backPackId: string, bagCat: BagCat, name: string, validateutils): void {
        const jsonBags: Record<string, Bag> = bagCat.ids;

        const jsonBag = jsonBags[backPackId];
        if (!jsonBag) {
            return;
        }

        const jsonGrids = jsonBag.Grids;
        if (!backPackProps?.Grids) {
            return;
        }
        let modified = false;
        for (const sptGrid of backPackProps.Grids) {
            const jsonGrid = sptGrid._id ? jsonGrids[sptGrid._id] : null;
            if (jsonGrid && sptGrid._props) {
                sptGrid._props.cellsH = validateutils.validateAndCastIntPmc(jsonGrid.cellsH);
                sptGrid._props.cellsV = validateutils.validateAndCastIntPmc(jsonGrid.cellsV);
                modified = true;
            }
        }
        if (!modified) {
            this.logger.debug(`[ModParameter] No resize applied to backpack '${name}' — no matching grids found.`);
        }

    }


}
