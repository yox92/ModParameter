import { ItemService } from "./Service/ItemService";
import { PmcService } from "./Service/PmcService";
import { IPostDBLoadMod } from "@spt-server/models/external/IPostDBLoadMod";
import { DependencyContainer } from "@spt-server/models/external/tsyringe";
import { ILogger } from "@spt-server/models/spt/utils/ILogger";
import { DependencyUtils } from "./Service/DependencyUtils";
import { IDatabaseTables } from "@spt-server/models/spt/server/IDatabaseTables";

class ModItemPmcStat implements IPostDBLoadMod {
    private modName: string;

    constructor() {
        this.modName = "ModItemPmcStat";
    }

    /**
     * Initializes the module and registers the dependency container.
     * @param dependencyContainer The instance of the dependency container.
     */
    public postDBLoad(dependencyContainer: DependencyContainer): void {
        DependencyUtils.initialize(dependencyContainer);

        const tableData: IDatabaseTables | null = DependencyUtils.getTableData();
        const logger: ILogger | null = DependencyUtils.getLogger();

        if (!tableData || !logger) {
            console.error(`[${this.modName}] Critical error: Missing dependencies. Mod cannot function properly.`);
            return;
        }

        const itemService = new ItemService(logger, tableData);
        const pmcService = new PmcService(logger, tableData);

        itemService.updateItems();
        pmcService.updatePmc();

    }
}

module.exports = { mod: new ModItemPmcStat() };
