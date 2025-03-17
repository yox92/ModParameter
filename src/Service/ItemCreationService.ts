// import {inject, injectable} from "tsyringe";
// import {ILogger} from "@spt/models/spt/utils/ILogger";
// import {HashUtil} from "@spt/utils/HashUtil";
// import {ItemHelper} from "@spt/helpers/ItemHelper";
// import { IProps } from "@spt/models/eft/common/tables/ITemplateItem";
// import {ItemBaseClassService} from "@spt/services/ItemBaseClassService";
// import {ICloner} from "@spt/utils/cloners/ICloner";
// import {ITemplateItem} from "@spt/models/eft/common/tables/ITemplateItem";
// import {IDatabaseTables} from "@spt/models/spt/server/IDatabaseTables";
// import {LocaleDetails, NewItemFromCloneDetails} from "@spt/models/spt/mod/NewItemDetails";
//
//
// @injectable()
// export class ItemCreationService {
//     @inject("HashUtil") private readonly hashUtil: HashUtil;
//     @inject("ItemHelper") protected itemHelper: ItemHelper
//     @inject("ItemBaseClassService") protected itemBaseClassService: ItemBaseClassService;
//     @inject("PrimaryCloner") protected cloner: ICloner;
//
//     constructor(
//         private readonly logger: ILogger,
//         private readonly iDatabaseTables: IDatabaseTables,
//         //
//     ) {}
//
//     public generateId(): string {
//         return this.hashUtil.generate();
//     }
//
//     public updateBaseItemPropertiesWithOverrides(overrideProperties: IProps, itemClone: ITemplateItem): void {
//         for (const propKey in overrideProperties) {
//             itemClone._props[propKey] = overrideProperties[propKey];
//         }
//     }
//
//     public addToItemsDb(newItemId: string, itemToAdd: ITemplateItem): void {
//         this.iDatabaseTables.templates.items[newItemId] = itemToAdd;
//     }
//
//     public addToHandbookDb(newItemId: string, parentId: string, priceRoubles: number): void {
//         this.iDatabaseTables.templates.handbook.Items.push({ Id: newItemId, ParentId: parentId, Price: priceRoubles });
//     }
//
//     public addToLocaleDbs(localeDetails: Record<string, LocaleDetails>, newItemId: string): void {
//         for (const lang in this.iDatabaseTables.locales.global) {
//             const newLocaleDetails = localeDetails[lang] || localeDetails[Object.keys(localeDetails)[0]];
//             this.iDatabaseTables.locales.global[lang][`${newItemId} Name`] = newLocaleDetails.name;
//             this.iDatabaseTables.locales.global[lang][`${newItemId} ShortName`] = newLocaleDetails.shortName;
//             this.iDatabaseTables.locales.global[lang][`${newItemId} Description`] = newLocaleDetails.description;
//         }
//     }
//
//     public addToFleaPriceDb(newItemId: string, fleaPriceRoubles: number): void {
//         this.iDatabaseTables.templates.prices[newItemId] = fleaPriceRoubles;
//     }
//
//     public addToWeaponShelf(newItemId: string): void {
//         const wallStashIds = [
//             "HIDEOUTAREACONTAINER_WEAPONSTAND_STASH_1",
//             "HIDEOUTAREACONTAINER_WEAPONSTAND_STASH_2",
//             "HIDEOUTAREACONTAINER_WEAPONSTAND_STASH_3",
//         ];
//         for (const wallId of wallStashIds) {
//             const wall = this.itemHelper.getItem(wallId);
//             if (wall[0]) {
//                 wall[1]._props.Grids[0]._props.filters[0].Filter.push(newItemId);
//             }
//         }
//     }
// }
