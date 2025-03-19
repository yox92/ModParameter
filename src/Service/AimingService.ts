import {ILogger} from "@spt/models/spt/utils/ILogger";
import {DatabaseService} from "@spt/services/DatabaseService";
import {IAiming, IConfig, IGlobals, IStamina} from "@spt/models/eft/common/IGlobals";
import {Aiming} from "../Entity/Aiming";
import {ValidateUtils} from "../Utils/ValidateUtils";
import {Stamina} from "../Entity/Stamina";

export class AimingService {
    private readonly logger: ILogger;

    constructor(logger: ILogger) {
        this.logger = logger;
    }

    /**
     * Applies modifications from a JSON PMC attributes to an SPT attributes.
     * If any value is invalid, the modification is skipped for that item.
     * @param aimingJson The PMC attributes data aiming from JSON
     * @param staminaJson The PMC attributes data stamina from JSON
     * @param dataService dataservice from the SPT database
     * @returns true if the attributes were modified, false if skipped
     */
    public applyModifications(aimingJson: Aiming, staminaJson: Stamina, dataService: DatabaseService): boolean {

        const validateUtils = new ValidateUtils();
        this.logger.debug(`[ModParameter] Starting Aiming modifications...`);

        const globals: IGlobals | undefined = dataService.getGlobals();
        const config: IConfig | undefined = globals?.config;
        const aimingSpt: IAiming | undefined = config?.Aiming;
        const staminaSpt: IStamina | undefined = config?.Stamina;

        if (!globals || !config || !aimingSpt) {
            this.logger.debug(`[ModParameter] Invalid Global structure. Modification aborted. Missing: ${
                !globals ? "globals " : ""
            }${!config ? "config " : ""}${!aimingSpt ? "aiming " : ""}`.trim());
            return false;
        }

        if (!validateUtils.aimingIsOriginal(aimingJson)) {
            this.logger.debug(`[ModParameter] modifications aiming.`)
            this.assigneAttributsAiming(aimingJson, aimingSpt, config);
        }
        if (!validateUtils.staminaIsOriginal(staminaJson)) {
             this.logger.debug(`[ModParameter] modifications stamina.`)
            this.assigneAttributsStamina(staminaJson, staminaSpt);
        }

        this.logger.debug(`[ModParameter] Successfully applied PMC modifications.`);
        return true;
    }

    private assigneAttributsStamina(staminaJson: Stamina, staminaSpt: IStamina): void {

        const validateUtils = new ValidateUtils();
        staminaSpt.SprintDrainRate = validateUtils.validateAndCastIntPmc(staminaJson.SprintDrainRate)
        staminaSpt.JumpConsumption = validateUtils.validateAndCastIntPmc(staminaJson.JumpConsumption)
        staminaSpt.StandupConsumption.x = validateUtils.validateAndCastIntPmc(staminaJson.StandupConsumption)
        staminaSpt.StandupConsumption.y = validateUtils.validateAndCastIntPmc(staminaJson.StandupConsumption * 2)

        if (staminaSpt.AimDrainRate != (validateUtils.validateAndCastIntPmc(staminaJson.AimDrainRate) + 0.1))
            staminaSpt.AimDrainRate = validateUtils.validateAndCastFloatPmc(staminaJson.AimDrainRate, 1)

        if (staminaSpt.BaseRestorationRate != (validateUtils.validateAndCastIntPmc(staminaJson.BaseRestorationRate) + 0.5)) {
            staminaSpt.BaseRestorationRate = validateUtils.validateAndCastFloatPmc(staminaJson.BaseRestorationRate, 1);
        }
    }

    private assigneAttributsAiming(aimingJson: Aiming, aimingSpt: IAiming, config: IConfig): void {
        const validateUtils = new ValidateUtils();

        aimingSpt.AimProceduralIntensity = validateUtils.validateAndCastFloatPmc(aimingJson.AimProceduralIntensity, 1)
        aimingSpt.RecoilHandDamping = validateUtils.validateAndCastFloatPmc(aimingJson.RecoilHandDamping, 2);
        aimingSpt.RecoilDamping = validateUtils.validateAndCastFloatPmc(aimingJson.RecoilDamping, 1);

        if (aimingJson.AimPunchMagnitude !== undefined) {
            config.AimPunchMagnitude = validateUtils.validateAndCastFloatPmc(aimingJson.AimPunchMagnitude, 1);
        }

        if (aimingJson.RecoilHandDamping !== undefined) {
            aimingSpt.RecoilHandDamping = validateUtils.validateAndCastFloatPmc(aimingJson.RecoilHandDamping, 2);
        }

        if (aimingJson.RecoilDamping !== undefined) {
            aimingSpt.RecoilDamping = validateUtils.validateAndCastFloatPmc(aimingJson.RecoilDamping, 1);
        }

        if (aimingJson.ProceduralIntensityByPoseStanding !== undefined) {
            aimingSpt.ProceduralIntensityByPose.z = validateUtils.validateAndCastFloatPmc(aimingJson.ProceduralIntensityByPoseStanding, 1);
        }

        if (aimingJson.ProceduralIntensityByPoseCrouching !== undefined) {
            aimingSpt.ProceduralIntensityByPose.y = validateUtils.validateAndCastFloatPmc(aimingJson.ProceduralIntensityByPoseCrouching, 1);
        }

        if (aimingJson.ProceduralIntensityByPoseProne !== undefined) {
            aimingSpt.ProceduralIntensityByPose.x = validateUtils.validateAndCastFloatPmc(aimingJson.ProceduralIntensityByPoseProne, 1);
        }

        if (aimingJson.RecoilIntensityStanding !== undefined) {
            aimingSpt.RecoilXIntensityByPose.z = validateUtils.validateAndCastFloatPmc(aimingJson.RecoilIntensityStanding, 1);
            aimingSpt.RecoilYIntensityByPose.z = validateUtils.validateAndCastFloatPmc(aimingJson.RecoilIntensityStanding, 1);
            aimingSpt.RecoilZIntensityByPose.z = validateUtils.validateAndCastFloatPmc(aimingJson.RecoilIntensityStanding, 1);
        }

        if (aimingJson.RecoilIntensityCrouching !== undefined) {
            aimingSpt.RecoilXIntensityByPose.y = validateUtils.validateAndCastFloatPmc(aimingJson.RecoilIntensityCrouching, 1);
            aimingSpt.RecoilYIntensityByPose.y = validateUtils.validateAndCastFloatPmc(aimingJson.RecoilIntensityCrouching, 1);
            aimingSpt.RecoilZIntensityByPose.y = validateUtils.validateAndCastFloatPmc(aimingJson.RecoilIntensityCrouching, 1);
        }

        if (aimingJson.RecoilIntensityProne !== undefined) {
            aimingSpt.RecoilXIntensityByPose.x = validateUtils.validateAndCastFloatPmc(aimingJson.RecoilIntensityProne, 1);
            aimingSpt.RecoilYIntensityByPose.x = validateUtils.validateAndCastFloatPmc(aimingJson.RecoilIntensityProne, 1);
            aimingSpt.RecoilZIntensityByPose.x = validateUtils.validateAndCastFloatPmc(aimingJson.RecoilIntensityProne, 1);
        }
    }

}
