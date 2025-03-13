import {ItemService} from "./Service/ItemService";
import {PmcService} from "./Service/PmcService";
import { DependencyContainer } from "tsyringe";
import type { ILogger } from "@spt-aki/models/spt/utils/ILogger";
import { IPostDBLoadMod } from "@spt-aki/models/external/IPostDBLoadMod";
import { DatabaseServer } from "@spt-aki/servers/DatabaseServer";

class AttributMod implements IPostDBLoadMod {
    private dependencyContainer: DependencyContainer

    /**
     * Initializes the module and registers the dependency container.
     * @param dependencyContainer The instance of the dependency container.
     */
    public postDBLoad(dependencyContainer: DependencyContainer): void {
        this.dependencyContainer = dependencyContainer
        const tableData = this.dependencyContainer.resolve<DatabaseServer>("DatabaseServer").getTables()
        const logger = dependencyContainer.resolve<ILogger>("WinstonLogger");

        if (!tableData || !logger) {
            console.error(`[AttributMod] Critical error: Missing dependencies. Mod cannot function properly.`);
            return;
        }

        const itemService = new ItemService(logger, tableData);
        const pmcService = new PmcService(logger, tableData);

        itemService.updateItems();
        itemService.updateItems();
        pmcService.updatePmc();

    }
}

module.exports = {mod: new AttributMod()};
