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
    public applyClone(props: Partial<ItemProps> | Partial<Ammo>,
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
        const price: number | undefined = this.dataService.getTemplates().prices[id];
        const handbook: IHandbookBase | undefined = this.dataService.getHandbook();

        const iHandbookItems: IHandbookItem[] | undefined = handbook.Items;
        const foundItem: IHandbookItem | undefined = iHandbookItems.find(item => item.Id === id);
        const handbookParentId: string | undefined = foundItem.ParentId
        const handbookPrice: number | undefined = foundItem.Price

        const sptItems: Record<string, ITemplateItem> | undefined = templates?.items;
        const sptItem: ITemplateItem | undefined = sptItems[id];

        const checks = [
            {name: "templates", value: this.dataService.getTables().templates},
            {name: "handbook", value: this.dataService.getHandbook()},
            {name: "iHandbookItems", value: this.dataService.getHandbook()?.Items},
            {name: "foundItem", value: this.dataService.getHandbook()?.Items?.find(item => item.Id === id)},
            {
                name: "handbookParentId",
                value: this.dataService.getHandbook()?.Items?.find(item => item.Id === id)?.ParentId
            },
            {name: "sptItems", value: this.dataService.getTables().templates?.items},
            {name: "sptItem", value: this.dataService.getTables().templates?.items?.[id]}
        ];

        for (const check of checks) {
            if (check.value === null || check.value === undefined) {
                this.logger.debug(`[ModParameter] ERROR : ${check.name} are null or undefined`);
            }
        }

        const locales = Languages.generateLocales(name, shortName);

        if (!id || !sptItem._parent || !handbookParentId || !locales) {
            this.logger.debug(`[ModParameter] can not clone ${name} : leak member parameters`)
            return;
        }

        if (itemTypeEnum === ItemTypeEnum.Ammo) {
            this.creatAmmoClone(id,
                props,
                sptItem._parent,
                AmmoCloneRegistry.getClonedId(id),
                price,
                handbookPrice,
                handbookParentId,
                locales,
                name)
        } else if (itemTypeEnum === ItemTypeEnum.Weapon) {
            this.creatWeaponClone(id,
                props,
                sptItem._parent,
                WeaponCloneRegistry.getClonedId(id),
                price,
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


}