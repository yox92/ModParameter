import {IContainer} from "./Entity/Container";
import {ILogger} from "./Entity/Logger";
import {IDatabaseServer} from "./Entity/DatabaseServer";
import {WeaponService} from "./Service/WeaponService";

class MyWeaponMod {
    private readonly modName: string;

    constructor() {
        this.modName = "MyWeaponMod";
    }

    public postDBLoad(container: IContainer): void {
        const logger = container.resolve<ILogger>("WinstonLogger");
        const databaseServer = container.resolve<IDatabaseServer>("DatabaseServer");
        const weaponService = new WeaponService(logger, databaseServer);

        weaponService.updateWeapons();
    }
}

module.exports = {mod: new MyWeaponMod()};
