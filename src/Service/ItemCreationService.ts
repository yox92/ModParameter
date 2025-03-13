import {injectable} from "tsyringe";
import {ILogger} from "@spt-aki/models/spt/utils/ILogger";
import {HashUtil} from "@spt-aki/utils/HashUtil";
import {ItemHelper} from "@spt-aki/helpers/ItemHelper";
import {ItemBaseClassService} from "@spt-aki/services/ItemBaseClassService";
import {ICloner} from "@spt-aki/utils/cloners/ICloner";
import {IProps} from "@spt-aki/models/eft/common/ILocationBase";
import {ITemplateItem} from "@spt-aki/models/eft/common/tables/ITemplateItem";


@injectable()
export class ItemCreationService {

    constructor(
        private readonly logger: ILogger,
        private readonly tableData: any,
        @inject("ItemHelper") protected itemHelper: ItemHelper,
        @inject("ItemBaseClassService") protected itemBaseClassService: ItemBaseClassService,
        @inject("PrimaryCloner") protected cloner: ICloner,
        @inject("HashUtil") protected hashUtil: HashUtil
    ) {
    }

    public generateId(): string {
        return this.hashUtil.generate();
    }

    public updateBaseItemPropertiesWithOverrides(overrideProperties: IProps, itemClone: ITemplateItem): void {
        for (const propKey in overrideProperties) {
            itemClone._props[propKey] = overrideProperties[propKey];
        }
    }

    public addToItemsDb(newItemId: string, itemToAdd: ITemplateItem): void {
        this.tableData.templates.items[newItemId] = itemToAdd;
    }

    public addToHandbookDb(newItemId: string, parentId: string, priceRoubles: number): void {
        this.tableData.templates.handbook.Items.push({ Id: newItemId, ParentId: parentId, Price: priceRoubles });
    }

    public addToLocaleDbs(localeDetails: Record<string, any>, newItemId: string): void {
        for (const lang in this.tableData.locales.global) {
            const newLocaleDetails = localeDetails[lang] || localeDetails[Object.keys(localeDetails)[0]];
            this.tableData.locales.global[lang][`${newItemId} Name`] = newLocaleDetails.name;
            this.tableData.locales.global[lang][`${newItemId} ShortName`] = newLocaleDetails.shortName;
            this.tableData.locales.global[lang][`${newItemId} Description`] = newLocaleDetails.description;
        }
    }

    public addToFleaPriceDb(newItemId: string, fleaPriceRoubles: number): void {
        this.tableData.templates.prices[newItemId] = fleaPriceRoubles;
    }

    public addToWeaponShelf(newItemId: string): void {
        const wallStashIds = [
            "HIDEOUTAREACONTAINER_WEAPONSTAND_STASH_1",
            "HIDEOUTAREACONTAINER_WEAPONSTAND_STASH_2",
            "HIDEOUTAREACONTAINER_WEAPONSTAND_STASH_3",
        ];
        for (const wallId of wallStashIds) {
            const wall = this.itemHelper.getItem(wallId);
            if (wall[0]) {
                wall[1]._props.Grids[0]._props.filters[0].Filter.push(newItemId);
            }
        }
    }
}
