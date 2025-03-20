import {DependencyContainer} from "tsyringe";
import {ItemService} from "./Service/ItemService";
import {PmcService} from "./Service/PmcService";
import type {ILogger} from "@spt/models/spt/utils/ILogger";
import {IPostDBLoadMod} from "@spt/models/external/IPostDBLoadMod";
import {CustomItemService} from "@spt/services/mod/CustomItemService";
import {DatabaseService} from "@spt/services/DatabaseService";
import {ItemHelper} from "@spt/helpers/ItemHelper";
import {PreSptModLoader} from "@spt/loaders/PreSptModLoader";
import {IPostSptLoadMod} from "@spt/models/external/IPostSptLoadMod";
import {SaveServer} from "@spt/servers/SaveServer";
import {ClearCloneService} from "./Service/ClearCloneService";
import {LocaleService} from "@spt/services/LocaleService";
import {PmcModifyService} from "./Service/PmcModifyService";
import {MedicalService} from "./Service/MedicalService";

class ModParameter implements IPostDBLoadMod, PreSptModLoader, IPostSptLoadMod {

    /**
     * Initializes the module and registers the dependency container.
     * @param container The instance of the dependency container.
     */
    public postDBLoad(container: DependencyContainer): void {
        const dataService: DatabaseService = container.resolve<DatabaseService>("DatabaseService")
        const customItemService: CustomItemService = container.resolve<CustomItemService>("CustomItemService");
        const logger: ILogger = container.resolve<ILogger>("WinstonLogger");
        const itemHelper: ItemHelper = container.resolve<ItemHelper>("ItemHelper");
        dataService.getGlobals()
        if (!dataService || !logger || !itemHelper || !customItemService) {
            console.error(`[ModParameter] Critical error: Missing dependencies. Mod cannot function properly.`);
            return;
        }

        const itemService = new ItemService(logger,
            dataService,
            customItemService,
            itemHelper);

        const pmcService = new PmcService(logger, dataService);
        const medicalService = new MedicalService(logger, itemHelper, dataService);

        itemService.cloneItems();
        pmcService.updatePmc();
        medicalService.applyMedicalBuff()


    }

    public postSptLoad(container: DependencyContainer): void {
        const logger = container.resolve<ILogger>("WinstonLogger");
        const saveServer: SaveServer = container.resolve<SaveServer>("SaveServer");
        const itemHelper: ItemHelper = container.resolve<ItemHelper>("ItemHelper");
        const localeService: LocaleService = container.resolve<LocaleService>("LocaleService");
        const dataService: DatabaseService = container.resolve<DatabaseService>("DatabaseService")

        if (!logger || !saveServer || !localeService || !dataService) {
            console.error(`[ModParameter] Critical error: Missing dependencies. Mod cannot function properly.`);
            return;
        }

        if (!saveServer.getProfiles()) {
            console.error(`[ModParameter] Critical error: Missing Profil on SPT. Please create at least ONE`);
            return;
        }

        const clearCloneService = new ClearCloneService(logger, saveServer, itemHelper, localeService);
        const pmcModify = new PmcModifyService(logger, dataService);

        clearCloneService.clearAmmoWeaponNotUseAnymore()
        pmcModify.displayLog()
    }


    // private overrideDebugMethod(logger: ILogger): void {
    //     const originalDebugMethod = logger.debug.bind(logger);
    //
    //     logger.debug = (data: string | Record<string, unknown>, onlyShowInConsole?: boolean): void => {
    //         if (!debug) return;
    //
    //         originalDebugMethod(data, false);
    //     };
    // }


}

module.exports = {mod: new ModParameter()};
