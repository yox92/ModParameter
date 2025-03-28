import {DatabaseService} from "@spt/services/DatabaseService";
import {ILogger} from "@spt/models/spt/utils/ILogger";
import {IAiming, IConfig, IGlobals, IStamina} from "@spt/models/eft/common/IGlobals";
import {ValidateUtils} from "../Utils/ValidateUtils";

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
         const validateUtils = new ValidateUtils();

        const globals: IGlobals | undefined = this.dataService.getGlobals();
        const config: IConfig | undefined = globals?.config;
        const aimingSpt: IAiming | undefined = config?.Aiming;
        const staminaSpt: IStamina | undefined = config?.Stamina;

        if (!globals || !aimingSpt || !staminaSpt || !config) {
            this.logger.debug(`[ModParameter] can not display PMC value`);
        }

        if (!validateUtils.istaminaIsOriginal(staminaSpt)) {
            this.logger.info(`[ModParameter] PMC ${this.GREEN}Stamina${this.RESET} properties(s) change`);
        }

        if (!validateUtils.iaimingIsOriginal(aimingSpt)) {
            this.logger.info(`[ModParameter] PMC ${this.GREEN}Aiming${this.RESET} properties(s) change`);
        }
    }
}