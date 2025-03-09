import {ItemService} from "./Service/ItemService";
import {PmcService} from "./Service/PmcService";
import { DependencyContainer } from "tsyringe";
// import {ILogger} from "@spt-server/models/spt/utils/ILogger";
// import {DatabaseServer} from "@spt-server/servers/DatabaseServer";
// import {IPostDBLoadMod} from "@spt-server/models/external/IPostDBLoadMod";
import type { Ilogger } from "@spt-aki/models/spt/utils/Ilogger";
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
        const logger = dependencyContainer.resolve<Ilogger>("WinstonLogger");

        if (!tableData || !logger) {
            console.error(`[AttributMod] Critical error: Missing dependencies. Mod cannot function properly.`);
            return;
        }

        const itemService = new ItemService(logger, tableData);
        const pmcService = new PmcService(logger, tableData);

        itemService.updateItems();
        pmcService.updatePmc();

    }
}

module.exports = {mod: new AttributMod()};
