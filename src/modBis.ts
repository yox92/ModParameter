import { IContainer } from "./Entity/Container";
import { ILogger } from "./Entity/Logger";
import { WeaponService } from "./Service/WeaponService";

interface IGlobalConfig {
    Aiming?: {
        AimProceduralIntensity?: number;
        AimingSpeedMultiplier?: number;
        WeaponStability?: number; // Added for aimStability support
    };
}

interface IDatabaseServer {
    getTables(): {
        globals: {
            config: IGlobalConfig;
        };
    };
}

class MyWeaponMod {
    private readonly modName: string;

    constructor() {
        this.modName = "MyWeaponMod";
    }

    public postDBLoad(container: IContainer): void {
        const logger = container.resolve<ILogger>("WinstonLogger");
        const databaseServer = container.resolve<IDatabaseServer>("DatabaseServer");

        // Appeler listPropOfGlobals après le chargement de la DB
        this.listPropOfGlobals(container);
    }

    public listPropOfGlobals(container: IContainer): void {
        const logger = container.resolve<ILogger>("WinstonLogger");
        const databaseServer = container.resolve<IDatabaseServer>("DatabaseServer");
        const tables = databaseServer.getTables();

        if (!tables.globals) {
            logger.error(`[${this.modName}] La table "globals" est introuvable.`);
            return;
        }

        logger.info(`[${this.modName}] Liste des propriétés de "globals" :`);

        // Parcours récursif uniquement des "globals.config"
        this.logRecursiveProperties(logger, tables.globals.config);
    }

    /**
     * Fonction récursive pour parcourir et afficher les propriétés de "globals.config".
     */
    private logRecursiveProperties(logger: ILogger, obj: any, prefix: string = "config"): void {
        Object.entries(obj).forEach(([key, value]) => {
            const fullKey = prefix ? `${prefix}.${key}` : key;

            if (typeof value === "object" && value !== null) {
                logger.info(`- ${fullKey}: [Object]`);
                this.logRecursiveProperties(logger, value, fullKey); // Appel récursif pour explorer les enfants
            } else {
                logger.info(`- ${fullKey}: ${JSON.stringify(value, null, 2)}`);
            }
        });
    }
}

module.exports = { mod: new MyWeaponMod() };
