import {ILogger} from "@spt-aki/models/spt/utils/ILogger";
import {IDatabaseTables} from "@spt-aki/models/spt/server/IDatabaseTables";
import {ITemplates} from "@spt-aki/models/spt/templates/ITemplates";
import {IProps, ITemplateItem} from "@spt-aki/models/eft/common/tables/ITemplateItem";
import {ItemUpdaterService} from "@/Service/ItemUpdaterService";
import {ItemCreationService} from "@/Service/ItemCreationService";
import { inject, injectable } from "tsyringe";

export class ItemClonerService {
    private readonly logger: ILogger;
    private readonly itemCreationService: ItemCreationService;

    constructor(logger: ILogger) {
        this.itemCreationService = ItemCreationService(this.logger,);
        this.logger = logger;
         @inject("ItemCreationService") private readonly itemCreationService: ItemCreationService
    }

    public applyCloner(iDatabaseTables: IDatabaseTables) {
        const templates: ITemplates | undefined = iDatabaseTables?.templates;
        const itemsSpt: Record<string, ITemplateItem> | undefined = templates?.items;
        const sptItem: ITemplateItem | undefined = itemsSpt["54527a984bdc2d4e668b4567"];
        const sptItemProps: IProps | undefined = sptItem._props;

        sptItemProps.Damage = 50;
        sptItemProps.PenetrationPower = 50;

        let new_id: string  = this.itemCreationService.generateId();

        this.itemCreationService.updateBaseItemPropertiesWithOverrides(sptItemProps, sptItem)

    }


}