import {ILogger} from "@spt/models/spt/utils/ILogger";
import {ITemplates} from "@spt/models/spt/templates/ITemplates";
import {IProps, ITemplateItem} from "@spt/models/eft/common/tables/ITemplateItem";
import {CustomItemService} from "@spt/services/mod/CustomItemService";
import {IHandbookBase, IHandbookItem} from "@spt/models/eft/common/tables/IHandbookBase";
import {CreateItemResult, ItemClone} from "../Entity/ItemClone";
import {ItemHelper} from "@spt/helpers/ItemHelper";
import {Languages} from "../Utils/Languages";
import {DatabaseService} from "@spt/services/DatabaseService";
import {ClonerUtils} from "../Utils/ClonerUtils";
import {AmmoCloneRegistry} from "../Entity/AmmoCloneRegistry";
import {ItemTypeEnum} from "../Entity/ItemTypeEnum";
import {WeaponCloneRegistry} from "../Entity/WeaponCloneRegistry";
import {ItemProps} from "../Entity/ItemProps";
import {Ammo} from "../Entity/Ammo";
import {Medic} from "../Entity/Medic";
import {MedicCloneRegistry} from "../Entity/MedicCloneRegistry";

export class ItemClonerService {
    private readonly logger: ILogger;
    private readonly dataService: DatabaseService;
    private readonly customItemService: CustomItemService;
    private readonly itemHelper: ItemHelper;
    private readonly defaultPrice: number = 127
    private readonly defaultHandbookPrice: number = 127

    constructor(logger: ILogger,
                dataService: DatabaseService,
                customItemService: CustomItemService,
                itemHelper: ItemHelper) {
        this.logger = logger;
        this.dataService = dataService;
        this.customItemService = customItemService;
        this.itemHelper = itemHelper;
    }

    /**
     * Applies cloning logic to an item based on its type (Ammo or Weapon).
     * Validates input properties, fetches necessary metadata from the database,
     * and creates a new cloned item while ensuring its proper integration.
     *
     * @param props The modified properties for the cloned item.
     * @param id The original item's template ID (_tpl).
     * @param name The display name of the item being cloned.
     * @param shortName The short name of the cloned item.
     * @param itemTypeEnum The type of the item (Ammo or Weapon).
     */
    public applyClone(props: Partial<ItemProps> | Partial<Ammo>| Partial<Medic>,
                      id: string,
                      name: string,
                      shortName: string,
                      itemTypeEnum: ItemTypeEnum
    ) {
        if (!props || Object.keys(props).length === 0) {
            this.logger.debug(`[ModParameter] Error with ${name} : missing or empty properties`)
            return;
        }

        const templates: ITemplates | undefined = this.dataService.getTables().templates;
        let price: number | undefined = this.dataService.getTemplates().prices[id];
        const handbook: IHandbookBase | undefined = this.dataService.getHandbook();

        const iHandbookItems: IHandbookItem[] | undefined = handbook.Items;
        const foundItem: IHandbookItem | undefined = iHandbookItems.find(item => item.Id === id);
        let handbookParentId: string | undefined;
        let handbookPrice: number | undefined;
        let sptItems: Record<string, ITemplateItem> | undefined;
        let sptItem: ITemplateItem | undefined;

        if (!iHandbookItems || !foundItem) {
            this.logger.debug(`no handbook found item : ${name} id :${id}`);
        } else {
            handbookParentId = foundItem.ParentId
            handbookPrice = foundItem.Price
        }

        if (!templates) {
            this.logger.debug(`no templates found item ${name} id :${id}`);
        } else {
            sptItems = templates?.items;
            sptItem = sptItems[id];
        }

        const locales = Languages.generateLocales(name, shortName);

        if (!id || !sptItem._parent || !handbookParentId || !locales) {
            this.logger.debug(`[ModParameter] can not clone ${name} : leak member parameters id :${id}`)
            return;
        }

        if (itemTypeEnum === ItemTypeEnum.Ammo) {
            this.creatAmmoClone(id,
                props,
                sptItem._parent,
                AmmoCloneRegistry.getClonedId(id),
                this.applyPriceFactor(price, props.priceFactor), // price
                handbookPrice,
                handbookParentId,
                locales,
                name)
        } else if (itemTypeEnum === ItemTypeEnum.Weapon) {
            this.creatWeaponClone(id,
                props,
                sptItem._parent,
                WeaponCloneRegistry.getClonedId(id),
                this.applyPriceFactor(price, props.priceFactor), // price
                handbookPrice,
                handbookParentId,
                locales,
                shortName)
        } else if (itemTypeEnum === ItemTypeEnum.Medic) {
            this.creatMedicClone(id,
                props,
                sptItem._parent,
                MedicCloneRegistry.getClonedId(id),
                this.applyPriceFactor(price, props.priceFactor), // price
                handbookPrice,
                handbookParentId,
                locales,
                shortName)
        } else {
            this.logger.debug("[ModParameter] No Type Item Find For Cloning")
        }
    }

    /**
     * Creates a cloned ammunition item with the given properties.
     * Ensures that the cloned ammo is properly assigned a new template ID,
     * integrated with the trader system, and its compatibility is updated
     * across relevant game mechanics.
     *
     * @param id The original ammo template ID.
     * @param cloneSptProps The properties of the cloned ammunition.
     * @param parentId The parent ID of the cloned ammo.
     * @param cloneId The new unique ID assigned to the cloned ammo.
     * @param price The in-game price of the cloned ammunition.
     * @param handbookPrice The handbook reference price.
     * @param handbookParentId The parent category ID in the handbook.
     * @param locales The localized names and descriptions.
     * @param name The full name of the cloned ammunition.
     */
    private creatAmmoClone(id: string,
                           cloneSptProps: IProps,
                           parentId: string,
                           cloneId: string,
                           price: number,
                           handbookPrice: number,
                           handbookParentId: string,
                           locales,
                           name: string): void {
        const clonerUtils = new ClonerUtils(this.logger);
        const clone: ItemClone = new ItemClone(
            id,
            cloneSptProps,
            parentId,
            cloneId,
            price && price > 0 ? price : this.defaultPrice,
            handbookPrice && handbookPrice > 0 ? handbookPrice : this.defaultHandbookPrice,
            handbookParentId,
            locales
        );

        const result: CreateItemResult = this.customItemService.createItemFromClone(clone);
        if (result.success) {
            clonerUtils.addToTrader(id, result.itemId, this.dataService, name, ItemTypeEnum.Ammo);
            clonerUtils.propagateAmmoCompatibility(id, result.itemId, this.itemHelper, this.dataService);
            this.logger.debug(`[ModParameter] ${name} have new clone ! `);
        } else {
            this.logger.debug(`[ModParameter] Clone do not work for ${name} `)
        }
    }

    /**
     * Creates a cloned weapon item with the given properties.
     * Ensures that the cloned weapon is properly assigned a new template ID,
     * integrated with the trader system, and maintains appropriate pricing and classification.
     *
     * @param id The original weapon template ID.
     * @param cloneSptProps The properties of the cloned weapon.
     * @param parentId The parent ID of the cloned weapon.
     * @param cloneId The new unique ID assigned to the cloned weapon.
     * @param price The in-game price of the cloned weapon.
     * @param handbookPrice The handbook reference price.
     * @param handbookParentId The parent category ID in the handbook.
     * @param locales The localized names and descriptions.
     * @param shortName The short name of the cloned weapon.
     */
    private creatWeaponClone(id: string,
                             cloneSptProps: IProps,
                             parentId: string,
                             cloneId: string,
                             price: number,
                             handbookPrice: number,
                             handbookParentId: string,
                             locales,
                             shortName: string): void {
        const clonerUtils = new ClonerUtils(this.logger);
        const clone: ItemClone = new ItemClone(
            id,
            cloneSptProps,
            parentId,
            cloneId,
            price && price > 0 ? price : this.defaultPrice,
            handbookPrice && handbookPrice > 0 ? handbookPrice : this.defaultHandbookPrice,
            handbookParentId,
            locales
        );
        const result: CreateItemResult = this.customItemService.createItemFromClone(clone);
        if (result.success) {
            clonerUtils.addToTrader(id, result.itemId, this.dataService, shortName, ItemTypeEnum.Weapon);
            this.logger.debug(`[ModParameter] ${shortName} have new clone ! `);
        } else {
            this.logger.debug(`[ModParameter] Clone do not work for ${shortName} `)
        }
    }
    /**
     * Creates a cloned medic item with the given properties.
     * Ensures that the cloned medic is properly assigned a new template ID,
     * integrated with the trader system, and maintains appropriate pricing and classification.
     *
     * @param id The original medic template ID.
     * @param cloneSptProps The properties of the cloned medic.
     * @param parentId The parent ID of the cloned medic.
     * @param cloneId The new unique ID assigned to the cloned medic.
     * @param price The in-game price of the cloned medic.
     * @param handbookPrice The handbook reference price.
     * @param handbookParentId The parent category ID in the handbook.
     * @param locales The localized names and descriptions.
     * @param shortName The short name of the cloned medic.
     */
    private creatMedicClone(id: string,
                             cloneSptProps: IProps,
                             parentId: string,
                             cloneId: string,
                             price: number,
                             handbookPrice: number,
                             handbookParentId: string,
                             locales,
                             shortName: string): void {
        const clonerUtils = new ClonerUtils(this.logger);
        const clone: ItemClone = new ItemClone(
            id,
            cloneSptProps,
            parentId,
            cloneId,
            price && price > 0 ? price : this.defaultPrice,
            handbookPrice && handbookPrice > 0 ? handbookPrice : this.defaultHandbookPrice,
            handbookParentId,
            locales
        );
        const result: CreateItemResult = this.customItemService.createItemFromClone(clone);
        if (result.success) {
            clonerUtils.addToTrader(id, result.itemId, this.dataService, shortName, ItemTypeEnum.Medic);
            this.logger.debug(`[ModParameter] ${shortName} have new clone ! `);
        } else {
            this.logger.debug(`[ModParameter] Clone do not work for ${shortName} `)
        }
    }

    public applyPriceFactor(price: number, priceFactor: number): number {
        price = price * priceFactor;
        return price;
    }


}