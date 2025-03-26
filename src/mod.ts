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
import {IGrid} from "@spt/models/eft/common/tables/ITemplateItem";
import {IBuff, IBuffs} from "@spt/models/eft/common/IGlobals";

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

        const buffs: IBuffs = dataService.getGlobals().config.Health.Effects.Stimulator.Buffs

        const muleBuff : IBuff[] = buffs.Buffs_MULE
        const propitalBuff : IBuff[] = buffs.BuffsPropital

        // WeightLimit
        muleBuff[0].Duration = 900
        muleBuff[0].Value = 0.5
        // HealthRate
        muleBuff[1].Duration = 900
        muleBuff[1].Value = -0.1

        // HealthRate
        propitalBuff[0].Duration = 300
        propitalBuff[0].Value = 1

        // SkillRate Metabolism
        propitalBuff[1].Duration = 300
        propitalBuff[1].Value = 20

        // SkillRate Health
        propitalBuff[2].Duration = 300
        propitalBuff[2].Value = 20

        // SkillRate Vitality
        propitalBuff[3].Duration = 300
        propitalBuff[3].Value = 20

        // SkillRate HandsTremor
        propitalBuff[4].Delay = 270
        propitalBuff[4].Duration = 30
        propitalBuff[4].Value = 0

        // SkillRate QuantumTunnelling
        propitalBuff[4].Delay = 270
        propitalBuff[4].Duration = 30
        propitalBuff[4].Value = 0

        let grids :IGrid[] = dataService.getTemplates().items[""]._props.Grids
        grids.map(grid => {
            grid._id = ""
            grid._props.cellsH
            grid._props.cellsV
        } )
        let magazineCount: number = dataService.getTemplates().items[""]._props.Cartridges[0]._max_count;
        if (!dataService || !logger || !itemHelper || !customItemService) {
            console.error(`[ModParameter] Critical error: Missing dependencies. Mod cannot function properly.`);
            return;
        }

        const itemService = new ItemService(logger,
            dataService,
            customItemService,
            itemHelper);

        const pmcService = new PmcService(logger, dataService);

        itemService.allTracer();
        itemService.cloneItems();
        pmcService.updatePmc();
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

        const clearCloneService = new ClearCloneService(logger, saveServer, itemHelper, localeService, dataService);
        const pmcModify = new PmcModifyService(logger, dataService);

        clearCloneService.clearAmmoWeaponMedicNotUseAnymore();
        clearCloneService.checkTracerAllAmmoDB();
        pmcModify.displayLog();
    }

}

module.exports = {mod: new ModParameter()};
