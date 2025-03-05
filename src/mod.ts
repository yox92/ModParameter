
interface IDatabaseServer {
    getTables(): {
        templates: {
            items: Record<string, IItem>;
        };
        globals: {
            config: IGlobalConfig;
        };
    };
}

class CustomWeapon {
    private readonly modName: string;

    constructor() {
        this.modName = "CustomWeapon";
    }

    // figures out if something's increased or decreased
    private calculateEffect(value: number): string {
        if (value < 1) {
            return `${Math.round((1 - value) * 100)}% less`;
        } else if (value > 1) {
            return `${Math.round((value - 1) * 100)}% more`;
        }
        return "same as normal";
    }

    private validateConfig(config: IModConfig): void {
        const validateRange = (value: number, name: string): void => {
            if (value <= 0) {
                throw new Error(`${name} must be greater than 0`);
            }
        };

        // check recoil settings
        Object.entries(config.recoil).forEach(([key, value]) => {
            validateRange(value, `Recoil ${key}`);
        });

        // check aim settings
        Object.entries(config.aiming).forEach(([key, value]) => {
            validateRange(value, `Aiming ${key}`);
        });
    }

    private modifyWeaponProps(props: IItem["_props"], config: IModConfig, isPlayerWeapon: boolean): void {
        if (isPlayerWeapon && props.RecoilForceUp !== undefined) {
            // vertical recoil
            props.RecoilForceUp *= config.recoil.verticalMultiplier;

            // horizontal recoil
            if (props.RecoilForceBack !== undefined) {
                props.RecoilForceBack *= config.recoil.horizontalMultiplier;
            }

            // screen shake
            if (props.CameraRecoil !== undefined && props.CameraRecoil > 0) {
                props.CameraRecoil *= config.recoil.cameraMultiplier;
            }

            // centering speed
            if (props.Convergence !== undefined) {
                props.Convergence *= config.recoil.convergenceMultiplier;
            }

            // bullet spread
            if (props.RecoilDispersion !== undefined) {
                props.RecoilDispersion *= config.recoil.dispersionMultiplier;
            }

            // handling speed
            if (props.Ergonomics !== undefined) {
                props.Ergonomics *= config.aiming.ergonomicsMultiplier;
            }

            // aim steadiness
            if (props.AimSway !== undefined) {
                props.AimSway *= config.aiming.swayIntensity;
            }
        }
    }

    private modifyGlobalSettings(globals: IGlobalConfig, config: IModConfig): void {
        if (globals.Aiming) {
            // sway amount
            if (globals.Aiming.AimProceduralIntensity !== undefined) {
                globals.Aiming.AimProceduralIntensity *= config.aiming.swayIntensity;
            }

            // aim speed
            if (globals.Aiming.AimingSpeedMultiplier !== undefined) {
                globals.Aiming.AimingSpeedMultiplier *= config.aiming.mouseSensitivity;
            }

            // stability when aiming
            if (globals.Aiming.WeaponStability !== undefined) {
                globals.Aiming.WeaponStability *= config.aiming.aimStability;
            }
        }
    }

    public postDBLoad(container: IContainer): void {
        try {
            // Validate config before applying changes
            this.validateConfig(config);

            const logger = container.resolve("WinstonLogger") as ILogger;
            const databaseServer = container.resolve("DatabaseServer") as IDatabaseServer;
            const tables = databaseServer.getTables();

            // Get player profile
            const profileHelper = container.resolve("ProfileHelper") as IProfileHelper;
            const playerProfile = profileHelper.getPmcProfile();
            const playerItems = new Set<string>();

            // Get list of player's weapon IDs
            if (playerProfile?.Inventory?.items) {
                playerProfile.Inventory.items.forEach(item => {
                    playerItems.add(item._tpl);
                });
            }

            // Modify weapons
            Object.entries(tables.templates.items).forEach(([templateId, item]) => {
                const isPlayerWeapon = playerItems.has(templateId);
                this.modifyWeaponProps(item._props, config, isPlayerWeapon);
            });

            // Modify global settings (only affects player)
            this.modifyGlobalSettings(tables.globals.config, config);

            logger.info(`${this.modName}: Successfully applied modifications to player weapons only`);
        } catch (error) {
            const logger = container.resolve("WinstonLogger") as ILogger;
            logger.info(`${this.modName}: Error applying modifications: ${error instanceof Error ? error.message : error}`);
        }
    }
}

export = { mod: new RecoilStandalone() };