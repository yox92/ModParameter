import { IProps } from "@spt/models/eft/common/tables/ITemplateItem";

export class ItemClone {
    itemTplToClone: string;
    overrideProperties: IProps;
    parentId: string;
    newId: string = "";
    fleaPriceRoubles: number;
    handbookPriceRoubles: number;
    handbookParentId: string;
    locales: Record<string, LocaleDetails>;

    constructor(
        itemTplToClone: string,
        overrideProperties: IProps,
        parentId: string,
        newId: string,
        fleaPriceRoubles: number,
        handbookPriceRoubles: number,
        handbookParentId: string,
        locales: Record<string, LocaleDetails>
    ) {
        this.itemTplToClone = itemTplToClone;
        this.overrideProperties = overrideProperties;
        this.parentId = parentId;
        this.newId = newId;
        this.fleaPriceRoubles = fleaPriceRoubles;
        this.handbookPriceRoubles = handbookPriceRoubles;
        this.handbookParentId = handbookParentId;
        this.locales = locales;
    }
}

export class LocaleDetails {
    name: string;
    shortName: string;
    description: string;
}

export class CreateItemResult {
    constructor() {
        this.success = false;
        this.errors = [];
    }

    success: boolean;
    itemId: string;
    errors: string[];
}





