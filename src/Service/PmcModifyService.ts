import {DatabaseService} from "@spt/services/DatabaseService";
import {ILogger} from "@spt/models/spt/utils/ILogger";
import {IAiming, IConfig, IGlobals, IStamina} from "@spt/models/eft/common/IGlobals";

export class PmcModifyService {
    private readonly logger: ILogger;
    private readonly dataService: DatabaseService;
    private readonly GREEN: string = "\x1b[32m";
    private readonly RESET: string = "\x1b[0m";

    constructor(logger: ILogger, dataService: DatabaseService) {
        this.dataService = dataService;
        this.logger = logger;
    }

    /**
     * Logs whether the stamina or aiming values of the PMC have been modified.
     * Checks if the default stamina and aiming values have changed.
     */
    public displayLog(): void {
        const globals: IGlobals | undefined = this.dataService.getGlobals();
        const config: IConfig | undefined = globals?.config;
        const aimingSpt: IAiming | undefined = config?.Aiming;
        const staminaSpt: IStamina | undefined = config?.Stamina;

        if (!globals || !aimingSpt || !staminaSpt || !config) {
            this.logger.debug(`[ModParameter] can not display PMC value`);
        }

        if (!this.staminaIsOriginal(staminaSpt)) {
            this.logger.info(`[ModParameter] PMC ${this.GREEN}Stamina${this.RESET} properties(s) change`);
        }

        if (!this.aimingIsOriginal(aimingSpt)) {
            this.logger.info(`[ModParameter] PMC ${this.GREEN}Aiming${this.RESET} properties(s) change`);
        }
    }

    /**
     * PMC aiming by default ?
     */
    private aimingIsOriginal(aimingSpt: IAiming): boolean {
        return (
            aimingSpt.AimProceduralIntensity === 0.75 &&
            aimingSpt.RecoilHandDamping === 0.45 &&
            aimingSpt.RecoilDamping === 0.7 &&
            aimingSpt.ProceduralIntensityByPose.x === 0.6 &&
            aimingSpt.ProceduralIntensityByPose.y === 0.7 &&
            aimingSpt.ProceduralIntensityByPose.z === 1 &&
            aimingSpt.RecoilXIntensityByPose.x === 0.6 &&
            aimingSpt.RecoilXIntensityByPose.y === 0.7 &&
            aimingSpt.RecoilXIntensityByPose.z === 1
        );
    }

    /**
     * PMC stamina by default ?
     */
    private staminaIsOriginal(staminaSpt: IStamina): boolean {
        return (
            staminaSpt.SprintDrainRate === 4 &&
            staminaSpt.JumpConsumption === 14 &&
            staminaSpt.StandupConsumption.x === 10 &&
            staminaSpt.AimDrainRate === 1.1 &&
            staminaSpt.BaseRestorationRate === 4.5

        );
    }
}