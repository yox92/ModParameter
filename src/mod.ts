import {DependencyContainer} from "tsyringe";
import {ItemService} from "./Service/ItemService";
import {PmcService} from "./Service/PmcService";
import type {ILogger} from "@spt/models/spt/utils/ILogger";
import {IPostDBLoadMod} from "@spt/models/external/IPostDBLoadMod";
import {CustomItemService} from "@spt/services/mod/CustomItemService";
import {DatabaseService} from "@spt/services/DatabaseService";
import {colorBackgroundDebug, colorTextDebug, debug} from "./config";
import {ItemHelper} from "@spt/helpers/ItemHelper";
import {PreSptModLoader} from "@spt/loaders/PreSptModLoader";

class ModParameter implements IPostDBLoadMod, PreSptModLoader {

    public preSptLoad(container: DependencyContainer): void {
        console.log(`!!! Debug Mode: ${debug ? "Enabled" : "Disabled"} !!!`);
        container.afterResolution("WinstonLogger", (_t, result: ILogger) => {
            const originalDebugMethod = result.debug.bind(result);

            result.debug = (data: string | Record<string, unknown>, onlyShowInConsole?: boolean): void => {
                if (!debug) return;
                result.logWithColor(data, colorTextDebug, colorBackgroundDebug);
            };
        }, {frequency: "Always"});
    }

    /**
     * Initializes the module and registers the dependency container.
     * @param container The instance of the dependency container.
     */
    public postDBLoad(container: DependencyContainer): void {
        const dataService: DatabaseService = container.resolve<DatabaseService>("DatabaseService")
        const customItemService: CustomItemService = container.resolve<CustomItemService>("CustomItemService");
        const logger: ILogger = container.resolve<ILogger>("WinstonLogger");
        const itemHelper: ItemHelper = container.resolve<ItemHelper>("ItemHelper");

        if (!dataService || !logger || !itemHelper || !customItemService) {
            console.error(`[AttributMod] Critical error: Missing dependencies. Mod cannot function properly.`);
            return;
        }

        const itemService = new ItemService(logger,
            dataService,
            customItemService,
            itemHelper);
        const pmcService = new PmcService(logger, dataService);
        itemService.cloneItems();
        pmcService.updatePmc();

    }

    private overrideDebugMethod(logger: ILogger): void {
        const originalDebugMethod = logger.debug.bind(logger);

        logger.debug = (data: string | Record<string, unknown>, onlyShowInConsole?: boolean): void => {
            if (!debug) return;

            originalDebugMethod(data, false);
        };
    }


}

module.exports = {mod: new ModParameter()};
