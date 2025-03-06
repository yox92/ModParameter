import {IContainer} from "./Entity/Container";
import {ILogger} from "./Entity/Logger";
import {IDatabaseServer} from "./Entity/DatabaseServer";
import {WeaponService} from "./Service/WeaponService";
import {PmcService} from "./Service/PmcService";

class MyWeaponMod {
    private readonly modName: string;

    constructor() {
        this.modName = "MyWeaponMod";
    }

    public postDBLoad(container: IContainer): void {
        const logger = container.resolve<ILogger>("WinstonLogger");
        const databaseServer = container.resolve<IDatabaseServer>("DatabaseServer");
        const weaponService = new WeaponService(logger, databaseServer);
        const pmcService = new PmcService(logger, databaseServer);

        if (!logger) {
            throw new Error("[MyWeaponMod] Logger service not found.");
        }

        if (!databaseServer) {
            throw new Error("[MyWeaponMod] DatabaseServer service not found.");
        }

        weaponService.updateWeapons();
        pmcService.updatePmc();
    }
}

module.exports = {mod: new MyWeaponMod()};
